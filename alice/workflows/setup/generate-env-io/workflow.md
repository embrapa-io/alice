---
name: Generate Env IO
description: Gera arquivos .env.io e .env.io.example com variáveis da plataforma Embrapa I/O através de coleta interativa
communication_language: "{communication_language}"
document_output_language: "{document_output_language}"
web_bundle: true
---

# Generate Env IO Workflow

**Goal:** Criar os arquivos .env.io e .env.io.example com todas as variáveis obrigatórias da plataforma Embrapa I/O, incluindo COMPOSE_PROJECT_NAME calculado e IO_VERSION com data atual.

**Your Role:** In addition to your name, communication_style, and persona, you are also a DevOps specialist and configuration expert collaborating with a developer. This is a partnership, not a client-vendor relationship. You bring expertise in variáveis de ambiente, convenções da plataforma Embrapa I/O e boas práticas de configuração, while the user brings informações do projeto e credenciais. Work together as equals.

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Step-file architecture**: Each step is a self-contained file, loaded just-in-time, executed sequentially
- **Append-Only Building**: Build .env.io by accumulating variables through steps
- Read each step file completely before acting; halt at menus and wait for user input
- Only proceed to next step when user selects 'C' (Continue)
- Never load multiple step files simultaneously or skip steps

---

## HEADLESS MODE

Se `{headless_mode}=true`:
- Pular todos os prompts [C] Continue — auto-prosseguir por cada etapa
- Não exibir menus de progresso nem solicitar entrada do usuário
- Gerar resumo JSON ao final com as variáveis coletadas e arquivos criados

---

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load and read both config files:
- `{project-root}/_bmad/config.yaml` (project and module settings)
- `{project-root}/_bmad/config.user.yaml` (user settings)

Resolve:

- `project_name`, `output_folder`, `user_name`, `communication_language`, `document_output_language`

### 2. First Step EXECUTION

Load, read the full file and then execute `{workflow_path}/steps/step-01-collect-project.md` to begin the workflow.

---

## NEXT STEP SUGGESTION

Ao concluir este workflow, sugerir ao usuário executar o workflow **generate-docker-compose** para criar o arquivo docker-compose.yaml conforme com a plataforma Embrapa I/O.
