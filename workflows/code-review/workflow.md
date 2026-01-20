---
name: Code Review
description: Verifica se todas as implementações de conformidade foram realizadas corretamente
web_bundle: true
---

# Code Review Workflow

**Goal:** Confrontar o arquivo `{output_folder}/embrapa-io-compliance.md` com o codebase atual, verificando se todas as especificações de conformidade foram implementadas corretamente. Este review foca EXCLUSIVAMENTE em conformidade Embrapa I/O, não em boas práticas gerais de código.

**Your Role:** In addition to your name, communication_style, and persona, you are also a compliance auditor performing final verification. You verify that all action items from the compliance report have been correctly implemented and that the application will work with Docker Compose using the standard command.

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Report-Based Verification**: Compare implementation against compliance report
- **Compliance-Only Focus**: Do NOT review code quality, security, or best practices
- **Evidence-Based**: Document specific file locations and content
- **Pass/Fail Criteria**: Clear criteria for each verification

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **VERIFY AGAINST REPORT**: Each check references the compliance report
3. **DOCUMENT FINDINGS**: Record pass/fail with evidence
4. **NO CODE IMPROVEMENTS**: Only verify compliance, do not suggest improvements

### Critical Rules (NO EXCEPTIONS)

- 🛑 **ONLY** verify compliance with Embrapa I/O platform
- 📖 **DO NOT** review code quality, security, or maintainability
- 🚫 **DO NOT** suggest improvements to legacy code
- 💾 **DOCUMENT** all findings with file paths and evidence
- 🎯 **FOCUS** on Docker Compose functionality
- ⏸️ **PASS/FAIL** each verification clearly
- 📋 **UPDATE** the compliance report with final status

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

### Out of Scope (DO NOT REVIEW)

- Code quality
- Security vulnerabilities
- Performance issues
- Maintainability concerns
- Test coverage
- Documentation completeness
- CI/CD configuration

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

Load and read full config from `{project-root}/_bmad/embrapa-io/config.yaml`.

### 2. Load Compliance Report

Load `{output_folder}/embrapa-io-compliance.md` for reference.

### 3. First Step EXECUTION

Load, read the full file and then execute `{workflow_path}/steps/step-01-verify-docker.md` to begin review.
