---
name: 'step-03-validate-env'
description: 'Validação dos arquivos .env.example e .env.io.example'
nextStepFile: './step-04-validate-settings.md'
---

# Step 3: Validar Arquivos .env

## STEP GOAL:

Validar os arquivos de variáveis de ambiente (.env.example e .env.io.example) contra as regras da plataforma Embrapa I/O.

## PRE-COMPUTED VALIDATION

If `validate-compliance.py` JSON output is available, use `checks.env` results directly — skip manual file parsing. Focus LLM effort on generating remediation examples.

**Reference checklist:** `{workflow_path}/../references/env-validation-checklist.md`

## MANDATORY EXECUTION RULES:

- 🛑 NEVER skip any validation rule
- 📖 DOCUMENT every finding with severity
- 📋 Ensure no variable duplication between files

## Sequence of Instructions

### 1. Verificar Presença de Arquivos

**Arquivos obrigatórios:**
- [ ] `.env.io.example` - Variáveis da plataforma
- [ ] `.env.example` - Variáveis da aplicação

**Se ausente:**
- `.env.io.example` ausente: CRITICAL
- `.env.example` ausente: CRITICAL

### 2. Validar Estrutura do .env.io.example

**Variáveis OBRIGATÓRIAS no .env.io.example:**

```ini
COMPOSE_PROJECT_NAME={io_project}_{io_app}_development
COMPOSE_PROFILES=development
IO_SERVER=localhost
IO_PROJECT={io_project}
IO_APP={io_app}
IO_STAGE=development
IO_VERSION=0.YY.M-dev.1
IO_DEPLOYER=first.surname@embrapa.br
SENTRY_DSN=GET_IN_DASHBOARD
MATOMO_ID={matomo_id}
MATOMO_TOKEN=
```

**Validações:**
- [ ] `COMPOSE_PROJECT_NAME` presente e no formato correto: `{io_project}_{io_app}_{io_stage}` (SEMPRE 3 partes separadas por underscore, onde a terceira parte é o IO_STAGE — no ambiente local, `_development`)
  - ⚠️ Se o valor contiver apenas 2 partes (`{io_project}_{io_app}` sem `_development`), marcar como **INCORRETO** e gerar action item para corrigir
  - O formato correto é SEMPRE a concatenação de IO_PROJECT + "_" + IO_APP + "_" + IO_STAGE
- [ ] `COMPOSE_PROFILES` presente
- [ ] `IO_SERVER` presente
- [ ] `IO_PROJECT` presente (formato unix: lowercase, letras, números, hífens)
- [ ] `IO_APP` presente (formato unix: lowercase, letras, números, hífens)
- [ ] `IO_STAGE` presente
- [ ] `IO_VERSION` presente e no formato `0.YY.M-dev.1`
- [ ] `IO_DEPLOYER` presente (formato email)
- [ ] `SENTRY_DSN` presente
- [ ] `MATOMO_ID` presente

**Se variável obrigatória ausente:**
- Severidade: HIGH
- Action Item: "Adicionar variável `X` ao .env.io.example"

### 3. Validar Formato IO_VERSION

**Formato obrigatório:** `0.YY.M-dev.1`

Onde:
- YY = ano com 2 dígitos (ex: 25 para 2025, 26 para 2026)
- M = mês SEM zero à esquerda (1-12, não 01-12)

**Exemplos:**
```ini
# ✅ CORRETOS
IO_VERSION=0.25.10-dev.1    # Outubro 2025
IO_VERSION=0.26.1-dev.1     # Janeiro 2026
IO_VERSION=0.25.7-dev.1     # Julho 2025

# ❌ INCORRETOS
IO_VERSION=0.25.07-dev.1    # Mês com zero
IO_VERSION=1.0.0            # Formato semver padrão
IO_VERSION=0.2025.10-dev.1  # Ano com 4 dígitos
```

### 4. Validar .env.example (Variáveis da Aplicação)

**Regras críticas:**

#### 4.1 Sem duplicação de variáveis do .env.io

```ini
# ❌ INCORRETO - variável do .env.io no .env
IO_PROJECT=my-project
SENTRY_DSN=...

# ✅ CORRETO - apenas variáveis da aplicação
APP_PORT=3000
DB_HOST=db
DB_PASSWORD=secret
```

**Se encontrar variável duplicada:**
- Severidade: CRITICAL
- Action Item: "Remover variável `X` do .env.example (pertence ao .env.io)"

#### 4.2 Sem espaços ou aspas nos valores

```ini
# ❌ INCORRETO
APP_TITLE="My Application"
DB_NAME=my database

# ✅ CORRETO
APP_TITLE=My_Application
DB_NAME=my-database
```

**Se encontrar espaços ou aspas:**
- Severidade: CRITICAL
- Action Item: "Remover aspas/espaços do valor da variável `X`. Use underscore ou hífen"

#### 4.3 Convenção de nomenclatura para volumes

```ini
# ✅ CORRETO - padrão para volumes
DB_VOLUME={io_project}_{io_app}_{io_stage}_db
PGADMIN_VOLUME={io_project}_{io_app}_{io_stage}_pgadmin
```

### 5. Verificar .gitignore

**Regra:** `.env`, `.env.io` e `.env.sh` devem estar no .gitignore, além dos diretórios de agentes de IA.

```gitignore
# Variáveis de ambiente (não versionar valores reais)
.env
.env.io
.env.sh

# Agentes de IA e IDEs
.agent/
.agents/
.augment/
.claude/
.cline/
.codebuddy/
.crush/
.cursor/
.gemini/
.github/
.iflow/
.kilocode/
.kiro/
.ona/
.opencode/
.pi/
.qoder/
.qwen/
.roo/
.rovodev/
.trae/
.windsurf/
_bmad/
```

**Se não estiver no .gitignore:**
- Severidade: MEDIUM
- Action Item: "Adicionar `.env`, `.env.io` e `.env.sh` ao .gitignore, e incluir diretórios de agentes de IA"

### 6. Compilar Resultados da Validação Env

Organizar findings em:

```markdown
## 📝 Validação Arquivos .env

### Status: {COMPLIANT | PARTIAL | NON-COMPLIANT}

### .env.io.example
| Variável | Status | Observação |
|----------|--------|------------|
| COMPOSE_PROJECT_NAME | ✅/❌ | ... |
| IO_PROJECT | ✅/❌ | ... |
| ... | ... | ... |

### .env.example
| # | Severidade | Problema | Solução |
|---|------------|----------|---------|
| 1 | CRITICAL | Variável X duplicada | Remover do .env.example |
| ... | ... | ... | ... |

### Resumo
- CRITICAL: {count}
- HIGH: {count}
- MEDIUM: {count}
```

Store as `{env_findings}`.

### 7. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue to Settings Validation [X] Exit workflow"

#### Menu Handling Logic:

- IF C: Store env_findings, then load, read entire file, then execute {nextStepFile}
- IF X: End workflow gracefully

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected will you then load and read fully `{nextStepFile}` to continue validation.
