---
name: Implement Compliance
description: Executa os action items do relatório de conformidade para alcançar 100% de compliance com Embrapa I/O
web_bundle: true
---

# Implement Compliance Workflow

**Goal:** Executar todos os action items documentados em `{output_folder}/embrapa-io-compliance.md` para alcançar 100% de conformidade com a plataforma Embrapa I/O. Após a implementação, criar os arquivos `.env` e `.env.io` a partir dos templates e gerar o script `bootstrap.sh`.

**Your Role:** In addition to your name, communication_style, and persona, you are also a DevOps implementation specialist. You execute precise infrastructure changes based on the compliance report, adapting code examples to the project's technology stack while minimizing changes to functional code.

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Report-Driven**: All changes based on `embrapa-io-compliance.md`
- **Minimal Impact**: Only modify files within defined scope
- **Sequential Execution**: Process action items by priority (CRITICAL → HIGH → MEDIUM → LOW)
- **Verification After Each Change**: Validate syntax after modifications

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute action items in priority order
3. **VALIDATE**: Verify each change before proceeding
4. **DOCUMENT**: Mark completed items in the report

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** modify functional application code unless absolutely necessary for Sentry/Matomo
- 📖 **ALWAYS** read the compliance report first
- 🚫 **NEVER** create new API endpoints
- 💾 **ALWAYS** backup files before modifying (mental note of original content)
- 🎯 **ALWAYS** follow the exact code examples from the report
- ⏸️ **HALT** on any error and ask user for guidance
- 📋 **FOCUS** exclusively on Docker Compose - Docker Swarm is OUT OF SCOPE
- 🔧 **REUSE** existing health check endpoints when available

---

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load and read full config from `{project-root}/_bmad/embrapa-io/config.yaml`.

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

## SCOPE BOUNDARIES

### Allowed Modifications

- docker-compose.yaml / docker-compose.yml
- .env.example, .env.io.example, .env, .env.io
- .embrapa/settings.json
- LICENSE
- Dockerfile(s)
- bootstrap.sh
- Sentry/Matomo configuration files
- README.md (add compliance section only)

### Forbidden Modifications

- Application source code (except Sentry/Matomo integration points)
- API routes or endpoints
- Business logic
- Database schemas
- Test files
- CI/CD configurations

---

## TECHNOLOGY STACK ADAPTATION

The workflow must:

1. **Use code examples from the compliance report** (already adapted to stack)
2. **Follow existing code conventions** in the project
3. **Reuse existing dependencies** when possible
4. **Preserve existing functionality** in all modified files
