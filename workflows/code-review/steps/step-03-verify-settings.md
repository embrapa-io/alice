---
name: 'step-03-verify-settings'
description: 'Verificar implementação do .embrapa/settings.json'
nextStepFile: './step-04-verify-integrations.md'
---

# Step 3: Verificar .embrapa/settings.json

## STEP GOAL:

Verificar se o arquivo de metadados está corretamente implementado conforme o relatório de conformidade.

## MANDATORY EXECUTION RULES:

- 🛑 PASS/FAIL each verification clearly
- 📖 Validate JSON syntax
- 📋 Check all required fields

## Sequence of Instructions

### 1. Verificar Presença e Sintaxe

**Verificações:**
- [ ] Arquivo `.embrapa/settings.json` existe
- [ ] Arquivo contém JSON válido

**Resultado:** PASS ✅ / FAIL ❌

### 2. Verificar Campos Obrigatórios

**Campos que devem existir:**
- [ ] `boilerplate` (string)
- [ ] `platform` (string válida)
- [ ] `label` (string não vazia)
- [ ] `description` (string não vazia)
- [ ] `references` (array)
- [ ] `maintainers` (array não vazio)
- [ ] `variables` (objeto)
- [ ] `orchestrators` (array)

**Resultado:** PASS ✅ / FAIL ❌

### 3. Verificar Campo platform

**Valores válidos:**
```
android, apple, dart, dotnet, electron, elixir, flutter, go,
java, javascript, kotlin, native, node, php, python,
react-native, ruby, rust, unity, unreal
```

- [ ] Valor é um dos válidos

**Resultado:** PASS ✅ / FAIL ❌

### 4. Verificar maintainers

**Para cada maintainer:**
- [ ] Campo `name` presente
- [ ] Campo `email` presente
- [ ] Campo `phone` presente (formato: `+DDI (DDD) X XXXX-XXXX`)

**Resultado:** PASS ✅ / FAIL ❌

### 5. Verificar variables

**Estrutura obrigatória:**
- [ ] `variables.default` existe (array)
- [ ] `variables.alpha` existe (array)
- [ ] `variables.beta` existe (array)
- [ ] `variables.release` existe (array)

**Para cada variável em default:**
- [ ] Campo `name` presente
- [ ] Campo `type` é válido (TEXT, PASSWORD, SECRET, PORT, VOLUME, EMPTY)
- [ ] Se tem `value`, não contém espaços ou aspas

**Resultado:** PASS ✅ / FAIL ❌

### 6. Verificar orchestrators

**Verificação:**
- [ ] `orchestrators` contém `"DockerCompose"`
- [ ] NÃO contém `"DockerSwarm"` (fora do escopo)

```json
// ✅ CORRETO
"orchestrators": ["DockerCompose"]

// ❌ INCORRETO
"orchestrators": ["DockerCompose", "DockerSwarm"]
```

**Resultado:** PASS ✅ / FAIL ❌

### 7. Compilar Resultado da Verificação Settings

```markdown
## ⚙️ Verificação .embrapa/settings.json

### Estrutura

| Verificação | Status |
|-------------|--------|
| Arquivo existe | ✅/❌ |
| JSON válido | ✅/❌ |

### Campos Obrigatórios

| Campo | Status | Valor |
|-------|--------|-------|
| boilerplate | ✅/❌ | {valor} |
| platform | ✅/❌ | {valor} |
| label | ✅/❌ | {valor} |
| description | ✅/❌ | {resumo} |
| references | ✅/❌ | {count} items |
| maintainers | ✅/❌ | {count} pessoas |
| variables | ✅/❌ | {count} variáveis |
| orchestrators | ✅/❌ | {valor} |

### Variables

| Stage | Count | Status |
|-------|-------|--------|
| default | {n} | ✅/❌ |
| alpha | {n} | ✅/❌ |
| beta | {n} | ✅/❌ |
| release | {n} | ✅/❌ |

### Resultado Settings: {PASS/FAIL}
```

Store as `{settings_review}`.

### 8. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue to Integrations Verification [F] Show Failures Only [X] Abort Review"

#### Menu Handling Logic:

- IF C: Store settings_review, then load, read entire file, then execute {nextStepFile}
- IF F: Display only failed verifications, then return to menu
- IF X: End review with partial results

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected will you proceed to verify integrations.
