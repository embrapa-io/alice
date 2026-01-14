---
last-redoc-date: 2025-11-04
---

# Validate Workflows

Coleção de workflows para validação de conformidade com a plataforma Embrapa I/O.

Esta pasta contém workflows especializados em verificar se projetos atendem aos padrões e regras da plataforma Embrapa I/O, gerando relatórios detalhados sobre conformidade e problemas detectados.

## Workflows Disponíveis

### [validate-compliance](./validate-compliance/)
Workflow abrangente que executa validação completa de conformidade contra as 38 regras da plataforma Embrapa I/O. Carrega 6 arquivos de conhecimento (fundamentals, validation, workflows, deployment, stacks, integrations) e valida sistematicamente `docker-compose.yaml` (14 regras), arquivos `.env.io` (10 regras), `.embrapa/settings.json` (8 regras), e integrações de serviços (6 regras). Permite filtrar validações por severidade (CRITICAL, HIGH, MEDIUM, LOW, ALL) e oferece auto-fix opcional para problemas corrigíveis automaticamente. Gera dois relatórios: JSON estruturado e Markdown formatado, ambos timestampados.

## Uso Típico

Para validar um projeto existente:

```xml
<step n="1" goal="Validar conformidade com Embrapa I/O">
  <invoke-workflow>
    <path>{project-root}/_bmad/embrapa-io/workflows/validate/validate-compliance/workflow.yaml</path>
    <description>Executa validação completa e gera relatórios</description>
  </invoke-workflow>
</step>
```

O workflow detectará automaticamente o tipo de projeto (NEW, EXISTING, ALREADY_COMPLIANT) e executará validações apropriadas, fornecendo feedback detalhado e recomendações de correção priorizadas por severidade.

## Categorias de Validação

- **Docker Compose** (14 regras): Verdades Fundamentais, configuração de serviços, networks, volumes
- **Environment Variables** (10 regras): Formato, nomenclatura, valores obrigatórios
- **Settings JSON** (8 regras): Estrutura, metadados, variáveis por ambiente
- **Service Integrations** (6 regras): Sentry, Matomo, healthchecks, logging
