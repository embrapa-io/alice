---
name: 'step-01-detect-stack'
description: 'Verificar pré-requisitos e detectar stack tecnológica do projeto'

# File References
nextStepFile: './step-02-sync-variables.md'

# Template References
settingsBaseTemplate: './templates/settings/settings-base.json'
settingsNodejsTemplate: './templates/settings/settings-nodejs.json'
settingsFrontendTemplate: './templates/settings/settings-frontend.json'
---

# Step 1: Detectar Stack e Verificar Pré-requisitos

## STEP GOAL:

Verificar se .env.io existe (dependência), detectar a stack tecnológica do projeto, e carregar o template de variáveis apropriado.

## Rules

Follow `./references/step-file-protocol.md`. Step-specific:
- Verificar .env.io e detectar stack -- não coletar metadados do projeto neste step
- PROIBIDO prosseguir sem .env.io -- sugerir generate-env-io se ausente
- Carregar template de variáveis apropriado com base na stack detectada

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Verificar Pré-requisitos

Check if `.env.io` exists at `{project-root}/.env.io`:

**Se arquivo NÃO existe:**
```
⚠️ Arquivo .env.io não encontrado!

O workflow generate-settings-json depende de variáveis do .env.io para referência.

💡 **Sugestão**: Execute primeiro o workflow generate-env-io para criar o arquivo .env.io.

Caminho esperado: {project-root}/.env.io
```
Exit workflow.

**Se arquivo EXISTE:**
Read and extract:
- `IO_PROJECT`
- `IO_APP`
- `IO_VERSION`

### 2. Detectar Stack Tecnológica

Scan for indicator files:

**package.json encontrado:**
- Check for `"express"`, `"fastify"`, `"nest"` → Node.js Backend
- Check for `"vue"` → Vue.js Frontend
- Check for `"react"` (without react-native) → React Frontend
- Check for `"next"` → Next.js
- Default if none: Node.js Generic

**requirements.txt ou pyproject.toml encontrado:**
- Python

**composer.json encontrado:**
- PHP

**\*.csproj encontrado:**
- .NET

**go.mod encontrado:**
- Go

Store detected as `{detected_platform}`.

### 3. Selecionar Template de Variáveis

Based on `{detected_platform}`:

- Node.js Backend → Load `{settingsNodejsTemplate}`
- Vue/React Frontend → Load `{settingsFrontendTemplate}`
- Other → Load `{settingsBaseTemplate}`

Store default variables as `{default_variables}`.

### 4. Apresentar Detecção

Display:
```
🔍 **Análise do Projeto Concluída**

📋 **Pré-requisitos:**
- .env.io: ✅ Encontrado
- IO_PROJECT: {io_project}
- IO_APP: {io_app}

📦 **Stack detectada:** {detected_platform}

📝 **Variáveis padrão carregadas:** {variable_count} variáveis
```

### 5. Confirmar Plataforma

Ask:
```
A detecção de plataforma está correta?

[1] Node.js (backend)
[2] Vue.js (frontend)
[3] React (frontend)
[4] Next.js (fullstack)
[5] Python
[6] PHP
[7] .NET
[8] Go
[C] Confirmar detecção automática ({detected_platform})
```

Store confirmed value as `{selected_platform}`.

### 6. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue to Variable Sync [X] Exit"

#### Menu Handling Logic:

- IF C: Store platform and variables, then load, read entire file, then execute {nextStepFile}
- IF X: End workflow gracefully
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#6-present-menu-options)

