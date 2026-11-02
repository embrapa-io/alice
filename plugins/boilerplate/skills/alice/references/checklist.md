# Checklist — Pré e Pós Genericação

## Pré-checagem (antes de editar qualquer coisa)

Rode estas verificações. Se **qualquer** item falhar, pare e peça ao usuário para rodar a Alice de conformidade (`/compliance:alice` → `VC`, do plugin `compliance@embrapa-io`) antes de prosseguir — este plugin não substitui a validação.

### Estrutura de arquivos obrigatórios

- [ ] `docker-compose.yaml` presente na raiz
- [ ] `.env.io.example` presente na raiz
- [ ] `.env.example` presente na raiz
- [ ] `README.md` presente na raiz
- [ ] `LICENSE` presente na raiz (conteúdo pode ser qualquer um — **a skill vai substituí-lo por MIT** na etapa de genericação; ver `license-template.md`)
- [ ] `AGENTS.md` presente na raiz — **não bloqueia**: se faltar, a skill o gera (ver `agents-md.md`)
- [ ] `.embrapa/settings.json` existe e é JSON válido

Comando rápido:

```bash
for f in docker-compose.yaml .env.io.example .env.example README.md LICENSE .embrapa/settings.json; do
  test -f "$f" && echo "✓ $f" || echo "✗ $f FALTANDO"
done
```

### Conformidade do `docker-compose.yaml`

- [ ] **NÃO** tem campo `version:` no topo (Docker Compose v2)
- [ ] Network `stack` declarada como `external: true`
- [ ] Volumes persistentes declarados como `external: true`
- [ ] Todos os serviços long-running têm `healthcheck`
- [ ] Serviços CLI/one-shot usam `profiles: [cli]`
- [ ] **Nenhuma** variável com fallback (`${VAR:-default}` é proibido — deve ser apenas `${VAR}`)

Comando para checar fallbacks proibidos:

```bash
grep -n '\${[A-Z_]*:-' docker-compose.yaml && echo "⚠️  FALLBACKS ENCONTRADOS — rode a Alice"
```

### `.embrapa/settings.json`

- [ ] JSON válido (`jq . .embrapa/settings.json` sem erro)
- [ ] Campos mínimos esperados pela plataforma presentes (nome, tipo, stack)
- [ ] Textos descritivos em **português brasileiro correto, com acentos**

## `.gitignore` — ajustes da genericação

Um boilerplate bem feito ignora artefatos de ferramentas de IA e editores para que o fork na plataforma não herde lixo. Garanta presença destas entradas:

```gitignore
# Envs (nunca versionar os arquivos reais)
.env
.env.io
.env.sh

# Node / build
node_modules/
dist/
build/
coverage/

# OS
.DS_Store
Thumbs.db

# Logs
*.log

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
.idea/
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
.vscode/
.windsurf/
*.code-workspace
_bmad/
_bmad-output/
```

Adapte por linguagem (Python: `__pycache__/`, `.venv/`; Go: `bin/`; PHP: `vendor/`; etc.) mas **mantenha** o bloco de agentes de IA — é padrão do projeto e evita vazar conversas e configs pessoais.

## Pós-genericação (antes de commitar)

### Substituição completa

- [ ] `grep -rn '<nome-do-projeto-real>'` retorna vazio em `.env.io.example`, `.env.example`, `README.md`
- [ ] `grep -rn '<slug-do-projeto-real>'` retorna vazio nos mesmos arquivos
- [ ] Todos os placeholders usados estão na lista canônica (`references/placeholders.md`)
- [ ] `.env.io.example` bate byte-a-byte com o template de `references/env-io-template.md` (modulo os placeholders do projeto)
- [ ] `LICENSE` foi substituído por MIT com ano atual (primeira linha = `MIT License`, copyright Embrapa, ano corrente), com o `THIRD-PARTY-NOTICES` mantido quando houver — ver `license-template.md`

### Qualidade do texto em PT-BR

- [ ] Nenhuma palavra em português sem acento em `README.md` e comentários (revisar: aplicacao, configuracao, execucao, servicos, variaveis, producao, desenvolvimento, instalacao, autenticacao, informacao, operacao, atencao, manutencao, versao, criacao, remocao, conexao, integracao, gerenciamento, traducao, deteccao, validacao, documentacao)
- [ ] Termos técnicos em inglês consistentes (commit, endpoint, stack — sem tradução forçada)

Comando rápido para suspeitos comuns:

```bash
grep -rnE '\b(aplicacao|configuracao|execucao|servicos|variaveis|producao|autenticacao|informacao|operacao|atencao|manutencao|versao|criacao|remocao|conexao|integracao)\b' README.md *.example .embrapa/ 2>/dev/null
```

### `.gitlab-io.yml` (pipeline da plataforma)

- [ ] App classificada e confirmada com o usuário: **com código-fonte próprio** ou **de prateleira** (`references/gitlab-io.md`)
- [ ] Com código: `.gitlab-io.yml` com o scanner do SonarQube (`sonar-scanner`, ou `dotnet sonarscanner` no .NET) e a chave `"${CI_PROJECT_NAMESPACE##*/}_${CI_PROJECT_NAME}"`
- [ ] De prateleira: `.gitlab-io.yml` sem pipeline (`workflow: rules: - when: never` + job mínimo)
- [ ] Sem `.gitlab-ci.yml` no boilerplate (o antigo da plataforma removido; pipeline próprio da app só com aval do usuário)
- [ ] README cita o `.gitlab-io.yml` na árvore de arquivos, e não o `.gitlab-ci.yml`

### Análise do SonarQube (boilerplate com código, antes do catálogo)

- [ ] MCP do SonarQube ativo na sessão (ou usuário orientado a ligá-lo — `references/sonarqube-antes-do-catalogo.md`)
- [ ] Projeto `boilerplate_<nome>` existe no SonarQube e a análise rodou com a configuração atual (pipeline novo na `main`)
- [ ] Quality gate passando, sem vulnerabilidade nem bug; hotspots revisados; falsos positivos marcados com justificativa
- [ ] Só depois: boilerplate incluído em `metadata/boilerplates.json`

### Versões

- [ ] Imagens Docker na versão estável mais recente (validado via Context7 quando disponível)
- [ ] Dependências de `package.json` / `requirements.txt` / `composer.json` / `go.mod` em versão estável recente
- [ ] Upgrades controversos (major) foram confirmados pelo usuário

### Sanidade final

- [ ] `env $(cat .env.io.example) docker compose config` roda sem erro (valida o compose com as variáveis da plataforma) — **atenção**: os placeholders `%GENESIS_*%` vão aparecer literais; rode com valores dummy para teste: `IO_PROJECT=test IO_APP=test IO_STAGE=development IO_VERSION=0.0.0 docker compose config`
- [ ] README renderiza bem no GitHub/GitLab (cabeçalhos, code blocks, tabelas)
- [ ] Diff final revisado com o usuário antes de commitar
