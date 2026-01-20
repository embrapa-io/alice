---
name: 'step-04-verify-integrations'
description: 'Verificar integrações Sentry/Matomo e bootstrap.sh'
nextStepFile: './step-05-finalize-review.md'
---

# Step 4: Verificar Integrações e Bootstrap

## STEP GOAL:

Verificar se as integrações (quando aplicáveis) e o script bootstrap.sh estão corretamente implementados.

## MANDATORY EXECUTION RULES:

- 🛑 Integrações são verificadas apenas se foram requeridas no relatório
- 📖 bootstrap.sh é obrigatório
- 📋 LICENSE é obrigatório

## Sequence of Instructions

### 1. Verificar bootstrap.sh

**Verificações:**
- [ ] Arquivo `bootstrap.sh` existe
- [ ] Arquivo é executável (`chmod +x`)
- [ ] Script valida pré-requisitos (Docker, Docker Compose)
- [ ] Script cria network externa
- [ ] Script cria volumes externos
- [ ] Script usa variáveis do .env.io

**Resultado:** PASS ✅ / FAIL ❌

### 2. Verificar LICENSE

**Verificações:**
- [ ] Arquivo `LICENSE` existe
- [ ] Contém copyright da Embrapa

```
Copyright © {YEAR} Brazilian Agricultural Research Corporation (Embrapa). All rights reserved.
```

**Resultado:** PASS ✅ / FAIL ❌

### 3. Verificar Integração Sentry (se aplicável)

**Verificar se relatório indicou necessidade de Sentry:**

Se sim:
- [ ] Pacote Sentry instalado (package.json, composer.json, etc.)
- [ ] Sentry.init() configurado
- [ ] DSN vem de variável de ambiente (`SENTRY_DSN` ou `VITE_SENTRY_DSN`)
- [ ] Release configurado com IO_VERSION
- [ ] Environment configurado com IO_STAGE

**Resultado:** PASS ✅ / FAIL ❌ / N/A (não aplicável)

### 4. Verificar Integração Matomo (se aplicável)

**Verificar se relatório indicou necessidade de Matomo:**

Se sim:
- [ ] Código de tracking presente
- [ ] Host = `https://hit.embrapa.io`
- [ ] Site ID vem de variável de ambiente
- [ ] Custom dimensions configuradas

**Resultado:** PASS ✅ / FAIL ❌ / N/A (não aplicável)

### 5. Verificar README.md

**Verificações:**
- [ ] Arquivo README.md existe
- [ ] Contém seção sobre Embrapa I/O ou conformidade
- [ ] Documenta comando de inicialização: `env $(cat .env.io) docker compose up ...`

**Resultado:** PASS ✅ / FAIL ❌

### 6. Compilar Resultado das Verificações

```markdown
## 🔌 Verificação Integrações e Bootstrap

### Arquivos Obrigatórios

| Arquivo | Status |
|---------|--------|
| bootstrap.sh | ✅/❌ |
| LICENSE | ✅/❌ |
| README.md | ✅/❌ |

### bootstrap.sh

| Verificação | Status |
|-------------|--------|
| Existe | ✅/❌ |
| Executável | ✅/❌ |
| Valida Docker | ✅/❌ |
| Cria network | ✅/❌ |
| Cria volumes | ✅/❌ |

### Integrações

| Integração | Status | Observação |
|------------|--------|------------|
| Sentry | ✅/❌/N/A | {obs} |
| Matomo | ✅/❌/N/A | {obs} |

### Resultado Integrações: {PASS/FAIL}
```

Store as `{integrations_review}`.

### 7. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue to Final Report [F] Show Failures Only [X] Abort Review"

#### Menu Handling Logic:

- IF C: Store integrations_review, then load, read entire file, then execute {nextStepFile}
- IF F: Display only failed verifications, then return to menu
- IF X: End review with partial results

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected will you proceed to generate final review report.
