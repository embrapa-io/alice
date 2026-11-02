# Placeholders `%GENESIS_*%` — Referência Completa

Conjunto fechado de placeholders observados nos boilerplates de https://git.embrapa.io/io/boilerplate (verificado via `grep -rh -oE '%GENESIS_[A-Z_]+%'`). **Não invente novos sem antes conversar com o usuário** — a lista é contrato com a plataforma.

## Placeholders válidos

### `%GENESIS_PROJECT_NAME%`

Nome legível do projeto (usado em títulos, textos descritivos).

- **Onde aparece**: H1 do README, descrições de stack.
- **Exemplo substituído**: `Portal Web do Pasto Certo`, `Sistema de Monitoramento Ambiental`.
- **Regra**: não use em código ou configuração — apenas em texto voltado a humano.

### `%GENESIS_PROJECT_UNIX%`

Slug unix do projeto. Lowercase, apenas `a-z`, `0-9` e `-`.

- **Onde aparece**: `.env.io.example` (`IO_PROJECT`, `COMPOSE_PROJECT_NAME`), `.env.example` (nomes de volumes), `README.md` (comandos `docker network create`, `docker volume create`).
- **Exemplo substituído**: `pasto-certo`, `monitoramento`, `openproject`.

### `%GENESIS_APP_UNIX%`

Slug unix da app dentro do projeto. Mesma convenção de charset.

- **Onde aparece**: mesmo contexto do `%GENESIS_PROJECT_UNIX%` — sempre andam juntos.
- **Exemplo substituído**: `web`, `api`, `mobile`, `admin`, `cms`.

> `%GENESIS_PROJECT_UNIX%` + `%GENESIS_APP_UNIX%` formam a identidade única da app na plataforma: `<projeto>_<app>_<stage>`. É o que a plataforma usa para criar volumes, networks e container names sem colisão.

### `%GENESIS_VERSION%`

Versão semântica inicial do boilerplate / da app. Geralmente `1.0.0`.

- **Onde aparece**: `.env.io.example` (`IO_VERSION`), `README.md` (rodapé de licença).
- **Exemplo substituído**: `1.0.0`, `0.1.0`, `2.3.1`.

### `%GENESIS_MATOMO_ID%`

ID numérico do site no Matomo (analytics) configurado pela plataforma.

- **Onde aparece**: `.env.io.example` (`MATOMO_ID`).
- **Exemplo substituído**: `42`, `137`.
- **Regra**: não precisa aparecer em `.env.example` — a variável `MATOMO_ID` chega via `.env.io`, é só repassar no `docker-compose.yaml`.

### `%GENESIS_ACTUAL_YEAR%`

Ano atual no momento do fork. Usado em copyright.

- **Onde aparece**: `README.md` (rodapé), ocasionalmente em `LICENSE` customizada (raro — o padrão é manter LICENSE da Embrapa intacto).
- **Exemplo substituído**: `2026`.

## Tabela de substituição (resumo)

| Placeholder              | `.env.io.example` | `.env.example` | `README.md` | `docker-compose.yaml` |
| ------------------------ | :---------------: | :------------: | :---------: | :-------------------: |
| `%GENESIS_PROJECT_NAME%` |                   |                | ✅          |                       |
| `%GENESIS_PROJECT_UNIX%` | ✅                | ✅             | ✅          | (indireto via env)    |
| `%GENESIS_APP_UNIX%`     | ✅                | ✅             | ✅          | (indireto via env)    |
| `%GENESIS_VERSION%`      | ✅                |                | ✅          | (indireto via env)    |
| `%GENESIS_MATOMO_ID%`    | ✅                |                |             |                       |
| `%GENESIS_ACTUAL_YEAR%`  |                   |                | ✅          |                       |

**Atenção**: o `docker-compose.yaml` **não** contém placeholders `%GENESIS_*%` diretamente. Ele usa `${IO_PROJECT}`, `${IO_APP}`, `${IO_STAGE}`, `${IO_VERSION}` — que a plataforma injeta via `.env.io` em runtime. Se você encontrar `%GENESIS_*%` em `docker-compose.yaml` durante a genericação, isso é um bug — corrija para usar a variável de ambiente.

## Como descobrir os valores reais na app atual

Antes de substituir, identifique os valores reais que estão hoje no codebase. Comandos úteis (rode a partir da raiz da app):

```bash
# Slug do projeto (valor de IO_PROJECT no .env.io atual)
grep -E '^IO_PROJECT=' .env.io 2>/dev/null

# Slug da app
grep -E '^IO_APP=' .env.io 2>/dev/null

# Versão
grep -E '^IO_VERSION=' .env.io 2>/dev/null

# Nome legível — geralmente no H1 do README.md ou em .embrapa/settings.json
head -1 README.md
cat .embrapa/settings.json | grep -E '"name"|"title"' 2>/dev/null

# Onde já existem placeholders (caso a app esteja parcialmente genericada)
grep -rn '%GENESIS_' . --include='*.md' --include='*.example' --include='.env*'

# Volumes e networks derivados no .env.example atual (candidatos a placeholder)
grep -E '_(development|production|staging)_' .env.example
```

Leve a lista de valores reais → placeholder ao usuário para confirmar antes do rewrite.
