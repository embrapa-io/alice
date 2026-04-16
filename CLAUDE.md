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

- `alice/SKILL.md` — Entry point da agente (persona, capabilities, headless, escopo)
- `alice/workflows/` — 8 workflows (3 core + 4 setup + 1 deprecated)
- `alice/knowledge/` — 8 knowledge files com regras da plataforma
- `alice/templates/` — Templates reutilizáveis (docker-compose, env, settings)
- `alice/scripts/validate-compliance.py` — Validação determinística (rodar com `uv run`)
- `agents/alice.md` — Definição legada em formato XML (mantida para compatibilidade)
- `.claude-plugin/marketplace.json` — Registra `./alice` como único skill instalável

## Salvaguardas — Erros Comuns a Evitar

### Config paths
- O installer do BMad gera config em `{project-root}/_bmad/embrapa-io/config.yaml` (per-module), NÃO em `{project-root}/_bmad/config.yaml` (consolidado).
- O SKILL.md e workflows devem tentar o path per-module PRIMEIRO, com fallback para o consolidado.
- NUNCA fazer hard-stop se config não existir — usar defaults sensatos e prosseguir.

### Paths dentro do skill
- Dentro de `alice/`, SEMPRE usar paths relativos (`./workflows/...`, `./knowledge/...`, `./scripts/...`, `./templates/...`).
- NUNCA usar `{project-root}/_bmad/embrapa-io/` dentro de `alice/` — esses paths não resolvem quando o skill é instalado em `.claude/skills/alice/`.
- Config externo ao skill é exceção: `{project-root}/_bmad/embrapa-io/config.yaml` está fora do skill directory.

### Menu da agente
- O menu interativo mostra APENAS: MH, CH, VC, IA, CR, PM, DA.
- Workflows utilitários (GEI, GDC, GSJ, GLI) são INTERNOS — invocados pelos workflows principais ou via `/bmad-help`. NÃO devem aparecer no menu.
- No SKILL.md, eles ficam na seção "Internal Workflows", separada da Capabilities table principal.

### SKILL.md — padrão BMad
- Seções obrigatórias: `## Overview`, `## Identity`, `## Communication Style`, `## Principles`, `## Capabilities`, `## On Activation`, `## Knowledge Base`, `## Rules`.
- NÃO usar `## Persona` (dividir em Identity + Communication Style + Principles).
- NÃO usar `## Activation` (usar `## On Activation`).
- Frontmatter: apenas `name` e `description`. NÃO incluir `icon`, `module`, `type` (não são campos padrão BMad).

### marketplace.json
- Apenas `"./alice"` no array `skills`. O `embrapa-io-setup` NÃO deve estar no array (o installer do BMad já faz merge de config e help CSV automaticamente).
- O array `skills` determina o que é copiado para `.claude/skills/` — TUDO que a agente precisa deve estar dentro de `alice/`.

### module-help.csv
- TODAS as entries devem ter `skill` = `alice` (é o único skill instalável).
- NÃO usar nomes de skills standalone como `generate-docker-compose` — são sub-workflows da alice.
- Manter sincronizado com `embrapa-io-setup/assets/module-help.csv` (copiar após edição).

### Persistência de estado
- Workflows core (VC, IA, CR) devem escrever findings intermediários em disco a cada step (ver `workflows/references/state-persistence.md`).
- Isso previne perda de dados por context compaction em sessões longas.

### Script validate-compliance.py
- Após qualquer modificação, SEMPRE rodar: `uv run alice/scripts/validate-compliance.py --self-test`
- Todas as strings em português DEVEM ter acentos corretos.
- PEP 723 inline metadata obrigatório.

### Deprecated
- O workflow `validate-compliance` (VCL) em `alice/workflows/validate/` está deprecated — NÃO investir, NÃO editar, NÃO referenciar em novos código.
- O `agents/alice.md` é legado (formato XML) — a definição canônica é `alice/SKILL.md`.

## Regras Gerais

- Sempre usar grafia correta em português brasileiro com acentos (á, é, í, ó, ú, ã, õ, â, ê, ô, ç).
- Antes de editar um arquivo, SEMPRE ler o estado atual primeiro.
- Ao modificar paths, verificar se resolvem corretamente tanto no repo source quanto no skill instalado.
- Testar mudanças no projeto-alvo (não apenas no repo source) para confirmar que funcionam pós-instalação.
