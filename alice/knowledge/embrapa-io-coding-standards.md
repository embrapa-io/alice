# Padrões de Codificação Embrapa I/O

Referência de padrões de codificação obrigatórios para conformidade com a plataforma Embrapa I/O.

---

## Grafia Correta em Português Brasileiro

SEMPRE usar acentuação e caracteres especiais corretos do português brasileiro em TODOS os textos gerados, incluindo:
- Comentários em arquivos (.env, docker-compose.yaml, Dockerfile, etc.)
- Documentação (README.md, relatórios, etc.)
- Mensagens e outputs para o usuário

### Exemplos Obrigatórios

❌ ERRADO: "Variaveis de Ambiente da Aplicacao"
✅ CORRETO: "Variáveis de Ambiente da Aplicação"

❌ ERRADO: "Configuracoes do Banco de Dados"
✅ CORRETO: "Configurações do Banco de Dados"

❌ ERRADO: "Convencao de nomenclatura"
✅ CORRETO: "Convenção de nomenclatura"

Esta regra é INEGOCIÁVEL - texto sem acentuação é considerado ERRO GRAVE.

---

## Variáveis de Ambiente Sem Fallback

NUNCA gerar código com valores padrão (fallback) para variáveis de ambiente. Todas as variáveis DEVEM ser obrigatórias - se não estiverem definidas, o código DEVE falhar explicitamente.

### PHP

❌ ERRADO (com fallback):
```php
$dbHost = getenv('DB_HOST') ?: 'db';
```

✅ CORRETO (sem fallback, falha se não definida):
```php
$dbHost = getenv('DB_HOST');
if ($dbHost === false) throw new Exception('DB_HOST não definida');
```

### Node.js

❌ ERRADO (com fallback):
```javascript
const dbHost = process.env.DB_HOST || 'localhost';
```

✅ CORRETO (sem fallback, falha se não definida):
```javascript
if (!process.env.DB_HOST) throw new Error('DB_HOST não definida');
const dbHost = process.env.DB_HOST;
```

### Python

❌ ERRADO (com fallback):
```python
db_host = os.getenv('DB_HOST', 'localhost')
```

✅ CORRETO (sem fallback, falha se não definida):
```python
db_host = os.environ['DB_HOST']  # Lança KeyError se não definida
```

### Motivo

Fallbacks mascaram erros de configuração e causam comportamentos inesperados em produção. O usuário DEVE configurar todas as variáveis no `.env`.

---

## Arquivo LICENSE

O arquivo LICENSE DEVE sempre conter EXATAMENTE o seguinte conteúdo (substituindo YYYY pelo ano corrente):

```
Copyright ⓒ YYYY Brazilian Agricultural Research Corporation (Embrapa). All rights reserved.
```

❌ ERRADO: BSD-3-Clause, MIT, Apache, GPL ou qualquer outra licença
✅ CORRETO: Apenas o texto de copyright da Embrapa acima

Projetos Embrapa I/O são propriedade da Embrapa e NÃO são open source.

---

## Integrações Sentry e Matomo - Exceção de Código Funcional

As integrações com Sentry e Matomo são OBRIGATÓRIAS para codebases com código-fonte e TÊM PRIORIDADE sobre a regra de não modificar código funcional.

### Quando o projeto é um codebase com código-fonte (PHP, Node.js, Vue.js, React, etc.), DEVE-SE:

1. Criar/modificar arquivos de configuração para Sentry (SentryInitializer, sentry.js, etc.)
2. Criar/modificar arquivos de configuração para Matomo (MatomoInitializer, middleware, plugins, etc.)
3. Adicionar inicialização no entry point da aplicação (index.php, app.js, main.js, etc.)

### NÃO APLICÁVEL para serviços de prateleira:

- Nginx Proxy Manager, Directus, Strapi, MinIO, n8n, etc.
- Qualquer serviço que usa imagem Docker oficial sem código-fonte customizado

### OBRIGATÓRIO para codebases com código-fonte:

- Aplicações PHP (Slim, Laravel, etc.)
- Aplicações Node.js (Express, Fastify, etc.)
- Frontends (Vue.js, React, Angular, etc.)
- APIs e backends customizados
