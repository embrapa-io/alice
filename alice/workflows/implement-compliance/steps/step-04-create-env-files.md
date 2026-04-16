---
name: 'step-04-create-env-files'
description: 'Criar arquivos .env e .env.io a partir dos templates e gerar bootstrap.sh'
nextStepFile: './step-05-finalize.md'
---

# Step 4: Criar Arquivos .env e bootstrap.sh

## STEP GOAL:

Criar os arquivos `.env` e `.env.io` a partir dos templates `.env.example` e `.env.io.example`, gerando valores aleatórios para secrets e hashes. Criar o script `bootstrap.sh` para preparar o ambiente.

## Rules

Follow `./references/step-file-protocol.md`. Step-specific:
- MUST create .env from .env.example
- MUST create .env.io from .env.io.example
- GENERATE random values for PASSWORD, SECRET types
- CREATE bootstrap.sh with network/volume creation
- CALCULATE correct IO_VERSION format

## Sequence of Instructions

### 1. Criar .env.io a partir de .env.io.example

**Transformações a aplicar:**

#### 1.1 Solicitar informações do projeto

```markdown
Para criar o arquivo .env.io, preciso de algumas informações:

1. **Nome do projeto** (formato unix: lowercase, letras, números, hífens)
   Exemplo: meu-projeto

2. **Nome da aplicação** (formato unix: lowercase, letras, números, hífens)
   Exemplo: api-backend

3. **Email do desenvolvedor** (formato: nome.sobrenome@embrapa.br)
   Exemplo: joao.silva@embrapa.br
```

Aguardar input do usuário.

#### 1.2 Calcular IO_VERSION

Formato: `0.YY.M-dev.1`

```javascript
// Exemplo de cálculo
const now = new Date();
const YY = now.getFullYear().toString().slice(-2); // "26" para 2026
const M = (now.getMonth() + 1).toString(); // "1" para janeiro (sem zero)
const IO_VERSION = `0.${YY}.${M}-dev.1`;
// Resultado: "0.26.1-dev.1"
```

#### 1.3 Gerar .env.io

```ini
COMPOSE_PROJECT_NAME={io_project}_{io_app}_development
COMPOSE_PROFILES=development
IO_SERVER=localhost
IO_PROJECT={io_project}
IO_APP={io_app}
IO_STAGE=development
IO_VERSION={calculated_version}
IO_DEPLOYER={user_email}
SENTRY_DSN=GET_IN_DASHBOARD
MATOMO_ID=522
MATOMO_TOKEN=
```

### 2. Criar .env a partir de .env.example

**Transformações a aplicar:**

#### 2.1 Gerar valores aleatórios para secrets

Para variáveis do tipo PASSWORD/SECRET no settings.json:

```bash
# PASSWORD (16 caracteres alfanuméricos)
openssl rand -base64 12 | tr -dc 'a-zA-Z0-9' | head -c 16

# SECRET (64 caracteres alfanuméricos)
openssl rand -base64 48 | tr -dc 'a-zA-Z0-9' | head -c 64
```

#### 2.2 Calcular nomes de volumes

Usar padrão: `{io_project}_{io_app}_development_{volume_name}`

Exemplo:
```ini
DB_VOLUME=meu-projeto_api-backend_development_db
PGADMIN_VOLUME=meu-projeto_api-backend_development_pgadmin
```

#### 2.3 Preservar outros valores

Manter valores existentes do .env.example para variáveis não-sensíveis.

### 3. Criar bootstrap.sh

**Conteúdo do script:**

```bash
#!/bin/bash
# ============================================
# Bootstrap Script - Embrapa I/O
# ============================================
# Este script prepara o ambiente de desenvolvimento:
# - Valida pré-requisitos (Docker, Docker Compose)
# - Cria network externa
# - Cria volumes externos
# - Orienta o usuário para iniciar a aplicação
#
# Uso: ./bootstrap.sh
# ============================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Emojis
CHECK="✅"
CROSS="❌"
WARN="⚠️"
INFO="ℹ️"
ROCKET="🚀"

echo ""
echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}  Bootstrap - Embrapa I/O${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# ============================================
# 1. Validate Prerequisites
# ============================================
echo -e "${INFO} Validando pré-requisitos..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${CROSS} ${RED}Docker não encontrado!${NC}"
    echo "   Instale o Docker: https://docs.docker.com/get-docker/"
    exit 1
fi
echo -e "${CHECK} Docker instalado: $(docker --version | cut -d' ' -f3 | cut -d',' -f1)"

# Check Docker Compose
if ! docker compose version &> /dev/null; then
    echo -e "${CROSS} ${RED}Docker Compose não encontrado!${NC}"
    echo "   O Docker Compose V2 é necessário."
    exit 1
fi
echo -e "${CHECK} Docker Compose instalado: $(docker compose version --short)"

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo -e "${CROSS} ${RED}Docker não está rodando!${NC}"
    echo "   Inicie o Docker Desktop ou o serviço Docker."
    exit 1
fi
echo -e "${CHECK} Docker está rodando"

echo ""

# ============================================
# 2. Load environment variables
# ============================================
echo -e "${INFO} Carregando variáveis de ambiente..."

if [ ! -f ".env.io" ]; then
    echo -e "${CROSS} ${RED}Arquivo .env.io não encontrado!${NC}"
    exit 1
fi

# Load .env.io
set -a
source .env.io
set +a

# Validate required variables
if [ -z "$IO_PROJECT" ] || [ -z "$IO_APP" ] || [ -z "$IO_STAGE" ]; then
    echo -e "${CROSS} ${RED}Variáveis IO_PROJECT, IO_APP e IO_STAGE são obrigatórias!${NC}"
    exit 1
fi

PREFIX="${IO_PROJECT}_${IO_APP}_${IO_STAGE}"
echo -e "${CHECK} Prefixo: ${BLUE}${PREFIX}${NC}"

echo ""

# ============================================
# 3. Create external network
# ============================================
echo -e "${INFO} Criando network externa..."

NETWORK_NAME="${PREFIX}"
if docker network inspect "$NETWORK_NAME" &> /dev/null; then
    echo -e "${CHECK} Network ${BLUE}${NETWORK_NAME}${NC} já existe"
else
    docker network create "$NETWORK_NAME"
    echo -e "${CHECK} Network ${BLUE}${NETWORK_NAME}${NC} criada"
fi

echo ""

# ============================================
# 4. Create external volumes
# ============================================
echo -e "${INFO} Criando volumes externos..."

# Load .env for volume names
if [ -f ".env" ]; then
    set -a
    source .env
    set +a
fi

# Create volumes based on .env variables
# Backup volume (always created)
VOLUME_BACKUP="${PREFIX}_backup"
if docker volume inspect "$VOLUME_BACKUP" &> /dev/null; then
    echo -e "${CHECK} Volume ${BLUE}${VOLUME_BACKUP}${NC} já existe"
else
    docker volume create "$VOLUME_BACKUP"
    echo -e "${CHECK} Volume ${BLUE}${VOLUME_BACKUP}${NC} criado"
fi

# Database volume (if DB_VOLUME is set)
if [ -n "$DB_VOLUME" ]; then
    if docker volume inspect "$DB_VOLUME" &> /dev/null; then
        echo -e "${CHECK} Volume ${BLUE}${DB_VOLUME}${NC} já existe"
    else
        docker volume create "$DB_VOLUME"
        echo -e "${CHECK} Volume ${BLUE}${DB_VOLUME}${NC} criado"
    fi
fi

# Additional volumes (pgadmin, uploads, etc.)
for VAR in PGADMIN_VOLUME UPLOADS_VOLUME CACHE_VOLUME; do
    VALUE="${!VAR}"
    if [ -n "$VALUE" ]; then
        if docker volume inspect "$VALUE" &> /dev/null; then
            echo -e "${CHECK} Volume ${BLUE}${VALUE}${NC} já existe"
        else
            docker volume create "$VALUE"
            echo -e "${CHECK} Volume ${BLUE}${VALUE}${NC} criado"
        fi
    fi
done

echo ""

# ============================================
# 5. Summary
# ============================================
echo -e "${GREEN}============================================${NC}"
echo -e "${ROCKET} ${GREEN}Bootstrap concluído com sucesso!${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo -e "${INFO} Para iniciar a aplicação, execute:"
echo ""
echo -e "   ${BLUE}env \$(cat .env.io) docker compose up --force-recreate --build --remove-orphans --wait${NC}"
echo ""
echo -e "${INFO} Para derrubar a aplicação:"
echo ""
echo -e "   ${BLUE}env \$(cat .env.io) docker compose down${NC}"
echo ""
echo -e "${INFO} Para executar backup:"
echo ""
echo -e "   ${BLUE}env \$(cat .env.io) docker compose run --rm backup${NC}"
echo ""
```

### 4. Tornar bootstrap.sh executável

```bash
chmod +x bootstrap.sh
```

### 5. Apresentar Resumo

```markdown
## ✅ Arquivos Criados

### .env.io
```ini
{conteúdo_gerado}
```

### .env
```ini
{conteúdo_gerado_com_secrets}
```

### bootstrap.sh
Script criado com:
- Validação de pré-requisitos
- Criação de network externa: `{prefix}`
- Criação de volumes externos

---

## 🚀 Próximos Passos

1. **Revise os arquivos .env.io e .env**
   Verifique se os valores estão corretos.

2. **Execute o bootstrap.sh**
   ```bash
   ./bootstrap.sh
   ```

3. **Inicie a aplicação**
   ```bash
   env $(cat .env.io) docker compose up --force-recreate --build --remove-orphans --wait
   ```

4. **Teste a aplicação**
   Verifique se está funcionando corretamente.

5. **Execute o Code Review [CR]**
   Inicie uma NOVA SESSÃO do assistente de codificação
   e execute o workflow [CR] Code Review para validar a implementação.
```

### 6. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue to Finalize [X] Exit"

#### Menu Handling Logic:

- IF C: Store all created files info, then load, read entire file, then execute {nextStepFile}
- IF X: End workflow with current progress

