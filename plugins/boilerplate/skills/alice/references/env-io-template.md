# `.env.io.example` — Template Fixo da Plataforma

O `.env.io.example` é **padronizado** em toda a plataforma Embrapa I/O. Verificado idêntico em: `pocketbase`, `bun-postgresql`, `directus`, `nodejs-postgresql`, `strapi`, `vuejs-pocketbase`, `hermes-agent`, `nginx-proxy-manager`, `gitea`, `garage`, `mcp-server-ts` (e equivalente em `minio`, `mysql`, `wordpress` com pequena variação de `_development`).

## Conteúdo obrigatório (padrão canônico)

Copie **exatamente** este bloco como `.env.io.example`:

```dotenv
COMPOSE_PROJECT_NAME=%GENESIS_PROJECT_UNIX%_%GENESIS_APP_UNIX%_development
COMPOSE_PROFILES=development
IO_SERVER=localhost
IO_PROJECT=%GENESIS_PROJECT_UNIX%
IO_APP=%GENESIS_APP_UNIX%
IO_STAGE=development
IO_VERSION=%GENESIS_VERSION%
IO_DEPLOYER=first.surname@embrapa.br
SENTRY_DSN=GET_IN_DASHBOARD
MATOMO_ID=%GENESIS_MATOMO_ID%
MATOMO_TOKEN=
```

## Regras

- **Não adicione** variáveis neste arquivo. É injetado pela plataforma e tem contrato fixo.
- **Não remova** nenhuma variável, mesmo que a app atual não use (ex.: `MATOMO_ID`). A plataforma espera todas presentes.
- **`SENTRY_DSN=GET_IN_DASHBOARD`** é literal (um _marker_, não um placeholder). A plataforma substitui pelo DSN real a partir do dashboard do Sentry configurado no projeto.
- **`IO_DEPLOYER=first.surname@embrapa.br`** é o valor-exemplo canônico. Mantenha assim — é substituído no fork pelo e-mail de quem fez o deploy.
- **`MATOMO_TOKEN=`** fica vazio de propósito (é preenchido pelo deployer, não pela plataforma).
- **`COMPOSE_PROJECT_NAME`** inclui `_development` por padrão. A plataforma troca por `_production`, `_staging` etc. em outros stages. Alguns boilerplates antigos (wordpress, minio, mysql) omitem o `_development`; prefira **incluir** em boilerplates novos, seguindo a convenção majoritária.
- **`COMPOSE_PROFILES=development`**: mesma lógica — é substituído por stage nos outros ambientes.

## Por que este arquivo existe

A plataforma Embrapa I/O injeta estas variáveis **fora do `.env`** para separar:

- `.env.io` → metadados da plataforma (projeto, app, stage, versão, observabilidade).
- `.env` → configuração da aplicação (credenciais, portas, features).

Isso permite que a plataforma re-injete os metadados a cada deploy sem poluir o `.env` da app. Os comandos `docker compose` sempre rodam precedidos de `env $(cat .env.io)` para carregar esses metadados no ambiente.

## O que **não** colocar aqui

- Segredos (senhas, chaves) — vão no `.env`.
- Portas — vão no `.env`.
- Nomes de volumes derivados — vão no `.env` (usando as variáveis `IO_*` já injetadas).
- Configuração específica da aplicação — vão no `.env`.
