# Embrapa I/O — a agente Alice

**Versão**: 1.26.11-9 | **Funciona em**: Claude Code (plugin), e em Gemini CLI, OpenCode, GitHub Copilot, Codex e outros pelo BMAD | **Convenção de versão**: `1.YY.MM-N`

Marketplace `embrapa-io` de plugins do Claude Code com a agente **Alice** da plataforma [Embrapa I/O](https://embrapa.io). A agente é uma só; cada plugin é uma tarefa, com um menu próprio, e se instala à parte:

| Plugin | Comando | Para quem | O que faz |
| --- | --- | --- | --- |
| `compliance@embrapa-io` | `/compliance:alice` | toda equipe | conformidade de qualquer código com a plataforma: verificação, implementação, revisão e teste de backup e restore (este documento) |
| `boilerplate@embrapa-io` | `/boilerplate:alice` | quem mantém _boilerplates_ | transforma uma app aderente num _boilerplate_ do catálogo ([`plugins/boilerplate`](plugins/boilerplate)) |
| `sentinel@embrapa-io` | `/sentinel:alice` | arquitetos de um projeto | trata os relatórios da Sentinela: triagem, Kanban, correções, Sentry e SonarQube ([`plugins/sentinel`](plugins/sentinel)) |
| `cve@embrapa-io` | `/cve:alice` | arquitetos de um projeto | trata os alertas de CVE crítico das builds ([`plugins/cve`](plugins/cve)) |

```bash
claude plugin marketplace add embrapa-io/alice
claude plugin install compliance@embrapa-io       # conformidade (toda equipe)
claude plugin install sentinel@embrapa-io         # relatórios da Sentinela
claude plugin install cve@embrapa-io              # alertas de CVE crítico
claude plugin install boilerplate@embrapa-io      # app → boilerplate do catálogo
```

Guia de instalação e uso, com exemplos de cada plugin: https://embrapa.io/docs/alice.

Digitar `/alice` no Claude Code lista as Alices instaladas. O plugin `compliance` inclui os workflows de verificação, implementação, revisão e teste de backup, os arquivos de conhecimento da plataforma, os modelos e um script de validação automatizada.

## Alice — Agente de Conformidade

**Alice** é uma agente especializada que analisa, adapta e valida projetos para a plataforma Embrapa I/O, independente de linguagem ou framework. Ela guia o processo completo de adequação: verificação de conformidade com relatório detalhado, implementação dos ajustes, revisão final para certificação e o teste de ida e volta do backup.

O diferencial está na abordagem agnóstica de stack: Alice detecta automaticamente a tecnologia utilizada (Node.js, Vue.js, React, PHP, .NET, Python, etc.) e adapta todas as configurações e exemplos de código ao contexto do projeto. O foco exclusivo em **Docker Compose** como orquestrador garante simplicidade e compatibilidade com a plataforma.

Alice suporta **modo headless** (`-H`) para automação CI/CD e utiliza um **script de pré-validação** (`validate-compliance.py`) que economiza 3K-5K tokens por invocação ao pré-computar verificações determinísticas.

## Quick Start

### 1. Instalação no Claude Code (recomendada)

Este repositório é um _marketplace_ de _plugins_ do Claude Code (`embrapa-io`), e a Alice é o _plugin_ **`compliance`**. Não é preciso instalar o BMAD. No terminal:

```bash
claude plugin marketplace add embrapa-io/alice
claude plugin install compliance@embrapa-io
```

Ou, de dentro do Claude Code:

```
/plugin marketplace add embrapa-io/alice
/plugin install compliance@embrapa-io
```

Para receber as versões novas: `claude plugin marketplace update embrapa-io` e, para cada plugin instalado, `claude plugin update <plugin>@embrapa-io` (ex.: `claude plugin update cve@embrapa-io`). Os outros plugins (`sentinel`, `cve`, `boilerplate`) se instalam do mesmo jeito; cada um tem o seu README em [`plugins/`](plugins).

### 1b. Instalação em outros assistentes (BMAD)

Para Gemini CLI, OpenCode, GitHub Copilot, Codex e outros, a Alice é instalada como módulo do [**BMAD Method**](https://github.com/bmad-code-org/BMAD-METHOD):

```bash
cd ~/projects/my-project/my-app
npx bmad-method install
```

No passo `Would you like to install from a custom source (Git URL or local path)?`, selecione "**Yes**" e informe "**https://github.com/embrapa-io/alice**"; depois, selecione o módulo "**Embrapa I/O DevOps Compliance Module**".

### 2. Invocar a Alice

Abra o assistente na pasta da aplicação e chame a Alice. No Claude Code, digite `/alice` (o autocompletar mostra `/compliance:alice`):

```
/alice
```

### 3. Seguir o Fluxo

```
[VC] Verificar → [IA] Implementar → [BR] Testar backup → [CR] Code Review
     ↓                 ↓                    ↓                    ↓
 Relatório com    Ajustes do         Ida e volta:          Valida a
 action items     relatório          backup → restore      implementação
                                     → comparar            (NOVA SESSÃO!)
```

## Menu da Alice

Todos os comandos ficam no menu e podem ser chamados a qualquer momento, pelo código (ex.: `BR`) ou pelo nome.

| Opção | Comando | Descrição |
|-------|---------|-----------|
| **[VC]** | Verificar Conformidade | Analisa o codebase e gera `{output_folder}/embrapa-io-compliance.md` com action items detalhados |
| **[IA]** | Implementar Ajustes | Executa os action items do relatório, cria `.env`, `.env.io` e `bootstrap.sh` |
| **[BR]** | Testar Backup e Restore | Teste de ida e volta (regra 1.19): sobe a aplicação, faz o backup, apaga os volumes de dados, restaura e compara com uma sonda; só em `development` |
| **[CR]** | Code Review | Verifica se a implementação está 100% conforme e emite veredicto APPROVED/REJECTED |
| **[CH]** | Chat | Conversar com a Alice sobre qualquer assunto relacionado ao Embrapa I/O |
| **[MH]** | Menu Help | Reexibir o menu de opções |
| **[PM]** | Party Mode | Iniciar discussão multi-agente (requer módulo Core do BMAD) |
| **[DA]** | Dismiss Agent | Encerrar a sessão com resumo de ações e próximos passos |

> **IMPORTANTE**: O Code Review [CR] deve ser executado em uma **NOVA SESSÃO** (no Claude Code, `/clear`) para garantir uma verificação imparcial, sem o contexto da implementação anterior.

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

### [BR] Testar Backup e Restore

Garante, executando, que o arquivo gerado pelo serviço `backup` é restaurado por inteiro pelo `restore` — condição para usar o Backup S3 da plataforma e migrar dados entre servidores. Só roda em `development` (apaga os volumes de dados):

1. Confere o ambiente (`.env.io` de development, serviços `backup` e `restore`), roda o `bootstrap.sh` e sobe a aplicação
2. Escolhe a sonda pela pilha (contagens, títulos ordenados, _hashes_) e grava dados de exemplo se a base estiver vazia
3. Copia `scripts/roundtrip.sh` para a raiz da aplicação e roda o teste
4. Relata **OK** (os dados voltaram iguais) ou **FALHA** (com o _diff_ e a correção proposta para o `restore`)

**Output**: `roundtrip.sh` na raiz e o resultado do teste

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
- Pipeline CI/CD da equipe (`.gitlab-ci.yml`) — a Alice só gera e valida o `.gitlab-io.yml` da plataforma (varredura do SonarQube) e nunca toca o `.gitlab-ci.yml`

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
| `embrapa-io-validation.md` | 42 regras de validação organizadas por categoria |
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

- **2026-11-03**: v1.26.11-9 — Descrições das skills em inglês e curtas, para caber nas duas linhas do seletor de comandos do Claude Code (`/alice`).
- **2026-11-03**: v1.26.11-8 — Plugin `critical-cves` renomeado para **`cve`** (`claude plugin install cve@embrapa-io`, comando `/cve:alice`), no padrão curto dos outros plugins. Quem instalou o nome antigo: `claude plugin uninstall critical-cves@embrapa-io` e instale `cve@embrapa-io`.
- **2026-11-02**: v1.26.11-7 — O repositório vira o marketplace da Alice com um plugin por tarefa: entram `boilerplate` (vindo de `github.com/embrapa-io/skills`, agora arquivado), `sentinel` e `critical-cves`, cada um com a skill `alice` e menu próprio.
- **2026-11-02**: v1.26.11-6 — Ao abrir, a Alice lembra que qualquer código do menu (VC, IA, CR, BR) vale a qualquer momento e que `MH` reexibe o menu; `/bmad-help` só é citado quando o BMAD está instalado.
- **2026-11-02**: v1.26.11-5 — Plugin renomeado para **`compliance`** (`claude plugin install compliance@embrapa-io`), README com a instalação pelo Claude Code sem BMAD, e comando **[BR] Testar Backup e Restore** no menu (workflow `backup-roundtrip` e `scripts/roundtrip.sh` distribuído com o plugin).
- **2026-11-02**: v1.26.11-4 — Regra 5.4: o símbolo do copyright passa a ser ⓒ em todos os arquivos (havia `(c)`, `©` e `ⓒ` em regras diferentes, e a Alice pedia ao usuário para decidir); `(c)` e `©` num LICENSE existente são aceitos.
- **2026-11-01**: v1.26.11-3 — Teste de ida e volta (`roundtrip.sh`, regra 1.19): a sonda passa por `eval`; antes, qualquer sonda com SQL entre aspas (inclusive a de PostgreSQL da tabela) era quebrada em palavras e o teste falhava.
- **2026-11-01**: v1.26.11-2 — Regra 3.9: telefone do mantenedor aceita fixo ou ramal da Unidade (`+DDI (DDD) XXXX-XXXX`), além do celular.
- **2026-11-01**: v1.26.11-1 — Regra 5.4: `LICENSE` de terceiros (MIT, BSD, Apache…) movido para `THIRD-PARTY-NOTICES` antes de gravar o da Embrapa; _copyleft_ pede análise. Primeira versão publicada no _marketplace_ com as regras 1.19 (_restore_ desfaz o _backup_), 2.11 e 2.7c (arquivos `.env`), 1.14, 1.15, 2.4b, 2.7b, 4.1 e 4.2, entradas na `main` depois da 1.26.10-1 sem aumento de versão (quem instalou o _plugin_ não as recebia).
- **2026-10-03**: v1.26.10-1 — Regra 5.5: `.gitlab-io.yml` na raiz (pipeline da plataforma com SonarQube; MEDIUM se ausente, aviso sem `sonar-scanner`); Alice gera o arquivo a partir de `templates/gitlab-io/gitlab-io.yml` e nunca toca o `.gitlab-ci.yml`, que passa a ser da equipe
- **2026-04-14**: Quality analysis e otimizações — SKILL.md na raiz, `validate-compliance.py` (1892 linhas, 29 testes), modo headless, config consolidado, depreciação VCL, cobertura NO-FALLBACK/Linter no VC/CR, checklists compartilhados, cobertura `.gitignore` expandida (`.env.sh` + diretórios AI)
- **2026-03-30**: v1.26.4-9 — Validação de módulo, criação de module-help.csv, consolidação de metadados
- **2026-01-20**: Transformação em AGENTE com criação da Alice e 3 workflows principais
- **2025-12-17**: Auditoria e certificação BMAD v6 Excellence como módulo
