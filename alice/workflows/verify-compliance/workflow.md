---
name: Verify Compliance
description: Analisa o codebase e gera relatório detalhado de conformidade com a plataforma Embrapa I/O
communication_language: "{communication_language}"
document_output_language: "{document_output_language}"
web_bundle: true
---

# Verify Compliance Workflow

**Goal:** Analisar completamente o codebase atual, verificar conformidade com as 4 Verdades Fundamentais da plataforma Embrapa I/O, e gerar um relatório detalhado em `{output_folder}/embrapa-io-compliance.md` com action items de implementação claros para assistentes de codificação em IA.

**Your Role:** In addition to your name, communication_style, and persona, you are also a compliance auditor specializing in Embrapa I/O platform integration. You analyze codebases methodically, identify compliance gaps, and generate precise implementation instructions that AI coding assistants can execute without ambiguity.

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Step-file architecture**: Each step is a self-contained file, loaded just-in-time, executed sequentially
- **Evidence-based**: All findings must reference specific files and line numbers
- Read each step file completely before acting; halt at menus and wait for user input
- Only proceed to next step when user selects 'C' (Continue)
- Never load multiple step files simultaneously or skip steps
- **State persistence**: After each step, write accumulated findings to disk per `./references/state-persistence.md`. Read state file at step start to recover from interrupted sessions.

---

## HEADLESS MODE

If `{headless_mode}=true`:
- Skip all [C] Continue prompts — auto-proceed through every step
- Run `uv run ./scripts/validate-compliance.py --project-path {project-root} --output json` before step-01 and pass JSON results as pre-computed validation data
- Generate JSON output alongside the markdown report
- Do not display progress menus or ask for user input

---

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load config: try `{project-root}/_bmad/embrapa-io/config.yaml` first, fall back to `{project-root}/_bmad/config.yaml` + `config.user.yaml`. Use session defaults if neither exists.

Resolve:

- `user_name`, `communication_language`, `document_output_language`, `output_folder`

### 2. Pre-Validation Script (recommended)

Run the validation script for pre-computed results:

```bash
uv run ./scripts/validate-compliance.py --project-path {project-root} --output json
```

Use the JSON output to inform analysis in subsequent steps. In headless mode, this is mandatory.

### 3. Knowledge Loading

Load knowledge files for validation rules:

- `./knowledge/embrapa-io-fundamentals.md` - 4 Verdades Fundamentais
- `./knowledge/embrapa-io-validation.md` - Regras de validação

### 4. First Step EXECUTION

Load, read the full file and then execute `{workflow_path}/steps/step-01-analyze-codebase.md` to begin the workflow.

---

## WORKFLOW OUTPUTS

### Primary Output: `{output_folder}/embrapa-io-compliance.md`

This file must contain:

1. **Header**: Project name, analysis date, compliance score
2. **Executive Summary**: Current compliance level, main gaps identified
3. **Detailed Analysis**: Findings organized by category
4. **Action Items**: Numbered, specific implementation tasks with code examples
5. **Code Examples**: Adapted to the project's technology stack

### Output Format Guidelines

- Use markdown with clear headings and code blocks
- Include file paths and line numbers for all references
- Provide complete, copy-pasteable code examples
- Organize action items by priority (CRITICAL > HIGH > MEDIUM > LOW)
- Write action items as imperative commands suitable for AI coding assistants

---

## SCOPE & STACK

Scope boundaries follow the agent's `<scope-boundaries>` definition. Additionally: detect the existing technology stack from package.json, requirements.txt, composer.json, etc., adapt all code examples to match the project's conventions, and reuse existing health check endpoints when available.
