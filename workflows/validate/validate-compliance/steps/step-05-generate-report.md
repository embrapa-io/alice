---
name: 'step-05-generate-report'
description: 'Consolidar resultados, calcular score e gerar relatórios JSON e Markdown'

# Path Definitions
workflow_path: '{project-root}/.bmad/embrapa-io/workflows/validate/validate-compliance'

# File References
thisStepFile: '{workflow_path}/steps/step-05-generate-report.md'
workflowFile: '{workflow_path}/workflow.md'

# Output References
reportJson: '{output_folder}/validation-report-{project_name}-{date}.json'
reportMd: '{output_folder}/compliance-summary-{project_name}-{date}.md'

# Template References
reportTemplate: '{workflow_path}/templates/compliance-report.md'
---

# Step 5: Gerar Relatórios de Compliance

## STEP GOAL:

Consolidar todos os erros encontrados, calcular o score de compliance, gerar relatórios em JSON e Markdown, e apresentar recomendações priorizadas.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: This is the final step - ensure complete execution
- 📋 YOU ARE A FACILITATOR, completing the validation

### Role Reinforcement:

- ✅ You are a compliance auditor finalizing the report
- ✅ If you already have been given a name, communication_style and persona, continue to use those while playing this new role
- ✅ Provide actionable recommendations

### Step-Specific Rules:

- 🎯 Focus on consolidation and report generation
- 🚫 FORBIDDEN to skip any error category
- 💬 Approach: Consolidate, calculate, generate, present
- 📋 Prioritize recommendations by severity

## EXECUTION PROTOCOLS:

- 🎯 Consolidate all errors from previous steps
- 💾 Calculate compliance score
- 📖 Generate both JSON and Markdown reports
- 🚫 FORBIDDEN to complete without actionable recommendations

## CONTEXT BOUNDARIES:

- Available context: All errors from steps 2-4
- Focus: Report generation and recommendations
- Limits: This is the final step
- Dependencies: All validations completed

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Consolidar Todos os Erros

Combine all error arrays:
```
all_errors = docker_compose_errors
           + env_files_errors
           + no_fallback_errors
           + linter_errors
```

### 2. Calcular Contagens por Severidade

```
critical_count = count where severity == "CRITICAL"
high_count = count where severity == "HIGH"
medium_count = count where severity == "MEDIUM"
low_count = count where severity == "LOW"
total_errors = sum of all counts
```

### 3. Calcular Compliance Score

```
IF critical_count > 0 OR high_count > 3:
    compliance_score = "LOW" 🔴
ELIF high_count > 0 AND high_count <= 3:
    compliance_score = "MEDIUM" 🟡
ELSE:
    compliance_score = "HIGH" 🟢
```

### 4. Gerar Relatório JSON

```json
{
  "project": {
    "name": "{project_name}",
    "path": "{project_path}",
    "type": "{project_type}"
  },
  "validation": {
    "timestamp": "{date}",
    "score": "{compliance_score}",
    "summary": {
      "critical": {critical_count},
      "high": {high_count},
      "medium": {medium_count},
      "low": {low_count},
      "total": {total_errors}
    }
  },
  "results": {
    "docker_compose": {
      "status": "{docker_compose_status}",
      "errors": [...]
    },
    "env_files": {
      "status": "{env_files_status}",
      "errors": [...]
    },
    "no_fallback": {
      "status": "{no_fallback_status}",
      "errors": [...]
    },
    "linter": {
      "status": "{linter_status}",
      "errors": [...]
    }
  },
  "all_errors": [...]
}
```

Save to `{reportJson}`.

### 5. Gerar Relatório Markdown

```markdown
# Relatório de Compliance Embrapa I/O

## 📊 Resumo Executivo

**Projeto:** {project_name}
**Data:** {date}
**Score:** {compliance_score_emoji} {compliance_score}

### Estatísticas

| Severidade | Quantidade |
|------------|------------|
| 🔴 CRITICAL | {critical_count} |
| 🟠 HIGH | {high_count} |
| 🟡 MEDIUM | {medium_count} |
| 🔵 LOW | {low_count} |
| **Total** | **{total_errors}** |

## 📋 Detalhamento por Categoria

### Docker Compose
Status: {docker_compose_status}
{docker_compose_error_list}

### Arquivos .env
Status: {env_files_status}
{env_files_error_list}

### NO-FALLBACK
Status: {no_fallback_status}
{no_fallback_error_list}

### Linter
Status: {linter_status}
{linter_error_list}

## 🎯 Ações Recomendadas

### Prioridade 1 - CRITICAL
{critical_recommendations}

### Prioridade 2 - HIGH
{high_recommendations}

### Prioridade 3 - MEDIUM
{medium_recommendations}

### Prioridade 4 - LOW
{low_recommendations}

---
*Gerado pelo BMAD Embrapa I/O Module*
```

Save to `{reportMd}`.

### 6. Aplicar Auto-fix (se solicitado)

If `{auto_fix}` == true:
```
Filter errors where auto_fixable == true
For each fixable error:
  1. Create backup: {file}.bak
  2. Apply fix
  3. Validate result
  4. Log action
```

### 7. Apresentar Resultado Final

Display:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 **Validação de Compliance Embrapa I/O - Resultado Final**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📂 **Projeto:** {project_name}
📍 **Caminho:** {project_path}
📊 **Score:** {compliance_score_emoji} {compliance_score}

📈 **Resumo:**
- ❌ CRITICAL: {critical_count}
- ⚠️ HIGH: {high_count}
- ⚡ MEDIUM: {medium_count}
- ℹ️ LOW: {low_count}
- 📋 Total: {total_errors}

📝 **Relatórios gerados:**
- JSON: {reportJson}
- Markdown: {reportMd}

{if auto_fix applied}
🔧 **Correções automáticas:** {fixes_count} aplicadas
{endif}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 **Próximos passos:**

{if critical_count > 0}
🚨 URGENTE: Corrija {critical_count} erros CRITICAL imediatamente
{endif}

{if high_count > 0}
⚠️ ALTA PRIORIDADE: Corrija {high_count} erros HIGH antes do deploy
{endif}

{if total_errors == 0}
✅ PARABÉNS! Projeto 100% conforme com Embrapa I/O!
{endif}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🙏 Obrigado por usar o módulo Embrapa I/O!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All errors consolidated
- Compliance score calculated correctly
- Both reports generated and saved
- Recommendations prioritized by severity
- Workflow completed gracefully

### ❌ SYSTEM FAILURE:

- Missing error categories in consolidation
- Wrong score calculation
- Reports not saved
- No actionable recommendations
- Leaving user without clear next steps

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.

---

## WORKFLOW COMPLETION

This is the **FINAL STEP** of the validate-compliance workflow.

Upon successful completion:
1. All errors are consolidated
2. Compliance score is calculated
3. JSON and Markdown reports are saved
4. User has clear prioritized recommendations
5. Workflow ends gracefully

**No further step files to load.**
