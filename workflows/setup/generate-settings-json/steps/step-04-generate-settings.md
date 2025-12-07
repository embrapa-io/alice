---
name: 'step-04-generate-settings'
description: 'Gerar e salvar arquivo .embrapa/settings.json'

# Path Definitions
workflow_path: '{project-root}/.bmad/embrapa-io/workflows/setup/generate-settings-json'

# File References
thisStepFile: '{workflow_path}/steps/step-04-generate-settings.md'
workflowFile: '{workflow_path}/workflow.md'

# Output References
settingsOutput: '{project-root}/.embrapa/settings.json'
---

# Step 4: Gerar settings.json

## STEP GOAL:

Gerar o arquivo .embrapa/settings.json com toda a configuração coletada, validar a estrutura JSON, e salvar o arquivo.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: This is the final step - ensure complete execution
- 📋 YOU ARE A FACILITATOR, completing the workflow

### Role Reinforcement:

- ✅ You are a platform configuration specialist generating settings.json
- ✅ If you already have been given a name, communication_style and persona, continue to use those while playing this new role
- ✅ Generate valid, complete settings.json

### Step-Specific Rules:

- 🎯 Focus on generating valid JSON and saving
- 🚫 FORBIDDEN to save invalid JSON
- 💬 Approach: Generate, validate, present, save
- 📋 Variables structure must follow type rules

## EXECUTION PROTOCOLS:

- 🎯 Build settings.json from collected values
- 💾 Validate JSON syntax before saving
- 📖 Create .embrapa directory if needed
- 🚫 FORBIDDEN to include 'value' for PASSWORD/SECRET/PORT/EMPTY types

## CONTEXT BOUNDARIES:

- Available context: All values from steps 1-3 (platform, sync_plan, project_info)
- Focus: JSON generation and file saving
- Limits: This is the final step
- Dependencies: All values from previous steps

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Aplicar Plano de Sincronização

**Processar variáveis do sync_plan (step 2):**

```
1. Se settings.json já existe:
   - Ler variáveis atuais de variables.default
   - Adicionar variáveis de {variables_to_add}
   - Remover variáveis de {variables_to_remove}
   - Manter variáveis não afetadas

2. Se settings.json não existe:
   - Usar todas as variáveis de {expected_variables}
   - Aplicar tipos inferidos automaticamente
```

### 2. Construir Estrutura JSON

Build settings.json following Embrapa I/O structure:

```json
{
  "boilerplate": "_",
  "platform": "{selected_platform}",
  "label": "{app_label}",
  "description": "{app_description}",
  "references": [],
  "maintainers": [
    {
      "name": "{maintainer_name}",
      "email": "{maintainer_email}",
      "phone": "{maintainer_phone}"
    }
  ],
  "variables": {
    "default": [
      // Variables from sync_plan (synced with .env files)
    ],
    "alpha": [],
    "beta": [],
    "release": [
      // Release-specific overrides here
    ]
  },
  "orchestrators": ["DockerCompose"]
}
```

**🔄 IMPORTANTE - Variáveis vêm do sync_plan:**
- As variáveis em `variables.default` devem refletir EXATAMENTE as variáveis sincronizadas no step 2
- Variáveis adicionadas pelo usuário via step 3 são ADICIONAIS ao sync_plan

### 3. Aplicar Regras de Variáveis

**🚨 REGRA CRÍTICA - Estrutura por tipo:**

**Tipo TEXT:**
```json
{ "name": "BASE_URL", "type": "TEXT", "value": "http://localhost:3000" }
```

**Tipo VOLUME:**
```json
{ "name": "MONGODB_VOLUME", "type": "VOLUME", "value": "mongodb" }
```
⚠️ value contém APENAS o sufixo, sem `${IO_PROJECT}_${IO_APP}_${IO_STAGE}_`

**Tipos PASSWORD, SECRET, PORT, EMPTY:**
```json
{ "name": "APP_PORT", "type": "PORT" }
{ "name": "DB_PASSWORD", "type": "PASSWORD" }
{ "name": "JWT_SECRET", "type": "SECRET" }
{ "name": "OPTIONAL_VAR", "type": "EMPTY" }
```
⚠️ atributo 'value' é **OMITIDO** (não incluir no JSON)

### 4. Validar JSON

- Parse generated JSON to verify syntax
- Check all required fields present
- Verify variables follow type rules

**Se JSON inválido:**
```
❌ Erro de validação JSON!

Problema encontrado: {error}

Corrigindo automaticamente...
```

### 5. Apresentar Conteúdo Gerado

Display:
```
📄 **Arquivo settings.json gerado:**

\`\`\`json
{generated_json_content}
\`\`\`

📊 **Resumo:**
- Platform: {selected_platform}
- Variáveis default: {default_count}
- Variáveis release: {release_count}
- Mantenedores: 1
```

### 6. Salvar Arquivo

- Create `.embrapa/` directory if not exists
- Save to `{project-root}/.embrapa/settings.json`
- Encoding: UTF-8

Display:
```
✅ **Arquivo salvo com sucesso!**

📍 Localização: {project-root}/.embrapa/settings.json
```

### 7. Apresentar Próximos Passos

Display:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 **PRÓXIMOS PASSOS:**

**1. Revisar settings.json**
- Verifique se todas as variáveis estão corretas
- Adicione referências de documentação se houver

**2. Commitar arquivo**
- O settings.json DEVE ser commitado no repositório
- Este arquivo é lido pela plataforma Embrapa I/O

**3. Validar na plataforma**
- Acesse https://dashboard.embrapa.io
- Valide a configuração do projeto

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 8. Finalização

Display:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 **Workflow generate-settings-json concluído!**

📄 **Arquivo criado:**
- {project-root}/.embrapa/settings.json ✅

💡 **Dica:**
Execute o workflow validate-compliance para verificar
se todos os arquivos do projeto estão conforme Embrapa I/O.

🙏 Obrigado por usar o módulo Embrapa I/O!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Valid JSON generated
- Variables follow type rules
- File saved to .embrapa/settings.json
- Directory created if needed
- Next steps provided

### ❌ SYSTEM FAILURE:

- Saving invalid JSON
- Including 'value' for PASSWORD/SECRET/PORT/EMPTY
- Not creating .embrapa directory
- Not validating JSON before saving
- Leaving user without next steps

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.

---

## WORKFLOW COMPLETION

This is the **FINAL STEP** of the generate-settings-json workflow.

Upon successful completion:
1. .embrapa/settings.json is saved and valid
2. User understands variable type rules
3. User knows next steps
4. Workflow ends gracefully

**No further step files to load.**
