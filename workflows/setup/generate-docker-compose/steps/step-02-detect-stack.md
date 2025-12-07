---
name: 'step-02-detect-stack'
description: 'Detectar automaticamente a stack tecnológica do projeto e confirmar com usuário'

# Path Definitions
workflow_path: '{project-root}/.bmad/embrapa-io/workflows/setup/generate-docker-compose'

# File References
thisStepFile: '{workflow_path}/steps/step-02-detect-stack.md'
nextStepFile: '{workflow_path}/steps/step-03-collect-config.md'
workflowFile: '{workflow_path}/workflow.md'
---

# Step 2: Detecção de Stack Tecnológica

## STEP GOAL:

Analisar a estrutura do projeto para identificar automaticamente a stack tecnológica (Node.js, Vue, React, PHP, .NET, etc.) e confirmar a detecção com o usuário.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator

### Role Reinforcement:

- ✅ You are a DevOps specialist with expertise in multiple stacks
- ✅ If you already have been given a name, communication_style and persona, continue to use those while playing this new role
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring stack detection expertise, user brings project knowledge

### Step-Specific Rules:

- 🎯 Focus only on stack detection and confirmation
- 🚫 FORBIDDEN to generate docker-compose.yaml in this step
- 💬 Approach: Analyze files, present findings, confirm with user
- 📋 Store confirmed stack for use in later steps

## EXECUTION PROTOCOLS:

- 🎯 Scan project files for stack indicators
- 💾 Store detected stack and database preferences
- 📖 Present detection results clearly to user
- 🚫 FORBIDDEN to assume stack without user confirmation

## CONTEXT BOUNDARIES:

- Available context: IO_* variables from step 1, project root path
- Focus: Stack detection only
- Limits: Do not collect ports or other config yet
- Dependencies: Successful completion of step 1

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Analisar Estrutura do Projeto

Scan for indicator files:

**Arquivos a procurar:**
- `package.json` → Possível Node.js, Vue, React, React Native
- `requirements.txt` / `pyproject.toml` → Python
- `composer.json` → PHP
- `*.csproj` → .NET
- `pom.xml` / `build.gradle` → Java
- `go.mod` → Go

### 2. Identificar Framework Específico

**Se package.json encontrado, analisar dependencies:**

- `"express"` ou `"fastify"` ou `"nest"` → Node.js API
- `"vue"` → Vue.js Frontend
- `"react"` e `"react-dom"` (sem react-native) → React Frontend
- `"react-native"` → React Native Mobile
- `"next"` → Next.js (SSR)
- `"nuxt"` → Nuxt.js (SSR)

**Se composer.json encontrado:**

- `"laravel/framework"` → PHP Laravel
- `"symfony/framework-bundle"` → PHP Symfony

**Se *.csproj encontrado:**

- Blazor references → .NET Blazor
- ASP.NET Core → .NET API

### 3. Identificar Banco de Dados

Scan for database indicators:

- MongoDB connection strings or `mongoose` dependency
- PostgreSQL/pg dependencies
- MySQL dependencies
- SQL Server dependencies
- Redis dependencies

### 4. Apresentar Detecção

Display to {user_name}:
```
🔍 **Análise de Stack Concluída**

📦 **Stack detectada:** {detected_stack}
   Indicadores encontrados: {indicators_list}

💾 **Banco de dados detectado:** {detected_database}
   Indicadores encontrados: {db_indicators}

Esta detecção está correta?
```

### 5. Confirmar ou Selecionar Stack

Ask {user_name}:
```
A detecção automática está correta? Caso contrário, selecione a stack:

[1] Node.js API (Express/Fastify + MongoDB/PostgreSQL)
[2] Vue.js Frontend (Vuetify/Quasar)
[3] React Frontend
[4] React Native Mobile
[5] Next.js (SSR)
[6] PHP Laravel
[7] .NET Blazor
[8] Python FastAPI/Django
[9] Outro (especificar)
[C] Confirmar detecção automática
```

Store response as `{selected_stack}`.

### 6. Confirmar Banco de Dados (se aplicável)

If stack requires database, ask:
```
Qual banco de dados será usado?

[1] MongoDB
[2] PostgreSQL
[3] MySQL
[4] SQL Server
[5] Nenhum
[C] Confirmar detecção automática ({detected_database})
```

Store response as `{selected_database}`.

### 7. Apresentar Resumo

Display:
```
✅ **Configuração de Stack Confirmada:**

📦 Stack: {selected_stack}
💾 Banco de dados: {selected_database}

🎯 **Próximo passo:** Coletar configurações específicas (portas, healthcheck, etc.)
```

### 8. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue to Configuration [X] Exit"

#### Menu Handling Logic:

- IF C: Store stack and database in context, then load, read entire file, then execute {nextStepFile}
- IF X: End workflow gracefully
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#8-present-menu-options)

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu items execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [stack and database confirmed], will you then load and read fully `{workflow_path}/steps/step-03-collect-config.md` to execute and begin configuration collection.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Project files scanned for stack indicators
- Stack correctly identified or user-selected
- Database preference confirmed
- User informed of detected configuration
- Menu presented and user input handled correctly

### ❌ SYSTEM FAILURE:

- Assuming stack without user confirmation
- Not scanning for all indicator files
- Skipping database detection
- Proceeding without clear stack selection
- Not presenting detection results to user

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
