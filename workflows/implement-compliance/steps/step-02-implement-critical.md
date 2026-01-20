---
name: 'step-02-implement-critical'
description: 'Implementar action items CRITICAL'
nextStepFile: './step-03-implement-high.md'
---

# Step 2: Implementar Action Items CRITICAL

## STEP GOAL:

Executar todos os action items de severidade CRITICAL do relatório de conformidade.

## MANDATORY EXECUTION RULES:

- 🛑 MUST implement ALL critical items before proceeding
- 📖 FOLLOW exact code examples from the report
- 📋 VALIDATE syntax after each modification
- 🔧 HALT on any error and ask user for guidance

## Sequence of Instructions

### 1. Listar Action Items CRITICAL

Apresentar todos os items CRITICAL do relatório:

```markdown
## 🚨 Action Items CRITICAL ({n} items)

{Para cada item}:
### AI-{number}: {título}
- **Localização:** {file_path}
- **Ação:** {descrição}
```

### 2. Implementar Cada Item Sequencialmente

Para cada action item CRITICAL:

#### 2.1 Anunciar Implementação
```
🔧 Implementando AI-{number}: {título}
   Arquivo: {file_path}
```

#### 2.2 Executar Modificação

Seguir EXATAMENTE o código especificado no action item.

**Exemplos comuns de items CRITICAL:**

**Remover campo version do docker-compose.yaml:**
```yaml
# ANTES
version: '3.8'
services:
  ...

# DEPOIS
services:
  ...
```

**Adicionar network stack externa:**
```yaml
# Adicionar ao final do docker-compose.yaml
networks:
  stack:
    external: true
    name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}
```

**Conectar serviços à network stack:**
```yaml
# Para cada serviço, adicionar
services:
  app:
    ...
    networks:
      - stack
```

**Criar .env.io.example:**
```ini
COMPOSE_PROJECT_NAME={io_project}_{io_app}_development
COMPOSE_PROFILES=development
IO_SERVER=localhost
IO_PROJECT={io_project}
IO_APP={io_app}
IO_STAGE=development
IO_VERSION=0.{YY}.{M}-dev.1
IO_DEPLOYER=first.surname@embrapa.br
SENTRY_DSN=GET_IN_DASHBOARD
MATOMO_ID={matomo_id}
MATOMO_TOKEN=
```

**Criar .embrapa/settings.json:**
```json
{
  "boilerplate": "_",
  "platform": "{platform}",
  "label": "{label}",
  "description": "{description}",
  "references": [],
  "maintainers": [
    {
      "name": "{name}",
      "email": "{email}",
      "phone": "+55 (XX) X XXXX-XXXX"
    }
  ],
  "variables": {
    "default": [],
    "alpha": [],
    "beta": [],
    "release": []
  },
  "orchestrators": ["DockerCompose"]
}
```

#### 2.3 Validar Modificação

Após cada modificação:
- Verificar sintaxe YAML (docker-compose)
- Verificar sintaxe JSON (settings.json)
- Verificar formato INI (.env files)

#### 2.4 Confirmar Conclusão

```
✅ AI-{number} implementado com sucesso
```

### 3. Tratamento de Erros

Se qualquer implementação falhar:

```markdown
❌ Erro ao implementar AI-{number}

**Problema:** {descrição_do_erro}
**Arquivo:** {file_path}

### Opções:
[R] Retry - Tentar novamente
[S] Skip - Pular este item e continuar
[M] Manual - Marcar para implementação manual
[X] Abort - Cancelar workflow
```

### 4. Resumo de Implementações CRITICAL

```markdown
## ✅ Implementações CRITICAL Concluídas

| # | Action Item | Status |
|---|-------------|--------|
| AI-1 | {título} | ✅ Implementado |
| AI-2 | {título} | ✅ Implementado |
| ... | ... | ... |

**Total:** {n}/{total} items CRITICAL implementados
```

### 5. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue to HIGH Items [V] View Changes [X] Abort"

#### Menu Handling Logic:

- IF C: Store progress, then load, read entire file, then execute {nextStepFile}
- IF V: Show diff of all modified files, then return to menu
- IF X: End workflow (changes already made will persist)

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected will you proceed to implement HIGH priority items.
