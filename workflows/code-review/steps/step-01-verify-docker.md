---
name: 'step-01-verify-docker'
description: 'Verificar implementação do Docker Compose contra 4 Verdades Fundamentais'
nextStepFile: './step-02-verify-env.md'
---

# Step 1: Verificar Docker Compose

## STEP GOAL:

Verificar se o docker-compose.yaml implementa corretamente as 4 Verdades Fundamentais conforme especificado no relatório de conformidade.

## MANDATORY EXECUTION RULES:

- 🛑 PASS/FAIL each verification clearly
- 📖 Reference specific lines in files
- 📋 Compare against compliance report action items
- 🔧 Do NOT suggest improvements beyond compliance

## Sequence of Instructions

### 1. Carregar Relatório de Referência

Ler `{output_folder}/embrapa-io-compliance.md` e extrair os action items relacionados a Docker Compose.

### 2. Verificar Verdade #1: Sem Campo version

**Verificação:**
- [ ] Campo `version` NÃO está presente no docker-compose.yaml

```yaml
# ✅ CORRETO: Arquivo inicia com services
services:
  app:
    ...

# ❌ INCORRETO: Campo version presente
version: '3.8'
services:
  ...
```

**Resultado:** PASS ✅ / FAIL ❌

### 3. Verificar Verdade #2: Network Externa

**Verificação:**
- [ ] Seção `networks:` existe no final do arquivo
- [ ] Network `stack` declarada
- [ ] `external: true` presente
- [ ] `name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}` correto

```yaml
# ✅ CORRETO
networks:
  stack:
    external: true
    name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}
```

**Resultado:** PASS ✅ / FAIL ❌

### 4. Verificar Verdade #3: Volumes Externos

**Para cada volume declarado:**
- [ ] `external: true` presente
- [ ] `name` usa variável ou padrão correto

```yaml
# ✅ CORRETO
volumes:
  postgres_data:
    external: true
    name: ${DB_VOLUME}

  backup_data:
    external: true
    name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}_backup
```

**Resultado:** PASS ✅ / FAIL ❌

### 5. Verificar Verdade #4: Sem container_name

**Para cada serviço:**
- [ ] Atributo `container_name` NÃO está presente

```yaml
# ✅ CORRETO
services:
  app:
    build: .
    # sem container_name

# ❌ INCORRETO
services:
  app:
    container_name: my-app  # PROIBIDO
```

**Resultado:** PASS ✅ / FAIL ❌

### 6. Verificar Serviços de Longa Duração

**Para cada serviço que não é CLI:**
- [ ] `restart: unless-stopped` presente
- [ ] `healthcheck` configurado
- [ ] Conectado à network `stack`

```yaml
# ✅ CORRETO
services:
  app:
    restart: unless-stopped
    networks:
      - stack
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

**Resultado:** PASS ✅ / FAIL ❌

### 7. Verificar Serviços CLI

**Para backup, restore, sanitize (se existirem):**
- [ ] `profiles: ['cli']` presente
- [ ] `restart: "no"` ou `restart: no` presente
- [ ] Conectado à network `stack`

```yaml
# ✅ CORRETO
backup:
  profiles: ['cli']
  restart: "no"
  networks:
    - stack
```

**Resultado:** PASS ✅ / FAIL ❌

### 8. Verificar Portas

**Para cada mapeamento de porta:**
- [ ] Porta do host usa variável de ambiente

```yaml
# ✅ CORRETO
ports:
  - "${APP_PORT}:3000"

# ❌ INCORRETO
ports:
  - "3000:3000"  # Hardcoded
```

**Resultado:** PASS ✅ / FAIL ❌

### 9. Compilar Resultado da Verificação Docker

```markdown
## 🐳 Verificação Docker Compose

### Verdades Fundamentais

| # | Verdade | Status | Evidência |
|---|---------|--------|-----------|
| 1 | Sem campo version | ✅/❌ | {evidência} |
| 2 | Network externa | ✅/❌ | {evidência} |
| 3 | Volumes externos | ✅/❌ | {evidência} |
| 4 | Sem container_name | ✅/❌ | {evidência} |

### Serviços

| Serviço | Restart | Healthcheck | Network | Status |
|---------|---------|-------------|---------|--------|
| app | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| db | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| ... | ... | ... | ... | ... |

### Serviços CLI

| Serviço | Profiles | Restart | Network | Status |
|---------|----------|---------|---------|--------|
| backup | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| restore | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| sanitize | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |

### Resultado Docker: {PASS/FAIL}
```

Store as `{docker_review}`.

### 10. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue to Env Verification [F] Show Failures Only [X] Abort Review"

#### Menu Handling Logic:

- IF C: Store docker_review, then load, read entire file, then execute {nextStepFile}
- IF F: Display only failed verifications, then return to menu
- IF X: End review with partial results

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected will you proceed to verify environment files.
