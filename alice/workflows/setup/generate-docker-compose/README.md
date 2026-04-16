---
last-redoc-date: 2025-12-03
---

# Generate Docker Compose Workflow

Workflow interativo que gera arquivos `docker-compose.yaml` conformes com a plataforma Embrapa I/O, adaptando-se automaticamente à stack tecnológica do projeto detectada através de análise de arquivos indicadores.

Este workflow realiza detecção inteligente da tecnologia utilizada (Node.js API, Vue.js, React, React Native, PHP Laravel, .NET Blazor) através da análise de `package.json`, `composer.json`, `*.csproj`, `pom.xml` e `go.mod`. Com base na stack identificada, carrega templates apropriados e configura serviços Docker específicos, incluindo bancos de dados (MongoDB, PostgreSQL, MySQL, SQL Server) quando necessário.

O diferencial está na validação rigorosa e automática contra as **4 Verdades Fundamentais** da plataforma Embrapa I/O: (1) ausência do campo `version` no compose, (2) network `stack` externa com nomenclatura `${IO_PROJECT}_${IO_APP}_${IO_STAGE}`, (3) volumes externos seguindo mesmo padrão de nomenclatura, e (4) ausência de `container_name` nos serviços. Problemas detectados são corrigidos automaticamente antes da geração final. Suporte opcional para serviços CLI (backup, restore, sanitize) através de Docker Compose profiles permite operações de manutenção sem modificar o compose principal.

A dependência do arquivo `.env.io` (gerado pelo workflow `generate-env-io`) é obrigatória, pois as variáveis `IO_PROJECT`, `IO_APP`, `IO_STAGE` e `IO_VERSION` são essenciais para nomenclatura de recursos e configuração de rede. O workflow suporta multi-stage builds para aplicações frontend, otimizando imagens Docker com nginx como servidor de produção.

## Usage

```xml
<invoke-workflow>
  <path>./workflows/setup/generate-docker-compose/workflow.yaml</path>
  <description>Gera docker-compose.yaml conforme com Embrapa I/O</description>
</invoke-workflow>
```

## Inputs

- **Stack Detection**: Automática através de arquivos de projeto (pode ser sobrescrita manualmente)
- **Application Port**: Porta principal da aplicação (validada entre 1024-65535)
- **Additional Ports**: Portas adicionais se aplicável (MQTT, WebSocket, Metrics, etc)
- **Healthcheck Endpoint**: Caminho do endpoint de health (padrão: `/health`)
- **Database Type**: MongoDB, PostgreSQL, MySQL, SQL Server, ou nenhum
- **CLI Services**: Opcional - inclusão de serviços backup/restore/sanitize com profiles

## Outputs

- **File**: `{project-root}/docker-compose.yaml` (com portas via variáveis do .env)
- **File**: `{project-root}/.env` (criado/atualizado com variáveis de porta e volume)
- **Validation**: Conformidade automática com as 4 Verdades Fundamentais + regra de portas via .env
- **Scripts**: Opcionalmente gera `scripts/docker-helpers.sh` com comandos úteis para criação de network e volumes

## Configuration

- **base_template_path**: `./templates/docker-compose/base.yaml`
- **Template adaptável** para diferentes stacks com configurações específicas de imagem, porta, volumes e healthchecks
- **Validação em Step 5** garante conformidade antes de salvar arquivo final

## Quality

Workflow auditado e certificado BMAD v6 (Score: 100%). Template mapping completo com todas as variáveis mapeadas corretamente para substituição no arquivo final.
