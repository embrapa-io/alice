---
name: 'step-03-implement-high'
description: 'Implementar action items HIGH e MEDIUM'
nextStepFile: './step-04-create-env-files.md'
---

# Step 3: Implementar Action Items HIGH e MEDIUM

## STEP GOAL:

Executar todos os action items de severidade HIGH e MEDIUM do relatório de conformidade.

## MANDATORY EXECUTION RULES:

- 🛑 MUST implement HIGH items
- 📖 MEDIUM items are recommended but can be skipped by user request
- 📋 VALIDATE syntax after each modification
- 🔧 Follow exact code examples from report

## Sequence of Instructions

### 1. Implementar Items HIGH

Para cada action item HIGH, seguir o mesmo processo do step anterior:

**Exemplos comuns de items HIGH:**

**Remover container_name dos serviços:**
```yaml
# ANTES
services:
  app:
    container_name: my-app
    ...

# DEPOIS
services:
  app:
    # container_name removido - nome gerado pelo COMPOSE_PROJECT_NAME
    ...
```

**Converter volumes para externos:**
```yaml
# ANTES
volumes:
  postgres_data:

# DEPOIS
volumes:
  postgres_data:
    external: true
    name: ${DB_VOLUME}
```

**Adicionar healthcheck aos serviços:**
```yaml
services:
  app:
    ...
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/{health_endpoint}"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
```

**Adicionar restart policy:**
```yaml
services:
  app:
    restart: unless-stopped
    ...
```

**Implementar integração Sentry (Node.js):**
```javascript
// Adicionar ao arquivo de entrada (app.js, index.js, main.js)
const Sentry = require('@sentry/node');

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  release: process.env.IO_VERSION.split('-')[0],
  environment: process.env.IO_STAGE,
  tracesSampleRate: 1.0
});
```

**Implementar integração Matomo (Vue.js):**
```javascript
// Adicionar ao plugins/index.js ou main.js
import VueMatomo from 'vue-matomo';

app.use(VueMatomo, {
  host: 'https://hit.embrapa.io',
  siteId: import.meta.env.VITE_MATOMO_ID,
  router,
  preInitActions: [
    ['setCustomDimension', 1, import.meta.env.VITE_IO_STAGE],
    ['setCustomDimension', 2, import.meta.env.VITE_IO_VERSION]
  ]
});
```

### 2. Implementar Items MEDIUM (com confirmação)

Apresentar lista de items MEDIUM:

```markdown
## ℹ️ Action Items MEDIUM ({n} items)

Estes items são recomendados mas não obrigatórios:

{lista de items}

Deseja implementar os items MEDIUM? [Y] Yes [N] No (skip)
```

Se usuário confirmar, implementar cada item.

**Exemplos comuns de items MEDIUM:**

**Adicionar serviços CLI (backup, restore, sanitize):**
```yaml
  backup:
    image: postgres:17-alpine
    profiles: ['cli']
    restart: "no"
    environment:
      PGPASSWORD: ${DB_PASSWORD}
    volumes:
      - backup_data:/backup
      - postgres_data:/var/lib/postgresql/data
    networks:
      - stack
    command: >
      sh -c "
        set -ex &&
        BACKUP_DIR=${IO_PROJECT}_${IO_APP}_${IO_STAGE}_${IO_VERSION}_$$(date +'%Y-%m-%d_%H-%M-%S') &&
        mkdir -p /backup/$$BACKUP_DIR &&
        pg_dump -h db -U ${DB_USER} ${DB_NAME} > /backup/$$BACKUP_DIR/database.sql &&
        tar -czf /backup/$$BACKUP_DIR.tar.gz -C /backup $$BACKUP_DIR &&
        rm -rf /backup/$$BACKUP_DIR &&
        echo 'Backup concluído: '$$BACKUP_DIR'.tar.gz'
      "

  restore:
    image: postgres:17-alpine
    profiles: ['cli']
    restart: "no"
    environment:
      PGPASSWORD: ${DB_PASSWORD}
      BACKUP_FILE_TO_RESTORE: ${BACKUP_FILE_TO_RESTORE:-}
    volumes:
      - backup_data:/backup
      - postgres_data:/var/lib/postgresql/data
    networks:
      - stack
    command: >
      sh -c "
        set -ex &&
        FILE_TO_RESTORE=$${BACKUP_FILE_TO_RESTORE:-no_file_to_restore} &&
        test -f /backup/$$FILE_TO_RESTORE &&
        RESTORE_DIR=$$(mktemp -d) &&
        tar -xf /backup/$$FILE_TO_RESTORE -C $$RESTORE_DIR --strip-components=1 &&
        psql -h db -U ${DB_USER} ${DB_NAME} < $$RESTORE_DIR/database.sql &&
        rm -rf $$RESTORE_DIR &&
        echo 'Restore concluído'
      "

  sanitize:
    image: postgres:17-alpine
    profiles: ['cli']
    restart: "no"
    environment:
      PGPASSWORD: ${DB_PASSWORD}
    networks:
      - stack
    command: >
      sh -c "
        set -ex &&
        psql -h db -U ${DB_USER} ${DB_NAME} -c 'VACUUM ANALYZE;' &&
        echo 'Database otimizado'
      "
```

**Criar arquivo LICENSE:**
```
Copyright © {YEAR} Brazilian Agricultural Research Corporation (Embrapa). All rights reserved.
```

**Substituir portas hardcoded por variáveis:**
```yaml
# ANTES
ports:
  - "3000:3000"

# DEPOIS
ports:
  - "${APP_PORT}:3000"
```

### 3. Resumo de Implementações HIGH/MEDIUM

```markdown
## ✅ Implementações HIGH/MEDIUM Concluídas

### HIGH Items
| # | Action Item | Status |
|---|-------------|--------|
| ... | ... | ✅ Implementado |

### MEDIUM Items
| # | Action Item | Status |
|---|-------------|--------|
| ... | ... | ✅/⏭️ |

**Progresso:**
- HIGH: {n}/{total} implementados
- MEDIUM: {n}/{total} implementados
```

### 4. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue to Create Env Files [V] View Changes [X] Abort"

#### Menu Handling Logic:

- IF C: Store progress, then load, read entire file, then execute {nextStepFile}
- IF V: Show summary of all changes, then return to menu
- IF X: End workflow

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected will you proceed to create env files and bootstrap script.
