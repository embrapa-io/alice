---
name: 'step-03-validate-env'
description: 'Validar arquivos .env e .env.io contra regras da plataforma'

# File References
nextStepFile: './step-04-validate-code.md'
---

# Step 3: Validar Arquivos .env

## STEP GOAL:

Validar os arquivos .env.io.example, .env.example e variáveis de ambiente contra as regras da plataforma Embrapa I/O (IDs 2.1-2.10).

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, executing validation

### Role Reinforcement:

- ✅ You are a compliance auditor validating environment configuration
- ✅ If you already have been given a name, communication_style and persona, continue to use those while playing this new role
- ✅ Document every violation found

### Step-Specific Rules:

- 🎯 Focus on .env files validation only
- 🚫 FORBIDDEN to skip any validation check
- 💬 Approach: Systematic validation with documentation
- 📋 Check for NO-QUOTES and NO-SPACES rules

## EXECUTION PROTOCOLS:

- 🎯 Read and validate .env files
- 💾 Document all errors with structured format
- 📖 Apply all validation rules (IDs 2.1-2.10)
- 🚫 FORBIDDEN to miss format violations

## CONTEXT BOUNDARIES:

- Available context: All errors from step 2, project_path
- Focus: .env files validation only
- Limits: Do not validate code yet
- Dependencies: Docker validation from step 2

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Validar Existência de Arquivos

**ID 2.1 - .env.io.example**
```
Check: Arquivo .env.io.example existe
Severity: CRITICAL
Solution: Execute workflow generate-env-io
```

**ID 2.2 - .env.example**
```
Check: Arquivo .env.example existe
Severity: CRITICAL
Solution: Criar .env.example como referência
```

### 2. Validar Duplicação

**ID 2.3 - Sem duplicação**
```
Check: Não há variáveis duplicadas entre .env.io e .env
Severity: CRITICAL
Explanation: Cada variável deve estar em apenas um arquivo
```

### 3. Validar Variáveis Obrigatórias

**ID 2.4 - Variáveis IO_***
```
Check: IO_PROJECT presente
Check: IO_APP presente
Check: IO_STAGE presente
Check: IO_VERSION presente
Check: IO_DEPLOYER presente
Severity: HIGH
```

### 4. Validar Formato de Valores

**ID 2.5 - Sem aspas ou espaços**
```
Check: Nenhum valor contém aspas simples ou duplas
Check: Nenhum valor contém espaços
Severity: HIGH
Examples:
  ❌ MY_VAR="value"
  ❌ MY_VAR='value'
  ❌ MY_VAR=value with spaces
  ✅ MY_VAR=value_without_spaces
```

**ID 2.6 - Convenção de nomes**
```
Check: Variáveis seguem UPPER_SNAKE_CASE
Severity: HIGH
```

### 5. Validar Variáveis de Volume

**ID 2.7 - Volumes referenciados**
```
Check: Cada volume no docker-compose tem variável correspondente
Severity: HIGH
Cross-reference with docker_compose_errors
```

**ID 2.10 - Padrão de nomenclatura**
```
Check: Variáveis de volume seguem ${IO_PROJECT}_${IO_APP}_${IO_STAGE}_[a-z0-9]+
Severity: MEDIUM
```

### 6. Validar .gitignore

**ID 2.8 - Configuração do .gitignore**
```
Check: .env, .env.io e .env.sh estão ignorados
Check: .env.example e .env.io.example NÃO estão ignorados
Check: Diretórios de agentes de IA estão ignorados (.claude/, _bmad/, etc.)
Severity: MEDIUM
Auto-fixable: true
```

### 7. Estruturar Erros

For each error found:
```json
{
  "id": "2.X",
  "severity": "CRITICAL|HIGH|MEDIUM|LOW",
  "category": "env-files",
  "message": "Descrição clara do problema",
  "location": ".env.io:linha ou .env:linha",
  "solution": "Instrução específica de correção",
  "auto_fixable": true|false
}
```

Store all errors in `{env_files_errors}`.
Calculate `{env_files_status}`.

### 8. Apresentar Resultados

Display:
```
📋 **Validação Arquivos .env - Resultados**

**Arquivos verificados:**
- .env.io.example: [✅|❌]
- .env.example: [✅|❌]
- .gitignore: [✅|❌]

📊 Status: {env_files_status}

**Erros encontrados:** {error_count}
- CRITICAL: {critical_count}
- HIGH: {high_count}
- MEDIUM: {medium_count}
- LOW: {low_count}

{error_details_if_any}
```

### 9. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue to Code Validation [D] Details [X] Exit"

#### Menu Handling Logic:

- IF C: Store errors, then load, read entire file, then execute {nextStepFile}
- IF D: Show detailed error list
- IF X: End workflow gracefully

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected, will you then load and read fully `{nextStepFile}` to execute and begin code validation (NO-FALLBACK and Linter).

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All 10 validation rules checked
- Format violations detected (quotes, spaces)
- Errors documented properly
- Cross-referenced with docker-compose volumes

### ❌ SYSTEM FAILURE:

- Not checking for quotes/spaces in values
- Skipping validation rules
- Not cross-referencing volumes
- Proceeding without completing checks

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
