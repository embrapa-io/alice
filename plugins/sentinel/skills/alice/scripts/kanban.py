#!/usr/bin/env python3
"""Kanban do projeto no GitLab do Embrapa I/O (board, milestones e issues do GRUPO). Só stdlib; rode com `python3 -I`.

    kanban.py state PROJETO [--keys K1,K2]       board e colunas, etiquetas, milestones, séries de versão por app, equipe
                                                  e, com --keys, as issues que já citam esses identificadores (JSON)
    kanban.py calendar [--from AAAA-MM] [--months N] [--holidays DD/MM/AAAA,...]
                                                  janelas dos milestones (segunda → sexta), feriados e dias úteis (JSON)
    kanban.py plan PLANO.json                     distribui as issues nos milestones pela capacidade e escalona os prazos
    kanban.py apply PLANO.json [--yes]            cria board/colunas, milestones e issues; sem --yes só mostra o que faria
    kanban.py sync PROJETO [--yes]                sugere mover as issues entre colunas pelas tags alpha/beta/release

O acesso é o do `glab` autenticado em git.embrapa.io (`glab config get token`) ou, sem ele, a variável GITLAB_TOKEN (token
pessoal com escopo api); o token fica só na memória do processo.
Regras (https://embrapa.io/docs/kanban/ e deployer): milestones sempre no GRUPO, título = versão `V.AA.M` da série da app (a parte
antes do `-` da tag); board do grupo com as colunas To Do, Doing, Alpha, Beta e On Hold (Open e Closed já existem);
issue só entra em To Do com responsável, milestone e prazo.
"""
from __future__ import annotations

import argparse
import os
import json
import math
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from datetime import date, timedelta

GITLAB = "git.embrapa.io"
COLUMNS = ["To Do", "Doing", "Alpha", "Beta", "On Hold"]
SIZES = {"P": 1, "M": 3, "G": 8}  # dias de trabalho de uma pessoa
STAGE_TAG = {"alpha": re.compile(r"^\d+\.\d+\.\d+-alpha\.\d+$"), "beta": re.compile(r"^\d+\.\d+\.\d+-beta\.\d+$"),
             "release": re.compile(r"^\d+\.\d+\.\d+-\d+$")}
_TOKEN = ""


# ---------------------------------------------------------------- GitLab

def token() -> str:
    global _TOKEN
    if not _TOKEN:
        _TOKEN = os.environ.get("GITLAB_TOKEN", "").strip()
    if not _TOKEN:
        try:
            r = subprocess.run(["glab", "config", "get", "token", "--host", GITLAB], capture_output=True, text=True)
            _TOKEN = r.stdout.strip()
        except FileNotFoundError:
            pass
        if not _TOKEN:
            raise SystemExit(f"sem token para {GITLAB}: rode `glab auth login --hostname {GITLAB}` ou defina GITLAB_TOKEN (escopo api)")
    return _TOKEN


def api(method: str, path: str, data: dict | None = None, params: dict | None = None):
    url = f"https://{GITLAB}/api/v4/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True)
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, method=method,
                                 headers={"PRIVATE-TOKEN": token(), "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read()
            nxt = r.headers.get("X-Next-Page", "")
    except urllib.error.HTTPError as e:
        raise SystemExit(f"{method} {path}: {e.code} {e.read().decode(errors='replace')[:300]}")
    out = json.loads(raw) if raw else None
    return (out, nxt) if method == "GET" else out


def get_all(path: str, params: dict | None = None) -> list:
    params = dict(params or {}, per_page=100, page=1)
    items: list = []
    while True:
        out, nxt = api("GET", path, params=params)
        items += out if isinstance(out, list) else [out]
        if not nxt:
            return items
        params["page"] = int(nxt)


def get(path: str, params: dict | None = None):
    return api("GET", path, params=params)[0]


def enc(path: str) -> str:
    return urllib.parse.quote(path, safe="")


# ---------------------------------------------------------------- calendário

def easter(y: int) -> date:
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    return date(y, (h + l - 7 * m + 114) // 31, (h + l - 7 * m + 114) % 31 + 1)


LOCAL_NAMES: dict[date, str] = {}


def place_of(project: str) -> tuple[str, dict]:
    """O lugar do projeto e a tabela de feriados locais (references/local-holidays.json, mesclado com
    ~/.config/sentinel/local-holidays.json). Sem entrada para o projeto, vale default_place; vazio = só os nacionais
    (a skill pergunta uma vez onde a equipe trabalha e oferece gravar no arquivo do usuário)."""
    base = Path(__file__).resolve().parent.parent / "references" / "local-holidays.json"
    table = json.loads(base.read_text(encoding="utf-8"))
    user = Path.home() / ".config" / "sentinel" / "local-holidays.json"
    if user.exists():
        extra = json.loads(user.read_text(encoding="utf-8"))
        for k in ("projects", "states", "cities"):
            table.setdefault(k, {}).update(extra.get(k, {}))
        table["default_place"] = extra.get("default_place", table.get("default_place", ""))
    return table.get("projects", {}).get(project, table.get("default_place", "")), table


def local_holidays(project: str, years: list[int]) -> tuple[str, set[date]]:
    """Feriados estaduais e municipais do lugar do projeto nos anos pedidos; os nomes ficam em LOCAL_NAMES."""
    place, table = place_of(project)
    uf = place.rsplit("/", 1)[-1] if "/" in place else ""
    out = set()
    for md, name in table.get("states", {}).get(uf, []) + table.get("cities", {}).get(place, []):
        m, d = (int(v) for v in md.split("-"))
        for y in years:
            out.add(date(y, m, d))
            LOCAL_NAMES[date(y, m, d)] = name
    return place, out


def holidays(y: int, extra: set[date]) -> dict[date, str]:
    """Feriados nacionais e pontos facultativos federais que param a Embrapa. Estaduais e municipais vêm da tabela de
    feriados locais (local_holidays) e de --holidays."""
    e = easter(y)
    out = {date(y, 1, 1): "Confraternização Universal", date(y, 4, 21): "Tiradentes", date(y, 5, 1): "Dia do Trabalho",
           date(y, 9, 7): "Independência", date(y, 10, 12): "Nossa Senhora Aparecida", date(y, 11, 2): "Finados",
           date(y, 11, 15): "Proclamação da República", date(y, 11, 20): "Consciência Negra", date(y, 12, 25): "Natal",
           e - timedelta(48): "Carnaval", e - timedelta(47): "Carnaval", e - timedelta(2): "Sexta-feira Santa",
           e + timedelta(60): "Corpus Christi"}
    out.update({d: LOCAL_NAMES.get(d, "informado") for d in extra if d.year == y})
    return out


def is_off(d: date, extra: set[date]) -> bool:
    return d.weekday() >= 5 or d in holidays(d.year, extra)


def month_end(y: int, m: int, extra: set[date]) -> date:
    """Última sexta útil do mês. Dezembro fecha antes das festas: a última sexta útil até o dia 20."""
    d = date(y, 12, 20) if m == 12 else (date(y + (m == 12), m % 12 + 1, 1) - timedelta(1))
    while d.weekday() != 4 or d in holidays(y, extra):
        d -= timedelta(1)
    return d


def month_start(y: int, m: int, extra: set[date]) -> date:
    """Segunda depois do fim do milestone anterior. Janeiro começa na primeira segunda a partir do dia 2 (depois das festas)."""
    if m == 1:
        d = date(y, 1, 2)
    else:
        d = month_end(y if m > 1 else y - 1, m - 1, extra) + timedelta(1)
    while d.weekday() != 0:
        d += timedelta(1)
    return d


def workdays(a: date, b: date, extra: set[date]) -> int:
    return sum(1 for i in range((b - a).days + 1) if not is_off(a + timedelta(i), extra))


def add_workdays(a: date, n: int, extra: set[date]) -> date:
    d = a
    while is_off(d, extra):
        d += timedelta(1)
    while n > 1:
        d += timedelta(1)
        if not is_off(d, extra):
            n -= 1
    return d


def months_from(y: int, m: int, n: int):
    for _ in range(n):
        yield y, m
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def window(y: int, m: int, extra: set[date]) -> dict:
    s, e = month_start(y, m, extra), month_end(y, m, extra)
    hol = {d.isoformat(): n for d, n in sorted({**holidays(y, extra), **holidays(s.year, extra)}.items()) if s <= d <= e and d.weekday() < 5}
    return {"month": f"{y % 100}.{m}", "start": s.isoformat(), "due": e.isoformat(), "workdays": workdays(s, e, extra), "holidays": hol}


def parse_extra(s: str) -> set[date]:
    out = set()
    for x in filter(None, (s or "").split(",")):
        d, mth, y = (int(v) for v in x.strip().split("/"))
        out.add(date(y, mth, d))
    return out


# ---------------------------------------------------------------- state

def tag_series(tags: list[str]) -> dict:
    last = {}
    for stage, rx in STAGE_TAG.items():
        hit = [t for t in tags if rx.match(t)]
        if hit:
            last[stage] = hit[0]
    any_tag = next((t for t in tags if re.match(r"^\d+\.\d+\.\d+-", t)), "")
    # series vazia = a app não usa o padrão V.AA.M-estágio.P (ex.: apps de loja com 1.27.3+7): perguntar ao usuário a série.
    # Tag fora do padrão de versão (um nome qualquer, como "Prototype") não é a mais recente da app
    versioned = next((t for t in tags if re.match(r"^\d+\.\d+\.\d+", t)), "")
    return {"last": last, "series": any_tag.split(".")[0] if any_tag else "", "latest_tag": versioned}


def cmd_state(project: str, keys: list[str]) -> dict:
    g = get(f"groups/{enc(project)}")
    gid = g["id"]
    labels = {l["name"]: l["id"] for l in get_all(f"groups/{gid}/labels")}
    boards = []
    for b in get_all(f"groups/{gid}/boards"):
        cols = [l["label"]["name"] for l in sorted(b["lists"], key=lambda l: l["position"]) if l.get("label")]
        boards.append({"id": b["id"], "name": b["name"], "columns": cols,
                       "missing": [c for c in COLUMNS if c not in cols], "extra": [c for c in cols if c not in COLUMNS]})
    milestones = [{"id": m["id"], "title": m["title"], "start": m["start_date"], "due": m["due_date"]}
                  for m in get_all(f"groups/{gid}/milestones", {"state": "active"})]
    apps = []
    since = (date.today() - timedelta(90)).isoformat()
    authors: dict[str, int] = {}
    for p in get_all(f"groups/{gid}/projects", {"archived": "false", "include_subgroups": "false"}):
        tags = [t["name"] for t in get_all(f"projects/{p['id']}/repository/tags", {"order_by": "version", "sort": "desc"})[:200]]
        info = tag_series(tags)
        if p["path"].startswith("io-") and not info["series"]:
            continue  # io-doc, io-web, io-api: suporte, não app
        for c in get_all(f"projects/{p['id']}/repository/commits", {"since": since, "all": "true"}):
            authors[c["author_name"].strip().lower()] = authors.get(c["author_name"].strip().lower(), 0) + 1
        apps.append({"app": p["path"], "id": p["id"], "default_branch": p.get("default_branch"), **info})
    team = []
    for mbr in get_all(f"groups/{gid}/members/all"):
        u = mbr["username"]
        if mbr.get("bot") or u.startswith(("bot_", "adm_", "project_", "group_")) or mbr["state"] != "active" or mbr["access_level"] < 30:
            continue
        team.append({"username": u, "id": mbr["id"], "name": mbr["name"], "access": mbr["access_level"],
                     "commits_90d": authors.get(mbr["name"].strip().lower(), 0)})
    active = [t for t in team if t["commits_90d"]]
    found = {}
    for k in keys:
        hits = get_all(f"groups/{gid}/issues", {"search": k, "in": "description", "scope": "all", "state": "all"})
        found[k] = [{"ref": h["references"]["full"], "state": h["state"], "labels": h["labels"],
                     "milestone": (h.get("milestone") or {}).get("title"), "web_url": h["web_url"]} for h in hits]
    return {"project": project, "group_id": gid, "labels": sorted(labels), "boards": boards, "milestones": milestones,
            "apps": apps, "team": team, "devs_estimate": len(active) or len(team), "issues_by_key": found,
            "note": "devs_estimate = membros (Developer ou acima, sem robôs) com commit nos últimos 90 dias; o usuário ajusta."}


# ---------------------------------------------------------------- plan

def cmd_plan(spec: dict) -> dict:
    """spec: {devs, dedication (0–1), start?, holidays?, milestones e apps (do state), issues: [{key, app, series, priority,
    size P|M|G, ...}]}. Ordena por prioridade, enche cada janela até a capacidade (devs × dias úteis × dedicação) e
    dá a cada issue o prazo em que o esforço acumulado termina. Usa milestone existente da série quando ele cobre a data."""
    extra = parse_extra(spec.get("holidays", ""))
    y0 = date.today().year
    place, local = local_holidays(spec.get("project", ""), [y0, y0 + 1])
    extra |= local
    devs = max(1, int(spec.get("devs") or 1))
    rate = devs * float(spec.get("dedication") or 0.5)  # dias de trabalho entregues por dia útil
    today = date.fromisoformat(spec["start"]) if spec.get("start") else date.today() + timedelta(1)
    # Milestone de versão já lançada (release da série igual ou mais nova) não recebe trabalho novo.
    released: dict[str, tuple] = {}
    for a in spec.get("apps", []):
        rel = (a.get("last") or {}).get("release", "")
        if rel and a.get("series"):
            v = tuple(int(x) for x in rel.split("-")[0].split(".")[1:3])
            released[a["series"]] = max(released.get(a["series"], (0, 0)), v)

    def open_ms(x: dict) -> bool:
        parts = str(x["title"]).split(".")
        if len(parts) != 3 or not all(p.isdigit() for p in parts):
            return False
        return (int(parts[1]), int(parts[2])) > released.get(parts[0], (0, 0))

    existing = [x for x in spec.get("milestones", []) if open_ms(x)]
    issues = sorted(spec["issues"], key=lambda i: (i.get("priority", 99), SIZES.get(i.get("size", "M"), 3)))
    # depends_on: [keys]; a dependência vem antes de quem depende dela, mesmo com prioridade menor (ex.: a issue da PWA
    # que usa um simulador corrigido depende da issue do simulador)
    ordered, placed = [], set()
    def put(it, stack=()):
        if it["key"] in placed or it["key"] in stack:
            return
        for dep in it.get("depends_on") or []:
            d = next((x for x in issues if x["key"] == dep), None)
            if d:
                put(d, stack + (it["key"],))
        placed.add(it["key"])
        ordered.append(it)
    for it in issues:
        put(it)
    issues = ordered
    y, m = today.year, today.month
    if today > month_end(y, m, extra):
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    plan, cursor_days, windows = [], 0.0, []
    month_iter = months_from(y, m, 36)
    cy, cm = next(month_iter)
    w = window(cy, cm, extra)
    w_start = max(date.fromisoformat(w["start"]), today)
    cap = workdays(w_start, date.fromisoformat(w["due"]), extra) * rate
    load = 0.0
    windows.append({**w, "capacity_days": round(cap, 1), "load_days": 0.0})
    for it in issues:
        effort = SIZES.get(it.get("size", "M"), 3)
        while load + effort > cap and load > 0:
            cy, cm = next(month_iter)
            w = window(cy, cm, extra)
            w_start = date.fromisoformat(w["start"])
            cap = workdays(w_start, date.fromisoformat(w["due"]), extra) * rate
            load = 0.0
            windows.append({**w, "capacity_days": round(cap, 1), "load_days": 0.0})
        load += effort
        windows[-1]["load_days"] = round(load, 1)
        due = min(add_workdays(w_start, max(1, math.ceil(load / rate)), extra), date.fromisoformat(w["due"]))
        series = str(it.get("series") or "1")
        title = f"{series}.{w['month']}"
        hit = next((x for x in existing if x["title"] == title), None) or next(
            (x for x in existing if str(x["title"]).split(".")[0] == series and x.get("start") and x.get("due")
             and x["start"] <= due.isoformat() <= x["due"]), None)
        plan.append({**it, "milestone": hit["title"] if hit else title, "due_date": due.isoformat(), "effort_days": effort})
    have = {x["title"] for x in spec.get("milestones", [])}
    create, seen = [], set()
    for p in plan:
        t = p["milestone"]
        if t in have or t in seen:
            continue
        seen.add(t)
        yy, mm = (int(v) for v in t.split(".")[1:3])
        w = window(2000 + yy, mm, extra)
        create.append({"title": t, "start_date": w["start"], "due_date": w["due"]})
    return {"local_holidays": {"place": place, "dates": {d.isoformat(): LOCAL_NAMES.get(d, "") for d in sorted(local)}},
            "rate_days_per_workday": rate, "windows": windows, "milestones_to_create": create, "issues": plan,
            "months_needed": len(windows)}


# ---------------------------------------------------------------- apply

def cmd_apply(spec: dict, yes: bool) -> None:
    """spec: saída do plan acrescida de project, board (true para criar/completar) e, por issue, title, description,
    type (Bug|Request) e assignee (username). Issue cujo identificador (key) já está numa issue do grupo ganha só um
    comentário (note) com o relatório novo, se houver `note`."""
    st = cmd_state(spec["project"], [i["key"] for i in spec["issues"] if i.get("key")])
    gid = st["group_id"]
    labels = {l["name"]: l["id"] for l in get_all(f"groups/{gid}/labels")}
    users = {t["username"]: t["id"] for t in st["team"]}
    apps = {a["app"]: a["id"] for a in st["apps"]}
    acts: list[tuple[str, str, str, dict | None]] = []
    if spec.get("board"):
        b = st["boards"][0] if st["boards"] else None
        if not b:
            acts.append(("POST", f"groups/{gid}/boards", "board Development", {"name": "Development"}))
        for c in (b["missing"] if b else COLUMNS):
            if c not in labels:
                print(f"! etiqueta {c} não existe no grupo; crie antes (a plataforma cria as padrão nos projetos novos)")
                continue
            acts.append(("POST", f"groups/{gid}/boards/{{board}}/lists", f"coluna {c}", {"label_id": labels[c]}))
    for mi in spec.get("milestones_to_create", []):
        acts.append(("POST", f"groups/{gid}/milestones", f"milestone {mi['title']} ({mi['start_date']} → {mi['due_date']})", mi))
    for it in spec["issues"]:
        dup = st["issues_by_key"].get(it.get("key"), [])
        if dup:
            ref = dup[0]["ref"]
            if it.get("note"):
                proj, iid = ref.split("#")
                acts.append(("POST", f"projects/{enc(proj)}/issues/{iid}/notes", f"comentário em {ref}", {"body": it["note"]}))
            else:
                print(f"= {it['key']} já registrado em {ref} ({dup[0]['state']}, {dup[0]['milestone']})")
            continue
        if it["app"] not in apps:
            print(f"! app {it['app']} não encontrada no grupo; issue {it['key']} fica de fora")
            continue
        ready = bool(it.get("assignee") and it.get("milestone") and it.get("due_date"))
        desc = it["description"]
        others = [a for a in it.get("apps") or [] if a != it["app"]]
        if others:
            desc += f"\n\n**Também afeta:** {', '.join(others)} (esta issue fica em {it['app']}, a app principal)."
        deps = [x for x in spec.get("issues", []) if x.get("key") in (it.get("depends_on") or [])]
        if deps:
            desc += "\n\n**Depende de:** " + "; ".join(f"{d['app']}: {d.get('title', d['key'])} (`{d['key']}`)" for d in deps) + "."
        data = {"title": it["title"], "description": desc, "due_date": it.get("due_date"),
                "labels": ",".join([it.get("type", "Bug")] + (["To Do"] if ready else [])),
                "milestone_title": it.get("milestone"), "assignee_username": it.get("assignee")}
        acts.append(("POST", f"projects/{apps[it['app']]}/issues", f"issue {it['app']}: {it['title']} → {it.get('milestone')}, "
                     f"{it.get('assignee') or 'sem responsável'}, {it.get('due_date')}{' [To Do]' if ready else ' [Open]'}", data))
    for _, _, desc, _ in acts:
        print(("+ " if yes else "- ") + desc)
    if not yes:
        print(f"\n{len(acts)} ações. Nada foi gravado: rode de novo com --yes depois da aprovação.")
        return
    board_id = st["boards"][0]["id"] if st["boards"] else None
    ms = {m["title"]: m["id"] for m in st["milestones"]}
    for method, path, desc, data in acts:
        if "{board}" in path:
            path = path.replace("{board}", str(board_id))
        if data and "milestone_title" in data:
            data = dict(data)
            t = data.pop("milestone_title")
            if t:
                data["milestone_id"] = ms.get(t)
            u = data.pop("assignee_username")
            if u:
                data["assignee_ids"] = [users[u]] if u in users else []
        out = api(method, path, data=data)
        if path.endswith("/boards"):
            board_id = out["id"]
        if path.endswith("/milestones"):
            ms[out["title"]] = out["id"]
        if path.endswith("/issues"):
            print(f"  {out['web_url']}")
    print(f"\n{len(acts)} ações gravadas.")


# ---------------------------------------------------------------- sync

def cmd_sync(project: str, yes: bool) -> None:
    """Para cada issue aberta do grupo nas colunas Doing/Alpha/Beta, acha os MRs mesclados ligados a ela e as tags que
    contêm o commit do merge: na release → fechar com Release; na beta → Beta; na alpha → Alpha. Só sugere; --yes aplica."""
    st = cmd_state(project, [])
    gid = st["group_id"]
    order = ["Doing", "Alpha", "Beta", "Release"]
    moves = []
    for iss in get_all(f"groups/{gid}/issues", {"state": "opened", "scope": "all"}):
        col = next((c for c in ["Beta", "Alpha", "Doing", "To Do"] if c in iss["labels"]), None)
        if col is None:
            continue
        stage_hit = None
        # Só o MR que referencia a issue ("Relacionado a #N") e foi mesclado depois da criação dela. A lista de relacionados
        # do GitLab também traz o MR que a issue só cita na descrição, e ele moveria para Alpha uma issue criada minutos
        # antes.
        ref = re.compile(rf"(?<![\w!])(?:{re.escape(iss['references']['full'])}|#{iss['iid']})(?!\d)")
        for mr in get_all(f"projects/{iss['project_id']}/issues/{iss['iid']}/related_merge_requests"):
            if mr["state"] != "merged" or (mr.get("merged_at") or "") < iss["created_at"]:
                continue
            if mr.get("project_id") != iss["project_id"] and iss["references"]["full"] not in f"{mr.get('title', '')} {mr.get('description') or ''}":
                continue
            if not ref.search(f"{mr.get('title', '')} {mr.get('description') or ''}"):
                continue
            sha = mr.get("merge_commit_sha") or mr.get("squash_commit_sha") or mr.get("sha")
            if not sha:
                continue
            tags = [r["name"] for r in get_all(f"projects/{mr['project_id']}/repository/commits/{sha}/refs", {"type": "tag"})]
            for stage, target in (("release", "Release"), ("beta", "Beta"), ("alpha", "Alpha")):
                if any(STAGE_TAG[stage].match(t) for t in tags):
                    if stage_hit is None or order.index(target) > order.index(stage_hit[0]):
                        stage_hit = (target, next(t for t in tags if STAGE_TAG[stage].match(t)))
                    break
        if stage_hit and (col not in order or order.index(stage_hit[0]) > order.index(col)):
            moves.append((iss, col, *stage_hit))
    for iss, col, target, tag in moves:
        verb = "fechar com Release" if target == "Release" else f"{col} → {target}"
        print(f"{'+' if yes else '-'} {iss['references']['full']} {iss['title'][:70]}: {verb} (tag {tag})")
        if yes:
            data = {"add_labels": target, "remove_labels": ",".join(c for c in ["To Do", "Doing", "Alpha", "Beta"] if c != target)}
            if target == "Release":
                data["state_event"] = "close"
            api("PUT", f"projects/{iss['project_id']}/issues/{iss['iid']}", data=data)
    if not moves:
        print("Nenhuma issue precisa mudar de coluna pelas tags atuais.")
    elif not yes:
        print(f"\n{len(moves)} sugestões. Nada foi gravado: rode com --yes depois da aprovação.")


# ---------------------------------------------------------------- main

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("state"); s.add_argument("project"); s.add_argument("--keys", default="")
    c = sub.add_parser("calendar"); c.add_argument("--from", dest="start", default=""); c.add_argument("--months", type=int, default=4)
    c.add_argument("--holidays", default=""); c.add_argument("--project", default="")
    p = sub.add_parser("plan"); p.add_argument("file")
    a = sub.add_parser("apply"); a.add_argument("file"); a.add_argument("--yes", action="store_true")
    y = sub.add_parser("sync"); y.add_argument("project"); y.add_argument("--yes", action="store_true")
    args = ap.parse_args()
    dump = lambda o: print(json.dumps(o, ensure_ascii=False, indent=1))
    if args.cmd == "state":
        dump(cmd_state(args.project, [k for k in args.keys.split(",") if k]))
    elif args.cmd == "calendar":
        t = date.today()
        yy, mm = (int(v) for v in args.start.split("-")) if args.start else (t.year, t.month)
        extra = parse_extra(args.holidays) | local_holidays(args.project, [yy, yy + 1])[1]
        dump([window(y_, m_, extra) for y_, m_ in months_from(yy, mm, args.months)])
    elif args.cmd == "plan":
        dump(cmd_plan(json.loads(open(args.file, encoding="utf-8").read())))
    elif args.cmd == "apply":
        cmd_apply(json.loads(open(args.file, encoding="utf-8").read()), args.yes)
    elif args.cmd == "sync":
        cmd_sync(args.project, args.yes)


if __name__ == "__main__":
    sys.exit(main())
