---
name: 'step-01-analyze-codebase'
description: 'Análise inicial do codebase para detectar stack tecnológica e estrutura existente'
nextStepFile: './step-02-validate-docker.md'
---

# Step 1: Analisar Codebase

## STEP GOAL:

Realizar análise inicial do codebase para detectar a stack tecnológica, estrutura existente, e preparar o contexto para validação de conformidade.

## MANDATORY EXECUTION RULES:

- 🛑 NEVER proceed without completing all analysis tasks
- 📖 READ entire step before taking any action
- 📋 DOCUMENT all findings in context for next steps
- 🔧 FOCUS on detection, not modification

## Sequence of Instructions

### 1. Detectar Stack Tecnológica

Verificar e documentar:

**Para Node.js:**
```
- package.json → detectar frameworks (Express, Fastify, NestJS, etc.)
- Detectar gerenciador de pacotes (npm, yarn, pnpm, bun)
- Detectar TypeScript vs JavaScript
```

**Para Python:**
```
- requirements.txt ou pyproject.toml → detectar frameworks (Django, Flask, FastAPI, etc.)
- Detectar gerenciador de pacotes (pip, poetry, pipenv)
```

**Para PHP:**
```
- composer.json → detectar frameworks (Laravel, Slim, Symfony, etc.)
```

**Para Frontend:**
```
- package.json → detectar Vue.js, React, Angular, Svelte
- Detectar build tool (Vite, Webpack, etc.)
```

**Para outros:**
```
- go.mod → Go
- Cargo.toml → Rust
- *.csproj → .NET
```

Store as `{detected_stack}`.

### 2. Verificar Estrutura de Diretórios

Documentar estrutura existente:

```
- Diretório principal do código-fonte (src/, app/, etc.)
- Diretório de configuração (config/, etc.)
- Diretório Docker (docker/, etc.)
- Presença de .embrapa/
- Presença de docs/
```

Store as `{project_structure}`.

### 3. Verificar Arquivos de Conformidade Existentes

Checar presença de:

```
- [ ] docker-compose.yaml ou docker-compose.yml
- [ ] .env.example
- [ ] .env.io.example
- [ ] .embrapa/settings.json
- [ ] LICENSE
- [ ] Dockerfile(s)
- [ ] .gitignore
- [ ] README.md
```

Store as `{existing_files}`.

### 4. Detectar Endpoints de Health Check

Buscar endpoints existentes que possam ser usados para health check:

```
Padrões comuns:
- /health
- /healthz
- /status
- /api/health
- /api/status
- / (root endpoint retornando 200)
```

**IMPORTANTE**: Se existir endpoint de health check, documentar para reutilizar. NÃO criar novos endpoints.

Store as `{health_endpoint}`.

### 5. Detectar Integrações Existentes

Verificar se já existem:

```
- Sentry: buscar por @sentry, sentry.init, SENTRY_DSN
- Matomo: buscar por matomo, _paq, MATOMO_ID
- Logger estruturado: buscar por winston, pino, bunyan
```

Store as `{existing_integrations}`.

### 6. Apresentar Resumo da Análise

Apresentar ao usuário:

```markdown
## 📊 Resumo da Análise do Codebase

**Stack Detectada:** {detected_stack}
**Estrutura:** {project_structure}

### Arquivos de Conformidade
{existing_files}

### Health Check Endpoint
{health_endpoint}

### Integrações Existentes
{existing_integrations}

---

🎯 **Próximo passo:** Validar configuração Docker Compose
```

### 7. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue to Docker Validation [X] Exit workflow"

#### Menu Handling Logic:

- IF C: Store all findings, then load, read entire file, then execute {nextStepFile}
- IF X: End workflow gracefully, inform user they can restart later

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected will you then load and read fully `{nextStepFile}` to continue validation.
