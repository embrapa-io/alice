---
name: 'step-02-sync-variables'
description: 'Sincronizar variáveis entre arquivos .env e settings.json'

# Path Definitions
workflow_path: '{project-root}/.bmad/embrapa-io/workflows/setup/generate-settings-json'

# File References
thisStepFile: '{workflow_path}/steps/step-02-sync-variables.md'
nextStepFile: '{workflow_path}/steps/step-03-collect-info.md'
workflowFile: '{workflow_path}/workflow.md'

# Source Files
envFile: '{project-root}/.env'
envExampleFile: '{project-root}/.env.example'
envIoFile: '{project-root}/.env.io'
envIoExampleFile: '{project-root}/.env.io.example'
settingsFile: '{project-root}/.embrapa/settings.json'
---

# Step 2: Sincronizar Variáveis

## STEP GOAL:

Ler todas as variáveis definidas nos arquivos .env, .env.example, .env.io e .env.io.example, comparar com as variáveis em .embrapa/settings.json (se existir), e garantir sincronização completa.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, ensuring variable consistency

### Role Reinforcement:

- ✅ You are a platform configuration specialist ensuring variable sync
- ✅ If you already have been given a name, communication_style and persona, continue to use those while playing this new role
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring expertise in environment variable management

### Step-Specific Rules:

- 🎯 Focus on reading and comparing variables across files
- 🚫 FORBIDDEN to modify any files in this step
- 💬 Approach: Read, compare, report discrepancies
- 📋 Variables from .env.io are PLATFORM variables (IO_*)
- 📋 Variables from .env are APPLICATION variables

## EXECUTION PROTOCOLS:

- 🎯 Read all .env* files and extract variable names
- 💾 Read settings.json if exists and extract variables.default
- 📖 Compare and identify discrepancies
- 🚫 FORBIDDEN to skip any source file

## CONTEXT BOUNDARIES:

- Available context: selected_platform, io_project, io_app from step 1
- Focus: Variable synchronization analysis only
- Limits: Do not collect project metadata yet
- Dependencies: Stack detection from step 1

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Ler Variáveis dos Arquivos .env

**Ler .env.example (ou .env se example não existir):**
```
Extrair todas as linhas no formato:
VARIABLE_NAME=value
VARIABLE_NAME=
# Comentários são ignorados
```

Store as `{env_variables}` (array of variable names).

**Ler .env.io.example (ou .env.io se example não existir):**
```
Extrair todas as variáveis IO_*
```

Store as `{env_io_variables}` (array of variable names).

### 2. Consolidar Variáveis Esperadas

Combine all variables:
```
{expected_variables} = {env_variables} + {env_io_variables}
```

**Excluir variáveis de plataforma que NÃO vão no settings.json:**
- IO_PROJECT (metadata, não variável de runtime)
- IO_APP (metadata, não variável de runtime)
- IO_STAGE (injetado pela plataforma)
- IO_VERSION (metadata, não variável de runtime)
- IO_DEPLOYER (metadata, não variável de runtime)

Store final list as `{expected_variables}`.

### 3. Verificar settings.json Existente

**Se {settingsFile} NÃO existe:**
```
📄 **Arquivo settings.json não encontrado**

Este é um novo projeto. O settings.json será criado com todas as
variáveis detectadas nos arquivos .env.

📊 **Variáveis detectadas:** {expected_count}
```

Set `{settings_exists}` = false.
Set `{settings_variables}` = [].
Skip to section 5.

**Se {settingsFile} EXISTE:**
```
📄 **Arquivo settings.json encontrado**

Analisando variáveis existentes...
```

Read settings.json and extract all variable names from `variables.default[]`.
Store as `{settings_variables}`.
Set `{settings_exists}` = true.

### 4. Comparar Variáveis

**Calcular diferenças:**
```
{missing_in_settings} = {expected_variables} - {settings_variables}
{extra_in_settings} = {settings_variables} - {expected_variables}
```

**Classificar por origem:**
```
For each variable in {missing_in_settings}:
  - Se começa com IO_ → origem: .env.io
  - Senão → origem: .env

For each variable in {extra_in_settings}:
  - Marcar como "definida apenas em settings.json"
```

### 5. Apresentar Análise

**Se nenhuma discrepância:**
```
✅ **Variáveis Sincronizadas**

Todas as {expected_count} variáveis dos arquivos .env estão
corretamente definidas em settings.json.

📊 **Resumo:**
- Variáveis .env: {env_count}
- Variáveis .env.io: {env_io_count}
- Total em settings.json: {settings_count}
```

**Se há discrepâncias:**
```
⚠️ **Discrepâncias Detectadas**

📊 **Resumo da Análise:**
- Variáveis esperadas (dos .env): {expected_count}
- Variáveis em settings.json: {settings_count}

❌ **Variáveis FALTANDO em settings.json:** {missing_count}
{for each missing}
  - {variable_name} (origem: {source_file})
{end for}

⚠️ **Variáveis SOBRANDO em settings.json:** {extra_count}
{for each extra}
  - {variable_name} (não existe em nenhum .env)
{end for}
```

### 6. Determinar Ação para Discrepâncias

**Se há variáveis faltando:**
```
🔧 **Ação para Variáveis Faltando**

As seguintes variáveis existem nos arquivos .env mas não estão
definidas em settings.json:

{missing_variables_list}

Como deseja proceder?

[A] Adicionar todas automaticamente ao settings.json
[M] Escolher manualmente quais adicionar
[I] Ignorar (apenas reportar no compliance)
```

Store choice as `{missing_action}`.

**Se escolheu A ou M:**
For each variable to add, determine type:
```
Analisando tipo da variável {var_name}...

Baseado no nome e valor padrão:
- Se termina em _PORT → type: PORT
- Se termina em _PASSWORD → type: PASSWORD
- Se termina em _SECRET ou _KEY → type: SECRET
- Se termina em _VOLUME → type: VOLUME
- Se valor está vazio → type: EMPTY
- Senão → type: TEXT (com value do .env)
```

Store variables to add as `{variables_to_add}`.

**Se há variáveis sobrando:**
```
🔧 **Ação para Variáveis Sobrando**

As seguintes variáveis existem em settings.json mas não estão
definidas em nenhum arquivo .env:

{extra_variables_list}

Como deseja proceder?

[R] Remover todas do settings.json
[M] Escolher manualmente quais remover
[K] Manter todas (podem ser variáveis legadas)
```

Store choice as `{extra_action}`.
Store variables to remove as `{variables_to_remove}`.

### 7. Apresentar Plano de Sincronização

Display:
```
📋 **Plano de Sincronização**

**Variáveis a ADICIONAR em settings.json:**
{if variables_to_add is empty}
  (nenhuma)
{else}
  {for each var in variables_to_add}
  - {var.name}: {var.type} {if var.value}= {var.value}{endif}
  {end for}
{endif}

**Variáveis a REMOVER de settings.json:**
{if variables_to_remove is empty}
  (nenhuma)
{else}
  {for each var in variables_to_remove}
  - {var.name}
  {end for}
{endif}

**Variáveis a MANTER (sem alteração):**
- {unchanged_count} variáveis
```

### 8. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue to Project Info [R] Refazer análise [X] Exit"

#### Menu Handling Logic:

- IF C: Store sync plan (variables_to_add, variables_to_remove), then load, read entire file, then execute {nextStepFile}
- IF R: Return to section 1 and re-read files
- IF X: End workflow gracefully
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#8-present-menu-options)

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [sync plan confirmed], will you then load and read fully `{workflow_path}/steps/step-03-collect-info.md` to execute and begin project info collection.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All .env files read and parsed
- Variables correctly extracted from each source
- Discrepancies clearly identified with origin
- User informed of sync plan
- Variables typed correctly based on naming convention

### ❌ SYSTEM FAILURE:

- Missing any .env source file in analysis
- Not identifying discrepancies
- Not asking user how to handle discrepancies
- Proceeding without sync plan confirmation
- Wrong variable type inference

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
