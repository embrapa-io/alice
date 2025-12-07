---
name: Generate Settings JSON
description: Gera arquivo .embrapa/settings.json conforme com a plataforma Embrapa I/O com sincronização automática de variáveis dos arquivos .env
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

- **Micro-file Design**: Each step is a self contained instruction file that is a part of an overall workflow that must be followed exactly
- **Just-In-Time Loading**: Only the current step file is in memory - never load future step files until told to do so
- **Sequential Enforcement**: Sequence within the step files must be completed in order, no skipping or optimization allowed
- **State Tracking**: Document progress in context for settings tracking
- **Variable Synchronization**: Ensure variables.default matches .env files exactly
- **Append-Only Building**: Build settings.json by accumulating configuration through steps

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order, never deviate
3. **WAIT FOR INPUT**: If a menu is presented, halt and wait for user selection
4. **CHECK CONTINUATION**: If the step has a menu with Continue as an option, only proceed to next step when user selects 'C' (Continue)
5. **SAVE STATE**: Track collected variables in context before loading next step
6. **LOAD NEXT**: When directed, load, read entire file, then execute the next step file

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** load multiple step files simultaneously
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps or optimize the sequence
- 💾 **ALWAYS** validate JSON structure before saving
- 🎯 **ALWAYS** follow the exact instructions in the step file
- ⏸️ **ALWAYS** halt at menus and wait for user input
- 📋 **NEVER** create mental todo lists from future steps

---

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load and read full config from {project-root}/.bmad/embrapa-io/config.yaml and resolve:

- `project_name`, `output_folder`, `user_name`, `communication_language`, `document_output_language`

### 2. First Step EXECUTION

Load, read the full file and then execute `{workflow_path}/steps/step-01-detect-stack.md` to begin the workflow.
