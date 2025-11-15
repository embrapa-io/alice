# Generate .embrapa/settings.json - Instruções

<critical>The workflow execution engine is governed by: {project-root}/bmad/core/tasks/workflow.xml</critical>
<critical>You MUST have already loaded and processed: {project-root}/bmad/embrapa-io/workflows/setup/generate-settings-json/workflow.yaml</critical>
<critical>Communicate in {communication_language} throughout the workflow</critical>

<workflow>

<step n="1" goal="Verificar dependências e identificar stack">
<action>Verificar se .env.io existe (necessário para variáveis IO_*)</action>

<check if=".env.io exists">
<action>Ler variáveis: IO_PROJECT, IO_APP, IO_VERSION</action>
</check>

<action>Detectar stack automaticamente através de arquivos:</action>
- package.json → Node.js ou Frontend
- requirements.txt → Python
- composer.json → PHP
- *.csproj → .NET

<action>Exibir detecção para {user_name}</action>
</step>

<step n="2" goal="Coletar informações do projeto">
<ask>{user_name}, qual o nome/label da aplicação? (ex: "API de Catálogo de Produtos")</ask>
<action>Armazenar como {{app_label}}</action>

<ask>{user_name}, forneça uma breve descrição da aplicação (1 linha):</ask>
<action>Armazenar como {{app_description}}</action>

<ask>{user_name}, qual o nome do mantenedor principal?</ask>
<action>Armazenar como {{maintainer_name}}</action>

<ask>{user_name}, qual o email do mantenedor?</ask>
<action>Validar formato de email</action>
<action>Armazenar como {{maintainer_email}}</action>

<ask optional="true">{user_name}, qual o telefone do mantenedor (opcional)?
Formato obrigatório: "+[DDI] (DDD) X XXXX-XXXX"
Exemplo: "+55 (67) 9 8111-8060"</ask>

<check if="telefone fornecido">
<action>Validar formato do telefone:</action>
<action>- Deve começar com "+"</action>
<action>- Deve ter espaço após DDI</action>
<action>- DDD entre parênteses com espaço antes e depois</action>
<action>- Formato: "+[DDI] (DDD) X XXXX-XXXX"</action>
<action>- Regex: `^\+\d{1,3} \(\d{2}\) \d \d{4}-\d{4}$`</action>

<check if="formato inválido">
<action>Informar erro: "Formato inválido. Use: +[DDI] (DDD) X XXXX-XXXX"</action>
<action>Exemplo: "+55 (67) 9 8111-8060"</action>
<action>Solicitar telefone novamente</action>
</check>
</check>

<action>Armazenar como {{maintainer_phone}}</action>
</step>

<step n="3" goal="Definir variáveis de ambiente">
<action>Carregar template base conforme stack detectada:</action>
- Se Node.js backend: Ler {project-root}/bmad/embrapa-io/templates/settings/settings-nodejs.json
- Se Frontend (React/Vue): Ler {project-root}/bmad/embrapa-io/templates/settings/settings-frontend.json
- Outro: Ler {project-root}/bmad/embrapa-io/templates/settings/settings-base.json

<action>Extrair variáveis padrão do template carregado</action>

<action>Apresentar variáveis padrão da stack:</action>
- ENVIRONMENT (default: test, release: production)
- PORT
- BASE_URL
- SECRET
- Outras específicas da stack

<ask>{user_name}, deseja adicionar variáveis personalizadas além das padrão? (s/n)</ask>

<check if="resposta == 's'">
<action>Coletar variáveis adicionais:</action>
<ask>Nome da variável:</ask>
<ask>Tipo (TEXT, PORT, SECRET, PASSWORD, VOLUME, EMPTY):</ask>

<action>🚨 REGRA CRÍTICA - Atributo 'value' por tipo:</action>
<action>- TEXT: 'value' OBRIGATÓRIO (valor textual)</action>
<action>- VOLUME: 'value' OBRIGATÓRIO (sufixo sem prefixo ${IO_PROJECT}_${IO_APP}_${IO_STAGE}_)</action>
<action>- PASSWORD: 'value' DEVE SER OMITIDO</action>
<action>- SECRET: 'value' DEVE SER OMITIDO</action>
<action>- PORT: 'value' DEVE SER OMITIDO</action>
<action>- EMPTY: 'value' DEVE SER OMITIDO</action>

<check if="tipo == TEXT">
<ask>Valor padrão (obrigatório para TEXT):</ask>
<action>Armazenar como {{variable_value}}</action>
</check>

<check if="tipo == VOLUME">
<ask>Sufixo do volume (apenas a parte final, ex: 'servicedata' para ${IO_PROJECT}_${IO_APP}_${IO_STAGE}_servicedata):</ask>
<action>Validar que sufixo contém apenas lowercase e números (regex: ^[a-z0-9]+$)</action>
<action>Armazenar como {{variable_value}}</action>
<action>Exemplo: se .env tem "SERVICE_VOLUME=${IO_PROJECT}_${IO_APP}_${IO_STAGE}_mongodb"</action>
<action>Então o sufixo é apenas: "mongodb"</action>
</check>

<check if="tipo == PASSWORD OR tipo == SECRET OR tipo == PORT OR tipo == EMPTY">
<action>Atributo 'value' será OMITIDO (não aplicável para este tipo)</action>
<action>Variável terá apenas 'name' e 'type'</action>
</check>

<ask>Adicionar mais variáveis? (s/n)</ask>
</check>
</step>

<step n="4" goal="Gerar settings.json">
<action>Construir objeto JSON com estrutura Embrapa I/O:</action>

<action>🚨 REGRA CRÍTICA - Estrutura das variáveis:</action>

**Para cada variável, incluir atributos conforme o tipo:**

**Tipo TEXT:**
```json
{ "name": "BASE_URL", "type": "TEXT", "value": "http://localhost:3000" }
```

**Tipo VOLUME:**
```json
{ "name": "MONGODB_VOLUME", "type": "VOLUME", "value": "mongodb" }
```
⚠️ Note: value contém APENAS o sufixo, sem `${IO_PROJECT}_${IO_APP}_${IO_STAGE}_`

**Tipos PASSWORD, SECRET, PORT, EMPTY:**
```json
{ "name": "APP_PORT", "type": "PORT" }
{ "name": "DB_PASSWORD", "type": "PASSWORD" }
{ "name": "JWT_SECRET", "type": "SECRET" }
{ "name": "OPTIONAL_VAR", "type": "EMPTY" }
```
⚠️ Note: atributo 'value' é OMITIDO (não incluir no JSON)

**Estrutura completa do settings.json:**

```json
{
  "boilerplate": "_",
  "platform": "{{platform}}",
  "label": "{{app_label}}",
  "description": "{{app_description}}",
  "references": [{{references}}],
  "maintainers": [
    {
      "name": "{{maintainer_name}}",
      "email": "{{maintainer_email}}",
      "phone": "{{maintainer_phone}}"
    }
  ],
  "variables": {
    "default": [{{default_variables}}],
    "alpha": [],
    "beta": [],
    "release": [{{release_variables}}]
  },
  "orchestrators": ["DockerCompose"]
}
```

<action>Para cada variável em variables.default, variables.alpha, variables.beta, variables.release:</action>
<action>- Incluir SEMPRE: "name" e "type"</action>
<action>- Incluir "value" APENAS se tipo == TEXT ou tipo == VOLUME</action>
<action>- Se tipo == VOLUME, value = sufixo sem prefixo (ex: "mongodb" ao invés de "${IO_PROJECT}_${IO_APP}_${IO_STAGE}_mongodb")</action>

<template-output>settings_json_content</template-output>
</step>

<step n="5" goal="Validar e salvar arquivo">
<action>Validar JSON gerado (sintaxe válida)</action>
<action>Criar diretório .embrapa/ se não existir</action>
<action>Salvar em {project-root}/.embrapa/settings.json</action>

<action>Exibir resumo para {user_name}:</action>

**Arquivo .embrapa/settings.json criado!**

**Localização**: {project-root}/.embrapa/settings.json
**Platform**: {{platform}}
**Label**: {{app_label}}
**Variáveis padrão**: {{variable_count}}
**Mantenedores**: 1

**Próximos passos**:
1. Revisar arquivo gerado
2. Ajustar variáveis se necessário
3. Committar no repositório
</step>

</workflow>
