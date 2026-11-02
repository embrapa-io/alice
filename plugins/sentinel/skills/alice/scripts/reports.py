#!/usr/bin/env python3
"""Relatórios da Sentinela (Embrapa I/O) para o projeto do diretório atual. Só stdlib; rode com `python3 -I`.

    reports.py locate                        projeto, clones locais por app, boilerplates e io-doc (JSON)
    reports.py fetch [--n 3] [--app APP]     achados por app nos N últimos relatórios do io-doc (JSON)
    reports.py email [--n 1]                 sem io-doc: baixa os N últimos e-mails da Sentinela pela CLI gws (opcional)
    reports.py vote PROJETO FP useful|noise  URL de voto no Dashboard (abra no navegador em que você está logado)

Funciona de dois lugares: de dentro do clone de uma app (`git.embrapa.io:<projeto>/<app>`) ou da pasta de um projeto
polyrepo, que reúne os clones das apps e o do io-doc com qualquer nome (ex.: `docs`): os clones são achados pelo
remoto, não pelo nome da pasta.

Nada aqui altera um checkout seu: o io-doc só recebe `git fetch`, e os relatórios são lidos de `origin/<padrão>` e de
`origin/sentinela` (io-doc com o ramo principal protegido) com `git show`. Sem clone local, o io-doc é clonado em
~/.cache/sentinel/<projeto>/io-doc.
"""
from __future__ import annotations

import base64
import html
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

GITLAB = "git.embrapa.io"
DASHBOARD = "https://dashboard.embrapa.io"
CACHE = Path.home() / ".cache" / "sentinel"
REPORT = re.compile(r"(?:^|/)\d{4}-\d{2}-\d{2}-(weekly|daily|semanal|diario)\.md$")
REMOTE = re.compile(r"git\.embrapa\.io[:/]+([^/]+)/([^/]+?)(?:\.git)?/?$")


def sh(*args: str, cwd: str | Path | None = None, check: bool = True) -> str:
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit(f"falhou: {' '.join(args)}\n{r.stderr.strip()[:400]}")
    return r.stdout.strip()


def remote_of(path: Path) -> tuple[str, str] | None:
    url = sh("git", "remote", "get-url", "origin", cwd=path, check=False)
    m = REMOTE.search(url)
    return (m.group(1), m.group(2)) if m else None


def settings_of(path: Path) -> dict:
    try:
        return json.loads((path / ".embrapa" / "settings.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def default_branch(path: Path) -> str:
    return sh("git", "symbolic-ref", "--short", "refs/remotes/origin/HEAD", cwd=path, check=False).removeprefix("origin/") or "main"


def locate(cwd: Path) -> dict:
    """Projeto, clones locais (por repositório) e io-doc, a partir de um clone de app ou de uma pasta de projeto."""
    inside = sh("git", "rev-parse", "--show-toplevel", cwd=cwd, check=False)
    if inside:
        rem = remote_of(Path(inside))
        if not rem:
            raise SystemExit("o remoto deste repositório não é do git.embrapa.io: não é uma app da plataforma")
        project, current = rem
        candidates = [Path(inside)] + [p for p in Path(inside).parent.iterdir() if (p / ".git").exists() and p != Path(inside)]
    else:
        project, current = "", ""
        candidates = [p for p in cwd.iterdir() if (p / ".git").exists()] + [q for p in cwd.iterdir() if p.is_dir() for q in p.iterdir() if (q / ".git").exists()]
    clones: dict[str, list[str]] = {}
    projects: dict[str, int] = {}
    for c in candidates:
        rem = remote_of(c)
        if not rem:
            continue
        projects[rem[0]] = projects.get(rem[0], 0) + 1
        clones.setdefault(f"{rem[0]}/{rem[1]}", []).append(str(c))
    if not project:
        if not projects:
            raise SystemExit("nenhum clone do git.embrapa.io nesta pasta nem um nível abaixo: rode de um projeto ou de uma app")
        project = max(projects, key=projects.get)
        if len(projects) > 1:
            print(f"aviso: clones de vários projetos ({', '.join(sorted(projects))}); usando '{project}'", file=sys.stderr)
    repos = {}
    for key, paths in clones.items():
        p, name = key.split("/", 1)
        if p != project:
            continue
        # dois clones do mesmo remoto (ex.: pwa e pwa-old): o de nome igual ao repositório vem primeiro
        paths.sort(key=lambda x: (Path(x).name != name, x))
        st = settings_of(Path(paths[0]))
        boiler = (st.get("boilerplate") or "").strip()
        repos[name] = {"clones": paths, "default_branch": default_branch(Path(paths[0])),
                       "dirty": bool(sh("git", "status", "--porcelain", cwd=paths[0], check=False)),
                       "boilerplate": boiler if boiler not in ("", "_") else "", "platform": st.get("platform") or "",
                       "stores": st.get("stores") or {}}
    iodoc = repos.pop("io-doc", None)
    return {"project": project, "current_app": current if current != "io-doc" else "",
            "iodoc": iodoc["clones"][0] if iodoc else str(CACHE / project / "io-doc"), "iodoc_local": bool(iodoc), "repos": repos}


def sync_iodoc(project: str, path: Path) -> bool:
    """Só `git fetch` (nunca pull: o checkout pode ter trabalho seu); sem clone, clona no cache."""
    if (path / ".git").exists():
        sh("git", "fetch", "--quiet", "origin", cwd=path, check=False)
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["git", "clone", "--quiet", "--no-checkout", f"git@{GITLAB}:{project}/io-doc.git", str(path)], capture_output=True, text=True)
    return r.returncode == 0


def reports_in(path: Path) -> list[tuple[str, str, str]]:
    """(nome, ref, caminho) dos relatórios em origin/<padrão> e origin/sentinela, do mais antigo ao mais novo."""
    found: dict[str, tuple[str, str, str]] = {}
    for ref in (f"origin/{default_branch(path)}", "origin/sentinela"):
        listing = sh("git", "ls-tree", "-r", "--name-only", ref, "--", "06-Support/Sentinel", cwd=path, check=False)
        for name in listing.splitlines():
            if REPORT.search(name):
                found.setdefault(Path(name).name, (Path(name).name, ref, name))
    return [found[k] for k in sorted(found)]


FINDING = re.compile(r"^- \*\*\[(?P<sev>[^\]]+)\] (?P<title>.+)\*\*$")


def parse(text: str, project: str) -> dict:
    """Um relatório inteiro, por app: achados (os consolidados do projeto vão para cada app que cobrem e também para
    `projeto`), insights, itens em aberto, loja e resumo do período."""
    lines = text.splitlines()
    front = {}
    if lines and lines[0] == "---":
        for l in lines[1:]:
            if l == "---":
                break
            if ":" in l:
                k, v = l.split(":", 1)
                front[k.strip()] = v.strip()
    apps: dict[str, dict] = {}

    def bucket(app: str) -> dict:
        return apps.setdefault(app, {"findings": [], "insights": [], "still_open": [], "store": [], "summary": []})
    whole = f"{project} · projeto inteiro"
    section, sub, cur, owner, in_code = "", "", None, "", False
    for l in lines:
        if l.startswith("## "):
            section, sub, cur = l[3:].strip(), "", None
            owner = "projeto" if section == whole else section.split("/", 1)[1] if section.startswith(project + "/") else ""
            continue
        if l.startswith("### "):
            sub = l[4:].strip()
            continue
        if owner:
            if l.startswith("> - **"):
                bucket(owner)["insights"].append(re.sub(r"^> - ", "", l).replace("**", ""))
                continue
            m = FINDING.match(l)
            if m:
                cur = {"severity": m["sev"], "title": m["title"], "category": sub, "scope": "projeto" if owner == "projeto" else "app",
                       "apps": [], "evidence": "", "code": "", "action": "", "link": "", "id": ""}
                bucket(owner)["findings"].append(cur)
                continue
            if cur is not None:
                s = l.strip()
                if s == "```":
                    in_code = not in_code
                elif in_code:
                    cur["code"] += s + "\n"
                else:
                    for key, label in (("apps", "Apps: "), ("evidence", "Evidência: "), ("action", "Ação sugerida: "), ("link", "Link: "), ("id", "Identificador: ")):
                        if s.startswith("- " + label):
                            v = s[len(label) + 2:].strip().strip("`")
                            cur[key] = [a.strip() for a in v.split(",")] if key == "apps" else v
        elif section == "Continua em aberto" and l.startswith("- ["):
            m = re.search(r"\] (?:" + re.escape(project) + r"/([^:]+)|" + re.escape(whole) + r"): ", l)
            fp = re.search(r"`([0-9a-f]{12})`\s*$", l)
            bucket((m.group(1) if m and m.group(1) else "projeto"))["still_open"].append({"text": l[2:], "id": fp.group(1) if fp else ""})
        elif section == "Loja (Google Play)" and sub.startswith(project + "/") and l.strip():
            bucket(sub.split("/", 1)[1].split(" ")[0])["store"].append(l)
        elif section == "Resumo do período" and sub.startswith(project + "/") and l.startswith("- "):
            bucket(sub.split("/", 1)[1])["summary"].append(l[2:])
    for f in apps.get("projeto", {}).get("findings", []):
        for a in f["apps"]:
            bucket(a)["findings"].append(f)
    return {"generated": front.get("gerado_em", ""), "period": [front.get("periodo_inicio", ""), front.get("periodo_fim", "")],
            "model": front.get("modelo", ""), "apps": apps}


def cmd_fetch(n: int, only: str) -> None:
    loc = locate(Path.cwd())
    path = Path(loc["iodoc"])
    if not sync_iodoc(loc["project"], path):
        print(json.dumps({**loc, "iodoc_ok": False, "reports": []}, ensure_ascii=False, indent=1))
        return
    files = reports_in(path)
    reports = []
    for name, ref, rel in reversed(files[-n:]):
        r = parse(sh("git", "show", f"{ref}:{rel}", cwd=path), loc["project"])
        if only:
            r["apps"] = {k: v for k, v in r["apps"].items() if k in (only, "projeto")}
        reports.append({"file": name, "ref": ref, **r})
    print(json.dumps({**loc, "iodoc_ok": True, "available": len(files), "reports": reports}, ensure_ascii=False, indent=1))


class _Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.out: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in ("br", "div", "p", "tr", "li", "h1", "h2", "h3"):
            self.out.append("\n")

    def handle_data(self, data):
        self.out.append(data)


def cmd_email(n: int) -> None:
    """Fallback sem MCP e sem io-doc: e-mails da Sentinela pela CLI gws (github.com/googleworkspace/cli), autenticada
    na conta que recebe os relatórios. Opcional: sem ela, cole o texto do e-mail na conversa."""
    import shutil
    if not shutil.which("gws"):
        raise SystemExit("CLI gws não encontrada: cole o texto do e-mail da Sentinela na conversa ou use o MCP do Dashboard")
    loc = locate(Path.cwd())
    q = f'subject:"[Embrapa I/O Sentinela]" "{loc["project"]}"'
    lst = json.loads(sh("gws", "gmail", "users", "messages", "list", "--params", json.dumps({"userId": "me", "q": q, "maxResults": n})) or "{}")
    outdir = CACHE / loc["project"] / "email"
    outdir.mkdir(parents=True, exist_ok=True)
    saved = []
    for m in lst.get("messages") or []:
        msg = json.loads(sh("gws", "gmail", "users", "messages", "get", "--params", json.dumps({"userId": "me", "id": m["id"], "format": "full"})))
        parts, body = [msg.get("payload") or {}], ""
        while parts:
            p = parts.pop(0)
            parts += p.get("parts") or []
            if p.get("mimeType") == "text/html" and (p.get("body") or {}).get("data"):
                body = base64.urlsafe_b64decode(p["body"]["data"] + "==").decode("utf-8", "replace")
                break
        t = _Text()
        t.feed(body)
        text = re.sub(r"\n\s*\n+", "\n\n", html.unescape("".join(t.out)))
        subject = next((h["value"] for h in (msg.get("payload") or {}).get("headers", []) if h["name"].lower() == "subject"), m["id"])
        f = outdir / f"{m['id']}.txt"
        f.write_text(f"{subject}\n\n{text}", encoding="utf-8")
        saved.append({"subject": subject, "file": str(f)})
    print(json.dumps({**loc, "query": q, "emails": saved}, ensure_ascii=False, indent=1))


def main() -> None:
    a = sys.argv[1:]
    opt = lambda k: a[a.index(k) + 1] if k in a and a.index(k) + 1 < len(a) else ""
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
    elif a[0] == "locate":
        print(json.dumps(locate(Path.cwd()), ensure_ascii=False, indent=1))
    elif a[0] == "fetch":
        cmd_fetch(int(opt("--n") or 3), opt("--app"))
    elif a[0] == "email":
        cmd_email(int(opt("--n") or 1))
    elif a[0] == "vote" and len(a) == 4 and a[3] in ("useful", "noise"):
        print(f"{DASHBOARD}/?sentinel={a[1]}&fp={a[2]}&vote={a[3]}")
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
