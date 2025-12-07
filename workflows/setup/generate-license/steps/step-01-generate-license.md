---
name: 'step-01-generate-license'
description: 'Calcular ano atual e gerar arquivo LICENSE com copyright da Embrapa'

# Path Definitions
workflow_path: '{project-root}/.bmad/embrapa-io/workflows/setup/generate-license'

# File References
thisStepFile: '{workflow_path}/steps/step-01-generate-license.md'
workflowFile: '{workflow_path}/workflow.md'

# Output References
licenseOutput: '{project-root}/LICENSE'

# Template References
licenseTemplate: '{workflow_path}/templates/template.LICENSE'
---

# Step 1: Gerar Arquivo LICENSE

## STEP GOAL:

Calcular o ano atual dinamicamente do sistema e gerar o arquivo LICENSE com o copyright correto da Embrapa (Brazilian Agricultural Research Corporation).

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER use hardcoded year values
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: This is an autonomous workflow with minimal interaction
- 📋 YOU ARE A FACILITATOR, executing the generation

### Role Reinforcement:

- ✅ You are a configuration specialist generating license files
- ✅ If you already have been given a name, communication_style and persona, continue to use those while playing this new role
- ✅ This is largely autonomous - execute and confirm

### Step-Specific Rules:

- 🎯 Focus on calculating year and generating LICENSE
- 🚫 FORBIDDEN to use hardcoded years (2024, 2025, etc.)
- 💬 Approach: Calculate, generate, save, confirm
- 📋 Year MUST come from current system date

## EXECUTION PROTOCOLS:

- 🎯 Get current year from system date
- 💾 Generate LICENSE content with dynamic year
- 📖 Save file and confirm to user
- 🚫 FORBIDDEN to prompt for year - always use current date

## CONTEXT BOUNDARIES:

- Available context: user_name, communication_language from config
- Focus: LICENSE file generation
- Limits: This is a simple, autonomous workflow
- Dependencies: None - standalone workflow

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Calcular Ano Atual

**Obter data atual do sistema:**
- Extract current year in YYYY format (4 digits)
- Store as `{current_year}`

**Exemplo:**
- Se data atual é 2025-12-07, então `{current_year}` = 2025

⚠️ **IMPORTANTE:** NUNCA usar ano fixo/hardcoded. SEMPRE calcular da data atual do sistema.

### 2. Gerar Conteúdo do LICENSE

Generate content using the copyright symbol ⓒ (U+24D2):

```
Copyright ⓒ {current_year} Brazilian Agricultural Research Corporation (Embrapa). All rights reserved.
```

Store as `{license_content}`.

### 3. Salvar Arquivo LICENSE

Save to `{project-root}/LICENSE`:
- Content: `{license_content}`
- Encoding: UTF-8 (to preserve ⓒ symbol)
- Ensure trailing newline

**Se arquivo LICENSE já existir:**
- Sobrescrever silenciosamente (comportamento esperado)

### 4. Confirmar Criação

Display to {user_name}:
```
✅ **Arquivo LICENSE criado com sucesso!**

📍 **Localização:** {project-root}/LICENSE
📅 **Ano do copyright:** {current_year}

📄 **Conteúdo:**
\`\`\`
Copyright ⓒ {current_year} Brazilian Agricultural Research Corporation (Embrapa). All rights reserved.
\`\`\`

✨ O arquivo LICENSE está pronto e conforme com os padrões da Embrapa.
```

### 5. Finalização

Display:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 **Workflow generate-license concluído!**

📄 **Arquivo criado:**
- {project-root}/LICENSE ✅

💡 **Observações:**
- O arquivo LICENSE deve ser commitado no repositório
- O ano é calculado automaticamente a cada execução
- Para atualizar o ano, basta executar este workflow novamente

🙏 Obrigado por usar o módulo Embrapa I/O!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Year calculated dynamically from system date
- LICENSE file created with correct content
- Copyright symbol ⓒ preserved (UTF-8)
- File saved at project root
- User informed of success

### ❌ SYSTEM FAILURE:

- Using hardcoded year (2024, 2025, etc.)
- Not calculating year from current date
- Copyright symbol corrupted
- File not saved correctly
- Not confirming to user

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.

---

## WORKFLOW COMPLETION

This is the **ONLY STEP** of the generate-license workflow (autonomous workflow).

Upon successful completion:
1. LICENSE file is saved at project root
2. User is informed of success
3. Workflow ends gracefully

**No further step files to load.**
