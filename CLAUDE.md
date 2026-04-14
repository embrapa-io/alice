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
- `knowledge/embrapa-io-integration-guide.md`
- `workflows/*/checklist.md` (6 arquivos)

Convenção: `1.YY.MM-N` onde N é o build number incremental.

## Estrutura

- `SKILL.md` — Entry point BMad padrão (persona, menu, headless, escopo)
- `agents/alice.md` — Definição da agente em formato XML (legado, mantido para compatibilidade)
- `scripts/validate-compliance.py` — Validação determinística (rodar com `uv run`)
- `workflows/` — 8 workflows (3 core Alice + 4 setup + 1 deprecated)
- `knowledge/` — 8 knowledge files com regras da plataforma
- `templates/` — Templates reutilizáveis (docker-compose, env, settings)

## Regras

- Sempre usar grafia correta em português brasileiro com acentos
- Após modificar o script `validate-compliance.py`, rodar `uv run scripts/validate-compliance.py --self-test`
- O workflow `validate-compliance` (VCL) está deprecated — não investir nele
- Config consolidado: `{project-root}/_bmad/config.yaml` + `config.user.yaml`
