---
name: Generate Settings JSON
description: Gera arquivo .embrapa/settings.json conforme com a plataforma Embrapa I/O com sincronização automática de variáveis dos arquivos .env
communication_language: "{communication_language}"
document_output_language: "{document_output_language}"
web_bundle: true
---

# Generate Settings JSON Workflow

**Goal:** Criar ou atualizar o arquivo .embrapa/settings.json com metadados do projeto, variáveis de ambiente sincronizadas com os arquivos .env, e configuração de orquestradores conforme padrões da plataforma Embrapa I/O.

**Your Role:** In addition to your name, communication_style, and persona, you are also a platform configuration specialist collaborating with a developer. This is a partnership, not a client-vendor relationship. You bring expertise in configuração da plataforma Embrapa I/O, sincronização de variáveis e estrutura de settings.json, while the user brings informações do projeto e requisitos de variáveis. Work together as equals.

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Workflow Steps Overview

| Step | Arquivo | Função |
|------|---------|--------|
| 1 | step-01-detect-stack.md | Verificar pré-requisitos e detectar stack tecnológica |
| 2 | step-02-sync-variables.md | **Sincronizar variáveis .env ↔ settings.json** |
| 3 | step-03-collect-info.md | Coletar informações do projeto e mantenedor |
| 4 | step-04-generate-settings.md | Gerar e salvar settings.json |

### Core Principles

- **Step-file architecture**: Each step is a self-contained file, loaded just-in-time, executed sequentially
- **Variable Synchronization**: Ensure variables.default matches .env files exactly
- **Append-Only Building**: Build settings.json by accumulating configuration through steps
- Read each step file completely before acting; halt at menus and wait for user input
- Only proceed to next step when user selects 'C' (Continue)
- Never load multiple step files simultaneously or skip steps

---

## HEADLESS MODE

Se `{headless_mode}=true`:
- Pular todos os prompts [C] Continue — auto-prosseguir por cada etapa
- Executar `uv run ./scripts/validate-compliance.py --project-path {project-root} --output json` antes do step-01 para pré-computar detecção de stack e verificações de validação
- Não exibir menus de progresso nem solicitar entrada do usuário
- Gerar resumo JSON ao final com a configuração gerada e resultado da sincronização

> **Nota:** O script `validate-compliance.py` pode pré-computar detecção de stack e verificações de validação, acelerando os steps de detecção e sincronização de variáveis.

---

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load and read both config files:
- `{project-root}/_bmad/config.yaml` (project and module settings)
- `{project-root}/_bmad/config.user.yaml` (user settings)

Resolve:

- `project_name`, `output_folder`, `user_name`, `communication_language`, `document_output_language`

### 2. First Step EXECUTION

Load, read the full file and then execute `{workflow_path}/steps/step-01-detect-stack.md` to begin the workflow.

---

## NEXT STEP SUGGESTION

Ao concluir este workflow, sugerir ao usuário executar o workflow **generate-license** para criar o arquivo LICENSE com copyright da Embrapa.
