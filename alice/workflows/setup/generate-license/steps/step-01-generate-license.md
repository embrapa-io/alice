---
name: 'step-01-generate-license'
description: 'Calcular ano atual e gerar arquivo LICENSE com copyright da Embrapa'

# Output References
licenseOutput: '{project-root}/LICENSE'

# Template References
licenseTemplate: '{workflow_path}/templates/template.LICENSE'
---

# Step 1: Gerar Arquivo LICENSE

## STEP GOAL:

Calcular o ano atual dinamicamente do sistema e gerar o arquivo LICENSE com o copyright correto da Embrapa (Brazilian Agricultural Research Corporation).

## Rules

Follow `./references/step-file-protocol.md`. Step-specific:
- NUNCA usar ano hardcoded -- ano DEVE vir da data atual do sistema
- Workflow autônomo: calcular, gerar, salvar, confirmar
- PROIBIDO solicitar ano ao usuário -- sempre usar data atual do sistema

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

## WORKFLOW COMPLETION

This is the **ONLY STEP** of the generate-license workflow (autonomous workflow).

Upon successful completion:
1. LICENSE file is saved at project root
2. User is informed of success
3. Workflow ends gracefully

**No further step files to load.**
