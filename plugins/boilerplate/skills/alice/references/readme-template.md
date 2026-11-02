# `README.md` — Estrutura e Placeholders

O `README.md` é **o rosto do boilerplate**. Ele precisa fazer sentido tanto no repositório do boilerplate (com placeholders visíveis) quanto depois do fork (com valores substituídos). Por isso, o texto deve fluir naturalmente mesmo quando o leitor vê `%GENESIS_PROJECT_NAME%` literal.

## Estrutura canônica (mínima)

Baseada nos padrões observados em `pocketbase`, `bun-postgresql`, `directus`, `nodejs-postgresql`, `strapi`, `nginx-proxy-manager`.

```markdown
### %GENESIS_PROJECT_UNIX% / %GENESIS_APP_UNIX%
# %GENESIS_PROJECT_NAME%

Boilerplate para <descrição curta da tecnologia principal> em conformidade com o padrão [Embrapa I/O](https://embrapa.io).

## Documentação

- **[Especificação Técnica](docs/tech-spec.md)** — Arquitetura, modelo de dados, padrões de código. *(Se existir.)*
- **[Instruções para Agentes de IA](AGENTS.md)** — Regras de conformidade com a plataforma. Leitura obrigatória antes de alterar código.

## Stack

- <tecnologia 1> <versão>
- <tecnologia 2> <versão>
- ...

## Requisitos

- Docker >= 24
- Docker Compose v2
- <outros específicos>

## Início rápido

### 1. Setup Inicial

Criar _network_ e _volumes_ externos:

```bash
docker network create %GENESIS_PROJECT_UNIX%_%GENESIS_APP_UNIX%_development && \
docker volume create %GENESIS_PROJECT_UNIX%_%GENESIS_APP_UNIX%_development_data
```

Copiar arquivos de configuração:

```bash
cp .env.io.example .env.io
cp .env.example .env
```

> **Importante!** Edite `.env` com suas senhas e configurações antes de subir a stack.

### 2. Subir a Stack

```bash
env $(cat .env.io) docker compose up --force-recreate --build --remove-orphans --wait
```

### 3. Acessar

- App: http://localhost:<APP_PORT>
- <outras URLs>

## Variáveis de Ambiente

A aplicação utiliza duas categorias de arquivos:

- **`.env`** — Variáveis da aplicação (banco, SMTP, autenticação).
- **`.env.io`** — Variáveis injetadas pela plataforma Embrapa I/O (projeto, versão, stage).

### Aplicação (`.env`)

<tabela ou lista das variáveis principais com descrição em PT-BR>

### Plataforma (`.env.io`)

<tabela das IO_* e SENTRY_DSN, MATOMO_*>

## Conformidade Embrapa I/O

Este projeto segue todas as regras de conformidade da plataforma:

- [x] `docker-compose.yaml` sem campo `version`
- [x] Network `stack` externa com nome correto
- [x] Volumes externos com nomenclatura padrão
- [x] Healthchecks em todos os serviços long-running
- [x] Serviços CLI com `profiles: [cli]`
- [x] NO-FALLBACK em todas as variáveis de ambiente
- [x] Arquivo `.embrapa/settings.json` válido
- [x] Arquivos `.env.example` e `.env.io.example` presentes

**IMPORTANTE**: Todo comando `docker compose` DEVE ser precedido por `env $(cat .env.io)` para injetar as variáveis da plataforma.

## Licença

Versão %GENESIS_VERSION% © %GENESIS_ACTUAL_YEAR% — Embrapa. Ver [LICENSE](LICENSE).
```

## Onde os placeholders entram (checklist)

Aplique a cada README:

| Local                                                               | Placeholder              |
| ------------------------------------------------------------------- | ------------------------ |
| **Primeira linha do arquivo** — subtítulo (H3)                       | `### %GENESIS_PROJECT_UNIX% / %GENESIS_APP_UNIX%` |
| Segunda linha — título (H1) *(ver regra abaixo)*                     | `# %GENESIS_PROJECT_NAME%` |
| `docker network create ...`                                         | `%GENESIS_PROJECT_UNIX%_%GENESIS_APP_UNIX%_development` |
| `docker volume create ...` (cada sufixo)                            | `%GENESIS_PROJECT_UNIX%_%GENESIS_APP_UNIX%_development_<sufixo>` |
| Menção à versão no rodapé / seção de licença                         | `%GENESIS_VERSION%` |
| Ano no rodapé / copyright                                           | `%GENESIS_ACTUAL_YEAR%` |
| Menção ao ID do Matomo (se a doc explica configuração)              | `%GENESIS_MATOMO_ID%` |

## Regra especial para o H1 (`# ...`)

Há duas convenções vivas no repositório:

- **Boilerplate "personalizável"** (maioria — `directus`, `joplin`, `openclaw`, `strapi`, `nodejs-postgresql`, `pocketbase`, `bun-postgresql` etc.): o H1 é substituído por `# %GENESIS_PROJECT_NAME%` — a plataforma injeta o nome real do projeto no fork.
- **Boilerplate "tech-centric"** (ex.: `php-slim-postgresql` mantém `# PHP Slim PostgreSQL Boilerplate` literal): o H1 descreve a tecnologia, não o projeto. Usado quando o boilerplate é genérico o suficiente para nunca ser renomeado.

**Como decidir**: pergunte ao usuário. Default recomendado = `%GENESIS_PROJECT_NAME%`. Só mantenha literal se o usuário confirmar que é um boilerplate tech-centric e o título não deve mudar no fork.

O subtítulo `### %GENESIS_PROJECT_UNIX% / %GENESIS_APP_UNIX%` é **sempre** obrigatório como primeira linha do arquivo — é a "etiqueta de identidade" do boilerplate, substituída pela plataforma no fork.

## Regras de escrita

- **Português brasileiro correto** em todo o texto, **com acentos**. Reveja cada seção.
- **Não mencione nome real do projeto** no corpo do texto. Use `%GENESIS_PROJECT_NAME%` ou referências genéricas ("esta aplicação", "a stack").
- **Não exponha senhas reais** ou URLs de produção em exemplos. Use `localhost`, portas padrão e placeholders `<...>`.
- **Comandos `docker compose` sempre com `env $(cat .env.io)`** no começo — é o contrato da plataforma.
- **Links externos** para documentação oficial das tecnologias (Docker Hub, site do projeto), não para forks internos.
- **Emojis são OK** nos cabeçalhos das seções (padrão visto em `directus`, `nginx-proxy-manager`), mas **não obrigatórios**. Use com moderação.
- **Código com blocos triplos** com a linguagem correta (`bash`, `dotenv`, `yaml`, `json`).

## Seções opcionais (dependem do tipo de app)

Inclua conforme fizer sentido para a tecnologia:

- **Arquitetura** — diagrama ASCII dos componentes (ver `pocketbase/README.md`).
- **Backup e Restore** — quando há persistência relevante.
- **Migrations / Seeds** — quando aplicável.
- **Storage S3/Garage** — quando há upload de arquivos.
- **Email (SMTP)** — quando há envio de e-mail.
- **Troubleshooting** — problemas comuns.
- **Rollback e Manutenção** — para apps em produção crítica.
