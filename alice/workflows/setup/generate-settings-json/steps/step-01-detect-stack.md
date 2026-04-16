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

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator

### Role Reinforcement:

- ✅ You are a platform configuration specialist
- ✅ If you already have been given a name, communication_style and persona, continue to use those while playing this new role
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring stack detection expertise

### Step-Specific Rules:

- 🎯 Focus on prerequisites and stack detection
- 🚫 FORBIDDEN to collect project info in this step
- 💬 Approach: Verify, detect, confirm with user
- 📋 Load appropriate template based on detected stack

## EXECUTION PROTOCOLS:

- 🎯 Check for .env.io existence
- 💾 Detect stack from project files
- 📖 Load appropriate settings template
- 🚫 FORBIDDEN to proceed without .env.io

## CONTEXT BOUNDARIES:

- Available context: user_name, communication_language from config
- Focus: Prerequisites and stack detection only
- Limits: Do not collect project metadata yet
- Dependencies: .env.io file must exist

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

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [platform confirmed], will you then load and read fully `{nextStepFile}` to execute and begin variable synchronization.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- .env.io verified and variables loaded
- Stack correctly detected
- Appropriate template loaded
- Platform confirmed with user

### ❌ SYSTEM FAILURE:

- Proceeding without .env.io
- Wrong template loaded for stack
- Not confirming platform with user
- Skipping stack detection

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
