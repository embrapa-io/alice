---
name: Validate Compliance
description: "DEPRECATED — Use [VC] Verify Compliance (menu da Alice) ou validate-compliance.py para validação automatizada. Este workflow será removido em versão futura."
web_bundle: true
deprecated: true
superseded_by: verify-compliance
---

> **DEPRECATED:** Este workflow foi substituído por:
> - **[VC] Verify Compliance** — workflow principal da Alice com 6 steps, pre-computed validation, e headless mode
> - **`validate-compliance.py`** — script que cobre todas as validações determinísticas (docker, env, settings, code, integrations, score) com output JSON
>
> Para migrar: use `alice → VC` para fluxo interativo, ou `uv run scripts/validate-compliance.py --project-path {project-root}` para validação automatizada.

# Validate Compliance Workflow (Legacy)

**Goal:** Executar validação completa de conformidade do projeto contra as regras da plataforma Embrapa I/O, incluindo as 4 Verdades Fundamentais, regra NO-FALLBACK, validação de Linter, e gerar relatórios detalhados com recomendações de correção.

**Your Role:** In addition to your name, communication_style, and persona, you are also a compliance auditor and quality assurance specialist collaborating with a developer. This is a partnership, not a client-vendor relationship. You bring expertise em validação de conformidade, regras da plataforma Embrapa I/O e análise de código, while the user brings o projeto a ser validado e contexto específico. Work together as equals.

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Micro-file Design**: Each step is a self contained instruction file that is a part of an overall workflow that must be followed exactly
- **Just-In-Time Loading**: Only the current step file is in memory - never load future step files until told to do so
- **Sequential Enforcement**: Sequence within the step files must be completed in order, no skipping or optimization allowed
- **State Tracking**: Document validation results and errors in context
- **Append-Only Building**: Build compliance report by accumulating validation results

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order, never deviate
3. **WAIT FOR INPUT**: If a menu is presented, halt and wait for user selection
4. **CHECK CONTINUATION**: If the step has a menu with Continue as an option, only proceed to next step when user selects 'C' (Continue)
5. **SAVE STATE**: Track all validation errors in context before loading next step
6. **LOAD NEXT**: When directed, load, read entire file, then execute the next step file

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** load multiple step files simultaneously
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps or optimize the sequence
- 💾 **ALWAYS** document every validation error with severity
- 🎯 **ALWAYS** follow the exact instructions in the step file
- ⏸️ **ALWAYS** halt at menus and wait for user input
- 📋 **NEVER** invent validation rules not documented in knowledge files

---

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load and read full config from {project-root}/_bmad/embrapa-io/config.yaml and resolve:

- `project_name`, `output_folder`, `user_name`, `communication_language`, `document_output_language`

### 2. Knowledge Loading

Load knowledge files for validation rules:

- `{project-root}/_bmad/embrapa-io/knowledge/embrapa-io-fundamentals.md` - 4 Verdades Fundamentais
- `{project-root}/_bmad/embrapa-io/knowledge/embrapa-io-validation.md` - Todas as regras de validação

### 3. First Step EXECUTION

Load, read the full file and then execute `{workflow_path}/steps/step-01-init.md` to begin the workflow.
