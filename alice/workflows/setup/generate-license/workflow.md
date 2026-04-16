---
name: Generate License
description: Gera arquivo LICENSE com copyright da Embrapa automaticamente usando ano atual do sistema
web_bundle: true
---

# Generate License Workflow

**Goal:** Criar o arquivo LICENSE na raiz do projeto com o copyright correto da Embrapa, utilizando o ano atual calculado dinamicamente.

**Your Role:** In addition to your name, communication_style, and persona, you are also a configuration specialist collaborating with a developer. This is a partnership, not a client-vendor relationship. You bring expertise in licenciamento e padrões Embrapa, while the user brings o contexto do projeto. Work together as equals.

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Micro-file Design**: Each step is a self contained instruction file that is a part of an overall workflow that must be followed exactly
- **Just-In-Time Loading**: Only the current step file is in memory - never load future step files until told to do so
- **Sequential Enforcement**: Sequence within the step files must be completed in order, no skipping or optimization allowed
- **State Tracking**: Document progress in context
- **Autonomous Execution**: This workflow is largely autonomous with minimal user interaction

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order, never deviate
3. **WAIT FOR INPUT**: If a menu is presented, halt and wait for user selection
4. **CHECK CONTINUATION**: If the step has a menu with Continue as an option, only proceed to next step when user selects 'C' (Continue)
5. **SAVE STATE**: Track variables in context before loading next step
6. **LOAD NEXT**: When directed, load, read entire file, then execute the next step file

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** load multiple step files simultaneously
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps or optimize the sequence
- 💾 **ALWAYS** use dynamic year from system date
- 🎯 **ALWAYS** follow the exact instructions in the step file
- ⏸️ **ALWAYS** halt at menus and wait for user input
- 📋 **NEVER** use hardcoded year values

---

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load and read both config files:
- `{project-root}/_bmad/config.yaml` (project and module settings)
- `{project-root}/_bmad/config.user.yaml` (user settings)

Resolve:

- `project_name`, `output_folder`, `user_name`, `communication_language`, `document_output_language`

### 2. First Step EXECUTION

Load, read the full file and then execute `{workflow_path}/steps/step-01-generate-license.md` to begin the workflow.
