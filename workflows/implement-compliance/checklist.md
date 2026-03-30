---
last-redoc-date: 2026-01-20
---

# Checklist de Validação - Implement Compliance Workflow

## Validação Pré-Execução

- [ ] Relatório de conformidade existe em `{output_folder}/embrapa-io-compliance.md`
- [ ] Relatório foi gerado pelo workflow Verify Compliance
- [ ] Action items estão presentes no relatório
- [ ] Stack tecnológica identificada no relatório

## Validação Durante Execução

### Step 1: Validar Relatório

- [ ] Relatório encontrado e lido
- [ ] Action items extraídos corretamente
- [ ] Priorização por severidade (CRITICAL > HIGH > MEDIUM)
- [ ] Stack tecnológica confirmada

### Step 2: Implementar Itens Críticos

- [ ] Todos os itens CRITICAL listados
- [ ] docker-compose.yaml ajustado (4 Verdades Fundamentais)
- [ ] Campo `version` removido (se presente)
- [ ] Network `stack` configurada como externa
- [ ] Volumes externos declarados
- [ ] `container_name` removido de todos os serviços
- [ ] Cada implementação documentada

### Step 3: Implementar Itens HIGH/MEDIUM

- [ ] Itens HIGH implementados
- [ ] Itens MEDIUM implementados
- [ ] Healthchecks configurados (endpoints existentes)
- [ ] Serviços CLI com `profiles: ['cli']`
- [ ] Serviços CLI com `restart: "no"`
- [ ] Integrações Sentry/Matomo (se aplicável)

### Step 4: Criar Arquivos de Ambiente

- [ ] `.env.io.example` criado com variáveis obrigatórias
- [ ] `.env.io` criado com valores preenchidos
- [ ] `.env.example` criado (se não existe)
- [ ] `.env` criado a partir do exemplo
- [ ] `IO_VERSION` no formato correto (`0.YY.M-dev.1`)
- [ ] `COMPOSE_PROJECT_NAME` calculado corretamente
- [ ] `.gitignore` atualizado (`.env` e `.env.io` listados)
- [ ] `bootstrap.sh` criado e executável

### Step 5: Finalização

- [ ] Relatório de conformidade atualizado
- [ ] Todos os action items marcados como implementados
- [ ] Status de implementação documentado
- [ ] README.md atualizado com seção Embrapa I/O (se necessário)

## Validação de Outputs

### Arquivos Criados/Modificados

- [ ] `docker-compose.yaml` - Conforme com 4 Verdades
- [ ] `.env.io.example` - Template com variáveis obrigatórias
- [ ] `.env.io` - Valores preenchidos para desenvolvimento
- [ ] `.env.example` - Template de variáveis da aplicação
- [ ] `.env` - Valores preenchidos
- [ ] `.gitignore` - Arquivos sensíveis ignorados
- [ ] `bootstrap.sh` - Script de inicialização

### Relatório Atualizado

- [ ] `{output_folder}/embrapa-io-compliance.md` atualizado
- [ ] Status de cada action item registrado
- [ ] Data de implementação registrada
- [ ] Próximos passos indicados (Code Review)

## Critérios de Sucesso

O workflow é considerado bem-sucedido quando:

1. ✅ Todos os action items CRITICAL implementados
2. ✅ Todos os action items HIGH implementados
3. ✅ Arquivos de ambiente criados corretamente
4. ✅ bootstrap.sh funcional
5. ✅ Relatório de conformidade atualizado
6. ✅ Comunicação em {communication_language}

## Notas Importantes

- Este workflow NÃO deve modificar código funcional da aplicação
- Healthchecks devem usar endpoints já existentes
- Valores sensíveis em `.env` devem ser gerados automaticamente
- O projeto deve ser validado via Code Review após implementação

---

**Versão:** 1.26.3
**Compatível com:** BMAD Core v6
**Última atualização:** 2026-03-30
