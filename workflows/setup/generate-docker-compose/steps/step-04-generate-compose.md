---
name: 'step-04-generate-compose'
description: 'Gerar docker-compose.yaml conforme as 4 Verdades Fundamentais da plataforma Embrapa I/O'

# File References
nextStepFile: './step-05-validate-finalize.md'

# Template References
baseTemplate: '{project-root}/_bmad/embrapa-io/templates/docker-compose/base.yaml'

# Knowledge References
fundamentalsKnowledge: '{project-root}/_bmad/embrapa-io/knowledge/embrapa-io-fundamentals.md'
---

# Step 4: Gerar docker-compose.yaml

## STEP GOAL:

Gerar o arquivo docker-compose.yaml aplicando todas as configurações coletadas e garantindo 100% de conformidade com as 4 Verdades Fundamentais da plataforma Embrapa I/O.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator

### Role Reinforcement:

- ✅ You are a DevOps specialist generating Embrapa I/O compliant Docker configuration
- ✅ If you already have been given a name, communication_style and persona, continue to use those while playing this new role
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring Docker Compose expertise and Embrapa I/O knowledge

### Step-Specific Rules:

- 🎯 Focus on generating valid, compliant docker-compose.yaml
- 🚫 FORBIDDEN to violate any of the 4 Verdades Fundamentais
- 💬 Approach: Generate, validate internally, present to user
- 📋 All ports and volumes MUST use environment variables

## EXECUTION PROTOCOLS:

- 🎯 Apply 4 Verdades Fundamentais strictly
- 💾 Generate .env variables for ports and volumes
- 📖 Explain generated configuration to user
- 🚫 FORBIDDEN to hardcode ports on host side

## CONTEXT BOUNDARIES:

- Available context: All config from previous steps
- Focus: docker-compose.yaml generation
- Limits: Do not save file yet - present for review first
- Dependencies: All configuration values from steps 1-3

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

If `{include_cli_services}` includes services:
```yaml
  backup:
    build:
      context: .
      dockerfile: Dockerfile.cli
    profiles: [cli]
    restart: "no"
    volumes:
      - backup_data:/backup
    networks:
      - stack
    command: ["backup"]

  restore:
    build:
      context: .
      dockerfile: Dockerfile.cli
    profiles: [cli]
    restart: "no"
    environment:
      BACKUP_FILE_TO_RESTORE: ${BACKUP_FILE_TO_RESTORE}
    volumes:
      - backup_data:/backup
    networks:
      - stack
    command: ["restore"]

  sanitize:
    build:
      context: .
      dockerfile: Dockerfile.cli
    profiles: [cli]
    restart: "no"
    networks:
      - stack
    command: ["sanitize"]

volumes:
  backup_data:
    name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}_backup
    external: true
```

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

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu items execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [docker-compose.yaml content generated and presented], will you then load and read fully `{nextStepFile}` to execute validation and file saving.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- 4 Verdades Fundamentais applied correctly
- No 'version' field in generated content
- Network 'stack' with external: true
- All volumes with external: true
- No container_name in any service
- All host ports using environment variables
- Complete content presented to user

### ❌ SYSTEM FAILURE:

- Including 'version' field
- Network without external: true
- Volumes without external: true
- Any service with container_name
- Hardcoded ports on host side
- Not presenting generated content before saving
- Proceeding without user confirmation

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
