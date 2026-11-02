# `.env.example` — Padrões de Placeholder

## Princípio

O `.env.example` é o template das variáveis **da aplicação** (não da plataforma). Ele contém **valores de exemplo para desenvolvimento local** — senhas fracas como `secret`, usuários como `proxy`, portas padrão. A plataforma **não** substitui a maioria dessas variáveis no fork; o desenvolvedor edita `.env` manualmente para ambiente local.

**Use placeholders `%GENESIS_*%` apenas onde o valor depende do nome do projeto/app** — tipicamente em nomes de volumes externos e, ocasionalmente, em networks nomeadas ou _labels_.

## Onde **usar** placeholders

### 1. Nomes de volumes externos

Padrão:

```
<NOME_SEMANTICO>=%GENESIS_PROJECT_UNIX%_%GENESIS_APP_UNIX%_development_<sufixo>
```

Exemplos reais do repositório:

```dotenv
# nginx-proxy-manager
DATA_PROXY=%GENESIS_PROJECT_UNIX%_%GENESIS_APP_UNIX%_development_data
DATA_SSL=%GENESIS_PROJECT_UNIX%_%GENESIS_APP_UNIX%_development_ssl
DATA_DB=%GENESIS_PROJECT_UNIX%_%GENESIS_APP_UNIX%_development_db

# bun-postgresql
PGADMIN_VOLUME=%GENESIS_PROJECT_UNIX%_%GENESIS_APP_UNIX%_development_pgadmin

# gitea
GITEA_VOLUME=%GENESIS_PROJECT_UNIX%_%GENESIS_APP_UNIX%_development_gitea
```

> Alguns boilerplates antigos que omitem `_development` no `COMPOSE_PROJECT_NAME` (minio, mysql, wordpress) também omitem aqui. Seja consistente: **se o `.env.io.example` tem `_development`, o `.env.example` também tem**.

### 2. Networks externas nomeadas

Quando aplicável (geralmente só no `docker-compose.yaml`, mas às vezes exposto em `.env.example`):

```dotenv
NETWORK_NAME=%GENESIS_PROJECT_UNIX%_%GENESIS_APP_UNIX%_development
```

## Onde **NÃO** usar placeholders

- **Senhas / segredos**: use valores de desenvolvimento legíveis (`secret`, `changeme`, `super-secret`) ou instruções inline (`# Gere com: openssl rand -hex 32`).
- **Portas**: use valores padrão descomentados (ex.: `APP_PORT=8090`).
- **Hosts internos do Docker Compose**: use o nome do serviço (`DB_HOST=db`, `SMTP_HOST=mailpit`).
- **URLs base locais**: `http://localhost:8090`.
- **E-mail de exemplo**: `first.surname@embrapa.br` ou `no-reply@embrapa.br`.
- **Usuários de banco/admin**: nome consistente com o tema (ex.: `DB_USER=directus` para Directus).

## Estrutura recomendada

Use blocos com cabeçalho separador para legibilidade (padrão visto em `directus`, `strapi`, `hermes-agent`):

```dotenv
# ============================================
# <Nome do Serviço> - Embrapa I/O Boilerplate
# ============================================
# IMPORTANTE: Copie este arquivo para .env e
# configure as variáveis conforme seu ambiente.
# ============================================

# ============================================
# GLOBAL
# ============================================
TZ=America/Sao_Paulo
LOG_LEVEL=info

# ============================================
# PORTS (HOST)
# ============================================
APP_PORT=8090
...

# ============================================
# VOLUMES (External - Created by bootstrap.sh)
# ============================================
# Estes valores são atualizados automaticamente
# pelo script bootstrap.sh
VOLUME_DATA=%GENESIS_PROJECT_UNIX%_%GENESIS_APP_UNIX%_development_data
...
```

## Regra NO-FALLBACK

Lembrete (é regra da Alice, mas vale reforçar aqui porque está no escopo da genericação): **nunca** use `${VAR:-default}` no `docker-compose.yaml` ou em scripts. Se uma variável é usada, precisa estar declarada no `.env.example`.

```yaml
# ❌ PROIBIDO
ports:
  - "${PB_PORT:-8090}:8090"

# ✅ CORRETO
ports:
  - "${PB_PORT}:8090"
```

Se você encontrar isso durante a genericação, pare e oriente o usuário a rodar a Alice.
