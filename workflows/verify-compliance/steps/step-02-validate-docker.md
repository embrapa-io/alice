---
name: 'step-02-validate-docker'
description: 'Validação do docker-compose.yaml contra as 4 Verdades Fundamentais'
nextStepFile: './step-03-validate-env.md'
---

# Step 2: Validar Docker Compose

## STEP GOAL:

Validar o arquivo docker-compose.yaml (ou .yml) contra as 4 Verdades Fundamentais da plataforma Embrapa I/O e documentar todas as não-conformidades encontradas.

## MANDATORY EXECUTION RULES:

- 🛑 NEVER skip any validation rule
- 📖 READ entire docker-compose file before validating
- 📋 DOCUMENT every finding with file path, line number, and severity
- 🔧 FOCUS on Docker Compose only - Docker Swarm is OUT OF SCOPE

## Sequence of Instructions

### 1. Localizar docker-compose

Buscar por:
- `docker-compose.yaml` (preferido)
- `docker-compose.yml`

Se não encontrar, registrar como **CRITICAL ERROR**.

### 2. Validar Verdade Fundamental #1: Sem campo 'version'

**Regra:** O campo `version` é obsoleto e NÃO deve estar presente.

```yaml
# ❌ INCORRETO
version: '3.8'
services:
  ...

# ✅ CORRETO
services:
  ...
```

**Se encontrar `version`:**
- Severidade: CRITICAL
- Action Item: "Remover o campo `version` da linha X do docker-compose.yaml"

### 3. Validar Verdade Fundamental #2: Network Externa

**Regra:** Deve existir network `stack` externa com nome `${IO_PROJECT}_${IO_APP}_${IO_STAGE}`.

```yaml
# ✅ CORRETO
networks:
  stack:
    external: true
    name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}
```

**Validações:**
- [ ] Seção `networks:` existe
- [ ] Network `stack` declarada
- [ ] `external: true` presente
- [ ] `name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}` presente

**Se falhar qualquer validação:**
- Severidade: CRITICAL
- Action Item específico para cada falha

### 4. Validar Verdade Fundamental #3: Volumes Externos

**Regra:** Todos os volumes devem ser externos com `external: true`.

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

**Validações para cada volume:**
- [ ] `external: true` presente
- [ ] `name` usando variável ou padrão `${IO_PROJECT}_${IO_APP}_${IO_STAGE}_[nome]`

**Se volume não for externo:**
- Severidade: HIGH
- Action Item: "Converter volume `X` para externo com `external: true` e `name: ${...}`"

### 5. Validar Verdade Fundamental #4: Sem container_name

**Regra:** NENHUM serviço pode ter o atributo `container_name`.

```yaml
# ❌ INCORRETO
services:
  app:
    container_name: my-app
    ...

# ✅ CORRETO
services:
  app:
    # sem container_name - nome gerado automaticamente pelo COMPOSE_PROJECT_NAME
    ...
```

**Se encontrar `container_name`:**
- Severidade: HIGH
- Action Item: "Remover `container_name` do serviço `X` na linha Y"

### 6. Validar Serviços de Longa Duração

**Regra:** Serviços que não são CLI devem ter:
- `restart: unless-stopped`
- `healthcheck` configurado

```yaml
# ✅ CORRETO
services:
  app:
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
    networks:
      - stack
```

**Para cada serviço de longa duração:**
- [ ] `restart: unless-stopped` presente
- [ ] `healthcheck` configurado
- [ ] Conectado à network `stack`

### 7. Validar Serviços CLI (backup, restore, sanitize)

**Regra:** Serviços CLI devem ter:
- `profiles: ['cli']`
- `restart: "no"` ou `restart: no`

```yaml
# ✅ CORRETO
backup:
  image: postgres:17-alpine
  profiles: ['cli']
  restart: "no"
  volumes:
    - backup_data:/backup
  networks:
    - stack
  command: |
    sh -c "..."
```

**Verificar presença de:**
- [ ] Serviço `backup` (MEDIUM se ausente)
- [ ] Serviço `restore` (MEDIUM se ausente)
- [ ] Serviço `sanitize` (MEDIUM se ausente)

### 8. Validar Portas Não-Hardcoded

**Regra:** Portas expostas no host devem usar variáveis.

```yaml
# ❌ INCORRETO
ports:
  - "3000:3000"

# ✅ CORRETO
ports:
  - "${APP_PORT}:3000"
```

**Se encontrar porta hardcoded no host:**
- Severidade: MEDIUM
- Action Item: "Substituir porta hardcoded `X` por variável `${VAR_PORT}:X`"

### 9. Compilar Resultados da Validação Docker

Organizar findings em:

```markdown
## 🐳 Validação Docker Compose

### Status: {COMPLIANT | PARTIAL | NON-COMPLIANT}

### Findings

| # | Severidade | Regra | Localização | Descrição |
|---|------------|-------|-------------|-----------|
| 1 | CRITICAL | Verdade #1 | linha X | Campo version presente |
| 2 | HIGH | Verdade #4 | linha Y | container_name em serviço Z |
| ... | ... | ... | ... | ... |

### Resumo
- CRITICAL: {count}
- HIGH: {count}
- MEDIUM: {count}
- LOW: {count}
```

Store as `{docker_findings}`.

### 10. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue to Env Validation [X] Exit workflow"

#### Menu Handling Logic:

- IF C: Store docker_findings, then load, read entire file, then execute {nextStepFile}
- IF X: End workflow gracefully

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected will you then load and read fully `{nextStepFile}` to continue validation.
