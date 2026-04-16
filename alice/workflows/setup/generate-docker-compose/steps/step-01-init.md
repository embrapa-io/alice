---
name: 'step-01-init'
description: 'Verificar pré-requisitos e dependências antes de gerar docker-compose.yaml'

# File References
nextStepFile: './step-02-detect-stack.md'

# Knowledge References
fundamentalsKnowledge: './knowledge/embrapa-io-fundamentals.md'
validationKnowledge: './knowledge/embrapa-io-validation.md'
---

# Step 1: Inicialização e Verificação de Pré-requisitos

## STEP GOAL:

Verificar se o projeto possui os pré-requisitos necessários para geração do docker-compose.yaml, especialmente a existência do arquivo .env.io com variáveis obrigatórias.

## Rules

Follow `./references/step-file-protocol.md`. Step-specific:
- Verificar existência do .env.io e carregar variáveis IO_* -- não gerar arquivos neste step
- PROIBIDO prosseguir se .env.io estiver ausente ou inválido
- Se .env.io não existir, sugerir executar generate-env-io primeiro

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

