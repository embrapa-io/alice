---
name: 'step-04-validate-code'
description: 'Validar código contra regra NO-FALLBACK e verificar presença de Linter'

# Path Definitions
workflow_path: '{project-root}/.bmad/embrapa-io/workflows/validate/validate-compliance'

# File References
thisStepFile: '{workflow_path}/steps/step-04-validate-code.md'
nextStepFile: '{workflow_path}/steps/step-05-generate-report.md'
workflowFile: '{workflow_path}/workflow.md'
---

# Step 4: Validar Código (NO-FALLBACK e Linter)

## STEP GOAL:

Escanear o código do projeto em busca de padrões de fallback proibidos (IDs 5.1-5.4) e verificar se Linter está configurado (IDs 6.1-6.2).

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, executing validation

### Role Reinforcement:

- ✅ You are a compliance auditor validating code patterns
- ✅ If you already have been given a name, communication_style and persona, continue to use those while playing this new role
- ✅ Document every NO-FALLBACK violation found

### Step-Specific Rules:

- 🎯 Focus on code scanning for forbidden patterns
- 🚫 FORBIDDEN to miss fallback patterns
- 💬 Approach: Systematic code scanning
- 📋 NO-FALLBACK violations are CRITICAL severity

## EXECUTION PROTOCOLS:

- 🎯 Scan code files for fallback patterns
- 💾 Check for Linter configuration
- 📖 Document all violations
- 🚫 FORBIDDEN to skip any file type

## CONTEXT BOUNDARIES:

- Available context: All errors from steps 2-3, project_path
- Focus: Code validation only
- Limits: Do not generate report yet
- Dependencies: Previous validations completed

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Validação NO-FALLBACK (IDs 5.1-5.4)

**🚨 REGRA CRÍTICA - Esta é uma das mais importantes da plataforma**

**ID 5.1 - JavaScript/TypeScript fallbacks**
```
Files: *.js, *.ts, *.jsx, *.tsx
Patterns to find:
  - process.env.VAR || default
  - process.env.VAR ?? default
Regex: process\.env\.\w+\s*(\|\|||\?\?)
Severity: CRITICAL
```

**ID 5.2 - Python fallbacks**
```
Files: *.py
Patterns to find:
  - os.environ.get('VAR', default)
  - os.getenv('VAR', default)
Regex: os\.(environ\.get|getenv)\(['"]\w+['"],\s*.+\)
Severity: CRITICAL
```

**ID 5.3 - Shell/Bash fallbacks**
```
Files: *.sh, *.bash, Dockerfile
Patterns to find:
  - ${VAR:-default}
Regex: \$\{\w+:-[^}]+\}
Severity: CRITICAL
```

**ID 5.4 - Docker Compose fallbacks**
```
File: docker-compose.yaml
Patterns to find:
  - ${VAR:-default} in environment or ports
Regex: \$\{\w+:-[^}]+\}
Severity: CRITICAL
```

**Para cada ocorrência encontrada:**
```json
{
  "id": "5.X",
  "severity": "CRITICAL",
  "category": "no-fallback",
  "message": "Fallback proibido detectado: {pattern}",
  "location": "{file}:{line}",
  "pattern_found": "{código encontrado}",
  "solution": "Remover fallback: usar apenas process.env.VAR",
  "auto_fixable": false,
  "explanation": "Plataforma sempre injeta variáveis. Fallback mascara erros."
}
```

Store in `{no_fallback_errors}`.

### 2. Validação de Linter (IDs 6.1-6.2)

**Detectar linguagem:**
- package.json → JavaScript/TypeScript
- composer.json → PHP
- requirements.txt/pyproject.toml → Python
- go.mod → Go
- Gemfile → Ruby
- *.csproj → .NET
- Cargo.toml → Rust

**ID 6.1 - Linter instalado**

**JavaScript/TypeScript:**
```
Check: eslint em devDependencies
Severity: MEDIUM
Solution: npm install --save-dev eslint eslint-config-standard
```

**PHP:**
```
Check: squizlabs/php_codesniffer ou phpstan
Severity: MEDIUM
Solution: composer require --dev squizlabs/php_codesniffer
```

**Python:**
```
Check: ruff, flake8, pylint ou black
Severity: MEDIUM
Solution: pip install ruff
```

**Go:**
```
Check: .golangci.yml ou golangci-lint em Makefile
Severity: LOW (gofmt é built-in)
```

**Rust:**
```
Clippy é built-in - marcar como conforme
```

**ID 6.2 - Scripts lint definidos**

**JavaScript/TypeScript:**
```
Check: package.json tem "lint" e "lint:fix" em scripts
Severity: LOW
```

**PHP:**
```
Check: composer.json tem scripts lint
Severity: LOW
```

Store in `{linter_errors}`.

### 3. Apresentar Resultados

Display:
```
📋 **Validação de Código - Resultados**

**🚨 NO-FALLBACK (Regra Crítica):**
{if no_fallback_errors is empty}
✅ Nenhum fallback proibido detectado
{else}
❌ {count} fallbacks proibidos encontrados!

{for each error}
📍 {file}:{line}
   Padrão: {pattern_found}
   Correção: {solution}
{end for}
{endif}

**🔍 Linter:**
Linguagem detectada: {detected_language}
{if linter configured}
✅ Linter configurado: {linter_name}
{else}
⚠️ Linter não configurado
   Sugestão: {installation_command}
{endif}

📊 Status NO-FALLBACK: {no_fallback_status}
📊 Status Linter: {linter_status}
```

### 4. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue to Report [D] Details [X] Exit"

#### Menu Handling Logic:

- IF C: Store all errors, then load, read entire file, then execute {nextStepFile}
- IF D: Show detailed list of all violations
- IF X: End workflow gracefully

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected, will you then load and read fully `{workflow_path}/steps/step-05-generate-report.md` to execute and generate final compliance report.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All code files scanned for fallback patterns
- NO-FALLBACK violations documented as CRITICAL
- Linter configuration checked
- All patterns correctly identified

### ❌ SYSTEM FAILURE:

- Missing fallback patterns in scan
- Not marking NO-FALLBACK as CRITICAL
- Skipping file types
- Not detecting language correctly

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
