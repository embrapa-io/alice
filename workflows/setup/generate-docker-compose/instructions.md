# Generate docker-compose.yaml - Instruções de Geração

<critical>The workflow execution engine is governed by: {project-root}/bmad/core/tasks/workflow.xml</critical>
<critical>You MUST have already loaded and processed: {project-root}/bmad/embrapa-io/workflows/setup/generate-docker-compose/workflow.yaml</critical>
<critical>Communicate in {communication_language} throughout the workflow</critical>

<workflow>

<step n="1" goal="Verificar arquivos de configuração existentes">
<action>Verificar se arquivo .env.io existe no projeto</action>
<action>Se .env.io não existe, informar ao {user_name} que este workflow depende de variáveis do .env.io</action>
<action>Sugerir executar generate-env-io primeiro se .env.io não encontrado</action>

<check if=".env.io exists">
<action>Ler variáveis obrigatórias do .env.io:</action>
- IO_PROJECT
- IO_APP
- IO_STAGE
- IO_VERSION

<action>Armazenar variáveis para uso no template</action>
<action>Gerar project_name combinando: {{IO_PROJECT}}_{{IO_APP}}</action>
</check>

<template-output>project_name</template-output>
</step>

<step n="2" goal="Identificar tipo de aplicação e stack">
<action>Analisar estrutura do projeto para identificar a stack tecnológica</action>

<action>Procurar por arquivos indicadores:</action>
- package.json → Node.js
- requirements.txt / pyproject.toml → Python
- composer.json → PHP
- *.csproj → .NET
- pom.xml / build.gradle → Java
- go.mod → Go

<action>Procurar por frameworks específicos:</action>
- package.json com "express" → Node.js API
- package.json com "vue" → Vue.js Frontend
- package.json com "react" e "react-dom" → React Frontend
- package.json com "react-native" → React Native Mobile
- composer.json com "laravel" → PHP Laravel

<action>Identificar tipo de banco de dados (se aplicável):</action>
- Procurar por conexões MongoDB, PostgreSQL, MySQL, SQL Server
- Verificar variáveis de ambiente relacionadas a banco

<action>Exibir resumo da detecção para {user_name}</action>

<ask>A detecção automática está correta? Caso contrário, qual é a stack?

Opções:
1. Node.js API (Express + MongoDB/PostgreSQL)
2. Vue.js Frontend (Vuetify)
3. React Frontend
4. React Native Mobile
5. PHP Laravel
6. .NET Blazor
7. Outro (especificar)
</ask>

<action>Armazenar stack selecionada como {{selected_stack}}</action>

<template-output>selected_stack</template-output>
</step>

<step n="3" goal="Coletar informações específicas da aplicação">
<ask>Qual porta a aplicação principal irá usar? (ex: 3000, 8080, 5000)</ask>
<action>Validar que porta é número entre 1024 e 65535</action>
<action>Armazenar como {{app_port}}</action>

<ask>A aplicação expõe outras portas além da principal? (ex: MQTT:1883, WebSocket:3001, Metrics:9090)
Se sim, liste no formato: NOME:PORTA,NOME:PORTA
Se não, deixe vazio.</ask>
<action>Parsear resposta e criar array {{additional_ports}}</action>
<action>Exemplo: "MQTT:1883,METRICS:9090" → [{"name":"MQTT", "port":"1883"}, {"name":"METRICS", "port":"9090"}]</action>

<ask>A aplicação possui healthcheck endpoint? (ex: /health, /api/health, /status)
Se sim, informe o caminho. Se não, deixe vazio.</ask>
<action>Armazenar como {{health_endpoint}} ou usar padrão /health</action>

<check if="selected_stack requires database">
<ask>Qual banco de dados será usado?

Opções:
1. MongoDB
2. PostgreSQL
3. MySQL
4. SQL Server
5. Nenhum
</ask>
<action>Armazenar como {{database_type}}</action>
</check>

<ask optional="true">Deseja adicionar serviços CLI extras? (backup, restore, sanitize)

Os serviços CLI são executados manualmente com perfis do Docker Compose e são úteis para:
- backup: Fazer backup de dados
- restore: Restaurar backup
- sanitize: Otimizar/limpar dados

[s] Sim, incluir todos
[n] Não, apenas aplicação principal
[c] Customizar (escolher quais incluir)
</ask>

<action>Armazenar escolha como {{include_cli_services}}</action>
</step>

<step n="4" goal="Gerar docker-compose.yaml baseado no template">
<action>Carregar template base de: {base_template_path}</action>

<action>Adaptar template conforme a stack selecionada:</action>

**Para Node.js API:**
- Usar imagem base: node:20-alpine
- Adicionar comando: npm start
- Expor porta: {{app_port}}
- Adicionar MongoDB ou PostgreSQL se necessário

**Para Vue.js Frontend:**
- Usar imagem base: node:20-alpine (build) + nginx:alpine (runtime)
- Multi-stage build
- Expor porta 80
- Configurar nginx

**Para React Frontend:**
- Usar imagem base: node:20-alpine (build) + nginx:alpine (runtime)
- Multi-stage build
- Expor porta 80
- Configurar nginx

**Para PHP Laravel:**
- Usar imagem base: php:8.2-fpm-alpine
- Adicionar nginx para servir aplicação
- Expor porta 80
- Adicionar MySQL ou PostgreSQL se necessário

**Para .NET Blazor:**
- Usar imagem base: mcr.microsoft.com/dotnet/aspnet:8.0
- Expor porta 5000
- Adicionar SQL Server ou PostgreSQL se necessário

<action>Configurar serviço principal com:</action>
- Nome do serviço: app
- Build context: .
- Restart policy: unless-stopped
- Environment variables referenciando .env e .env.io
- Network: stack (externa)
- Healthcheck com endpoint {{health_endpoint}}
- Volumes (se necessário para a stack)

<action>🚨 REGRA CRÍTICA: Configurar mapeamento de portas usando APENAS variáveis do .env (JAMAIS hardcoded):</action>

**Porta principal:**
```yaml
ports:
  - "${APP_PORT}:{{app_port}}"
```

**Portas adicionais (se existirem em {{additional_ports}}):**
```yaml
ports:
  - "${APP_PORT}:{{app_port}}"
  - "${PORT_MQTT}:1883"
  - "${PORT_METRICS}:9090"
```

<action>Para cada porta (principal + adicionais), criar variável de ambiente correspondente</action>
<action>Armazenar lista de variáveis de porta como {{port_env_vars}} para adicionar ao .env posteriormente</action>

**Exemplos de variáveis de porta:**
- APP_PORT (porta principal do host)
- PORT_WEB (se frontend com nginx)
- PORT_MQTT (se broker MQTT)
- PORT_METRICS (se Prometheus metrics)
- PORT_WEBSOCKET (se WebSocket server)

<action>Adicionar configuração de network:</action>
```yaml
networks:
  stack:
    name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}
    external: true
```

<check if="include_cli_services == 'sim' or 'customizar'">
<action>Adicionar serviços CLI (backup, restore, sanitize) com profile: cli</action>
<action>Configurar volumes externos para backup</action>
</check>

<check if="database_type != 'nenhum'">
<action>Adicionar serviço de banco de dados ao compose</action>
<action>Configurar volumes externos para persistência do banco</action>
<action>Adicionar healthcheck para banco</action>
</check>

<action>Configurar volumes seguindo as regras da plataforma Embrapa I/O:</action>

**REGRA CRÍTICA: Volumes DEVEM usar variáveis do .env (exceto backup)**

**Para volumes de serviços (dados, cache, etc):**
```yaml
volumes:
  service_data:
    name: ${SERVICE_VOLUME}
    external: true
```

**No arquivo .env, adicionar:**
```
SERVICE_VOLUME=${IO_PROJECT}_${IO_APP}_${IO_STAGE}_servicename
```

**Padrão obrigatório de nomenclatura:**
- Formato: `${IO_PROJECT}_${IO_APP}_${IO_STAGE}_[a-z0-9]+`
- Sufixo deve conter apenas lowercase e números
- Exemplos: `_data`, `_mongodb`, `_postgres`, `_cache`, `_uploads`

**EXCEÇÃO: Volume de backup (único hardcoded):**
```yaml
volumes:
  backup_data:
    name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}_backup
    external: true
```

**Volumes que devem ser criados baseado na stack:**
- MongoDB: `${MONGODB_VOLUME}` → `${IO_PROJECT}_${IO_APP}_${IO_STAGE}_mongodb`
- PostgreSQL: `${POSTGRES_VOLUME}` → `${IO_PROJECT}_${IO_APP}_${IO_STAGE}_postgres`
- MySQL: `${MYSQL_VOLUME}` → `${IO_PROJECT}_${IO_APP}_${IO_STAGE}_mysql`
- Aplicação (se necessário): `${APP_VOLUME}` → `${IO_PROJECT}_${IO_APP}_${IO_STAGE}_data`
- Backup: `backup_data` (nome hardcoded: `${IO_PROJECT}_${IO_APP}_${IO_STAGE}_backup`)

<action>Coletar nomes de volumes necessários e gerar variáveis correspondentes para o .env</action>
<action>Armazenar lista de variáveis de volume como {{volume_env_vars}} para adicionar ao .env posteriormente</action>

<action>Garantir que NÃO há campo 'version' no docker-compose (v6 não usa)</action>
<action>Garantir que NÃO há 'container_name' em nenhum serviço</action>
<action>Garantir que TODOS os volumes (exceto backup) usam variáveis do .env</action>
<action>Garantir que volume de backup tem nome hardcoded: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}_backup</action>

<template-output>docker_compose_content</template-output>
</step>

<step n="5" goal="Validar conformidade com Embrapa I/O">
<action>Validar conteúdo gerado contra as 4 Verdades Fundamentais:</action>

**Verdade 1: Sem campo 'version'**
- [ ] Campo 'version' ausente no arquivo

**Verdade 2: Network 'stack' externa**
- [ ] Network 'stack' configurada como external: true
- [ ] Nome da network: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}

**Verdade 3: Volumes externos**
- [ ] Todos os volumes configurados como external: true
- [ ] Nomes seguem padrão: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}_{nome}
- [ ] Volumes de serviço usam variáveis do .env (formato: `name: ${SERVICE_VOLUME}`)
- [ ] Volume de backup tem nome hardcoded: `${IO_PROJECT}_${IO_APP}_${IO_STAGE}_backup`

**Verdade 4: Sem container_name**
- [ ] Nenhum serviço possui campo 'container_name'

<action>🚨 VALIDAR REGRA CRÍTICA: Portas usando APENAS variáveis (JAMAIS hardcoded):</action>
- [ ] Todas as portas mapeadas usam variáveis do .env (formato: `"${PORT_VAR}:container_port"`)
- [ ] NENHUMA porta hardcoded no lado host (proibido: `"3000:3000"`, `"80:80"`)
- [ ] Lado container pode ser fixo, mas lado host DEVE ser variável

<action>Validar que serviços CLI usam profiles</action>
<action>Validar que healthchecks estão presentes</action>
<action>Validar que volumes (exceto backup) usam variáveis do .env</action>
<action>Validar que variáveis de volume seguem padrão: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}_[a-z0-9]+</action>

<check if="validation fails">
<action>Corrigir automaticamente os problemas encontrados</action>
<action>Regenerar template</action>
<goto step="4">Repetir geração com correções</goto>
</check>
</step>

<step n="5.5" goal="Criar/atualizar arquivo .env com variáveis de volume e portas">
<action>Verificar se arquivo .env existe no projeto</action>

<check if=".env exists">
<action>Ler conteúdo atual do .env</action>
<action>Verificar quais variáveis já existem (volumes e portas)</action>
</check>

<action>Se .env não existe, criar novo arquivo com cabeçalho:</action>
```bash
# Environment Variables for Docker Compose
# Generated by Embrapa I/O Module
# DO NOT commit this file to version control

# Import Embrapa I/O variables
# Include this at the top of docker-compose.yaml:
# env_file: [".env.io", ".env"]
```

<action>🚨 ADICIONAR VARIÁVEIS DE PORTA ({{port_env_vars}}):</action>

**Formato das variáveis de porta:**
```bash
# Application Port
APP_PORT=3000

# Additional Ports (if applicable)
PORT_MQTT=1883
PORT_METRICS=9090
PORT_WEBSOCKET=3001
```

<action>Para cada porta identificada em {{port_env_vars}}, adicionar ao .env</action>
<action>Usar valor padrão fornecido pelo usuário ou sugerir porta comum</action>

<action>ADICIONAR VARIÁVEIS DE VOLUME ({{volume_env_vars}}):</action>

**Formato das variáveis de volume:**
```bash
# Docker Volumes - Auto-generated by generate-docker-compose
MONGODB_VOLUME=${IO_PROJECT}_${IO_APP}_${IO_STAGE}_mongodb
POSTGRES_VOLUME=${IO_PROJECT}_${IO_APP}_${IO_STAGE}_postgres
APP_VOLUME=${IO_PROJECT}_${IO_APP}_${IO_STAGE}_data
# Backup volume is hardcoded in docker-compose.yaml
```

<action>Para cada volume identificado em {{volume_env_vars}}, adicionar ao .env</action>

<action>Salvar arquivo .env atualizado em {project-root}/.env</action>

<action>Informar ao {user_name} sobre as variáveis adicionadas:</action>
- Listar todas as variáveis de porta criadas
- Listar todas as variáveis de volume criadas
- Explicar que volumes devem ser criados manualmente antes do primeiro deploy
- Fornecer comandos para criação de cada volume

<template-output>env_vars_created</template-output>
</step>

<step n="6" goal="Criar arquivo docker-compose.yaml">
<action>Salvar conteúdo gerado em {project-root}/docker-compose.yaml</action>

<action>Exibir resumo para {user_name} em {communication_language}:</action>

**Arquivo docker-compose.yaml criado com sucesso!**

**Localização**: {project-root}/docker-compose.yaml

**Configuração**:
- Stack: {{selected_stack}}
- Porta principal: {{app_port}}
- Healthcheck: {{health_endpoint}}
- Banco de dados: {{database_type}}
- Serviços CLI: {{include_cli_services}}

**Conformidade Embrapa I/O**: ✅ VALIDADO
- ✅ Sem campo 'version'
- ✅ Network 'stack' externa
- ✅ Volumes externos
- ✅ Sem container_name

**Próximos passos**:
1. Revisar arquivo docker-compose.yaml gerado
2. Criar network externa: `docker network create ${IO_PROJECT}_${IO_APP}_${IO_STAGE}`
3. Criar volumes externos necessários
4. Executar: `docker compose up -d`

<action>Perguntar se {user_name} deseja visualizar o conteúdo completo do arquivo gerado</action>
</step>

<step n="7" goal="Gerar comandos helper">
<action optional="true">Criar arquivo scripts/docker-helpers.sh com comandos úteis:</action>

```bash
#!/bin/bash
# Docker Helpers - Embrapa I/O
# Gerado automaticamente

# Criar network externa
create-network:
  docker network create ${IO_PROJECT}_${IO_APP}_${IO_STAGE}

# Criar volumes externos
create-volumes:
  docker volume create ${IO_PROJECT}_${IO_APP}_${IO_STAGE}_backup
  # Adicionar outros volumes conforme necessário

# Executar backup
backup:
  docker compose --profile cli run --rm backup

# Restaurar backup
restore:
  BACKUP_FILE_TO_RESTORE=<arquivo> docker compose --profile cli run --rm restore

# Sanitize
sanitize:
  docker compose --profile cli run --rm sanitize
```

<ask>Deseja criar arquivo scripts/docker-helpers.sh com comandos úteis? (s/n)</ask>

<check if="resposta == 's'">
<action>Criar diretório scripts/ se não existir</action>
<action>Salvar docker-helpers.sh</action>
<action>Tornar arquivo executável: chmod +x scripts/docker-helpers.sh</action>
</check>
</step>

</workflow>
