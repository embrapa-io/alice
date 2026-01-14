---
name: 'step-02-validate-docker'
description: 'Validar docker-compose.yaml contra as 4 Verdades Fundamentais'

# File References
nextStepFile: './step-03-validate-env.md'
---

# Step 2: Validar Docker Compose

## STEP GOAL:

Validar o arquivo docker-compose.yaml contra as 4 Verdades Fundamentais da plataforma Embrapa I/O e demais regras de validação (IDs 1.1-1.17).

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, executing validation

### Role Reinforcement:

- ✅ You are a compliance auditor validating Docker configuration
- ✅ If you already have been given a name, communication_style and persona, continue to use those while playing this new role
- ✅ Document every violation found

### Step-Specific Rules:

- 🎯 Focus on docker-compose.yaml validation only
- 🚫 FORBIDDEN to skip any validation check
- 💬 Approach: Systematic validation with documentation
- 📋 Each error must have ID, severity, message, solution

## EXECUTION PROTOCOLS:

- 🎯 Read and parse docker-compose.yaml
- 💾 Document all errors with structured format
- 📖 Apply all 17 validation rules (IDs 1.1-1.17)
- 🚫 FORBIDDEN to invent errors not based on rules

## CONTEXT BOUNDARIES:

- Available context: project_path, severity_levels from step 1
- Focus: Docker Compose validation only
- Limits: Do not validate .env files yet
- Dependencies: Successful completion of step 1

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Ler docker-compose.yaml

Read file at `{project_path}/docker-compose.yaml`.

**Se arquivo não existe:**
Create error:
```json
{
  "id": "1.1",
  "severity": "CRITICAL",
  "category": "docker-compose",
  "message": "Arquivo docker-compose.yaml não encontrado",
  "location": "{project_path}/docker-compose.yaml",
  "solution": "Execute workflow generate-docker-compose",
  "auto_fixable": false
}
```

### 2. Validar 4 Verdades Fundamentais

**ID 1.2 - Verdade 1: Sem campo 'version'**
```
Check: Campo 'version' está AUSENTE
Severity: CRITICAL
Solution: Remover campo 'version' (Compose v2+ não usa)
Auto-fixable: true
```

**ID 1.3/1.4/1.5 - Verdade 2: Network 'stack' externa**
```
Check 1.3: Network 'stack' definida
Check 1.4: Network tem 'external: true'
Check 1.5: Nome segue padrão ${IO_PROJECT}_${IO_APP}_${IO_STAGE}
Severity: CRITICAL
Auto-fixable: partially
```

**ID 1.8 - Verdade 3: Volumes externos**
```
Check: Todos os volumes têm 'external: true'
Severity: HIGH
Auto-fixable: true
```

**ID 1.7 - Verdade 4: Sem container_name (PROIBIDO)**
```
Check: Nenhum serviço tem 'container_name'
Severity: HIGH
Auto-fixable: true
Reason: O nome dos containers é definido automaticamente pelo COMPOSE_PROJECT_NAME
        injetado pela plataforma (padrão: {IO_PROJECT}_{IO_APP}_{IO_STAGE}_{service}).
        Usar container_name quebra a convenção e causa conflitos entre ambientes.
```

### 3. Validar Regras Adicionais

**ID 1.6 - Serviços conectados à network stack**
```
Severity: HIGH
```

**ID 1.9 - Restart policy**
```
Check: Serviços principais têm 'restart: unless-stopped'
Check: Serviços CLI têm 'restart: "no"'
Severity: HIGH
```

**ID 1.10 - Healthcheck**
```
Check: Serviços principais têm healthcheck configurado
Severity: HIGH
```

**ID 1.11/1.17 - Portas via variáveis**
```
Check: Portas do host usam variáveis ${PORT_*}
Check: NENHUMA porta hardcoded no lado esquerdo
Severity: CRITICAL (1.17)
```

**ID 1.12 - Profiles CLI**
```
Check: Serviços CLI usam 'profiles: [cli]'
Severity: MEDIUM
```

**ID 1.14 - Volumes via variáveis**
```
Check: Volumes de serviço usam variáveis do .env
Severity: MEDIUM
```

**ID 1.16 - Backup volume hardcoded**
```
Check: Volume de backup tem nome hardcoded correto
Severity: LOW
```

### 4. Estruturar Erros Encontrados

For each error found, create structured object:
```json
{
  "id": "1.X",
  "severity": "CRITICAL|HIGH|MEDIUM|LOW",
  "category": "docker-compose",
  "message": "Descrição clara do problema",
  "location": "docker-compose.yaml:linha",
  "solution": "Instrução específica de correção",
  "auto_fixable": true|false
}
```

Store all errors in `{docker_compose_errors}`.

### 5. Calcular Status da Categoria

```
compliant: 0 erros
partial: apenas MEDIUM/LOW
non-compliant: CRITICAL ou HIGH presentes
```

Store as `{docker_compose_status}`.

### 6. Apresentar Resultados

Display:
```
📋 **Validação Docker Compose - Resultados**

📄 Arquivo: {project_path}/docker-compose.yaml
📊 Status: {docker_compose_status}

**4 Verdades Fundamentais:**
- [✅|❌] Sem campo 'version'
- [✅|❌] Network 'stack' externa
- [✅|❌] Volumes externos
- [✅|❌] Sem container_name

**Erros encontrados:** {error_count}
- CRITICAL: {critical_count}
- HIGH: {high_count}
- MEDIUM: {medium_count}
- LOW: {low_count}

{error_details_if_any}
```

### 7. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue to .env Validation [D] Details of Errors [X] Exit"

#### Menu Handling Logic:

- IF C: Store errors, then load, read entire file, then execute {nextStepFile}
- IF D: Show detailed error list with solutions
- IF X: End workflow gracefully
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#7-present-menu-options)

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [docker-compose validation complete], will you then load and read fully `{nextStepFile}` to execute and begin .env files validation.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All 17 validation rules checked
- Errors documented with proper structure
- Category status calculated
- Results presented clearly

### ❌ SYSTEM FAILURE:

- Skipping validation rules
- Not documenting errors properly
- Inventing errors not based on rules
- Proceeding without completing all checks

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
