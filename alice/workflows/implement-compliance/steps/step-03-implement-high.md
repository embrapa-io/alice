---
name: 'step-03-implement-high'
description: 'Implementar action items HIGH e MEDIUM'
nextStepFile: './step-04-create-env-files.md'
---

# Step 3: Implementar Action Items HIGH e MEDIUM

## STEP GOAL:

Executar todos os action items de severidade HIGH e MEDIUM do relatório de conformidade.

## Rules

Follow `./references/step-file-protocol.md`. Step-specific:
- MUST implement HIGH items
- MEDIUM items are recommended but can be skipped by user request
- VALIDATE syntax after each modification
- Follow exact code examples from report

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

🚨 **Padrão OBRIGATÓRIO do arquivo de backup** (https://embrapa.io/docs/boilerplate#cli:backup): UM `.tar.gz` na RAIZ de `/backup` com nome EXATO `${IO_PROJECT}_${IO_APP}_${IO_STAGE}_${IO_VERSION}_$$(date +'%Y-%m-%d_%H-%M-%S').tar.gz` (data como SUFIXO), sem extensão dupla (`.sql.tar.gz` é PROIBIDO — o dump fica DENTRO do tar), diretório temporário removido após compactar (`trap`), e `restore` recebendo `BACKUP_FILE_TO_RESTORE` validado com `test -f`. Motivo: o Doctor publica apenas `*.tar.gz` da raiz do volume e o Releaser (`cleaner`) lê a data do nome para a retenção 7 diários / 4 semanais / 3 mensais — sem data no nome, o arquivo fica no volume para sempre. Se o script precisar de aspas duplas, use `entrypoint: ["/bin/sh", "-c"]` + `command:` como lista com um único item em bloco literal (`- |`) em vez de `sh -c "..."` (ver `templates/docker-compose/base.yaml`).

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
        trap 'rm -rf /backup/'$$BACKUP_DIR EXIT &&
        mkdir -p /backup/$$BACKUP_DIR &&
        pg_dump -h db -U ${DB_USER} ${DB_NAME} > /backup/$$BACKUP_DIR/database.sql &&
        tar -czf /backup/$$BACKUP_DIR.tar.gz -C /backup $$BACKUP_DIR &&
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
        trap 'rm -rf '$$RESTORE_DIR EXIT &&
        tar -xzf /backup/$$FILE_TO_RESTORE -C $$RESTORE_DIR --strip-components=1 &&
        psql -h db -U ${DB_USER} ${DB_NAME} < $$RESTORE_DIR/database.sql &&
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

**Criar `.gitlab-io.yml` (pipeline da plataforma — ID 5.5):**

Se o `.gitlab-io.yml` faltar na raiz, **gerar** o arquivo copiando literalmente `./templates/gitlab-io/gitlab-io.yml` (gravar como `.gitlab-io.yml`, com o ponto). Se houver versão específica da pilha no boilerplate de origem (`.embrapa/settings.json` → `boilerplate`), preferir a do boilerplate. Conteúdo padrão (genérico):

```yaml
image:
    name: sonarsource/sonar-scanner-cli:11
    entrypoint: [""]

variables:
  SONAR_USER_HOME: "${CI_PROJECT_DIR}/.sonar"
  GIT_DEPTH: "0"

stages:
  - build-sonar

build-sonar:
  stage: build-sonar

  cache:
    policy: pull-push
    key: "sonar-cache-$CI_COMMIT_REF_SLUG"
    paths:
      - "${SONAR_USER_HOME}/cache"
      - sonar-scanner/

  script:
    - >
      sonar-scanner
      -Dsonar.host.url="${SONAR_HOST_URL}"
      -Dsonar.projectKey="${CI_PROJECT_NAMESPACE##*/}_${CI_PROJECT_NAME}"
      -Dsonar.qualitygate.wait=true
  allow_failure: true
  rules:
    - if: $CI_PIPELINE_SOURCE == 'merge_request_event'
    - if: $CI_COMMIT_BRANCH == 'main'
```

🚫 **NUNCA** gerar, editar, renomear ou remover o `.gitlab-ci.yml`: ele é da equipe (a plataforma não o lê, não o cria e não o exige — mesma lógica do `.env` × `.env.io`). Se a equipe pedir que o pipeline próprio rode também no runner da plataforma, o `.gitlab-io.yml` pode ter `include: - local: .gitlab-ci.yml`, e o job `build-sonar` passa a usar `inherit: { default: false, variables: false }`, `needs: []` e `stage: .post` (no lugar de `stages:`/`stage: build-sonar`), com `image:` e `variables:` declarados dentro do próprio job, para não herdar imagem, `before_script`, tags e variáveis globais da equipe — opcional, só sob pedido.

Se o `.gitlab-io.yml` existir mas não tiver `sonar-scanner` (aviso 5.5b), **não** sobrescrever: apenas apontar no relatório e perguntar ao usuário.

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

