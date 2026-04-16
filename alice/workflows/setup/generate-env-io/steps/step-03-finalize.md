---
name: 'step-03-finalize'
description: 'Salvar arquivos e orientar sobre regras críticas da plataforma Embrapa I/O'

# Output References
envIoOutput: '{project-root}/.env.io'
envIoExampleOutput: '{project-root}/.env.io.example'
---

# Step 3: Salvar e Finalizar

## STEP GOAL:

Salvar os arquivos .env.io e .env.io.example, e orientar o usuário sobre as regras críticas da plataforma Embrapa I/O (NO-FALLBACK, valores sem aspas, Linter obrigatório).

## Rules

Follow `./references/step-file-protocol.md`. Step-specific:
- Salvar ambos os arquivos e explicar regras críticas da plataforma (especialmente NO-FALLBACK)
- OBRIGATÓRIO explicar regras de plataforma -- não pular esta orientação
- Este é o step final

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Salvar Arquivos

**Save .env.io:**
- Path: `{project-root}/.env.io`
- Content: `{env_io_content}`

**Save .env.io.example:**
- Path: `{project-root}/.env.io.example`
- Content: `{env_io_example_content}`

Display:
```
✅ **Arquivos criados com sucesso!**

📄 {project-root}/.env.io
📄 {project-root}/.env.io.example
```

### 2. Explicar Regras Críticas

Display comprehensive guidance:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 **REGRAS CRÍTICAS DA PLATAFORMA EMBRAPA I/O**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**📌 REGRA 1: NO-FALLBACK OBRIGATÓRIO**

NUNCA use valores fallback nas variáveis de ambiente:

❌ INCORRETO:
\`\`\`javascript
const port = process.env.PORT || 3000
\`\`\`

✅ CORRETO:
\`\`\`javascript
const port = process.env.PORT
if (!port) throw new Error('PORT is required')
\`\`\`

**Por quê?** A plataforma sempre injeta as variáveis. Se faltar, é erro de configuração que deve falhar explicitamente.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**📌 REGRA 2: VALORES SEM ASPAS E ESPAÇOS**

NUNCA use aspas ou espaços nos valores:

❌ INCORRETO:
\`\`\`bash
MY_VAR="valor com espaços"
MY_VAR='valor'
\`\`\`

✅ CORRETO:
\`\`\`bash
MY_VAR=valor_sem_espacos
MY_VAR=valor-com-hifens
MY_VAR=dG9rZW5fZW5jb2RlZA==  # Base64
\`\`\`

**Para valores complexos, use Base64:**
\`\`\`bash
echo -n "Meu Valor" | base64
\`\`\`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**📌 REGRA 3: PORTAS VIA VARIÁVEIS**

NUNCA hardcode portas no docker-compose.yaml:

❌ INCORRETO:
\`\`\`yaml
ports:
  - "3000:3000"
\`\`\`

✅ CORRETO:
\`\`\`yaml
ports:
  - "${APP_PORT}:3000"
\`\`\`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**📌 REGRA 4: LINTER OBRIGATÓRIO**

A plataforma exige Linter configurado:

**JavaScript/TypeScript:**
\`\`\`bash
npm install --save-dev eslint eslint-config-standard
\`\`\`

**Python:**
\`\`\`bash
pip install ruff
\`\`\`

**PHP:**
\`\`\`bash
composer require --dev squizlabs/php_codesniffer
\`\`\`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 3. Orientar Próximos Passos

Display:
```
📋 **PRÓXIMOS PASSOS OBRIGATÓRIOS:**

**1. Configurar .gitignore**
Adicione ao .gitignore:
\`\`\`
# Variáveis de ambiente
.env
.env.io
.env.sh

# Agentes de IA e IDEs
.agent/
.agents/
.augment/
.claude/
.cline/
.codebuddy/
.crush/
.cursor/
.gemini/
.github/
.iflow/
.kilocode/
.kiro/
.ona/
.opencode/
.pi/
.qoder/
.qwen/
.roo/
.rovodev/
.trae/
.windsurf/
_bmad/
_bmad-output/
\`\`\`
⚠️ .env.io.example DEVE ser commitado como referência!

**2. Obter Credenciais Reais**
- Acesse https://dashboard.embrapa.io
- Obtenha o SENTRY_DSN específico do projeto
- Atualize no .env.io local

**3. Entender Ambientes**
- .env.io é APENAS para desenvolvimento local
- Em alpha/beta/release a plataforma injeta automaticamente
- Valores locais simulam comportamento da plataforma

**4. Próximo Workflow Sugerido**
Execute `generate-docker-compose` para criar o docker-compose.yaml
```

### 4. Oferecer Ajuda Adicional

Ask:
```
💡 **Precisa de ajuda adicional?**

[G] Configurar .gitignore automaticamente
[L] Configurar Linter para minha stack
[N] Não, finalizar workflow
```

**Handle responses:**
- G: Update .gitignore with .env, .env.io, .env.sh entries and AI agent directories
- L: Suggest Linter configuration based on detected stack
- N: Complete workflow

### 5. Finalização do Workflow

Display:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 **Workflow generate-env-io concluído!**

📄 **Arquivos criados:**
- {project-root}/.env.io ✅
- {project-root}/.env.io.example ✅

📚 **Documentação:**
- Regras completas: ./knowledge/embrapa-io-validation.md
- Fundamentos: ./knowledge/embrapa-io-fundamentals.md

🙏 Obrigado por usar o módulo Embrapa I/O!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## WORKFLOW COMPLETION

This is the **FINAL STEP** of the generate-env-io workflow.

Upon successful completion:
1. .env.io and .env.io.example are saved
2. User understands critical platform rules
3. User knows next steps
4. Workflow ends gracefully

**No further step files to load.**
