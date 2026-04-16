---
name: 'step-05-validate-integrations-and-code'
description: 'Validação das integrações Sentry/Matomo, regra NO-FALLBACK e Linter'
nextStepFile: './step-06-generate-report.md'
---

# Step 5: Validar Integrações e Código

## STEP GOAL:

Validar integrações (Sentry, Matomo), regra NO-FALLBACK de variáveis de ambiente, e configuração de Linter.

## PRE-COMPUTED VALIDATION

If `validate-compliance.py` JSON output is available, use `checks.code` (NO-FALLBACK, LICENSE) and `checks.integrations` (Sentry, Matomo detection) results directly. Focus LLM effort on generating stack-specific remediation code examples.

## Rules

Follow `./references/step-file-protocol.md`. Step-specific:
- Integrações Sentry e Matomo são **OBRIGATÓRIAS** para codebases com código-fonte
- NO-FALLBACK: Variáveis de ambiente NUNCA devem ter valores padrão (fallback) -- severidade CRITICAL
- Integrações NÃO se aplicam a serviços de prateleira (Nginx Proxy Manager, Directus, MinIO, etc.)
- Adaptar à stack tecnológica detectada
- Fornecer exemplos de código específicos para a stack

### Determinação de Tipo de Projeto

**É um codebase com código-fonte SE:**
- Contém arquivos `.php`, `.js`, `.ts`, `.vue`, `.jsx`, `.tsx` fora de `node_modules` ou `vendor`
- Possui `package.json` com scripts de build/start customizados
- Possui `composer.json` com namespace da aplicação
- Dockerfile usa COPY para copiar código-fonte

**É um serviço de prateleira SE:**
- docker-compose usa apenas `image:` sem `build:`
- Não há código-fonte customizado (apenas configuração)
- Exemplos: nginx-proxy-manager, directus, strapi, minio, n8n, open-webui

## Sequence of Instructions

### 1. Determinar Aplicabilidade das Integrações

**Sentry (Monitoramento de Erros):**
- Aplicável a: Backends, APIs, Frontends
- SENTRY_DSN no .env.io indica que deve ser configurado

**Matomo (Analytics):**
- Aplicável a: Frontends, PWAs
- Pode ser usado em backends para tracking server-side
- MATOMO_ID no .env.io indica que deve ser configurado

### 2. Validar Integração Sentry

Se `SENTRY_DSN` está no `.env.io.example`:

**Para Node.js/Express:**
```javascript
// Verificar se @sentry/node está no package.json
// Verificar se Sentry.init() é chamado

// Exemplo de configuração esperada:
const Sentry = require('@sentry/node');

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  release: process.env.IO_VERSION.split('-')[0],
  environment: process.env.IO_STAGE,
  tracesSampleRate: 1.0
});
```

**Para Vue.js:**
```javascript
// Verificar se @sentry/vue está no package.json
import * as Sentry from '@sentry/vue';

Sentry.init({
  app,
  dsn: import.meta.env.VITE_SENTRY_DSN,
  release: import.meta.env.VITE_IO_VERSION?.split('-')[0],
  environment: import.meta.env.VITE_IO_STAGE,
  integrations: [Sentry.browserTracingIntegration({ router })],
  tracesSampleRate: 1.0
});
```

**Para PHP/Laravel:**
```php
// Verificar se sentry/sentry-laravel está no composer.json
// config/sentry.php deve ter:
return [
    'dsn' => env('SENTRY_DSN'),
    'release' => explode('-', env('IO_VERSION'))[0],
    'environment' => env('IO_STAGE'),
];
```

**Validações:**
- [ ] Pacote Sentry instalado (package.json, composer.json, etc.)
- [ ] Sentry.init() configurado
- [ ] DSN vindo de variável de ambiente
- [ ] Release usando IO_VERSION
- [ ] Environment usando IO_STAGE

**Se Sentry não configurado E projeto é codebase com código-fonte:**
- Severidade: **CRITICAL**
- Action Item: "Implementar integração Sentry conforme stack {detected_stack}"
- Motivo: Integração Sentry é OBRIGATÓRIA para codebases com código-fonte

### 3. Validar Integração Matomo

Se `MATOMO_ID` está no `.env.io.example` E projeto tem frontend:

**Para Vue.js com vue-matomo:**
```javascript
// Verificar se vue-matomo está no package.json
import VueMatomo from 'vue-matomo';

app.use(VueMatomo, {
  host: 'https://hit.embrapa.io',
  siteId: import.meta.env.VITE_MATOMO_ID,
  router,
  preInitActions: [
    ['setCustomDimension', 1, import.meta.env.VITE_IO_STAGE],
    ['setCustomDimension', 2, import.meta.env.VITE_IO_VERSION]
  ]
});
```

**Para qualquer frontend (script tag):**
```html
<script>
  var _paq = window._paq = window._paq || [];
  _paq.push(['setCustomDimension', 1, '%STAGE%']);
  _paq.push(['setCustomDimension', 2, '%VERSION%']);
  _paq.push(['trackPageView']);
  _paq.push(['enableLinkTracking']);
  (function() {
    var u="https://hit.embrapa.io/";
    _paq.push(['setTrackerUrl', u+'matomo.php']);
    _paq.push(['setSiteId', '%MATOMO_ID%']);
    var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
    g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
  })();
</script>
```

**Para Node.js backend (tracking server-side):**
```javascript
// Verificar se matomo-tracker está no package.json
const MatomoTracker = require('matomo-tracker');

const matomo = new MatomoTracker(
  process.env.MATOMO_ID,
  'https://hit.embrapa.io/matomo.php',
  process.env.MATOMO_TOKEN
);
```

**Validações:**
- [ ] Pacote/script Matomo presente
- [ ] Host configurado como `https://hit.embrapa.io`
- [ ] Site ID vindo de variável de ambiente
- [ ] Custom dimensions configuradas (stage, version)

**Se Matomo não configurado E projeto é codebase com código-fonte:**
- Severidade: **CRITICAL**
- Action Item: "Implementar integração Matomo conforme stack {detected_stack}"
- Motivo: Integração Matomo é OBRIGATÓRIA para codebases com código-fonte

### 4. Validar NO-FALLBACK (Regra Crítica)

Escanear código-fonte em busca de padrões de fallback proibidos. Variáveis de ambiente da plataforma são SEMPRE injetadas — fallbacks mascaram erros de configuração.

**Padrões proibidos por linguagem:**

- **JavaScript/TypeScript:** `process.env.VAR || 'default'`, `process.env.VAR ?? 'default'`, `process.env.VAR || defaultValue`
- **Python:** `os.getenv('VAR', 'default')`, `os.environ.get('VAR', 'default')`
- **PHP:** `env('VAR', 'default')`, `getenv('VAR') ?: 'default'`
- **Shell/Bash:** `${VAR:-default}`, `${VAR:=default}`
- **Docker Compose:** `${VAR:-default}` em qualquer valor

**Para cada violação encontrada:**
- Severidade: **CRITICAL**
- Documentar: arquivo, linha, padrão encontrado, variável afetada
- Fix: "Remover fallback — usar apenas `process.env.VAR` (ou equivalente na linguagem)"

### 5. Verificar Linter

**Verificar se projeto tem Linter configurado:**
- Node.js: `eslint` em devDependencies, scripts `lint`/`lint:fix` em package.json
- PHP: `phpstan` ou `php_codesniffer` em composer.json
- Python: `ruff`, `flake8`, `pylint`, ou `black` em requirements.txt/pyproject.toml
- Go: `.golangci.yml` na raiz

**Se Linter não configurado:**
- Severidade: **MEDIUM**
- Action Item: "Configurar Linter para a stack {detected_stack}"

### 6. Verificar LICENSE

**Formato obrigatório:**
```
Copyright © YYYY Brazilian Agricultural Research Corporation (Embrapa). All rights reserved.
```

**Se LICENSE ausente:**
- Severidade: MEDIUM
- Action Item: "Criar arquivo LICENSE com copyright da Embrapa"

**Se LICENSE existe mas formato incorreto:**
- Severidade: LOW
- Action Item: "Atualizar LICENSE para formato padrão Embrapa"

### 7. Verificar Logo Embrapa (se frontend)

**Se projeto tem interface visual:**
- [ ] Logo da Embrapa presente em assets
- [ ] Logo referenciada no código

**Se logo ausente:**
- Severidade: LOW
- Action Item: "Adicionar logo da Embrapa aos assets do projeto"

### 8. Compilar Resultados

```markdown
## 🔌 Validação Integrações

### Sentry
- Status: {CONFIGURED | NOT_CONFIGURED | NOT_APPLICABLE}
- Pacote: {package_name} {✅/❌}
- Inicialização: {✅/❌}
- DSN via env: {✅/❌}
- Release tracking: {✅/❌}
- Environment tracking: {✅/❌}

### Matomo
- Status: {CONFIGURED | NOT_CONFIGURED | NOT_APPLICABLE}
- Implementação: {vue-matomo | script | matomo-tracker}
- Host correto: {✅/❌}
- Site ID via env: {✅/❌}
- Custom dimensions: {✅/❌}

### NO-FALLBACK
- Status: {CLEAN | VIOLATIONS_FOUND}
- Violações: {count} encontradas

### Linter
- Status: {CONFIGURED | NOT_CONFIGURED}
- Ferramenta: {linter_name}

### LICENSE
- Status: {PRESENT | MISSING | INCORRECT_FORMAT}

### Findings
| # | Severidade | Problema | Solução |
|---|------------|----------|---------|
| ... | ... | ... | ... |
```

Store as `{integration_findings}`.

### 9. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue to Generate Report [X] Exit workflow"

#### Menu Handling Logic:

- IF C: Store integration_findings, then load, read entire file, then execute {nextStepFile}
- IF X: End workflow gracefully

