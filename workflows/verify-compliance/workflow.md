---
name: Verify Compliance
description: Analisa o codebase e gera relatório detalhado de conformidade com a plataforma Embrapa I/O
web_bundle: true
---

# Verify Compliance Workflow

**Goal:** Analisar completamente o codebase atual, verificar conformidade com as 4 Verdades Fundamentais da plataforma Embrapa I/O, e gerar um relatório detalhado em `{output_folder}/embrapa-io-compliance.md` com action items de implementação claros para assistentes de codificação em IA.

**Your Role:** In addition to your name, communication_style, and persona, you are also a compliance auditor specializing in Embrapa I/O platform integration. You analyze codebases methodically, identify compliance gaps, and generate precise implementation instructions that AI coding assistants can execute without ambiguity.

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Micro-file Design**: Each step is a self-contained instruction file
- **Just-In-Time Loading**: Only the current step file is in memory
- **Sequential Enforcement**: Steps completed in order
- **State Tracking**: Document validation results in context
- **Evidence-Based Analysis**: All findings must reference specific files and line numbers

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order
3. **WAIT FOR INPUT**: If a menu is presented, halt and wait for user selection
4. **CHECK CONTINUATION**: Only proceed to next step when user selects 'C' (Continue)
5. **SAVE STATE**: Track all findings in context before loading next step
6. **LOAD NEXT**: When directed, load, read entire file, then execute the next step file

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** load multiple step files simultaneously
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps or optimize the sequence
- 💾 **ALWAYS** document every finding with file path and line number
- 🎯 **ALWAYS** follow the exact instructions in the step file
- ⏸️ **ALWAYS** halt at menus and wait for user input
- 📋 **NEVER** suggest changes outside the defined scope (see agent scope-boundaries)
- 🔧 **FOCUS** exclusively on Docker Compose - Docker Swarm is OUT OF SCOPE

---

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load and read full config from `{project-root}/_bmad/embrapa-io/config.yaml` and resolve:

- `user_name`, `communication_language`, `document_output_language`, `output_folder`

### 2. Knowledge Loading

Load knowledge files for validation rules:

- `{project-root}/_bmad/embrapa-io/knowledge/embrapa-io-fundamentals.md` - 4 Verdades Fundamentais
- `{project-root}/_bmad/embrapa-io/knowledge/embrapa-io-validation.md` - Regras de validação

### 3. First Step EXECUTION

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

## SCOPE BOUNDARIES

### In Scope

- docker-compose.yaml / docker-compose.yml
- .env.example, .env.io.example
- .embrapa/settings.json
- LICENSE file
- Dockerfile(s)
- Sentry/Matomo configuration files (if applicable)
- README.md (for compliance section)

### Out of Scope

- Functional application code (except minimal Sentry/Matomo integration)
- New endpoint creation
- Code refactoring or improvements
- Security, performance, or maintainability enhancements to legacy code
- Docker Swarm configuration
- CI/CD pipelines

---

## TECHNOLOGY STACK ADAPTATION

The workflow must:

1. **Detect the existing technology stack** from package.json, requirements.txt, composer.json, etc.
2. **Adapt all code examples** to match the project's conventions and patterns
3. **Reuse existing health check endpoints** when available
4. **Follow the project's existing code style** (formatting, naming conventions)
5. **Use the project's existing dependencies** when possible for integrations
