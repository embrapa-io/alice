---
name: 'step-01-collect-project'
description: 'Coletar informações do projeto: IO_PROJECT, IO_APP e IO_DEPLOYER'

# Path Definitions
workflow_path: '{project-root}/.bmad/embrapa-io/workflows/setup/generate-env-io'

# File References
thisStepFile: '{workflow_path}/steps/step-01-collect-project.md'
nextStepFile: '{workflow_path}/steps/step-02-generate-files.md'
workflowFile: '{workflow_path}/workflow.md'

# Template References
envTemplate: '{workflow_path}/templates/template.env.io'
---

# Step 1: Coletar Informações do Projeto

## STEP GOAL:

Coletar as informações básicas do projeto: nome do projeto (IO_PROJECT), nome da aplicação (IO_APP) e email do desenvolvedor (IO_DEPLOYER), validando cada entrada conforme regras da plataforma Embrapa I/O.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator

### Role Reinforcement:

- ✅ You are a DevOps specialist collecting project configuration
- ✅ If you already have been given a name, communication_style and persona, continue to use those while playing this new role
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring validation expertise, user brings project information

### Step-Specific Rules:

- 🎯 Focus only on collecting and validating project information
- 🚫 FORBIDDEN to generate files in this step
- 💬 Approach: Interactive collection with strict validation
- 📋 Validate each input before proceeding

## EXECUTION PROTOCOLS:

- 🎯 Collect IO_PROJECT, IO_APP, IO_DEPLOYER
- 💾 Validate each value against platform rules
- 📖 Explain validation errors clearly
- 🚫 FORBIDDEN to accept invalid values

## CONTEXT BOUNDARIES:

- Available context: user_name, communication_language from config
- Focus: Project information collection only
- Limits: Do not calculate IO_VERSION yet
- Dependencies: None - this is the first step

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Coletar IO_PROJECT

Ask {user_name}:
```
📦 **Nome do Projeto (IO_PROJECT)**

Qual o nome unix do projeto?

Regras:
- Apenas letras minúsculas, números e hífens
- Sem espaços ou caracteres especiais
- Exemplos: mecaniza, agro-tools, meu-projeto

IO_PROJECT:
```

**Validate:**
- Regex: `^[a-z0-9-]+$`
- Must not be empty

**Se inválido:**
```
❌ Nome inválido: "{input}"

O nome deve conter apenas:
- Letras minúsculas (a-z)
- Números (0-9)
- Hífens (-)

Por favor, tente novamente.
```

Store valid value as `{io_project}`.

### 2. Coletar IO_APP

Ask {user_name}:
```
📱 **Nome da Aplicação (IO_APP)**

Qual o nome unix da aplicação?

Regras:
- Mesmas regras do IO_PROJECT
- Exemplos: api, frontend, web, mobile

IO_APP:
```

**Validate:**
- Regex: `^[a-z0-9-]+$`
- Must not be empty

Store valid value as `{io_app}`.

### 3. Coletar IO_DEPLOYER

Ask {user_name}:
```
📧 **Email do Desenvolvedor (IO_DEPLOYER)**

Qual o email do desenvolvedor responsável?

⚠️ **Formato obrigatório:** name.surname@embrapa.br

IO_DEPLOYER:
```

**Validate:**
- Must end with `@embrapa.br`
- Valid email format

**Se inválido:**
```
❌ Email inválido: "{input}"

O email deve:
- Terminar com @embrapa.br
- Seguir formato: name.surname@embrapa.br

Por favor, tente novamente.
```

Store valid value as `{io_deployer}`.

### 4. Apresentar Resumo

Display:
```
✅ **Informações do Projeto Coletadas:**

📦 IO_PROJECT: {io_project}
📱 IO_APP: {io_app}
📧 IO_DEPLOYER: {io_deployer}

📐 **Valores que serão calculados automaticamente:**
- COMPOSE_PROJECT_NAME = {io_project}_{io_app}_development
- IO_VERSION = 0.YY.M-dev.1 (baseado na data atual)
- IO_STAGE = development

🎯 **Próximo passo:** Gerar arquivos .env.io e .env.io.example
```

### 5. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue to Generate Files [E] Edit values [X] Exit"

#### Menu Handling Logic:

- IF C: Store all values in context, then load, read entire file, then execute {nextStepFile}
- IF E: Return to section 1 to recollect values
- IF X: End workflow gracefully
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#5-present-menu-options)

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu items execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [all values validated and stored], will you then load and read fully `{workflow_path}/steps/step-02-generate-files.md` to execute and begin file generation.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- IO_PROJECT collected and validated (lowercase, no spaces)
- IO_APP collected and validated (lowercase, no spaces)
- IO_DEPLOYER collected and validated (@embrapa.br)
- All values presented for user confirmation

### ❌ SYSTEM FAILURE:

- Accepting invalid values (uppercase, spaces, wrong email domain)
- Not validating each input
- Skipping validation on any field
- Proceeding without user confirmation

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
