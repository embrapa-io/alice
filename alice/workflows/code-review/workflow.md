---
name: Code Review
description: Verifica se todas as implementações de conformidade foram realizadas corretamente
communication_language: "{communication_language}"
document_output_language: "{document_output_language}"
web_bundle: true
---

# Code Review Workflow

**Goal:** Confrontar o arquivo `{output_folder}/embrapa-io-compliance.md` com o codebase atual, verificando se todas as especificações de conformidade foram implementadas corretamente. Este review foca EXCLUSIVAMENTE em conformidade Embrapa I/O, não em boas práticas gerais de código.

**Your Role:** In addition to your name, communication_style, and persona, you are also a compliance auditor performing final verification. You verify that all action items from the compliance report have been correctly implemented and that the application will work with Docker Compose using the standard command.

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Step-file architecture**: Each step is a self-contained file, loaded just-in-time, executed sequentially
- **Report-based verification**: Compare implementation against compliance report with clear pass/fail criteria
- Read each step file completely before acting; document all findings with file paths and evidence
- Only verify Embrapa I/O compliance — do NOT review code quality, security, or maintainability
- Update the compliance report with final status after each verification

---

## SCOPE OF REVIEW

### In Scope (VERIFY THESE)

1. **Docker Compose Configuration**
   - 4 Verdades Fundamentais implemented
   - Services start correctly with standard command
   - Health checks pass
   - CLI services (backup, restore, sanitize) work

2. **Environment Files**
   - .env.io.example has all required variables
   - .env.example has application variables
   - No duplicates between files
   - No spaces or quotes in values

3. **Settings File**
   - .embrapa/settings.json exists and is valid
   - All required fields present
   - orchestrators = ["DockerCompose"]

4. **Bootstrap Script**
   - bootstrap.sh exists and is executable
   - Creates network and volumes correctly

5. **Integrations (if applicable)**
   - Sentry configured with correct DSN source
   - Matomo configured with correct host and ID

### Out of Scope

Per agent's `<scope-boundaries>` — additionally: do NOT review code quality, security, performance, maintainability, test coverage, or CI/CD.

---

## HEADLESS MODE

If `{headless_mode}=true`:
- Skip all [C] Continue prompts — auto-proceed through every verification
- Run `uv run ./scripts/validate-compliance.py --project-path {project-root} --output json` for pre-computed validation
- Use script output for deterministic checks; LLM focuses on report-vs-code comparison
- Generate JSON pass/fail summary alongside the updated compliance report

---

## VERIFICATION COMMAND

The primary test is that the application starts correctly with:

```bash
env $(cat .env.io) docker compose up --force-recreate --build --remove-orphans --wait
```

This command must:
- Build all containers without errors
- Start all services
- Pass all health checks
- Be ready for use

---

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load and read both config files:
- `{project-root}/_bmad/config.yaml` (project and module settings)
- `{project-root}/_bmad/config.user.yaml` (user settings)

### 2. Load Compliance Report

Load `{output_folder}/embrapa-io-compliance.md` for reference.

### 3. First Step EXECUTION

Load, read the full file and then execute `{workflow_path}/steps/step-01-verify-docker.md` to begin review.
