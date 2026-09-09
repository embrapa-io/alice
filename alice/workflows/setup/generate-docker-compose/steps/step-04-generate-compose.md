---
name: 'step-04-generate-compose'
description: 'Gerar docker-compose.yaml conforme as 4 Verdades Fundamentais da plataforma Embrapa I/O'

# File References
nextStepFile: './step-05-validate-finalize.md'

# Template References
baseTemplate: './templates/docker-compose/base.yaml'

# Knowledge References
fundamentalsKnowledge: './knowledge/embrapa-io-fundamentals.md'
---

# Step 4: Gerar docker-compose.yaml

## STEP GOAL:

Gerar o arquivo docker-compose.yaml aplicando todas as configurações coletadas e garantindo 100% de conformidade com as 4 Verdades Fundamentais da plataforma Embrapa I/O.

## Rules

Follow `./references/step-file-protocol.md`. Step-specific:
- Gerar docker-compose.yaml aplicando as 4 Verdades Fundamentais -- PROIBIDO violar qualquer uma
- Todas as portas e volumes DEVEM usar variáveis de ambiente -- PROIBIDO hardcode no host
- Serviço `backup` DEVE gerar o `.tar.gz` com o nome-padrão da plataforma (ver seção 5) -- PROIBIDO outro nome, extensão dupla ou subdiretório
- Apresentar conteúdo ao usuário antes de salvar (não salvar neste step)

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Aplicar as 4 Verdades Fundamentais

**🚨 REGRAS CRÍTICAS - Aplicar TODAS:**

**Verdade 1: Sem campo 'version'**
- Docker Compose v2+ não usa campo version
- Arquivo DEVE iniciar com `services:`

**Verdade 2: Network 'stack' externa**
```yaml
networks:
  stack:
    name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}
    external: true
```

**Verdade 3: Volumes externos**
- TODOS os volumes com `external: true`
- Volumes de serviço via variáveis do .env
- Volume de backup com nome hardcoded: `${IO_PROJECT}_${IO_APP}_${IO_STAGE}_backup`

**Verdade 4: Sem container_name**
- NENHUM serviço pode ter campo `container_name`

### 2. Gerar Configuração Base

Generate docker-compose.yaml structure based on `{selected_stack}`:

**Para Node.js API:**
```yaml
services:
  app:
    build: .
    restart: unless-stopped
    ports:
      - "${APP_PORT}:{app_port}"
    environment:
      NODE_ENV: ${IO_STAGE}
    env_file:
      - .env.io
      - .env
    networks:
      - stack
    healthcheck:
      test: ["CMD", "wget", "--spider", "http://localhost:{app_port}{health_endpoint}"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

**Para Vue/React Frontend:**
```yaml
services:
  app:
    build: .
    restart: unless-stopped
    ports:
      - "${APP_PORT}:80"
    networks:
      - stack
    healthcheck:
      test: ["CMD", "wget", "--spider", "http://localhost:80/"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### 3. Adicionar Portas Adicionais

For each port in `{additional_ports}`:
```yaml
ports:
  - "${APP_PORT}:{app_port}"
  - "${PORT_MQTT}:1883"      # Example
  - "${PORT_METRICS}:9090"   # Example
```

### 4. Adicionar Banco de Dados (se aplicável)

**Para MongoDB:**
```yaml
  mongodb:
    image: mongo:7
    restart: unless-stopped
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGO_USER}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD}
    volumes:
      - mongodb_data:/data/db
    networks:
      - stack
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  mongodb_data:
    name: ${MONGODB_VOLUME}
    external: true
```

**Para PostgreSQL:**
```yaml
  postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - stack
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  postgres_data:
    name: ${POSTGRES_VOLUME}
    external: true
```

### 5. Adicionar Serviços CLI (se solicitado)

If `{include_cli_services}` includes services, use `{baseTemplate}` as reference and adapt the image/dump commands to `{selected_database}`.

**🚨 REGRA OBRIGATÓRIA - Nome do arquivo de backup** (https://embrapa.io/docs/boilerplate#cli:backup):

1. O serviço `backup` gera **UM** arquivo `.tar.gz` na **RAIZ** do volume de backup (montado em `/backup`) com o nome **EXATO**:
   `${IO_PROJECT}_${IO_APP}_${IO_STAGE}_${IO_VERSION}_$$(date +'%Y-%m-%d_%H-%M-%S').tar.gz`
   (`$$` para o Compose não interpolar o `$(date ...)`; a data é **SUFIXO** no formato `AAAA-MM-DD_HH-MM-SS`)
2. **PROIBIDO** extensão dupla (`.sql.tar.gz`, `.dump.tar.gz`): o dump e demais arquivos ficam **DENTRO** do `.tar.gz`
3. Diretório temporário criado dentro de `/backup` com o mesmo nome-base e removido após compactar (usar `trap` para o caso de erro). Nada além dos `.tar.gz` permanece na raiz do volume
4. Volume de backup: `${IO_PROJECT}_${IO_APP}_${IO_STAGE}_backup`, `external: true`
5. O serviço `restore` recebe `BACKUP_FILE_TO_RESTORE` (nome do `.tar.gz` relativo a `/backup`), valida existência (`test -f`), extrai em diretório temporário e restaura
6. **Motivo:** o Doctor (backup sob demanda da plataforma) publica apenas `*.tar.gz` da raiz do volume, e o Releaser (`cleaner`) lê a data do nome do arquivo para aplicar a retenção 7 diários / 4 semanais / 3 mensais — arquivos sem data no nome são ignorados e ficam no volume para sempre

**⚠️ Cuidado com `sh -c "..."` em `command: >`:** aspas duplas internas (ex.: `-H "Content-Type: ..."`) quebram o comando e `-exec {} \;` do `find` precisa ser `\\;`. Se o script tiver aspas, prefira `entrypoint: ["/bin/sh", "-c"]` + `command:` como lista com **um único item** em bloco literal (`- |`, como abaixo). Não use `command: |` (string): o Compose faz split por espaços e o `sh -c` receberia só a primeira palavra.

```yaml
  backup:
    image: postgres:16-alpine   # mesma imagem/tecnologia do banco
    profiles: [cli]
    restart: "no"
    environment:
      PGPASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - backup_data:/backup
    networks:
      - stack
    entrypoint: ["/bin/sh", "-c"]
    command:
      - |
        set -e
        BACKUP_NAME=${IO_PROJECT}_${IO_APP}_${IO_STAGE}_${IO_VERSION}_$$(date +'%Y-%m-%d_%H-%M-%S')
        BACKUP_DIR=/backup/$$BACKUP_NAME
        trap 'rm -rf "$$BACKUP_DIR"' EXIT
        mkdir -p "$$BACKUP_DIR"
        pg_dump -h postgres -U ${POSTGRES_USER} ${POSTGRES_DB} > "$$BACKUP_DIR/database.sql"
        tar -czf "/backup/$$BACKUP_NAME.tar.gz" -C /backup "$$BACKUP_NAME"
        echo "Backup concluído: $$BACKUP_NAME.tar.gz"

  restore:
    image: postgres:16-alpine
    profiles: [cli]
    restart: "no"
    environment:
      PGPASSWORD: ${POSTGRES_PASSWORD}
      BACKUP_FILE_TO_RESTORE: ${BACKUP_FILE_TO_RESTORE:-}
    volumes:
      - backup_data:/backup:ro
    networks:
      - stack
    entrypoint: ["/bin/sh", "-c"]
    command:
      - |
        set -e
        test -f "/backup/$$BACKUP_FILE_TO_RESTORE" || { echo "Arquivo /backup/$$BACKUP_FILE_TO_RESTORE não encontrado"; exit 1; }
        RESTORE_DIR=$$(mktemp -d)
        trap 'rm -rf "$$RESTORE_DIR"' EXIT
        tar -xzf "/backup/$$BACKUP_FILE_TO_RESTORE" -C "$$RESTORE_DIR" --strip-components=1
        psql -h postgres -U ${POSTGRES_USER} ${POSTGRES_DB} < "$$RESTORE_DIR/database.sql"
        echo "Restore concluído"

  sanitize:
    image: postgres:16-alpine
    profiles: [cli]
    restart: "no"
    environment:
      PGPASSWORD: ${POSTGRES_PASSWORD}
    networks:
      - stack
    entrypoint: ["/bin/sh", "-c"]
    command:
      - |
        psql -h postgres -U ${POSTGRES_USER} ${POSTGRES_DB} -c 'VACUUM ANALYZE;'

volumes:
  backup_data:
    name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}_backup
    external: true
```

**Validar antes de prosseguir:** o `command` do `backup` contém `_${IO_VERSION}_$$(date +'%Y-%m-%d_%H-%M-%S')` seguido de `.tar.gz`, o `tar -czf` grava direto em `/backup/`, e o `restore` usa `BACKUP_FILE_TO_RESTORE` com `test -f`.

### 6. Gerar Lista de Variáveis para .env

Compile list of environment variables needed:

**Variáveis de Porta:**
- `APP_PORT` - Porta principal do host
- `PORT_*` - Portas adicionais

**Variáveis de Volume:**
- `MONGODB_VOLUME=${IO_PROJECT}_${IO_APP}_${IO_STAGE}_mongodb`
- `POSTGRES_VOLUME=${IO_PROJECT}_${IO_APP}_${IO_STAGE}_postgres`
- etc.

Store as `{env_vars_list}`.

### 7. Apresentar docker-compose.yaml Gerado

Display complete generated content:
```
📄 **docker-compose.yaml gerado:**

\`\`\`yaml
{generated_content}
\`\`\`

📝 **Variáveis a adicionar no .env:**
{env_vars_list}

🎯 **Próximo passo:** Validar conformidade e salvar arquivo
```

### 8. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue to Validation [E] Edit configuration [X] Exit"

#### Menu Handling Logic:

- IF C: Store generated content, then load, read entire file, then execute {nextStepFile}
- IF E: Allow user to specify changes, regenerate
- IF X: End workflow gracefully
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#8-present-menu-options)

