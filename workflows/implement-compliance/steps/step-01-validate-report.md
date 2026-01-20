---
name: 'step-01-validate-report'
description: 'Validar presença e conteúdo do relatório de conformidade'
nextStepFile: './step-02-implement-critical.md'
---

# Step 1: Validar Relatório de Conformidade

## STEP GOAL:

Verificar se o relatório de conformidade existe e está válido antes de iniciar a implementação.

## MANDATORY EXECUTION RULES:

- 🛑 CANNOT proceed without valid compliance report
- 📖 MUST parse all action items from report
- 📋 MUST present summary to user before implementation

## Sequence of Instructions

### 1. Verificar Presença do Relatório

Verificar se `{project-root}/docs/embrapa-io-compliance.md` existe.

**Se não existir:**
```
❌ Relatório de conformidade não encontrado!

O arquivo `docs/embrapa-io-compliance.md` é necessário para este workflow.

🎯 **Ação requerida:** Execute primeiro o workflow [VC] Verificar Conformidade
   para gerar o relatório de compliance.

Retornando ao menu principal...
```
→ Retornar ao menu do agente

### 2. Carregar e Parsear o Relatório

Ler o arquivo e extrair:
- Compliance Score atual
- Lista de action items CRITICAL
- Lista de action items HIGH
- Lista de action items MEDIUM
- Lista de action items LOW
- Stack tecnológica detectada

Store as `{report_data}`.

### 3. Verificar se há Action Items

**Se não houver action items:**
```
✅ Projeto já está em conformidade!

O relatório indica que não há action items pendentes.
O projeto está com 100% de conformidade com a plataforma Embrapa I/O.

🎯 **Próximo passo:** Execute o workflow [CR] Code Review para validação final.
```
→ Retornar ao menu do agente

### 4. Apresentar Resumo para Confirmação

```markdown
## 📋 Resumo do Relatório de Conformidade

**Compliance Score Atual:** {score} {emoji}
**Stack Detectada:** {detected_stack}

### Action Items a Implementar

| Prioridade | Quantidade | Status |
|------------|------------|--------|
| 🚨 CRITICAL | {n} | Pendente |
| ⚠️ HIGH | {n} | Pendente |
| ℹ️ MEDIUM | {n} | Pendente |
| 💡 LOW | {n} | Pendente |
| **TOTAL** | **{n}** | **Pendente** |

---

### ⚠️ Aviso Importante

Este workflow irá modificar os seguintes tipos de arquivos:
- docker-compose.yaml
- .env.example / .env.io.example
- .embrapa/settings.json
- LICENSE
- Configurações de Sentry/Matomo (se aplicável)

**Arquivos de código-fonte da aplicação NÃO serão modificados**
(exceto pontos de integração Sentry/Matomo quando necessário).

---

Deseja prosseguir com a implementação?
```

### 5. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue with Implementation [R] Review Report First [X] Cancel"

#### Menu Handling Logic:

- IF C: Store report_data, then load, read entire file, then execute {nextStepFile}
- IF R: Display the full compliance report content, then return to this menu
- IF X: End workflow, return to agent menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input
- ONLY proceed when user explicitly confirms with 'C'

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected will you then load and read fully `{nextStepFile}` to begin implementing CRITICAL items.
