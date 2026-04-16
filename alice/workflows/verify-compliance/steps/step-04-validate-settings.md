---
name: 'step-04-validate-settings'
description: 'Validação do arquivo .embrapa/settings.json'
nextStepFile: './step-05-validate-integrations.md'
---

# Step 4: Validar .embrapa/settings.json

## STEP GOAL:

Validar o arquivo de metadados `.embrapa/settings.json` contra os requisitos da plataforma Embrapa I/O.

## PRE-COMPUTED VALIDATION

If `validate-compliance.py` JSON output is available, use `checks.settings` results directly — skip manual JSON parsing. Focus LLM effort on generating remediation examples.

**Reference checklist:** `{workflow_path}/../references/settings-validation-checklist.md`

## Rules

Follow `./references/step-file-protocol.md`. Step-specific:
- NEVER skip any validation rule
- Validate JSON syntax first (unless pre-computed)
- Check all mandatory fields

## Sequence of Instructions

### 1. Verificar Presença do Arquivo

**Caminho obrigatório:** `.embrapa/settings.json`

**Se ausente:**
- Severidade: CRITICAL
- Action Item: "Criar diretório `.embrapa/` e arquivo `settings.json` com estrutura base"

### 2. Validar Sintaxe JSON

Verificar se o arquivo é um JSON válido.

**Se JSON inválido:**
- Severidade: CRITICAL
- Action Item: "Corrigir sintaxe JSON do arquivo .embrapa/settings.json"

### 3. Validar Campos Obrigatórios

**Estrutura obrigatória:**

```json
{
  "boilerplate": "string",
  "platform": "string",
  "label": "string",
  "description": "string",
  "references": [],
  "maintainers": [],
  "variables": {
    "default": [],
    "alpha": [],
    "beta": [],
    "release": []
  },
  "orchestrators": ["DockerCompose"]
}
```

**Validações:**

#### 3.1 Campo `boilerplate`
- Deve ser string
- Use `"_"` para projetos greenfield (não baseados em boilerplate)

#### 3.2 Campo `platform`
**Valores válidos:**
```
android, apple, dart, dotnet, electron, elixir, flutter, go,
java, javascript, kotlin, native, node, php, python,
react-native, ruby, rust, unity, unreal
```

**Se valor inválido:**
- Severidade: HIGH
- Action Item: "Corrigir campo `platform` para um dos valores válidos: [lista]"

#### 3.3 Campo `label`
- String curta descritiva
- Sem espaços no início/fim

#### 3.4 Campo `description`
- Descrição detalhada da aplicação
- Mencionar stack tecnológica

#### 3.5 Campo `references`
```json
"references": [
  { "label": "Site oficial do NodeJS", "url": "https://nodejs.dev/" },
  { "label": "Documentação Express", "url": "https://expressjs.com/" }
]
```
- Cada referência deve ter `label` e `url`
- Array vazio é permitido mas não recomendado (MEDIUM)

#### 3.6 Campo `maintainers`
```json
"maintainers": [
  {
    "name": "Nome Completo",
    "email": "nome.sobrenome@embrapa.br",
    "phone": "+55 (67) 9 8111-8060"
  }
]
```
- Cada mantenedor deve ter `name`, `email`, `phone`
- Formato telefone: `+DDI (DDD) X XXXX-XXXX`
- Email no formato correto

**Se formato telefone incorreto:**
- Severidade: MEDIUM
- Action Item: "Corrigir formato do telefone para: +55 (XX) X XXXX-XXXX"

#### 3.7 Campo `variables`

```json
"variables": {
  "default": [
    { "name": "APP_PORT", "type": "PORT" },
    { "name": "DB_PASSWORD", "type": "PASSWORD" },
    { "name": "JWT_SECRET", "type": "SECRET" },
    { "name": "DB_VOLUME", "type": "VOLUME", "value": "db" }
  ],
  "alpha": [],
  "beta": [],
  "release": [
    { "name": "ENVIRONMENT", "type": "TEXT", "value": "production" }
  ]
}
```

**Tipos válidos:**
- `TEXT`: String sem espaços. Sem value = vazio
- `PASSWORD`: String sem espaços. Sem value = random 16 chars
- `SECRET`: String sem espaços. Sem value = random 256 chars
- `PORT`: Porta exposta publicamente
- `VOLUME`: Referência a volumes Docker
- `EMPTY`: Força string vazia como valor

**Validações:**
- [ ] `default` array existe e não está vazio
- [ ] `alpha`, `beta`, `release` arrays existem (podem estar vazios)
- [ ] Todos os tipos são válidos
- [ ] Valores não contêm espaços ou aspas

**Se tipo inválido:**
- Severidade: HIGH
- Action Item: "Corrigir tipo da variável `X` para um válido: TEXT, PASSWORD, SECRET, PORT, VOLUME, EMPTY"

#### 3.8 Campo `orchestrators`

**Valor obrigatório:** `["DockerCompose"]`

```json
"orchestrators": ["DockerCompose"]
```

**⚠️ IMPORTANTE:** Docker Swarm está FORA DO ESCOPO. Usar apenas `DockerCompose`.

### 4. Validar Consistência com .env.example

**Regra:** Variáveis em `variables.default` devem corresponder às do `.env.example`

- [ ] Todas as variáveis do `.env.example` estão em `variables.default`
- [ ] Tipos correspondem ao uso esperado

### 5. Compilar Resultados

```markdown
## ⚙️ Validação .embrapa/settings.json

### Status: {COMPLIANT | PARTIAL | NON-COMPLIANT}

### Campos Obrigatórios
| Campo | Status | Observação |
|-------|--------|------------|
| boilerplate | ✅/❌ | ... |
| platform | ✅/❌ | ... |
| label | ✅/❌ | ... |
| description | ✅/❌ | ... |
| references | ✅/❌ | ... |
| maintainers | ✅/❌ | ... |
| variables | ✅/❌ | ... |
| orchestrators | ✅/❌ | ... |

### Findings
| # | Severidade | Problema | Solução |
|---|------------|----------|---------|
| ... | ... | ... | ... |
```

Store as `{settings_findings}`.

### 6. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue to Integrations Validation [X] Exit workflow"

#### Menu Handling Logic:

- IF C: Store settings_findings, then load, read entire file, then execute {nextStepFile}
- IF X: End workflow gracefully

