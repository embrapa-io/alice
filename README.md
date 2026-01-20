---
last-redoc-date: 2026-01-20
---

# Alice - Agente de Conformidade Embrapa I/O

**Purpose**: Agente especialista do [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD) que garante conformidade de aplicações com a plataforma [Embrapa I/O](https://embrapa.io) por meio de análise automatizada, implementação guiada e validação rigorosa baseada nas 4 Verdades Fundamentais.

**Overview**: **Alice** é uma agente especializada em conformidade que analisa, implementa e valida projetos para a plataforma Embrapa I/O, independente de linguagem ou framework. Através de três workflows principais, Alice guia o processo completo de adequação: verificação de conformidade com geração de relatório detalhado, implementação dos ajustes necessários, e code review final para certificação.

O diferencial está na abordagem agnóstica de stack: Alice detecta automaticamente a tecnologia utilizada (Node.js, Vue.js, React, PHP, .NET, Python, etc.) e adapta todas as configurações e exemplos de código ao contexto do projeto. O foco exclusivo em **Docker Compose** como orquestrador garante simplicidade e compatibilidade com a plataforma.

## Quick Start

### 1. Instalação

Primeiramente, [instale o _framework_ do **BMAD Method**](https://github.com/bmad-code-org/BMAD-METHOD) em seu projeto (utilize a **Versão 6**).

Em seguida, clone este repositório:

```bash
git clone https://github.com/embrapa-io/bmad.git _bmad/embrapa-io
```

### 2. Invocar a Alice

Inicie seu assistente de codificação em IA (Claude Code, Gemini CLI, OpenCode, GitHub Copilot, Codex, etc) e invoque a Alice:

```
/bmad:embrapa-io:agents:alice
```

### 3. Seguir o Fluxo

```
[VC] Verify Compliance → [IA] Implement Adjustments → [CR] Code Review
         ↓                         ↓                         ↓
  Gera relatório          Implementa ajustes         Valida implementação
  com action items        do relatório               (NOVA SESSÃO!)
```

## Menu da Alice

| Opção | Comando | Descrição |
|-------|---------|-----------|
| **[VC]** | Verify Compliance | Analisa o codebase e gera `docs/embrapa-io-compliance.md` com action items detalhados |
| **[IA]** | Implement Adjustments | Executa os action items do relatório, cria `.env`, `.env.io` e `bootstrap.sh` |
| **[CR]** | Code Review | Verifica se a implementação está 100% conforme e emite veredicto APPROVED/REJECTED |
| **[CH]** | Chat | Conversar com a Alice sobre qualquer assunto relacionado ao Embrapa I/O |
| **[MH]** | Menu Help | Reexibir o menu de opções |
| **[DA]** | Dismiss Agent | Encerrar a sessão com a Alice |

> **IMPORTANTE**: O Code Review [CR] deve ser executado em uma **NOVA SESSÃO** para garantir uma verificação imparcial, sem o contexto da implementação anterior.

## Workflows da Alice

### [VC] Verify Compliance (6 steps)

Analisa completamente o codebase e gera relatório detalhado:

1. **Analyze Codebase** - Detecta stack tecnológica e estrutura do projeto
2. **Validate Docker** - Verifica as 4 Verdades Fundamentais no docker-compose
3. **Validate Env** - Valida estrutura dos arquivos .env
4. **Validate Settings** - Verifica .embrapa/settings.json
5. **Validate Integrations** - Checa Sentry, Matomo e healthchecks
6. **Generate Report** - Cria `docs/embrapa-io-compliance.md` com action items

**Output**: `{project-root}/docs/embrapa-io-compliance.md`

### [IA] Implement Adjustments (5 steps)

Executa os action items do relatório de conformidade:

1. **Validate Report** - Carrega e valida o relatório existente
2. **Implement Critical** - Implementa itens de severidade CRITICAL
3. **Implement High** - Implementa itens HIGH e MEDIUM
4. **Create Env Files** - Cria .env, .env.io e bootstrap.sh
5. **Finalize** - Atualiza relatório e documenta alterações

**Outputs**: Arquivos de infraestrutura modificados, `.env`, `.env.io`, `bootstrap.sh`

### [CR] Code Review (5 steps)

Verifica se todas as implementações estão corretas:

1. **Verify Docker** - Valida docker-compose contra as 4 Verdades
2. **Verify Env** - Checa arquivos .env e .gitignore
3. **Verify Settings** - Valida .embrapa/settings.json
4. **Verify Integrations** - Verifica bootstrap.sh, LICENSE, integrações
5. **Finalize Review** - Emite veredicto APPROVED ✅ ou REJECTED ❌

**Output**: Relatório atualizado com status final de conformidade

## 4 Verdades Fundamentais

A conformidade com Embrapa I/O é baseada em 4 regras invioláveis:

| # | Verdade | Descrição |
|---|---------|-----------|
| 1 | **Sem `version`** | Campo `version` deve estar AUSENTE do docker-compose.yaml |
| 2 | **Network externa** | Network `stack` deve ser `external: true` com nome `${IO_PROJECT}_${IO_APP}_${IO_STAGE}` |
| 3 | **Volumes externos** | TODOS os volumes devem ser `external: true` |
| 4 | **Sem `container_name`** | Nenhum serviço pode ter atributo `container_name` |

## Escopo da Alice

### ✅ In Scope (Alice pode modificar)

- `docker-compose.yaml` / `docker-compose.yml`
- `.env.example`, `.env.io.example`, `.env`, `.env.io`
- `.embrapa/settings.json`
- `LICENSE`
- `Dockerfile(s)`
- `bootstrap.sh`
- Configurações Sentry/Matomo (mínimas)
- Seção de conformidade no `README.md`

### ❌ Out of Scope (Alice NÃO modifica)

- Código funcional da aplicação
- Criação de novos endpoints ou rotas
- Refatoração de código existente
- Melhorias de segurança, performance ou manutenibilidade
- **Docker Swarm** (fora do escopo - apenas Docker Compose)
- Testes unitários ou de integração
- CI/CD pipelines

## Comandos Docker

**TODOS** os comandos `docker compose` em projetos Embrapa I/O **DEVEM** ser precedidos por `env $(cat .env.io)`:

```bash
# Inicializar (criar network e volumes)
./bootstrap.sh

# Subir a stack
env $(cat .env.io) docker compose up --force-recreate --build --remove-orphans --wait

# Parar a stack
env $(cat .env.io) docker compose down

# Ver logs
env $(cat .env.io) docker compose logs -f

# Executar serviços CLI
env $(cat .env.io) docker compose run --rm --no-deps backup
env $(cat .env.io) docker compose run --rm --no-deps sanitize
```

## Configuration

O arquivo `config.yaml` define configurações da agente:

```yaml
user_name: Camilo Carromeu
communication_language: Brazilian Portuguese
document_output_language: Brazilian Portuguese
output_folder: '{project-root}/docs'
```

## Knowledge Base

O diretório `knowledge/` contém a base de conhecimento da Alice:

| Arquivo | Descrição |
|---------|-----------|
| `embrapa-io-fundamentals.md` | 4 Verdades Fundamentais da plataforma |
| `embrapa-io-validation.md` | 39 regras de validação organizadas por categoria |
| `embrapa-io-workflows.md` | Padrões de adaptação por tipo de projeto |
| `embrapa-io-deployment.md` | Processos de deployment e ambientes |
| `embrapa-io-stacks.md` | Configurações específicas por stack tecnológica |
| `embrapa-io-integrations.md` | Integrações Sentry, Matomo, healthchecks |
| `embrapa-io-integration-guide.md` | Guia detalhado de integrações |

## Workflows Utilitários (Legado)

Além dos workflows da Alice, existem workflows utilitários que podem ser invocados diretamente por outros agentes BMAD:

### Setup (4 workflows)

- **[generate-env-io](./workflows/setup/generate-env-io/)**: Gera `.env.io` e `.env.io.example`
- **[generate-docker-compose](./workflows/setup/generate-docker-compose/)**: Cria `docker-compose.yaml`
- **[generate-settings-json](./workflows/setup/generate-settings-json/)**: Gera `.embrapa/settings.json`
- **[generate-license](./workflows/setup/generate-license/)**: Cria arquivo `LICENSE`

### Validate (1 workflow)

- **[validate-compliance](./workflows/validate/validate-compliance/)**: Validação completa contra 39 regras

> **Nota**: Estes workflows são mantidos para compatibilidade com agentes BMAD existentes. Para novos projetos, recomenda-se usar a agente Alice diretamente.

## Project Structure

```
_bmad/embrapa-io/
├── config.yaml               # Configurações da agente
├── README.md                 # Esta documentação
├── ROADMAP.md                # Planejamento de features futuras
├── agents/                   # Agentes especializados
│   └── alice.md              # Alice - Especialista em Conformidade
├── knowledge/                # Base de conhecimento (7 arquivos)
├── templates/                # Templates reutilizáveis
│   ├── docker-compose/       # Template base para docker-compose
│   └── settings/             # Templates JSON por stack
└── workflows/                # Workflows organizados por categoria
    ├── verify-compliance/    # [Alice] Verificação e relatório
    ├── implement-compliance/ # [Alice] Implementação de ajustes
    ├── code-review/          # [Alice] Validação de implementações
    ├── setup/                # 4 workflows utilitários
    └── validate/             # 1 workflow de validação (legado)
```

## Compliance & Quality

**BMAD v6 Compliance**: ✅ 100%

### Métricas de Qualidade

- ✅ Config Compliance: 100%
- ✅ Web Bundle Compliance: 100%
- ✅ Template Mapping: 100%
- ✅ Code Quality: 100%
- ✅ Documentation: 100%

### Histórico

- **2026-01-20**: Transformação em AGENTE com criação da Alice e 3 workflows principais
- **2025-12-17**: Auditoria e certificação BMAD v6 Excellence como módulo
