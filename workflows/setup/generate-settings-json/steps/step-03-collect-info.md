---
name: 'step-03-collect-info'
description: 'Coletar informações do projeto e do mantenedor para settings.json'

# File References
nextStepFile: './step-04-generate-settings.md'
---

# Step 3: Coletar Informações do Projeto

## STEP GOAL:

Coletar informações do projeto (label, description) e do mantenedor (name, email, phone) para compor o settings.json.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator

### Role Reinforcement:

- ✅ You are a platform configuration specialist collecting project metadata
- ✅ If you already have been given a name, communication_style and persona, continue to use those while playing this new role
- ✅ We engage in collaborative dialogue, not command-response

### Step-Specific Rules:

- 🎯 Focus on collecting project and maintainer info
- 🚫 FORBIDDEN to generate settings.json in this step
- 💬 Approach: Interactive collection with validation
- 📋 Validate phone format strictly

## EXECUTION PROTOCOLS:

- 🎯 Collect label, description, maintainer info
- 💾 Validate phone format: +DDI (DDD) X XXXX-XXXX
- 📖 Present collected info for review
- 🚫 FORBIDDEN to accept invalid phone format

## CONTEXT BOUNDARIES:

- Available context: selected_platform, default_variables from step 1, sync_plan from step 2
- Focus: Project metadata collection only
- Limits: Do not define custom variables yet
- Dependencies: Platform confirmed in step 1

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Coletar Label da Aplicação

Ask {user_name}:
```
🏷️ **Label da Aplicação**

Qual o nome/label da aplicação?
(Este é o nome amigável que aparecerá na plataforma)

Exemplo: "API de Catálogo de Produtos"

Label:
```

Store as `{app_label}`.

### 2. Coletar Descrição

Ask {user_name}:
```
📝 **Descrição da Aplicação**

Forneça uma breve descrição da aplicação (1 linha):

Exemplo: "API REST para gerenciamento do catálogo de produtos agrícolas"

Descrição:
```

Store as `{app_description}`.

### 3. Coletar Informações do Mantenedor

Ask {user_name}:
```
👤 **Mantenedor Principal**

Qual o nome completo do mantenedor principal?

Nome:
```

Store as `{maintainer_name}`.

Ask:
```
📧 **Email do Mantenedor**

Qual o email do mantenedor?

Email:
```

Validate email format. Store as `{maintainer_email}`.

Ask:
```
📱 **Telefone do Mantenedor (opcional)**

Qual o telefone do mantenedor?

⚠️ **Formato obrigatório:** +DDI (DDD) X XXXX-XXXX
Exemplo: +55 (67) 9 8111-8060

(Pressione Enter para pular)

Telefone:
```

**Se telefone fornecido, validar:**
- Regex: `^\+\d{1,3} \(\d{2}\) \d \d{4}-\d{4}$`

**Se formato inválido:**
```
❌ Formato inválido!

O telefone deve seguir exatamente o formato:
+DDI (DDD) X XXXX-XXXX

Exemplo correto: +55 (67) 9 8111-8060

Onde:
- DDI: Código do país (55 para Brasil)
- DDD: Código de área entre parênteses
- X: Dígito do celular (geralmente 9)
- XXXX-XXXX: Número com hífen

Por favor, tente novamente:
```

Store as `{maintainer_phone}` (empty string if skipped).

### 4. Perguntar sobre Variáveis Customizadas

Ask:
```
🔧 **Variáveis Personalizadas**

Deseja adicionar variáveis de ambiente além das padrão da plataforma?

As variáveis padrão já incluem:
{default_variables_list}

[S] Sim, adicionar variáveis personalizadas
[N] Não, usar apenas as padrão
```

**Se S:**
Loop to collect custom variables:
```
📝 **Nova Variável**

Nome da variável (UPPER_SNAKE_CASE):
```

```
Tipo da variável:
[1] TEXT - Valor textual (requer value)
[2] PORT - Porta (value omitido)
[3] SECRET - Segredo (value omitido)
[4] PASSWORD - Senha (value omitido)
[5] VOLUME - Volume Docker (requer sufixo)
[6] EMPTY - Valor vazio (value omitido)
```

**Se TEXT:** Ask for default value
**Se VOLUME:** Ask for suffix only (not full name)

Ask: "Adicionar mais variáveis? [S/N]"

Store custom variables as `{custom_variables}`.

### 5. Apresentar Resumo

Display:
```
✅ **Informações Coletadas:**

🏷️ **Aplicação:**
- Label: {app_label}
- Description: {app_description}
- Platform: {selected_platform}

👤 **Mantenedor:**
- Nome: {maintainer_name}
- Email: {maintainer_email}
- Telefone: {maintainer_phone}

📝 **Variáveis:**
- Padrão: {default_count} variáveis
- Personalizadas: {custom_count} variáveis

🎯 **Próximo passo:** Gerar settings.json
```

### 6. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue to Generate [E] Edit values [X] Exit"

#### Menu Handling Logic:

- IF C: Store all values, then load, read entire file, then execute {nextStepFile}
- IF E: Return to section 1 to recollect
- IF X: End workflow gracefully
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#6-present-menu-options)

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [all info collected and validated], will you then load and read fully `{nextStepFile}` to execute and generate settings.json.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Label and description collected
- Maintainer info complete
- Phone format validated (if provided)
- Custom variables collected (if requested)
- All info presented for review

### ❌ SYSTEM FAILURE:

- Accepting invalid phone format
- Not validating variable types
- Skipping maintainer collection
- Proceeding without user confirmation

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
