---
name: 'step-03-collect-config'
description: 'Coletar configurações específicas da aplicação: portas, healthcheck, serviços CLI'

# File References
nextStepFile: './step-04-generate-compose.md'
---

# Step 3: Coletar Configurações da Aplicação

## STEP GOAL:

Coletar todas as configurações específicas necessárias para gerar o docker-compose.yaml: portas, healthcheck endpoint, portas adicionais e serviços CLI opcionais.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator

### Role Reinforcement:

- ✅ You are a DevOps specialist collecting container configuration
- ✅ If you already have been given a name, communication_style and persona, continue to use those while playing this new role
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring Docker expertise, user brings application requirements

### Step-Specific Rules:

- 🎯 Focus only on collecting configuration values
- 🚫 FORBIDDEN to generate docker-compose.yaml in this step
- 💬 Approach: Interactive collection with validation
- 📋 Validate all inputs before storing

## EXECUTION PROTOCOLS:

- 🎯 Collect port configuration with validation
- 💾 Store all config values for next step
- 📖 Explain each configuration option clearly
- 🚫 FORBIDDEN to proceed with invalid port numbers

## CONTEXT BOUNDARIES:

- Available context: IO_* variables, selected_stack, selected_database from previous steps
- Focus: Configuration collection only
- Limits: Do not generate any files yet
- Dependencies: Stack and database confirmed in step 2

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Coletar Porta Principal

Ask {user_name}:
```
🔌 **Configuração de Porta Principal**

Qual porta a aplicação principal irá usar internamente?
(Esta é a porta DENTRO do container, ex: 3000, 8080, 5000)

Sugestões por stack:
- Node.js API: 3000
- Vue/React Frontend: 80 (nginx)
- PHP Laravel: 80
- .NET: 5000

Porta:
```

**Validate:**
- Must be number between 1 and 65535
- Warn if < 1024 (requires root)

Store as `{app_port}`.

### 2. Coletar Portas Adicionais (Opcional)

Ask {user_name}:
```
🔌 **Portas Adicionais (Opcional)**

A aplicação expõe outras portas além da principal?

Exemplos comuns:
- MQTT Broker: 1883
- WebSocket: 3001
- Metrics/Prometheus: 9090
- Debug: 9229

Se sim, liste no formato: NOME:PORTA,NOME:PORTA
(ex: MQTT:1883,METRICS:9090)

Se não, deixe vazio e pressione Enter.
```

**Parse response:**
- Split by comma
- Extract name and port from each
- Validate port numbers
- Store as array `{additional_ports}`

### 3. Coletar Healthcheck Endpoint

Ask {user_name}:
```
❤️ **Configuração de Healthcheck**

Qual endpoint de healthcheck a aplicação possui?

Sugestões:
- /health (mais comum)
- /api/health
- /status
- /ping

Se não possui, usaremos /health como padrão.

Endpoint:
```

Store as `{health_endpoint}` (default: `/health`).

### 4. Serviços CLI (Opcional)

Ask {user_name}:
```
🛠️ **Serviços CLI (Opcional)**

Deseja adicionar serviços CLI para operações manuais?

Estes serviços usam Docker Compose profiles e são executados sob demanda:
- **backup**: Fazer backup de dados
- **restore**: Restaurar backup
- **sanitize**: Otimizar/limpar dados

[S] Sim, incluir todos os serviços CLI
[N] Não, apenas aplicação principal
[C] Customizar (escolher quais incluir)
```

**Handle response:**
- S: `{include_cli_services}` = all
- N: `{include_cli_services}` = none
- C: Ask which services to include

### 5. Apresentar Resumo de Configurações

Display:
```
✅ **Configurações Coletadas:**

📦 **Stack:** {selected_stack}
💾 **Banco de dados:** {selected_database}

🔌 **Portas:**
- Principal: {app_port}
- Adicionais: {additional_ports_list}

❤️ **Healthcheck:** {health_endpoint}

🛠️ **Serviços CLI:** {include_cli_services}

🎯 **Próximo passo:** Gerar docker-compose.yaml conforme Embrapa I/O
```

### 6. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue to Generate [B] Back to edit config [X] Exit"

#### Menu Handling Logic:

- IF C: Store all config values, then load, read entire file, then execute {nextStepFile}
- IF B: Return to section 1 to recollect configuration
- IF X: End workflow gracefully
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#6-present-menu-options)

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu items execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [all configuration values collected and validated], will you then load and read fully `{nextStepFile}` to execute and begin docker-compose.yaml generation.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Main port collected and validated
- Additional ports parsed correctly (if provided)
- Healthcheck endpoint confirmed
- CLI services preference recorded
- All values presented for user confirmation

### ❌ SYSTEM FAILURE:

- Accepting invalid port numbers
- Not validating port range
- Skipping healthcheck configuration
- Not presenting summary before proceeding
- Proceeding without user confirmation

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
