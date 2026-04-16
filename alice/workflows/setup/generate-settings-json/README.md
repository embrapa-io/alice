---
last-redoc-date: 2025-12-03
---

# Generate Settings JSON Workflow

Workflow interativo que gera o arquivo `.embrapa/settings.json` contendo metadados e configurações da aplicação conforme padrão da plataforma Embrapa I/O.

Este workflow utiliza detecção automática de stack através de arquivos como `package.json`, `requirements.txt` e `composer.json` para carregar templates de variáveis de ambiente apropriados. Suporta três templates especializados: `settings-nodejs.json` para backends Node.js, `settings-frontend.json` para aplicações React/Vue, e `settings-base.json` como fallback genérico. Cada template contém variáveis pré-configuradas específicas da stack (PORT, BASE_URL, SECRET, etc.) organizadas por ambiente (default, alpha, beta, release).

O diferencial está na estrutura JSON completa da plataforma, incluindo campos `boilerplate`, `platform`, `label`, `description`, `references`, `maintainers` com dados completos (nome, email, telefone), e `variables` separadas por ambiente de deployment. O campo `orchestrators` sempre lista `["DockerCompose"]` indicando o método de orquestração. Variáveis podem ser de tipos específicos (TEXT, PORT, SECRET, PASSWORD, VOLUME, EMPTY), permitindo que a plataforma trate cada uma adequadamente durante deploy.

Após coletar informações do mantenedor e identificar a stack, o workflow oferece adição de variáveis personalizadas além das padrão, construindo o JSON final com estrutura válida e salvando em `.embrapa/settings.json` (diretório criado automaticamente se não existir).

## Usage

```xml
<invoke-workflow>
  <path>./workflows/setup/generate-settings-json/workflow.yaml</path>
  <description>Gera .embrapa/settings.json conforme com Embrapa I/O</description>
</invoke-workflow>
```

Este é um workflow **INTERATIVO** que requer input do usuário.

## Inputs

- **Stack Detection**: Automática (Node.js, Frontend, PHP, .NET, outros)
- **Application Label**: Nome/título da aplicação para display
- **Application Description**: Breve descrição em uma linha
- **Maintainer Name**: Nome do mantenedor principal
- **Maintainer Email**: Email do mantenedor (validado)
- **Maintainer Phone**: Telefone opcional (formato obrigatório: "+[DDI] (DDD) X XXXX-XXXX")
- **Custom Variables**: Opcionalmente adicionar variáveis além das padrão da stack (com validação de tipo)

## Outputs

- **File**: `{project-root}/.embrapa/settings.json`
- **Structure**:
  - `platform`: Stack detectada
  - `label` e `description`: Metadata da aplicação
  - `maintainers`: Array com dados do(s) mantenedor(es)
  - `variables`: Organizadas por ambiente (default, alpha, beta, release)
  - `orchestrators`: `["DockerCompose"]`
- **Templates**: Carrega variáveis padrão de `settings-nodejs.json`, `settings-frontend.json`, ou `settings-base.json`

## Variable Types Supported

**Tipos com atributo 'value' OBRIGATÓRIO:**
- **TEXT**: Valores texto simples (ex: `{"name": "BASE_URL", "type": "TEXT", "value": "http://localhost"}`)
- **VOLUME**: Sufixo de volumes Docker sem prefixo (ex: `{"name": "MONGODB_VOLUME", "type": "VOLUME", "value": "mongodb"}`)

**Tipos SEM atributo 'value' (apenas name e type):**
- **PORT**: Números de porta (ex: `{"name": "APP_PORT", "type": "PORT"}`)
- **SECRET**: Valores sensíveis mascarados (ex: `{"name": "JWT_SECRET", "type": "SECRET"}`)
- **PASSWORD**: Senhas mascaradas (ex: `{"name": "DB_PASSWORD", "type": "PASSWORD"}`)
- **EMPTY**: Placeholder vazio (ex: `{"name": "OPTIONAL_VAR", "type": "EMPTY"}`)

**Regras críticas:**
- ✅ TEXT e VOLUME: Incluir atributo 'value'
- ❌ PASSWORD, SECRET, PORT, EMPTY: Omitir atributo 'value'
- 🔧 VOLUME: value contém apenas sufixo (ex: "mongodb" ao invés de "${IO_PROJECT}_${IO_APP}_${IO_STAGE}_mongodb")
