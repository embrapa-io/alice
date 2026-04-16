---
name: 'step-01-collect-project'
description: 'Coletar informações do projeto: IO_PROJECT, IO_APP e IO_DEPLOYER'

# File References
nextStepFile: './step-02-generate-files.md'
---

# Step 1: Coletar Informações do Projeto

## STEP GOAL:

Coletar as informações básicas do projeto: nome do projeto (IO_PROJECT), nome da aplicação (IO_APP) e email do desenvolvedor (IO_DEPLOYER), validando cada entrada conforme regras da plataforma Embrapa I/O.

## Rules

Follow `./references/step-file-protocol.md`. Step-specific:
- Coletar e validar IO_PROJECT, IO_APP, IO_DEPLOYER -- não gerar arquivos neste step
- Validar cada entrada contra regras da plataforma antes de aceitar

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

