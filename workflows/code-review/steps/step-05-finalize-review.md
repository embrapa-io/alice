---
name: 'step-05-finalize-review'
description: 'Consolidar resultados e atualizar relatório de conformidade'
---

# Step 5: Finalizar Code Review

## STEP GOAL:

Consolidar todos os resultados do code review, atualizar o relatório de conformidade com o status final, e marcar todos os action items como completos (se aprovados).

## MANDATORY EXECUTION RULES:

- 🛑 MUST calculate overall PASS/FAIL
- 📖 MUST update compliance report with review results
- 📋 MUST mark action items as complete if all passed

## Sequence of Instructions

### 1. Consolidar Resultados

**Agregar resultados de todas as verificações:**

```markdown
## 📊 Resumo do Code Review

| Categoria | Verificações | Passed | Failed | Resultado |
|-----------|--------------|--------|--------|-----------|
| Docker Compose | {n} | {n} | {n} | ✅/❌ |
| Arquivos .env | {n} | {n} | {n} | ✅/❌ |
| settings.json | {n} | {n} | {n} | ✅/❌ |
| Integrações | {n} | {n} | {n} | ✅/❌ |
| **TOTAL** | **{n}** | **{n}** | **{n}** | **✅/❌** |
```

### 2. Determinar Resultado Final

**Critérios:**
- **APPROVED ✅**: Todas as categorias passaram
- **REJECTED ❌**: Uma ou mais categorias falharam

### 3. Se APPROVED: Atualizar Relatório de Conformidade

Atualizar `{project-root}/docs/embrapa-io-compliance.md`:

**Adicionar no início do arquivo:**

```markdown
---

## ✅ Conformidade Verificada

**Data do Code Review:** {current_date}
**Resultado:** APROVADO ✅
**Revisado por:** Alice - Especialista em Conformidade Embrapa I/O

### Resumo da Verificação

| Categoria | Status |
|-----------|--------|
| Docker Compose | ✅ Conforme |
| Arquivos .env | ✅ Conforme |
| settings.json | ✅ Conforme |
| Integrações | ✅ Conforme |

### Action Items

Todos os action items foram implementados e verificados com sucesso.

| # | Action Item | Status |
|---|-------------|--------|
| AI-1 | {título} | ✅ Completo |
| AI-2 | {título} | ✅ Completo |
| ... | ... | ✅ Completo |

---

## 🎉 Projeto em Conformidade com Embrapa I/O

Este projeto atende a todos os requisitos de conformidade da plataforma Embrapa I/O:

✅ 4 Verdades Fundamentais implementadas
✅ Arquivos de configuração corretos
✅ Integrações configuradas
✅ Pronto para deployment na plataforma

---
```

### 4. Se REJECTED: Documentar Falhas

Atualizar `{project-root}/docs/embrapa-io-compliance.md`:

**Adicionar no início do arquivo:**

```markdown
---

## ❌ Code Review - Falhas Encontradas

**Data do Code Review:** {current_date}
**Resultado:** REJEITADO ❌
**Revisado por:** Alice - Especialista em Conformidade Embrapa I/O

### Falhas que Necessitam Correção

{lista_de_falhas_detalhada}

### Próximos Passos

1. Corrija as falhas listadas acima
2. Execute novamente o workflow [IA] Implementar Ajustes
3. Execute novamente o workflow [CR] Code Review

---
```

### 5. Apresentar Resultado Final

**Se APPROVED:**

```markdown
## 🎉 Code Review APROVADO!

### Resultado Final

O projeto está em **100% de conformidade** com a plataforma Embrapa I/O.

### Verificações Realizadas

- ✅ Docker Compose: 4 Verdades Fundamentais
- ✅ Arquivos .env: Estrutura e variáveis
- ✅ settings.json: Metadados do projeto
- ✅ Integrações: Sentry/Matomo (quando aplicável)
- ✅ Bootstrap: Script de inicialização

### Relatório Atualizado

O arquivo `docs/embrapa-io-compliance.md` foi atualizado com:
- Status de conformidade verificada
- Todos os action items marcados como completos
- Data e resultado do code review

---

## 🚀 Projeto Pronto para Deployment

O projeto pode agora ser deployado na plataforma Embrapa I/O.

### Comando de Inicialização

```bash
env $(cat .env.io) docker compose up --force-recreate --build --remove-orphans --wait
```

### Próximos Passos

1. Obtenha as credenciais no Dashboard: https://dashboard.embrapa.io
   - SENTRY_DSN
   - MATOMO_ID

2. Atualize os valores no `.env.io` com as credenciais reais

3. Faça o deploy seguindo a documentação da plataforma

---

Parabéns! 🎊
```

**Se REJECTED:**

```markdown
## ❌ Code Review REJEITADO

### Falhas Encontradas

{n} verificações falharam e precisam ser corrigidas.

### Detalhes das Falhas

{lista_detalhada_de_cada_falha}

### Ações Necessárias

1. **Corrija cada falha listada**
   Use as instruções detalhadas acima

2. **Execute novamente o workflow de Implementação [IA]**
   Se necessário, para aplicar correções

3. **Execute novamente este Code Review [CR]**
   Para verificar as correções

---

O relatório de conformidade foi atualizado com as falhas encontradas.
```

### 6. Present FINAL OPTIONS

Display: "**Select an Option:** [M] Return to Agent Menu [X] Exit Session"

#### Menu Handling Logic:

- IF M: Return to Alice's main menu
- IF X: End session

**Final message:**
```
Code Review finalizado!

📋 Relatório atualizado: docs/embrapa-io-compliance.md

{Se APPROVED:}
🎉 Parabéns! O projeto está em conformidade com a plataforma Embrapa I/O.

{Se REJECTED:}
⚠️ Corrija as falhas encontradas e execute o code review novamente.

Obrigada por usar o agente Alice! 👋
```

## WORKFLOW COMPLETION

O workflow de Code Review está completo. O relatório de conformidade foi atualizado com o resultado final da verificação.
