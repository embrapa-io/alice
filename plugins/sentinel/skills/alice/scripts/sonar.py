#!/usr/bin/env python3
"""SonarQube (code.embrapa.io) sem o MCP: plano B da skill alice do plugin sentinel, só biblioteca padrão.

    sonar.py hotspots CHAVE [--status TO_REVIEW]     hotspots do projeto (chave, regra, arquivo:linha, mensagem)
    sonar.py lines COMPONENTE INICIO FIM             trecho do código (ex.: projeto_pwa:src/x.js 200 230)
    sonar.py review HOTSPOT SAFE|FIXED|ACKNOWLEDGED "comentário" [--yes]
                                                     revisa um hotspot; sem --yes só mostra o que faria
    sonar.py issue ISSUE falsepositive|accept|reopen [--yes]

A chave do projeto é <projeto>_<app> (o sonar.projectKey do pipeline da plataforma). URL e token vêm das variáveis
SONARQUBE_URL e SONARQUBE_TOKEN do ambiente ou, na falta delas, da configuração do MCP `sonarqube` no ~/.claude.json
(env do servidor): o token nunca é impresso. Escrita só com --yes, depois da aprovação do usuário (passo 5).
"""
from __future__ import annotations

import base64
import json
import os
import sys
import urllib.parse
import urllib.request


def config() -> tuple[str, str]:
    if os.environ.get("SONARQUBE_TOKEN"):
        return os.environ.get("SONARQUBE_URL", "https://code.embrapa.io").rstrip("/"), os.environ["SONARQUBE_TOKEN"]
    try:
        d = json.load(open(os.path.expanduser("~/.claude.json"), encoding="utf-8"))
    except (OSError, ValueError):
        d = {}

    def find(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "sonarqube" and isinstance(v, dict) and "env" in v:
                    return v["env"]
                r = find(v)
                if r:
                    return r
    env = find(d) or {}
    url, token = env.get("SONARQUBE_URL", "https://code.embrapa.io").rstrip("/"), env.get("SONARQUBE_TOKEN", "")
    if not token:
        sys.exit("Sem SONARQUBE_TOKEN: defina a variável de ambiente ou configure o MCP 'sonarqube' no ~/.claude.json.")
    return url, token


def call(method: str, path: str, params: dict) -> dict:
    url, token = config()
    q = urllib.parse.urlencode(params)
    req = urllib.request.Request(f"{url}/api/{path}" + (f"?{q}" if method == "GET" else ""), method=method,
                                 data=q.encode() if method == "POST" else None,
                                 headers={"Authorization": "Basic " + base64.b64encode(f"{token}:".encode()).decode()})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read()
    return json.loads(body) if body else {}


def main() -> None:
    a = sys.argv[1:]
    yes = "--yes" in a
    a = [x for x in a if x != "--yes"]
    if not a:
        sys.exit(__doc__)
    if a[0] == "hotspots":
        status = a[a.index("--status") + 1] if "--status" in a else "TO_REVIEW"
        out = call("GET", "hotspots/search", {"projectKey": a[1], "status": status, "ps": 100})
        for h in out.get("hotspots", []):
            print(f"{h['key']}\t{h.get('vulnerabilityProbability', '')}\t{h.get('ruleKey', '')}\t"
                  f"{h['component'].split(':', 1)[-1]}:{h.get('line', '')}\t{h.get('message', '')[:120]}")
        print(f"# {out.get('paging', {}).get('total', 0)} hotspot(s) {status}")
    elif a[0] == "lines":
        out = call("GET", "sources/lines", {"key": a[1], "from": a[2], "to": a[3]})
        for ln in out.get("sources", []):
            code = ln.get("code", "")
            for tag in ("<span class=\"", "</span>"):
                while tag in code:
                    i = code.find(tag)
                    j = code.find(">", i) if tag.startswith("<span") else i + len(tag) - 1
                    code = code[:i] + code[j + 1:]
            print(f"{ln['line']:>5} {code.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&').replace('&quot;', '\"')}")
    elif a[0] == "review":
        key, resolution, comment = a[1], a[2].upper(), a[3] if len(a) > 3 else ""
        print(f"{'+' if yes else '-'} hotspot {key}: REVIEWED/{resolution} — {comment}")
        if yes:
            call("POST", "hotspots/change_status", {"hotspot": key, "status": "REVIEWED", "resolution": resolution, "comment": comment})
    elif a[0] == "issue":
        key, transition = a[1], {"falsepositive": "falsepositive", "accept": "accept", "reopen": "reopen"}[a[2]]
        print(f"{'+' if yes else '-'} issue {key}: {transition}")
        if yes:
            call("POST", "issues/do_transition", {"issue": key, "transition": transition})
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
