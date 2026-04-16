# Embrapa I/O DevOps Compliance Module

**Versão**: 1.26.4-6 | **Compatível com**: BMAD Core v6 | **Convenção de versão**: `1.YY.MM`

Módulo de conhecimento [BMAD](https://github.com/bmad-code-org/BMAD-METHOD) para conformidade de aplicações com a plataforma [Embrapa I/O](https://embrapa.io). Inclui a agente **Alice**, 8 workflows especializados, 8 knowledge files, 6 templates e um script de validação automatizada.

## Alice — Agente de Conformidade

**Alice** é uma agente especializada que analisa, implementa e valida projetos para a plataforma Embrapa I/O, independente de linguagem ou framework. Através de três workflows principais, Alice guia o processo completo de adequação: verificação de conformidade com geração de relatório detalhado, implementação dos ajustes necessários, e code review final para certificação.

O diferencial está na abordagem agnóstica de stack: Alice detecta automaticamente a tecnologia utilizada (Node.js, Vue.js, React, PHP, .NET, Python, etc.) e adapta todas as configurações e exemplos de código ao contexto do projeto. O foco exclusivo em **Docker Compose** como orquestrador garante simplicidade e compatibilidade com a plataforma.

Alice suporta **modo headless** (`-H`) para automação CI/CD, utiliza um **script de pré-validação** (`validate-compliance.py`) que economiza 3K-5K tokens por invocação ao pré-computar verificações determinísticas, e possui um **SKILL.md** padrão BMad na raiz do módulo para compatibilidade com a toolchain.

## Quick Start

### 1. Instalação

A agente é instalada juntamente com o _framework_ [**BMAD Method**](https://github.com/bmad-code-org/BMAD-METHOD):

```bash
cd ~/projects/my-project/my-app

npx bmad-method install
```

No passo `Select official modules to install`, selecione "**BMad Method Agile-AI Driven-Development**".

Em seguida, no passo: `Would you like to install from a custom source (Git URL or local path)?`, selecione "**Yes**".

Por fim, em `Git URL or local path:` coloque a URL deste repositório: "**https://github.com/embrapa-io/alice**". Quando aparecer, selecione o módulo "**Embrapa I/O DevOps Compliance Module**".

Continue a instalação auto-guiada até finalizar. A _skill_ da agente será instalada junto com os demais agentes BMAD. 

### 2. Invocar a Alice

Inicie seu assistente de codificação em IA (Claude Code, Gemini CLI, OpenCode, GitHub Copilot, Codex, etc) e invoque a Alice:

```
/alice
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
| **[VC]** | Verify Compliance | Analisa o codebase e gera `{output_folder}/embrapa-io-compliance.md` com action items detalhados |
| **[IA]** | Implement Adjustments | Executa os action items do relatório, cria `.env`, `.env.io` e `bootstrap.sh` |
| **[CR]** | Code Review | Verifica se a implementação está 100% conforme e emite veredicto APPROVED/REJECTED |
| **[CH]** | Chat | Conversar com a Alice sobre qualquer assunto relacionado ao Embrapa I/O |
| **[MH]** | Menu Help | Reexibir o menu de opções |
| **[PM]** | Party Mode | Iniciar discussão multi-agente (requer módulo Core) |
| **[DA]** | Dismiss Agent | Encerrar a sessão com resumo de ações e próximos passos |

> **IMPORTANTE**: O Code Review [CR] deve ser executado em uma **NOVA SESSÃO** para garantir uma verificação imparcial, sem o contexto da implementação anterior.

## Workflows da Alice

### [VC] Verify Compliance (6 steps)

Analisa completamente o codebase e gera relatório detalhado. Opcionalmente roda `validate-compliance.py` como pré-validação para acelerar a análise:

1. **Analyze Codebase** - Detecta stack tecnológica e estrutura do projeto
2. **Validate Docker** - Verifica as 4 Verdades Fundamentais no docker-compose
3. **Validate Env** - Valida estrutura dos arquivos `.env`, `.env.io`, `.env.sh` e `.gitignore`
4. **Validate Settings** - Verifica `.embrapa/settings.json`
5. **Validate Integrations & Code** - Checa Sentry, Matomo, regra NO-FALLBACK, Linter e LICENSE
6. **Generate Report** - Cria `{output_folder}/embrapa-io-compliance.md` com action items

**Output**: `{output_folder}/embrapa-io-compliance.md`

### [IA] Implement Adjustments (5 steps)

Executa os action items do relatório de conformidade:

1. **Validate Report** - Carrega e valida o relatório existente
2. **Implement Critical** - Implementa itens de severidade CRITICAL
3. **Implement High** - Implementa itens HIGH e MEDIUM
4. **Create Env Files** - Cria .env, .env.io e bootstrap.sh
5. **Finalize** - Atualiza relatório e documenta alterações

**Outputs**: Arquivos de infraestrutura modificados, `.env`, `.env.io`, `bootstrap.sh`

### [CR] Code Review (5 steps)

Verifica se todas as implementações estão corretas. Pode usar `validate-compliance.py` para pass/fail automatizado:

1. **Verify Docker** - Valida docker-compose contra as 4 Verdades
2. **Verify Env** - Checa arquivos `.env`, `.env.io`, `.env.sh` e `.gitignore`
3. **Verify Settings** - Valida `.embrapa/settings.json`
4. **Verify Integrations & Code** - Verifica bootstrap.sh, LICENSE, NO-FALLBACK, Linter e integrações
5. **Finalize Review** - Emite veredicto APPROVED ✅ ou REJECTED ❌

**Output**: Relatório atualizado com status final de conformidade

## Script de Validação Automatizada

O módulo inclui um script Python que pré-computa todas as verificações determinísticas, economizando 3K-5K tokens por invocação de workflow:

```bash
# Validação completa com output JSON
uv run scripts/validate-compliance.py --project-path /caminho/do/projeto --output json

# Validação específica
uv run scripts/validate-compliance.py --project-path . --checks docker,env,settings

# Output resumido (human-readable)
uv run scripts/validate-compliance.py --project-path . --output summary

# Self-test
uv run scripts/validate-compliance.py --self-test
```

### Categorias de validação

| Categoria | Verificações |
|-----------|-------------|
| `docker` | 4 Verdades Fundamentais, serviços CLI, health checks, portas |
| `env` | Variáveis obrigatórias, duplicatas, `.gitignore` (`.env`, `.env.io`, `.env.sh`, dirs AI) |
| `settings` | Estrutura `.embrapa/settings.json`, campos obrigatórios |
| `code` | Regra NO-FALLBACK (6 linguagens), LICENSE |
| `integrations` | Detecção Sentry, Matomo, health check endpoints |
| `score` | Cálculo de compliance ponderado por severidade |

O script é utilizado automaticamente pelos workflows VC e CR quando disponível, e é **obrigatório** no modo headless.

## Modo Headless

Alice suporta execução não-interativa para automação CI/CD:

```
# Via agente (quando suportado pelo framework)
alice -H VC    # Roda Verify Compliance sem interação
alice -H CR    # Roda Code Review sem interação
```

No modo headless:
- Pula saudação e exibição de menu
- Executa `validate-compliance.py` automaticamente antes do workflow
- Auto-avança por todos os gates `[C] Continue`
- Gera output JSON estruturado ao final

```json
{
  "headless_mode": true,
  "workflow": "verify-compliance",
  "completed": true,
  "report_file": "{output_folder}/embrapa-io-compliance.md",
  "score": { "percentage": 85, "grade": "B" },
  "findings": { "critical": 0, "high": 2, "medium": 3, "low": 1 }
}
```

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

- Código funcional da aplicação (exceto integrações Sentry/Matomo quando absolutamente necessário)
- Criação de novos endpoints ou rotas
- Refatoração de código existente
- Melhorias de segurança, performance ou manutenibilidade
- **Docker Swarm** (fora do escopo - apenas Docker Compose)
- Testes unitários ou de integração
- CI/CD pipelines (SonarQube é opcional e documentado, não implementado)

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

Após a instalação via `embrapa-io-setup`, as configurações são armazenadas em dois arquivos consolidados:

**`{project-root}/_bmad/config.yaml`** — Configurações compartilhadas do projeto:
```yaml
output_folder: '{project-root}/docs'
document_output_language: Brazilian Portuguese
# + seção do módulo embrapa-io
```

**`{project-root}/_bmad/config.user.yaml`** — Configurações pessoais (gitignored):
```yaml
user_name: Camilo Carromeu
communication_language: Brazilian Portuguese
```

## Knowledge Base

O diretório `knowledge/` contém a base de conhecimento da Alice:

| Arquivo | Descrição |
|---------|-----------|
| `embrapa-io-fundamentals.md` | 4 Verdades Fundamentais da plataforma |
| `embrapa-io-validation.md` | 40 regras de validação organizadas por categoria |
| `embrapa-io-workflows.md` | Padrões de adaptação por tipo de projeto |
| `embrapa-io-deployment.md` | Processos de deployment e ambientes |
| `embrapa-io-stacks.md` | Configurações específicas por stack tecnológica |
| `embrapa-io-integrations.md` | Integrações Sentry, Matomo, healthchecks |
| `embrapa-io-integration-guide.md` | Guia detalhado de integrações |
| `embrapa-io-coding-standards.md` | Padrões de codificação: grafia PT-BR, variáveis sem fallback, LICENSE, integrações Sentry/Matomo |

## Workflows de Setup

Workflows utilitários que podem ser invocados diretamente por outros agentes BMAD para scaffolding de projetos novos:

- **[generate-env-io](./workflows/setup/generate-env-io/)**: Gera `.env.io` e `.env.io.example`
- **[generate-docker-compose](./workflows/setup/generate-docker-compose/)**: Cria `docker-compose.yaml`
- **[generate-settings-json](./workflows/setup/generate-settings-json/)**: Gera `.embrapa/settings.json`
- **[generate-license](./workflows/setup/generate-license/)**: Cria arquivo `LICENSE`

### validate-compliance (DEPRECATED)

O workflow `validate-compliance` em `workflows/validate/` foi **depreciado**. Sua funcionalidade foi absorvida pelo workflow **[VC] Verify Compliance** da Alice (que inclui validação de settings.json, integrações Sentry/Matomo, regra NO-FALLBACK e Linter — ausentes no workflow legado) e pelo script `validate-compliance.py` (para validação automatizada sem LLM).

> Para novos projetos, use a agente Alice diretamente ou o script `validate-compliance.py`.

## Project Structure

```
embrapa-io/
├── alice/                      # Skill self-contained (instalado em .claude/skills/alice/)
│   ├── SKILL.md                # Entry point BMad (persona, menu, headless, escopo)
│   ├── knowledge/              # Base de conhecimento (8 arquivos)
│   ├── scripts/                # Scripts de validação automatizada
│   │   └── validate-compliance.py
│   ├── templates/              # Templates reutilizáveis
│   └── workflows/              # 8 workflows
│       ├── verify-compliance/  # [VC] 6 steps
│       ├── implement-compliance/ # [IA] 5 steps
│       ├── code-review/        # [CR] 5 steps
│       ├── references/         # Checklists compartilhados
│       ├── setup/              # 4 workflows utilitários
│       └── validate/           # validate-compliance (DEPRECATED)
├── module.yaml                 # Metadados do módulo
├── module-help.csv             # Capacidades para roteamento BMad
├── .claude-plugin/             # Registra ./alice como skill instalável
├── agents/alice.md             # Definição legada (formato XML)
├── embrapa-io-setup/           # Skill de setup (uso manual)
├── README.md / CLAUDE.md / ROADMAP.md / LICENSE
```

## Configuração de .gitignore

Alice verifica e orienta a configuração do `.gitignore` do projeto. Os seguintes itens são obrigatórios:

```gitignore
# Variáveis de ambiente (não versionar valores reais)
.env
.env.io
.env.sh

# Agentes de IA e IDEs
.agent/
.agents/
.augment/
.claude/
.cline/
.codebuddy/
.crush/
.cursor/
.gemini/
.github/
.iflow/
.kilocode/
.kiro/
.ona/
.opencode/
.pi/
.qoder/
.qwen/
.roo/
.rovodev/
.trae/
.windsurf/
_bmad/
_bmad-output/
```

> **Nota**: Arquivos `.example` (`.env.example`, `.env.io.example`) **NÃO** devem estar no `.gitignore` — são templates de referência e devem ser versionados.

## Compliance & Quality

**BMAD v6 Compliance**: ✅ 100%

### Métricas de Qualidade

- ✅ Config Compliance: 100%
- ✅ Web Bundle Compliance: 100%
- ✅ Template Mapping: 100%
- ✅ Code Quality: 100%
- ✅ Documentation: 100%

### Histórico

- **2026-04-14**: Quality analysis e otimizações — SKILL.md na raiz, `validate-compliance.py` (1892 linhas, 29 testes), modo headless, config consolidado, depreciação VCL, cobertura NO-FALLBACK/Linter no VC/CR, checklists compartilhados, cobertura `.gitignore` expandida (`.env.sh` + diretórios AI)
- **2026-03-30**: v1.26.4-6 — Validação de módulo, criação de module-help.csv, consolidação de metadados
- **2026-01-20**: Transformação em AGENTE com criação da Alice e 3 workflows principais
- **2025-12-17**: Auditoria e certificação BMAD v6 Excellence como módulo
