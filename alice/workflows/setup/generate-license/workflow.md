---
name: Generate License
description: Gera arquivo LICENSE com copyright da Embrapa automaticamente usando ano atual do sistema
communication_language: "{communication_language}"
document_output_language: "{document_output_language}"
web_bundle: true
---

# Generate License Workflow

**Goal:** Criar o arquivo LICENSE na raiz do projeto com o copyright correto da Embrapa, utilizando o ano atual calculado dinamicamente.

**Your Role:** In addition to your name, communication_style, and persona, you are also a configuration specialist collaborating with a developer. This is a partnership, not a client-vendor relationship. You bring expertise in licenciamento e padrões Embrapa, while the user brings o contexto do projeto. Work together as equals.

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Step-file architecture**: Each step is a self-contained file, loaded just-in-time, executed sequentially
- **Autonomous Execution**: Workflow autônomo com interação mínima do usuário
- ALWAYS use dynamic year from system date — NEVER use hardcoded year values
- Read each step file completely before acting

---

## HEADLESS MODE

Se `{headless_mode}=true`:
- Pular todos os prompts de confirmação — auto-prosseguir
- Não exibir menus de progresso nem solicitar entrada do usuário
- Gerar resumo JSON ao final com o arquivo criado e ano utilizado

---

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load config: try `{project-root}/_bmad/embrapa-io/config.yaml` first, fall back to `{project-root}/_bmad/config.yaml` + `config.user.yaml`. Use session defaults if neither exists.

Resolve:

- `project_name`, `output_folder`, `user_name`, `communication_language`, `document_output_language`

### 2. First Step EXECUTION

Load, read the full file and then execute `{workflow_path}/steps/step-01-generate-license.md` to begin the workflow.

---

## NEXT STEP SUGGESTION

Ao concluir este workflow, sugerir ao usuário executar o workflow **verify-compliance** (VC) para analisar a conformidade completa do projeto com a plataforma Embrapa I/O.
