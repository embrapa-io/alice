---
name: 'step-01-init'
description: 'Carregar conhecimento e coletar parâmetros de validação'

# File References
nextStepFile: './step-02-validate-docker.md'

# Knowledge References
fundamentalsKnowledge: './knowledge/embrapa-io-fundamentals.md'
validationKnowledge: './knowledge/embrapa-io-validation.md'
---

# Step 1: Inicialização e Parâmetros

## STEP GOAL:

Carregar os arquivos de conhecimento da plataforma Embrapa I/O e coletar os parâmetros de validação do usuário (caminho do projeto, severidades, auto-fix).

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator

### Role Reinforcement:

- ✅ You are a compliance auditor preparing for validation
- ✅ If you already have been given a name, communication_style and persona, continue to use those while playing this new role
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring validation expertise, user brings the project

### Step-Specific Rules:

- 🎯 Focus on loading knowledge and collecting parameters
- 🚫 FORBIDDEN to start validation in this step
- 💬 Approach: Load, collect, confirm parameters
- 📋 All validation rules must come from knowledge files

## EXECUTION PROTOCOLS:

- 🎯 Load knowledge files for validation rules
- 💾 Collect project path and validation parameters
- 📖 Explain what will be validated
- 🚫 FORBIDDEN to proceed without loaded knowledge

## CONTEXT BOUNDARIES:

- Available context: user_name, communication_language from config
- Focus: Initialization only
- Limits: Do not validate yet
- Dependencies: Knowledge files must exist

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Carregar Conhecimento

Load and process:
- `{fundamentalsKnowledge}` - Extract 4 Verdades Fundamentais
- `{validationKnowledge}` - Extract all validation rules

Display:
```
📚 **Conhecimento da Plataforma Carregado**

✅ 4 Verdades Fundamentais
✅ Regras de validação: {rule_count} regras identificadas

Categorias de validação:
- Docker Compose (IDs 1.x)
- Arquivos .env (IDs 2.x)
- Settings JSON (IDs 3.x)
- Integrações (IDs 4.x)
- NO-FALLBACK (IDs 5.x)
- Linter (IDs 6.x)
```

### 2. Coletar Caminho do Projeto

Ask {user_name}:
```
📂 **Projeto a Validar**

Qual o caminho absoluto do projeto a ser validado?

Caminho:
```

**Validate:**
- Directory exists and is accessible
- Can read files in directory

Store as `{project_path}`.
Extract project name as `{project_name}`.

### 3. Coletar Níveis de Severidade

Ask:
```
🎚️ **Níveis de Severidade**

Quais níveis de severidade validar?

[1] CRITICAL - Apenas erros críticos
[2] HIGH - Critical e High
[3] MEDIUM - Critical, High e Medium
[4] ALL - Todos os níveis (recomendado)
```

Store as `{severity_levels}`.

### 4. Perguntar sobre Auto-fix

Ask:
```
🔧 **Correções Automáticas**

Deseja aplicar correções automáticas quando possível?

[S] Sim - Corrigir automaticamente erros simples
[N] Não - Apenas reportar

Nota: Correções automáticas sempre criam backup (.bak)
```

Store as `{auto_fix}` (boolean).

### 5. Detectar Tipo de Projeto

Scan `{project_path}` for:
- `docker-compose.yaml` → `{hasDockerCompose}`
- `.embrapa/settings.json` → `{hasSettings}`
- `.env.io.example` → `{hasEnvIo}`

**Determine project type:**
- ALREADY_COMPLIANT: Has settings AND hasEnvIo
- EXISTING: Has docker-compose but not full compliance files
- NEW: No docker-compose

**Se NEW:**
```
⚠️ Projeto novo detectado (sem docker-compose.yaml)

Validação de conformidade não aplicável para projetos novos.

💡 **Sugestão:** Use os workflows de setup para iniciar:
- generate-env-io
- generate-docker-compose
- generate-settings-json
```
Exit workflow.

### 6. Apresentar Resumo

Display:
```
✅ **Parâmetros de Validação Configurados:**

📂 **Projeto:** {project_name}
📍 **Caminho:** {project_path}
🏷️ **Tipo:** {project_type}

🎚️ **Severidades:** {severity_levels}
🔧 **Auto-fix:** {auto_fix}

📋 **Arquivos detectados:**
- docker-compose.yaml: {hasDockerCompose}
- .embrapa/settings.json: {hasSettings}
- .env.io.example: {hasEnvIo}

🎯 **Próximo passo:** Iniciar validação do docker-compose.yaml
```

### 7. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue to Validation [X] Exit"

#### Menu Handling Logic:

- IF C: Store all parameters, then load, read entire file, then execute {nextStepFile}
- IF X: End workflow gracefully
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#7-present-menu-options)

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [all parameters collected], will you then load and read fully `{nextStepFile}` to execute and begin docker-compose validation.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Knowledge files loaded
- Project path validated
- Severity levels selected
- Auto-fix preference recorded
- Project type determined

### ❌ SYSTEM FAILURE:

- Not loading knowledge files
- Accepting non-existent project path
- Starting validation without parameters
- Inventing validation rules not in knowledge

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
