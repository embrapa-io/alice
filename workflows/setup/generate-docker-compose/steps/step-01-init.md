---
name: 'step-01-init'
description: 'Verificar pré-requisitos e dependências antes de gerar docker-compose.yaml'

# Path Definitions
workflow_path: '{project-root}/.bmad/embrapa-io/workflows/setup/generate-docker-compose'

# File References
thisStepFile: '{workflow_path}/steps/step-01-init.md'
nextStepFile: '{workflow_path}/steps/step-02-detect-stack.md'
workflowFile: '{workflow_path}/workflow.md'

# Knowledge References
fundamentalsKnowledge: '{project-root}/.bmad/embrapa-io/knowledge/embrapa-io-fundamentals.md'
validationKnowledge: '{project-root}/.bmad/embrapa-io/knowledge/embrapa-io-validation.md'
---

# Step 1: Inicialização e Verificação de Pré-requisitos

## STEP GOAL:

Verificar se o projeto possui os pré-requisitos necessários para geração do docker-compose.yaml, especialmente a existência do arquivo .env.io com variáveis obrigatórias.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator

### Role Reinforcement:

- ✅ You are a DevOps specialist and Docker expert
- ✅ If you already have been given a name, communication_style and persona, continue to use those while playing this new role
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring expertise in containerização e conformidade Embrapa I/O
- ✅ Maintain collaborative and technical tone throughout

### Step-Specific Rules:

- 🎯 Focus only on verifying prerequisites and loading required variables
- 🚫 FORBIDDEN to generate docker-compose.yaml in this step
- 💬 Approach: Systematic verification with clear feedback
- 📋 Collect and validate all IO_* variables before proceeding

## EXECUTION PROTOCOLS:

- 🎯 Check for .env.io file existence
- 💾 Load and validate required IO_* variables
- 📖 Inform user about missing prerequisites
- 🚫 FORBIDDEN to proceed if .env.io is missing or invalid

## CONTEXT BOUNDARIES:

- Available context: Project root path, config.yaml variables
- Focus: Prerequisites verification only
- Limits: Do not analyze stack or generate any files yet
- Dependencies: .env.io file with valid IO_* variables

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Verificar Arquivo .env.io

Check if file exists at `{project-root}/.env.io`:

**Se arquivo NÃO existe:**

Display to {user_name}:
```
⚠️ Arquivo .env.io não encontrado!

O workflow generate-docker-compose depende de variáveis definidas no arquivo .env.io para gerar um docker-compose.yaml conforme com a plataforma Embrapa I/O.

💡 **Sugestão**: Execute primeiro o workflow generate-env-io para criar o arquivo .env.io com as variáveis necessárias.

Caminho esperado: {project-root}/.env.io
```

**Se arquivo EXISTE:**

Continue to next section.

### 2. Carregar Variáveis Obrigatórias

Read `.env.io` file and extract:

- `IO_PROJECT` - Nome unix do projeto
- `IO_APP` - Nome unix da aplicação
- `IO_STAGE` - Ambiente (development/alpha/beta/release)
- `IO_VERSION` - Versão no formato 0.YY.M-dev.X

**Validar cada variável:**

- IO_PROJECT: deve ser lowercase, apenas letras, números e hífens
- IO_APP: deve ser lowercase, apenas letras, números e hífens
- IO_STAGE: deve ser um dos valores válidos
- IO_VERSION: deve seguir formato semver

**Se alguma variável estiver ausente ou inválida:**

Display error and suggest running generate-env-io workflow.

### 3. Calcular Variáveis Derivadas

Calculate and store:

- `project_name` = `${IO_PROJECT}_${IO_APP}`
- `network_name` = `${IO_PROJECT}_${IO_APP}_${IO_STAGE}`

### 4. Apresentar Resumo de Pré-requisitos

Display to {user_name}:
```
✅ Pré-requisitos verificados com sucesso!

📋 **Variáveis carregadas do .env.io:**
- IO_PROJECT: {io_project}
- IO_APP: {io_app}
- IO_STAGE: {io_stage}
- IO_VERSION: {io_version}

📐 **Valores calculados:**
- Project Name: {project_name}
- Network Name: {network_name}

🎯 **Próximo passo:** Detectar a stack tecnológica do projeto.
```

### 5. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue to Stack Detection [X] Exit"

#### Menu Handling Logic:

- IF C: Store variables in context, then load, read entire file, then execute {nextStepFile}
- IF X: End workflow gracefully with message about running again later
- IF .env.io missing: Suggest running generate-env-io and exit
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#5-present-menu-options)

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu items execution, return to this menu
- User can chat or ask questions - always respond and then end with display again of the menu options

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [.env.io validated and variables loaded], will you then load and read fully `{workflow_path}/steps/step-02-detect-stack.md` to execute and begin stack detection phase.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- .env.io file found and readable
- All required IO_* variables present and valid
- Derived variables calculated correctly
- User informed of next steps
- Menu presented and user input handled correctly

### ❌ SYSTEM FAILURE:

- Proceeding without valid .env.io file
- Not validating IO_* variable formats
- Skipping variable loading
- Proceeding without user confirmation
- Not suggesting generate-env-io when .env.io is missing

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
