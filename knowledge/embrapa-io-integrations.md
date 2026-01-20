# Integrações Embrapa I/O

## 🎯 Visão Geral

Este documento detalha como integrar as ferramentas do ecossistema Embrapa I/O: Sentry (erros), Matomo (analytics), SonarQube (qualidade), e Grafana Loki (logs).

## 🚨 Sentry (Monitoramento de Erros)

### Configuração por Stack

#### Node.js / Express

```bash
npm install @sentry/node @sentry/profiling-node
```

```javascript
// src/config/sentry.js
const Sentry = require('@sentry/node');
const { nodeProfilingIntegration } = require('@sentry/profiling-node');

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  release: process.env.IO_VERSION.split('-')[0],
  environment: process.env.IO_STAGE,
  tracesSampleRate: 1.0,
  profilesSampleRate: 1.0,
  integrations: [nodeProfilingIntegration()],
});

module.exports = Sentry;
```

```javascript
// src/index.js
const Sentry = require('./config/sentry');
const express = require('express');

const app = express();

// Sentry DEVE ser o primeiro middleware
app.use(Sentry.Handlers.requestHandler());
app.use(Sentry.Handlers.tracingHandler());

// Suas rotas...
app.get('/', (req, res) => {
  res.json({ status: 'ok' });
});

// Sentry error handler DEVE ser o último middleware
app.use(Sentry.Handlers.errorHandler());

app.listen(3000);
```

#### Vue.js

```bash
npm install @sentry/vue
```

```javascript
// src/plugins/sentry.js
import * as Sentry from "@sentry/vue";

export default function setupSentry(app, router) {
  Sentry.init({
    app,
    dsn: import.meta.env.VITE_SENTRY_DSN,
    release: import.meta.env.VITE_IO_VERSION?.split('-')[0],
    environment: import.meta.env.VITE_IO_STAGE,
    integrations: [
      Sentry.browserTracingIntegration({ router }),
      Sentry.replayIntegration(),
    ],
    tracesSampleRate: 1.0,
    replaysSessionSampleRate: 0.1,
    replaysOnErrorSampleRate: 1.0,
  });
}
```

```javascript
// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import setupSentry from './plugins/sentry'

const app = createApp(App)
setupSentry(app, router)
app.use(router)
app.mount('#app')
```

#### React

```bash
npm install @sentry/react
```

```javascript
// src/sentry.js
import * as Sentry from "@sentry/react";
import { createBrowserRouter } from "react-router-dom";

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
  release: import.meta.env.VITE_IO_VERSION?.split('-')[0],
  environment: import.meta.env.VITE_IO_STAGE,
  integrations: [
    Sentry.browserTracingIntegration(),
    Sentry.replayIntegration(),
  ],
  tracesSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
});
```

#### .NET

```bash
dotnet add package Sentry.AspNetCore
```

```csharp
// Program.cs
builder.WebHost.UseSentry(options =>
{
    options.Dsn = builder.Configuration["Sentry:Dsn"];
    options.Release = builder.Configuration["IO_VERSION"]?.Split('-')[0];
    options.Environment = builder.Configuration["IO_STAGE"];
    options.TracesSampleRate = 1.0;
});
```

#### PHP / Laravel

```bash
composer require sentry/sentry-laravel
```

```php
// config/sentry.php
return [
    'dsn' => env('SENTRY_LARAVEL_DSN', env('SENTRY_DSN')),
    'release' => explode('-', env('IO_VERSION'))[0],
    'environment' => env('IO_STAGE'),
    'traces_sample_rate' => 1.0,
];
```

#### PHP / Slim (Backend API)

```bash
composer require sentry/sentry
```

```php
<?php
// src/Bootstrap/SentryInitializer.php

declare(strict_types=1);

namespace App\Bootstrap;

use Sentry\Event;
use Sentry\EventHint;
use Sentry\State\Scope;

/**
 * Sentry Initializer - Embrapa I/O Compliant
 *
 * Usa APENAS variáveis de .env.io: SENTRY_DSN, IO_STAGE, IO_VERSION
 * URL do Sentry é hardcoded no DSN (não criar variáveis adicionais)
 */
class SentryInitializer
{
    private static bool $initialized = false;
    private static bool $enabled = false;

    private const SENSITIVE_PATTERNS = [
        'password', 'pin', 'secret', 'token',
        'authorization', 'bearer', 'api_key', 'credential',
    ];

    public static function initialize(): void
    {
        if (self::$initialized) {
            return;
        }

        self::$initialized = true;

        // SENTRY_DSN vem do .env.io (fornecido pela plataforma)
        $dsn = $_ENV['SENTRY_DSN'] ?? '';
        if ($dsn === '') {
            throw new \RuntimeException('SENTRY_DSN não definida');
        }

        self::$enabled = true;

        \Sentry\init([
            'dsn' => $dsn,
            'environment' => $_ENV['IO_STAGE'] ?? throw new \RuntimeException('IO_STAGE não definida'),
            'release' => $_ENV['IO_VERSION'] ?? throw new \RuntimeException('IO_VERSION não definida'),
            'traces_sample_rate' => 0.1,
            'before_send' => [self::class, 'beforeSend'],
            'send_default_pii' => false,
        ]);
    }

    public static function isEnabled(): bool
    {
        return self::$enabled;
    }

    public static function captureException(\Throwable $exception): void
    {
        if (!self::$enabled) {
            return;
        }
        \Sentry\captureException($exception);
    }

    public static function setUserContext(string $userId): void
    {
        if (!self::$enabled) {
            return;
        }
        \Sentry\configureScope(function (Scope $scope) use ($userId): void {
            $scope->setUser(['id' => $userId]);
        });
    }

    public static function beforeSend(Event $event, ?EventHint $hint): ?Event
    {
        // Filtrar dados sensíveis antes de enviar ao Sentry
        $request = $event->getRequest();
        $headers = $request['headers'] ?? [];
        $request['headers'] = self::filterSensitiveData($headers);
        if (isset($request['data'])) {
            $request['data'] = self::filterSensitiveData($request['data']);
        }
        $event->setRequest($request);
        return $event;
    }

    private static function filterSensitiveData(array $data): array
    {
        $filtered = [];
        foreach ($data as $key => $value) {
            if (!is_string($key)) {
                $filtered[$key] = is_array($value) ? self::filterSensitiveData($value) : $value;
                continue;
            }
            $keyLower = strtolower($key);
            $isSensitive = false;
            foreach (self::SENSITIVE_PATTERNS as $pattern) {
                if (str_contains($keyLower, $pattern)) {
                    $isSensitive = true;
                    break;
                }
            }
            $filtered[$key] = $isSensitive ? '[FILTERED]' : (is_array($value) ? self::filterSensitiveData($value) : $value);
        }
        return $filtered;
    }
}
```

```php
<?php
// public/index.php (entry point)

// Inicializar Sentry ANTES de qualquer outra coisa
SentryInitializer::initialize();

// ... resto da aplicação
```

### Variáveis de Ambiente

```ini
# .env.io (fornecido pela plataforma)
SENTRY_DSN=https://public@sentry.io/project-id
IO_VERSION=1.0.0-dev
IO_STAGE=development
```

### Teste de Integração

```javascript
// Node.js
Sentry.captureMessage("Sentry integration test");

// Vue.js / React
Sentry.captureMessage("Sentry integration test");
```

---

## 📊 Matomo (Analytics)

### Configuração por Stack

#### Frontend (Vue.js / React)

```html
<!-- public/index.html -->
<script>
  var _paq = window._paq = window._paq || [];
  _paq.push(['setCustomDimension', 1, import.meta.env.VITE_IO_STAGE]);
  _paq.push(['setCustomDimension', 2, import.meta.env.VITE_IO_VERSION]);
  _paq.push(['trackPageView']);
  _paq.push(['enableLinkTracking']);
  (function() {
    var u="https://hit.embrapa.io/";
    _paq.push(['setTrackerUrl', u+'matomo.php']);
    _paq.push(['setSiteId', import.meta.env.VITE_MATOMO_ID]);
    var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
    g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
  })();
</script>
```

#### Backend (Node.js)

```bash
npm install matomo-tracker
```

```javascript
// src/config/matomo.js
const MatomoTracker = require('matomo-tracker');

const matomo = new MatomoTracker(
  process.env.MATOMO_ID,
  'https://hit.embrapa.io/matomo.php',
  process.env.MATOMO_TOKEN
);

// Track server-side event
function trackEvent(category, action, name, value) {
  matomo.track({
    url: `https://${process.env.IO_PROJECT}.embrapa.io`,
    action_name: `${category} - ${action}`,
    e_c: category,
    e_a: action,
    e_n: name,
    e_v: value,
    dimension1: process.env.IO_STAGE,
    dimension2: process.env.IO_VERSION,
  });
}

module.exports = { trackEvent };
```

#### PHP / Slim (Backend API)

```php
<?php
// src/Bootstrap/MatomoInitializer.php

declare(strict_types=1);

namespace App\Bootstrap;

use MatomoTracker;

/**
 * Matomo Initializer - Embrapa I/O Compliant
 *
 * Usa APENAS variáveis de .env.io: MATOMO_ID, MATOMO_TOKEN, IO_STAGE, IO_VERSION
 * URL do Matomo é hardcoded (não criar variáveis adicionais)
 */
class MatomoInitializer
{
    private static bool $initialized = false;
    private static bool $enabled = false;
    private static ?MatomoTracker $tracker = null;

    private const MATOMO_URL = 'https://hit.embrapa.io/';

    public static function initialize(): void
    {
        if (self::$initialized) {
            return;
        }

        self::$initialized = true;

        // MATOMO_ID vem do .env.io (fornecido pela plataforma)
        $siteId = $_ENV['MATOMO_ID'] ?? '';
        if ($siteId === '') {
            throw new \RuntimeException('MATOMO_ID não definida');
        }

        $token = $_ENV['MATOMO_TOKEN'] ?? '';
        if ($token === '') {
            throw new \RuntimeException('MATOMO_TOKEN não definida');
        }

        self::$enabled = true;

        self::$tracker = new MatomoTracker((int) $siteId, self::MATOMO_URL);
        self::$tracker->setTokenAuth($token);

        // Custom dimensions obrigatórias
        $stage = $_ENV['IO_STAGE'] ?? throw new \RuntimeException('IO_STAGE não definida');
        $version = $_ENV['IO_VERSION'] ?? throw new \RuntimeException('IO_VERSION não definida');

        self::$tracker->setCustomDimension(1, $stage);
        self::$tracker->setCustomDimension(2, $version);
    }

    public static function isEnabled(): bool
    {
        return self::$enabled;
    }

    public static function getTracker(): ?MatomoTracker
    {
        return self::$tracker;
    }

    public static function trackEvent(string $category, string $action, ?string $name = null, ?float $value = null): void
    {
        if (!self::$enabled || self::$tracker === null) {
            return;
        }

        self::$tracker->doTrackEvent($category, $action, $name, $value);
    }

    public static function trackPageView(string $documentTitle): void
    {
        if (!self::$enabled || self::$tracker === null) {
            return;
        }

        self::$tracker->doTrackPageView($documentTitle);
    }
}
```

```php
<?php
// src/Middleware/MatomoMiddleware.php

declare(strict_types=1);

namespace App\Middleware;

use App\Bootstrap\MatomoInitializer;
use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\ServerRequestInterface;
use Psr\Http\Server\MiddlewareInterface;
use Psr\Http\Server\RequestHandlerInterface;

/**
 * Matomo Tracking Middleware - Embrapa I/O Compliant
 *
 * Rastreia automaticamente todas as requisições da API
 */
class MatomoMiddleware implements MiddlewareInterface
{
    public function process(ServerRequestInterface $request, RequestHandlerInterface $handler): ResponseInterface
    {
        $startTime = microtime(true);

        $response = $handler->handle($request);

        // Rastrear apenas se Matomo estiver habilitado
        if (MatomoInitializer::isEnabled()) {
            $this->trackRequest($request, $response, $startTime);
        }

        return $response;
    }

    private function trackRequest(ServerRequestInterface $request, ResponseInterface $response, float $startTime): void
    {
        $tracker = MatomoInitializer::getTracker();
        if ($tracker === null) {
            return;
        }

        $method = $request->getMethod();
        $path = $request->getUri()->getPath();
        $statusCode = $response->getStatusCode();
        $duration = (microtime(true) - $startTime) * 1000; // em ms

        // Configurar informações da requisição
        $tracker->setUrl((string) $request->getUri());
        $tracker->setIp($this->getClientIp($request));

        if ($request->hasHeader('User-Agent')) {
            $tracker->setUserAgent($request->getHeaderLine('User-Agent'));
        }

        // Rastrear como page view com título descritivo
        $tracker->doTrackPageView("{$method} {$path} [{$statusCode}]");

        // Rastrear métricas de performance como evento
        $tracker->doTrackEvent(
            'API',
            $method,
            $path,
            $duration
        );
    }

    private function getClientIp(ServerRequestInterface $request): string
    {
        $serverParams = $request->getServerParams();

        // Verificar headers de proxy
        $headers = ['HTTP_X_FORWARDED_FOR', 'HTTP_X_REAL_IP', 'REMOTE_ADDR'];

        foreach ($headers as $header) {
            if (!empty($serverParams[$header])) {
                $ips = explode(',', $serverParams[$header]);
                return trim($ips[0]);
            }
        }

        return '127.0.0.1';
    }
}
```

```php
<?php
// public/index.php (entry point)

// Inicializar Matomo APÓS Sentry
MatomoInitializer::initialize();

// Adicionar middleware ao Slim
$app->add(new MatomoMiddleware());

// ... resto da aplicação
```

### Custom Dimensions

| ID | Dimension | Exemplo |
|----|-----------|---------|
| 1  | Stage     | development, alpha, beta, release |
| 2  | Version   | 1.0.0, 1.2.3-beta |

### Variáveis de Ambiente

```ini
# .env.io (fornecido pela plataforma)
MATOMO_ID=42
MATOMO_TOKEN=abc123xyz456
```

---

## 🔍 SonarQube (Qualidade de Código)

### Configuração

#### Arquivo sonar-project.properties

```properties
sonar.projectKey=${IO_PROJECT}_${IO_APP}
sonar.projectName=${IO_PROJECT} ${IO_APP}
sonar.projectVersion=${IO_VERSION}
sonar.sources=src
sonar.exclusions=node_modules/**,dist/**,build/**,vendor/**,storage/**
sonar.sourceEncoding=UTF-8

# Node.js / JavaScript
sonar.javascript.lcov.reportPaths=coverage/lcov.info

# PHP
sonar.php.coverage.reportPaths=coverage/coverage-clover.xml

# .NET
sonar.cs.opencover.reportsPaths=coverage/coverage.opencover.xml
```

#### CI/CD Integration (GitHub Actions)

```yaml
# .github/workflows/sonarqube.yml
name: SonarQube Analysis

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  sonarqube:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: SonarQube Scan
        uses: sonarsource/sonarqube-scan-action@master
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
```

### Thresholds Recomendados

| Métrica | Threshold |
|---------|-----------|
| Coverage | ≥80% |
| Duplications | ≤3% |
| Maintainability Rating | ≤A |
| Reliability Rating | ≤A |
| Security Rating | ≤A |

---

## 📝 Grafana Loki (Logs Centralizados)

### Configuração Docker Compose

```yaml
services:
  api:
    logging:
      driver: loki
      options:
        loki-url: "https://loki.embrapa.io/loki/api/v1/push"
        loki-external-labels: "project=${IO_PROJECT},app=${IO_APP},stage=${IO_STAGE},service=api"
        loki-retries: 2
        loki-batch-size: 400
```

### Labels Padrão

| Label | Fonte | Exemplo |
|-------|-------|---------|
| project | ${IO_PROJECT} | meu-projeto |
| app | ${IO_APP} | minha-app |
| stage | ${IO_STAGE} | development |
| service | Nome do serviço | api, frontend, db |

### Consultas LogQL

#### Ver logs de um serviço

```logql
{project="meu-projeto", app="minha-app", stage="development", service="api"}
```

#### Filtrar por nível de log

```logql
{project="meu-projeto"} |= "ERROR"
```

#### Rate de erros

```logql
rate({project="meu-projeto"} |= "ERROR" [5m])
```

### Structured Logging (Node.js)

```bash
npm install winston
```

```javascript
// src/config/logger.js
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  defaultMeta: {
    project: process.env.IO_PROJECT,
    app: process.env.IO_APP,
    stage: process.env.IO_STAGE,
  },
  transports: [
    new winston.transports.Console(),
  ],
});

module.exports = logger;
```

```javascript
// Uso
logger.info('User logged in', { userId: 123 });
logger.error('Database connection failed', { error: err.message });
```

---

## 🔄 Matriz de Integração

| Stack | Sentry | Matomo | SonarQube | Loki |
|-------|--------|--------|-----------|------|
| Node.js + Express + MongoDB | ✅ | ✅ | ✅ | ✅ |
| Node.js + Express + PostgreSQL | ✅ | ✅ | ✅ | ✅ |
| Vue.js + Vuetify | ✅ | ✅ | ✅ | ✅ |
| React | ✅ | ✅ | ✅ | ✅ |
| React Native | ✅ | ⚠️ | ✅ | ❌ |
| .NET Blazor | ✅ | ✅ | ✅ | ✅ |
| PHP + Laravel | ✅ | ✅ | ✅ | ✅ |

**Legenda**:
- ✅ Totalmente suportado
- ⚠️ Suporte parcial
- ❌ Não suportado

---

## 📋 Checklist de Integração

### Sentry
- [ ] Pacote instalado
- [ ] DSN configurado via variável
- [ ] Release tracking com IO_VERSION
- [ ] Environment configurado com IO_STAGE
- [ ] Teste de integração executado

### Matomo
- [ ] Script de tracking adicionado (frontend)
- [ ] Site ID configurado
- [ ] Custom dimensions implementadas
- [ ] Events tracking implementado (opcional)
- [ ] Token configurado (backend, se aplicável)

### SonarQube
- [ ] sonar-project.properties criado
- [ ] Coverage configurado
- [ ] CI/CD integration configurada
- [ ] Quality Gates definidos
- [ ] Projeto criado no SonarQube

### Grafana Loki
- [ ] Logging driver configurado
- [ ] External labels definidos
- [ ] Structured logging implementado
- [ ] Queries de teste validadas
- [ ] Dashboards criados (opcional)

---

**Versão**: 1.1
**Última atualização**: 2026-01-20
**Autor**: Módulo Embrapa I/O BMAD
