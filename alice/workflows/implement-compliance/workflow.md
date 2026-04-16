---
name: Implement Compliance
description: Executa os action items do relatório de conformidade para alcançar 100% de compliance com Embrapa I/O
communication_language: "{communication_language}"
document_output_language: "{document_output_language}"
web_bundle: true
---

# Implement Compliance Workflow

**Goal:** Executar todos os action items documentados em `{output_folder}/embrapa-io-compliance.md` para alcançar 100% de conformidade com a plataforma Embrapa I/O. Após a implementação, criar os arquivos `.env` e `.env.io` a partir dos templates e gerar o script `bootstrap.sh`.

**Your Role:** In addition to your name, communication_style, and persona, you are also a DevOps implementation specialist. You execute precise infrastructure changes based on the compliance report, adapting code examples to the project's technology stack while minimizing changes to functional code.

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Step-file architecture**: Each step is a self-contained file, loaded just-in-time, executed sequentially
- **Report-driven**: All changes based on `embrapa-io-compliance.md`, processed by priority (CRITICAL → HIGH → MEDIUM → LOW)
- Read each step file completely before acting; verify each change before proceeding
- Never modify functional code unless absolutely necessary for Sentry/Matomo; never create new endpoints
- Halt on any error and ask user for guidance; reuse existing health check endpoints
- **State persistence**: After each step, write progress to disk per `./references/state-persistence.md`. Track completed action items for recovery.

---

## HEADLESS MODE

If `{headless_mode}=true`:
- Skip all confirmation prompts — auto-proceed through every action item
- Halt only on errors that require human judgment (ambiguous code changes)
- Generate JSON summary of all changes made alongside the updated compliance report

---

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load and read both config files:
- `{project-root}/_bmad/config.yaml` (project and module settings)
- `{project-root}/_bmad/config.user.yaml` (user settings)

### 2. Load Compliance Report

Load and parse `{output_folder}/embrapa-io-compliance.md`:
- Extract all action items
- Identify priorities (CRITICAL, HIGH, MEDIUM, LOW)
- Count total items to implement

### 3. First Step EXECUTION

Load, read the full file and then execute `{workflow_path}/steps/step-01-validate-report.md` to begin implementation.

---

## WORKFLOW OUTPUTS

### Modified/Created Files:

1. **Infrastructure Files:**
   - `docker-compose.yaml` (modified)
   - `.env.example` (created/modified)
   - `.env.io.example` (created/modified)
   - `.embrapa/settings.json` (created/modified)
   - `Dockerfile` (modified if needed)
   - `LICENSE` (created if needed)

2. **Environment Files (from templates):**
   - `.env` (created from `.env.example`)
   - `.env.io` (created from `.env.io.example`)

3. **Bootstrap Script:**
   - `bootstrap.sh` (created)

4. **Integration Files (if applicable):**
   - Sentry configuration
   - Matomo tracking configuration

---

## SCOPE & STACK

Scope boundaries follow the agent's `<scope-boundaries>` definition. Additionally: this workflow also creates `.env`, `.env.io`, and `bootstrap.sh`. Use code examples from the compliance report (already adapted to stack), follow existing code conventions, and preserve existing functionality in all modified files.
