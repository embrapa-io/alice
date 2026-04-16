---
name: 'step-02-verify-env'
description: 'Verificar implementação dos arquivos .env'
nextStepFile: './step-03-verify-settings.md'
---

# Step 2: Verificar Arquivos .env

## STEP GOAL:

Verificar se os arquivos de variáveis de ambiente estão corretamente implementados conforme o relatório de conformidade.

## PRE-COMPUTED VALIDATION

If `validate-compliance.py` JSON output is available, use `checks.env` results directly for pass/fail determination.

**Reference checklist:** `{workflow_path}/../references/env-validation-checklist.md`

## Rules

Follow `./references/step-file-protocol.md`. Step-specific:
- PASS/FAIL each verification clearly
- Check both .example and actual files (unless pre-computed)
- Verify no duplicates between files

## Sequence of Instructions

### 1. Verificar Presença de Arquivos

**Arquivos obrigatórios:**
- [ ] `.env.io.example` existe
- [ ] `.env.example` existe
- [ ] `.env.io` existe (criado pelo workflow de implementação)
- [ ] `.env` existe (criado pelo workflow de implementação)

**Resultado:** PASS ✅ / FAIL ❌

### 2. Verificar .env.io.example

**Variáveis obrigatórias:**
- [ ] `COMPOSE_PROJECT_NAME` presente e formato correto: `{io_project}_{io_app}_{io_stage}` (SEMPRE 3 partes — no local, `_development`). ⚠️ Formato `{io_project}_{io_app}` sem `_development` é INCORRETO
- [ ] `COMPOSE_PROFILES` presente
- [ ] `IO_SERVER` presente
- [ ] `IO_PROJECT` presente
- [ ] `IO_APP` presente
- [ ] `IO_STAGE` presente
- [ ] `IO_VERSION` presente e formato `0.YY.M-dev.1`
- [ ] `IO_DEPLOYER` presente
- [ ] `SENTRY_DSN` presente
- [ ] `MATOMO_ID` presente

**Resultado:** PASS ✅ / FAIL ❌

### 3. Verificar .env.io

**Verificar valores preenchidos:**
- [ ] `IO_PROJECT` tem valor válido (formato unix)
- [ ] `IO_APP` tem valor válido (formato unix)
- [ ] `IO_VERSION` formato correto (`0.YY.M-dev.1`)
- [ ] `COMPOSE_PROJECT_NAME` = `{IO_PROJECT}_{IO_APP}_development` (SEMPRE 3 partes: project_app_stage — NUNCA omitir `_development`)

**Resultado:** PASS ✅ / FAIL ❌

### 4. Verificar .env.example

**Regras:**
- [ ] Nenhuma variável do .env.io duplicada
- [ ] Nenhum valor com espaços
- [ ] Nenhum valor com aspas
- [ ] Variáveis de volume seguem padrão correto

**Variáveis que NÃO devem estar no .env.example:**
```
COMPOSE_PROJECT_NAME, COMPOSE_PROFILES, IO_SERVER, IO_PROJECT,
IO_APP, IO_STAGE, IO_VERSION, IO_DEPLOYER, SENTRY_DSN, MATOMO_ID, MATOMO_TOKEN
```

**Resultado:** PASS ✅ / FAIL ❌

### 5. Verificar .env

**Verificar:**
- [ ] Arquivo existe
- [ ] Valores de volume preenchidos corretamente
- [ ] Secrets/passwords gerados (não vazios para tipos sensíveis)

**Resultado:** PASS ✅ / FAIL ❌

### 6. Verificar .gitignore

**Verificar:**
- [ ] `.env` está listado
- [ ] `.env.io` está listado
- [ ] `.env.sh` está listado
- [ ] Diretórios de agentes de IA estão listados (`.claude/`, `_bmad/`, etc.)

**Resultado:** PASS ✅ / FAIL ❌

### 7. Compilar Resultado da Verificação Env

```markdown
## 📝 Verificação Arquivos .env

### Presença de Arquivos

| Arquivo | Status |
|---------|--------|
| .env.io.example | ✅/❌ |
| .env.example | ✅/❌ |
| .env.io | ✅/❌ |
| .env | ✅/❌ |

### .env.io.example - Variáveis Obrigatórias

| Variável | Status |
|----------|--------|
| COMPOSE_PROJECT_NAME | ✅/❌ |
| IO_PROJECT | ✅/❌ |
| IO_APP | ✅/❌ |
| IO_STAGE | ✅/❌ |
| IO_VERSION | ✅/❌ |
| SENTRY_DSN | ✅/❌ |
| MATOMO_ID | ✅/❌ |

### .env.example - Validações

| Verificação | Status |
|-------------|--------|
| Sem duplicatas do .env.io | ✅/❌ |
| Sem espaços nos valores | ✅/❌ |
| Sem aspas nos valores | ✅/❌ |

### .gitignore

| Entrada | Ignorado |
|---------|----------|
| .env | ✅/❌ |
| .env.io | ✅/❌ |
| .env.sh | ✅/❌ |
| Diretórios AI (.claude/, _bmad/, etc.) | ✅/❌ |

### Resultado Env: {PASS/FAIL}
```

Store as `{env_review}`.

### 8. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue to Settings Verification [F] Show Failures Only [X] Abort Review"

#### Menu Handling Logic:

- IF C: Store env_review, then load, read entire file, then execute {nextStepFile}
- IF F: Display only failed verifications, then return to menu
- IF X: End review with partial results

