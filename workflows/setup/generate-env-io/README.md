---
last-redoc-date: 2025-11-25
---

# Generate Environment Variables Workflow

Workflow interativo que gera os arquivos `.env.io` e `.env.io.example` contendo as variáveis de ambiente obrigatórias da plataforma Embrapa I/O.

Este workflow coleta informações do projeto através de perguntas interativas, validando rigorosamente os formatos de entrada. Nomes de projeto e aplicação devem seguir o padrão unix (lowercase, apenas letras, números e hífens), enquanto emails de desenvolvedores devem terminar obrigatoriamente com `@embrapa.br`. A versão do projeto é calculada automaticamente no formato `0.YY.M-dev.1`, onde YY representa o ano com 2 dígitos e M o mês sem zero à esquerda (1-12), garantindo versionamento consistente com a plataforma.

O diferencial está na geração dupla de arquivos: `.env.io` contém valores reais para uso local (não versionado), enquanto `.env.io.example` serve como referência versionada com valores de exemplo mascarando informações sensíveis como o email do desenvolvedor. Variáveis como `COMPOSE_PROJECT_NAME` são sempre calculadas como concatenação `${IO_PROJECT}_${IO_APP}_development`, seguindo as regras rígidas da plataforma. O workflow também orienta sobre boas práticas Git (não commitar `.env.io`, apenas `.env.io.example`) e explica que variáveis locais simulam o comportamento da plataforma, que injeta essas mesmas variáveis automaticamente em ambientes remotos (alpha, beta, release).

Placeholders como `SENTRY_DSN=GET_IN_DASHBOARD` e `MATOMO_ID=522` são incluídos com instruções para obtenção de valores reais em `https://dashboard.embrapa.io`.

## Usage

```xml
<invoke-workflow>
  <path>{project-root}/_bmad/embrapa-io/workflows/setup/generate-env-io/workflow.yaml</path>
  <description>Gera .env.io e .env.io.example com variáveis da plataforma (workflow interativo)</description>
</invoke-workflow>
```

**Este é um workflow INTERATIVO** que requer input do usuário durante a execução.

## Inputs

- **IO_PROJECT**: Nome unix do projeto (validado: lowercase, hífens permitidos)
- **IO_APP**: Nome unix da aplicação (validado: lowercase, hífens permitidos)
- **IO_DEPLOYER**: Email do desenvolvedor (validado: @embrapa.br obrigatório)

## Outputs

- **File 1**: `{project-root}/.env.io` - Variáveis reais para ambiente local (não commitar)
- **File 2**: `{project-root}/.env.io.example` - Template versionado com valores de exemplo
- **Calculated Values**:
  - `COMPOSE_PROJECT_NAME`: `${IO_PROJECT}_${IO_APP}_development`
  - `IO_VERSION`: `0.YY.M-dev.1` (calculado automaticamente da data atual)
  - `IO_STAGE`: `development` (fixo para ambiente local)
  - `IO_SERVER`: `localhost` (fixo para ambiente local)
  - `COMPOSE_PROFILES`: `development` (fixo para ambiente local)

## Validation Rules

- Nomes unix: lowercase, apenas letras, números e hífens
- Email: Deve terminar com @embrapa.br
- IO_VERSION: Sempre formato `0.YY.M-dev.1` onde YY=ano-2000, M=mês sem zero (1-12)
- COMPOSE_PROJECT_NAME: Sempre `${IO_PROJECT}_${IO_APP}_development`
- **🚨 Valores sem aspas e espaços**: Nenhum valor de variável pode conter aspas (simples ou duplas) ou espaços. Para valores complexos, usar Base64, URL encoding, ou substituição de caracteres

## Quality

Workflow auditado e certificado BMAD v6 (Score: 100%). Template mapping perfeito com todas as 6 variáveis mapeadas corretamente.
