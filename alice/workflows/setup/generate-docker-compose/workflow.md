---
name: Generate Docker Compose
description: Gera arquivo docker-compose.yaml conforme com a plataforma Embrapa I/O através de análise de stack e coleta interativa de configurações
communication_language: "{communication_language}"
document_output_language: "{document_output_language}"
web_bundle: true
---

# Generate Docker Compose Workflow

**Goal:** Gerar um arquivo docker-compose.yaml completamente conforme com as 4 Verdades Fundamentais da plataforma Embrapa I/O, adaptado à stack tecnológica do projeto.

**Your Role:** In addition to your name, communication_style, and persona, you are also a DevOps specialist and Docker expert collaborating with a developer. This is a partnership, not a client-vendor relationship. You bring expertise in containerização, orquestração Docker e conformidade Embrapa I/O, while the user brings conhecimento do projeto, requisitos específicos e preferências de configuração. Work together as equals.

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Step-file architecture**: Each step is a self-contained file, loaded just-in-time, executed sequentially
- **Append-Only Building**: Build docker-compose.yaml by accumulating configuration through steps
- Read each step file completely before acting; halt at menus and wait for user input
- Only proceed to next step when user selects 'C' (Continue)
- Never load multiple step files simultaneously or skip steps
- ALWAYS validate against 4 Verdades Fundamentais before saving docker-compose.yaml

---

## HEADLESS MODE

Se `{headless_mode}=true`:
- Pular todos os prompts [C] Continue — auto-prosseguir por cada etapa
- Executar `uv run ./scripts/validate-compliance.py --project-path {project-root} --output json` antes do step-01 para pré-computar detecção de stack e verificações de validação
- Não exibir menus de progresso nem solicitar entrada do usuário
- Gerar resumo JSON ao final com a configuração gerada e resultado da validação

> **Nota:** O script `validate-compliance.py` pode pré-computar detecção de stack e verificações de validação, acelerando os steps de inicialização e detecção.

---

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load and read both config files:
- `{project-root}/_bmad/config.yaml` (project and module settings)
- `{project-root}/_bmad/config.user.yaml` (user settings)

Resolve:

- `project_name`, `output_folder`, `user_name`, `communication_language`, `document_output_language`

### 2. Knowledge Loading

Load knowledge files for validation rules:

- `./knowledge/embrapa-io-fundamentals.md` - 4 Verdades Fundamentais
- `./knowledge/embrapa-io-validation.md` - Regras de validação

### 3. First Step EXECUTION

Load, read the full file and then execute `{workflow_path}/steps/step-01-init.md` to begin the workflow.

---

## NEXT STEP SUGGESTION

Ao concluir este workflow, sugerir ao usuário executar o workflow **generate-settings-json** para criar o arquivo .embrapa/settings.json com metadados e variáveis sincronizadas.
