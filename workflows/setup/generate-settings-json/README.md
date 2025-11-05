---
last-redoc-date: 2025-11-04
---

# Generate Settings JSON Workflow

Workflow interativo que gera o arquivo `.embrapa/settings.json` contendo metadados e configurações da aplicação conforme padrão da plataforma Embrapa I/O.

Este workflow utiliza detecção automática de stack através de arquivos como `package.json`, `requirements.txt` e `composer.json` para carregar templates de variáveis de ambiente apropriados. Suporta três templates especializados: `settings-nodejs.json` para backends Node.js, `settings-frontend.json` para aplicações React/Vue, e `settings-base.json` como fallback genérico. Cada template contém variáveis pré-configuradas específicas da stack (PORT, BASE_URL, SECRET, etc.) organizadas por ambiente (default, alpha, beta, release).

O diferencial está na estrutura JSON completa da plataforma, incluindo campos `boilerplate`, `platform`, `label`, `description`, `references`, `maintainers` com dados completos (nome, email, telefone), e `variables` separadas por ambiente de deployment. O campo `orchestrators` sempre lista `["DockerCompose"]` indicando o método de orquestração. Variáveis podem ser de tipos específicos (TEXT, PORT, SECRET, PASSWORD, VOLUME, EMPTY), permitindo que a plataforma trate cada uma adequadamente durante deploy.

Após coletar informações do mantenedor e identificar a stack, o workflow oferece adição de variáveis personalizadas além das padrão, construindo o JSON final com estrutura válida e salvando em `.embrapa/settings.json` (diretório criado automaticamente se não existir).

## Usage

```xml
<invoke-workflow>
  <path>{project-root}/bmad/embrapa-io/workflows/setup/generate-settings-json/workflow.yaml</path>
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
- **Maintainer Phone**: Telefone opcional
- **Custom Variables**: Opcionalmente adicionar variáveis além das padrão da stack

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

- **TEXT**: Valores texto simples
- **PORT**: Números de porta (validados)
- **SECRET**: Valores sensíveis (mascarados em logs)
- **PASSWORD**: Senhas (mascaradas em logs)
- **VOLUME**: Paths de volumes Docker
- **EMPTY**: Placeholder vazio para preenchimento futuro
