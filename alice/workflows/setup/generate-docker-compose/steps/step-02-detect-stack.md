---
name: 'step-02-detect-stack'
description: 'Detectar automaticamente a stack tecnológica do projeto e confirmar com usuário'

# File References
nextStepFile: './step-03-collect-config.md'
---

# Step 2: Detecção de Stack Tecnológica

## STEP GOAL:

Analisar a estrutura do projeto para identificar automaticamente a stack tecnológica (Node.js, Vue, React, PHP, .NET, etc.) e confirmar a detecção com o usuário.

## Rules

Follow `./references/step-file-protocol.md`. Step-specific:
- Detectar stack tecnológica e banco de dados -- não gerar docker-compose.yaml neste step
- PROIBIDO assumir stack sem confirmação do usuário
- Escanear arquivos indicadores e apresentar resultado para confirmação

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Analisar Estrutura do Projeto

Scan for indicator files:

**Arquivos a procurar:**
- `package.json` → Possível Node.js, Vue, React, React Native
- `requirements.txt` / `pyproject.toml` → Python
- `composer.json` → PHP
- `*.csproj` → .NET
- `pom.xml` / `build.gradle` → Java
- `go.mod` → Go

### 2. Identificar Framework Específico

**Se package.json encontrado, analisar dependencies:**

- `"express"` ou `"fastify"` ou `"nest"` → Node.js API
- `"vue"` → Vue.js Frontend
- `"react"` e `"react-dom"` (sem react-native) → React Frontend
- `"react-native"` → React Native Mobile
- `"next"` → Next.js (SSR)
- `"nuxt"` → Nuxt.js (SSR)

**Se composer.json encontrado:**

- `"laravel/framework"` → PHP Laravel
- `"symfony/framework-bundle"` → PHP Symfony

**Se *.csproj encontrado:**

- Blazor references → .NET Blazor
- ASP.NET Core → .NET API

### 3. Identificar Banco de Dados

Scan for database indicators:

- MongoDB connection strings or `mongoose` dependency
- PostgreSQL/pg dependencies
- MySQL dependencies
- SQL Server dependencies
- Redis dependencies

### 4. Apresentar Detecção

Display to {user_name}:
```
🔍 **Análise de Stack Concluída**

📦 **Stack detectada:** {detected_stack}
   Indicadores encontrados: {indicators_list}

💾 **Banco de dados detectado:** {detected_database}
   Indicadores encontrados: {db_indicators}

Esta detecção está correta?
```

### 5. Confirmar ou Selecionar Stack

Ask {user_name}:
```
A detecção automática está correta? Caso contrário, selecione a stack:

[1] Node.js API (Express/Fastify + MongoDB/PostgreSQL)
[2] Vue.js Frontend (Vuetify/Quasar)
[3] React Frontend
[4] React Native Mobile
[5] Next.js (SSR)
[6] PHP Laravel
[7] .NET Blazor
[8] Python FastAPI/Django
[9] Outro (especificar)
[C] Confirmar detecção automática
```

Store response as `{selected_stack}`.

### 6. Confirmar Banco de Dados (se aplicável)

If stack requires database, ask:
```
Qual banco de dados será usado?

[1] MongoDB
[2] PostgreSQL
[3] MySQL
[4] SQL Server
[5] Nenhum
[C] Confirmar detecção automática ({detected_database})
```

Store response as `{selected_database}`.

### 7. Apresentar Resumo

Display:
```
✅ **Configuração de Stack Confirmada:**

📦 Stack: {selected_stack}
💾 Banco de dados: {selected_database}

🎯 **Próximo passo:** Coletar configurações específicas (portas, healthcheck, etc.)
```

### 8. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue to Configuration [X] Exit"

#### Menu Handling Logic:

- IF C: Store stack and database in context, then load, read entire file, then execute {nextStepFile}
- IF X: End workflow gracefully
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#8-present-menu-options)

