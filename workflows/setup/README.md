---
last-redoc-date: 2025-11-04
---

# Setup Workflows

Coleção de workflows para configuração inicial de projetos conformes com a plataforma Embrapa I/O.

Esta pasta contém 4 workflows especializados que cobrem todos os aspectos de setup de um projeto para a plataforma Embrapa I/O. Executados em sequência, eles criam a estrutura completa necessária para deployment: variáveis de ambiente, configurações Docker, metadados da aplicação, e arquivo de licença.

## Workflows Disponíveis

### [generate-env-io](./generate-env-io/)
Gera arquivos `.env.io` e `.env.io.example` com as 10 variáveis obrigatórias da plataforma. Workflow interativo que valida nomes unix e emails @embrapa.br, calcula versão automaticamente no formato `0.YY.M-dev.1`, e orienta sobre boas práticas Git.

### [generate-docker-compose](./generate-docker-compose/)
Cria `docker-compose.yaml` conforme com as 4 Verdades Fundamentais da plataforma. Detecta automaticamente a stack tecnológica (Node.js, Vue, React, PHP, .NET), adapta configurações específicas, e valida rigorosamente contra regras Embrapa I/O. Suporta serviços CLI opcionais (backup, restore, sanitize) via profiles.

### [generate-settings-json](./generate-settings-json/)
Gera `.embrapa/settings.json` com metadados e configurações de variáveis por ambiente. Carrega templates especializados por stack (nodejs, frontend, base) e organiza variáveis em categorias (default, alpha, beta, release) com tipos específicos (TEXT, PORT, SECRET, PASSWORD, VOLUME, EMPTY).

### [generate-license](./generate-license/)
Workflow autônomo que cria arquivo `LICENSE` padrão da Embrapa com copyright atualizado. Executa silenciosamente, calculando ano automaticamente e garantindo encoding UTF-8 para o símbolo ⓒ.

## Ordem de Execução Recomendada

1. **generate-env-io** - Sempre executar primeiro (outros workflows dependem destas variáveis)
2. **generate-license** - Pode ser executado a qualquer momento (independente)
3. **generate-settings-json** - Requer `.env.io` para extrair IO_PROJECT, IO_APP, IO_VERSION
4. **generate-docker-compose** - Requer `.env.io` para nomenclatura de recursos

## Uso Típico

Para setup completo de um novo projeto:

```xml
<step n="1" goal="Gerar variáveis de ambiente">
  <invoke-workflow>
    <path>{project-root}/_bmad/embrapa-io/workflows/setup/generate-env-io/workflow.yaml</path>
  </invoke-workflow>
</step>

<step n="2" goal="Gerar licença">
  <invoke-workflow>
    <path>{project-root}/_bmad/embrapa-io/workflows/setup/generate-license/workflow.yaml</path>
  </invoke-workflow>
</step>

<step n="3" goal="Gerar settings">
  <invoke-workflow>
    <path>{project-root}/_bmad/embrapa-io/workflows/setup/generate-settings-json/workflow.yaml</path>
  </invoke-workflow>
</step>

<step n="4" goal="Gerar docker-compose">
  <invoke-workflow>
    <path>{project-root}/_bmad/embrapa-io/workflows/setup/generate-docker-compose/workflow.yaml</path>
  </invoke-workflow>
</step>
```

Após execução completa, o projeto terá: `.env.io`, `.env.io.example`, `LICENSE`, `.embrapa/settings.json`, e `docker-compose.yaml` - todos os arquivos necessários para deployment na plataforma Embrapa I/O.
