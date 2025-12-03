---
last-redoc-date: 2025-12-03
---

# Validate Compliance Workflow

Workflow interativo de validação completa que verifica conformidade de projetos com as 47 regras da plataforma Embrapa I/O (incluindo NO-FALLBACK, Volumes via .env, Portas via .env, e Linter obrigatório), gerando relatórios detalhados em JSON e Markdown.

Este é o workflow mais abrangente do módulo, carregando seis arquivos de conhecimento antes de iniciar validações: `embrapa-io-fundamentals.md` (4 Verdades Fundamentais), `embrapa-io-validation.md` (46 regras organizadas), `embrapa-io-workflows.md`, `embrapa-io-deployment.md`, `embrapa-io-stacks.md`, e `embrapa-io-integrations.md`. Executa validações sistemáticas em `docker-compose.yaml` (17 regras incluindo volumes e portas via .env), arquivos `.env.io` e `.env.io.example` (10 regras incluindo variáveis de volume), `.embrapa/settings.json` (8 regras), integrações de serviços (6 regras), validação NO-FALLBACK no codebase (4 regras CRÍTICAS), e validação de Linter configurado (2 regras de qualidade). Total: 47 regras de validação.

O diferencial está na capacidade de filtrar validações por nível de severidade (CRITICAL, HIGH, MEDIUM, LOW ou ALL), detecção automática de tipo de projeto (NEW, EXISTING, ALREADY_COMPLIANT), e opção de aplicar correções automáticas quando possível. Para projetos novos sem Docker Compose, o workflow encerra com sugestões de workflows `generate-*` apropriados. Gera dois relatórios: JSON estruturado para processamento programático e Markdown formatado para leitura humana, ambos com timestamp e nome do projeto.

Categoriza problemas por severidade, fornece recomendações corretivas específicas, e pode reexecutar validações após correções para verificar melhorias. Suporta análise de múltiplos arquivos simultaneamente, mantendo contexto entre validações relacionadas.

## Usage

```xml
<invoke-workflow>
  <path>{project-root}/.bmad/embrapa-io/workflows/validate/validate-compliance/workflow.yaml</path>
  <description>Validação completa de conformidade Embrapa I/O</description>
</invoke-workflow>
```

Este é um workflow **INTERATIVO** com opções de configuração.

## Inputs

- **Project Path**: Caminho absoluto do projeto a validar (validado: deve existir e ser acessível)
- **Severity Levels**: CRITICAL, HIGH, MEDIUM, LOW, ou ALL (filtra quais validações executar)
- **Auto-fix**: Boolean - aplicar correções automáticas quando disponíveis

## Outputs

- **File 1**: `{output_folder}/validation-report-{project_name}-{date}.json` - Relatório estruturado para processamento
- **File 2**: `{output_folder}/compliance-summary-{project_name}-{date}.md` - Resumo formatado para leitura
- **Console Output**:
  - Tipo de projeto detectado (NEW, EXISTING, ALREADY_COMPLIANT)
  - Arquivos relevantes encontrados
  - Resultados das 46 validações organizados por categoria
  - Contadores de problemas por severidade
  - Recomendações corretivas priorizadas
- **Knowledge Loaded**: 6 arquivos de conhecimento da plataforma

## Validation Categories

### Docker Compose (17 regras)
Valida conformidade com as 4 Verdades Fundamentais e melhores práticas Docker, incluindo volumes via variáveis do .env e portas sem hardcode.

### Environment Files (10 regras)
Verifica estrutura e valores de `.env.io` e `.env.io.example`, incluindo variáveis de volume.

### Settings JSON (8 regras)
Valida estrutura e completude de `.embrapa/settings.json`.

### Service Integrations (6 regras)
Verifica configurações de Sentry, Matomo e outros serviços.

### NO-FALLBACK Code Validation (4 regras CRÍTICAS)
Escaneia codebase (JS/TS, Python, Shell, Docker Compose) detectando padrões proibidos de fallback em variáveis de ambiente.

### Linter Configuration (2 regras de qualidade)
Verifica presença de Linter configurado (ESLint, PHP_CodeSniffer, Ruff, golangci-lint, RuboCop, etc) e comandos lint/lint:fix definidos.

## Severity Levels

- **CRITICAL**: Bloqueadores que impedem deploy
- **HIGH**: Problemas sérios que afetam funcionalidade
- **MEDIUM**: Melhorias importantes recomendadas
- **LOW**: Otimizações e boas práticas
