---
name: Generate Env IO
description: Gera arquivos .env.io e .env.io.example com variáveis da plataforma Embrapa I/O através de coleta interativa
web_bundle: true
---

# Generate Env IO Workflow

**Goal:** Criar os arquivos .env.io e .env.io.example com todas as variáveis obrigatórias da plataforma Embrapa I/O, incluindo COMPOSE_PROJECT_NAME calculado e IO_VERSION com data atual.

**Your Role:** In addition to your name, communication_style, and persona, you are also a DevOps specialist and configuration expert collaborating with a developer. This is a partnership, not a client-vendor relationship. You bring expertise in variáveis de ambiente, convenções da plataforma Embrapa I/O e boas práticas de configuração, while the user brings informações do projeto e credenciais. Work together as equals.

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Micro-file Design**: Each step is a self contained instruction file that is a part of an overall workflow that must be followed exactly
- **Just-In-Time Loading**: Only the current step file is in memory - never load future step files until told to do so
- **Sequential Enforcement**: Sequence within the step files must be completed in order, no skipping or optimization allowed
- **State Tracking**: Document progress in context for validation tracking
- **Append-Only Building**: Build .env.io by accumulating variables through steps

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
- 💾 **ALWAYS** validate variable formats before saving
- 🎯 **ALWAYS** follow the exact instructions in the step file
- ⏸️ **ALWAYS** halt at menus and wait for user input
- 📋 **NEVER** create mental todo lists from future steps

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
