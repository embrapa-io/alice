# Alice — Embrapa I/O Compliance Module

## Versionamento

A versão do módulo está em `module.yaml` (campo `version`) e é referenciada em 14+ arquivos.

**Antes de cada commit, pergunte ao usuário se deseja incrementar a versão.**

Para atualizar, faça replace-all de `{versão-atual}` em todos os arquivos:
- `module.yaml`
- `README.md`
- `ROADMAP.md`
- `.claude-plugin/marketplace.json`
- `embrapa-io-setup/assets/module.yaml`
- `alice/knowledge/embrapa-io-integration-guide.md`
- `alice/workflows/*/checklist.md` (6 arquivos)

Convenção: `1.YY.MM-N` onde N é o build number incremental.

## Estrutura

O módulo é um **skill self-contained**: o installer do BMad copia `alice/` inteiro para `.claude/skills/alice/`. Todos os recursos (workflows, knowledge, templates, scripts) vivem dentro de `alice/`.

- `alice/SKILL.md` — Entry point da agente (persona, menu, headless, escopo)
- `alice/workflows/` — 8 workflows (3 core + 4 setup + 1 deprecated)
- `alice/knowledge/` — 8 knowledge files com regras da plataforma
- `alice/templates/` — Templates reutilizáveis (docker-compose, env, settings)
- `alice/scripts/validate-compliance.py` — Validação determinística (rodar com `uv run`)
- `agents/alice.md` — Definição legada em formato XML (mantida para compatibilidade)
- `.claude-plugin/marketplace.json` — Registra `./alice` como skill instalável

**Paths**: Dentro de `alice/`, usar paths relativos (`./workflows/...`, `./knowledge/...`). Config externo ao skill usa `{project-root}/_bmad/config.yaml`.

## Regras

- Sempre usar grafia correta em português brasileiro com acentos
- Após modificar o script, rodar `uv run alice/scripts/validate-compliance.py --self-test`
- O workflow `validate-compliance` (VCL) está deprecated — não investir nele
- Config consolidado: `{project-root}/_bmad/config.yaml` + `config.user.yaml`
