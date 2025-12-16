# Validação de Conformidade Embrapa I/O

## 🎯 Objetivo

Este documento define as regras de validação para garantir que um projeto está em conformidade com os padrões da plataforma Embrapa I/O.

## 📊 Sistema de Scoring

Cada projeto recebe um **Compliance Score** baseado em validações de severidade:

| Score | Severidade | Critério |
|-------|-----------|----------|
| **HIGH** | ✅ Totalmente conforme | 0 erros CRITICAL, 0 erros HIGH |
| **MEDIUM** | ⚠️ Conformidade parcial | 0 erros CRITICAL, ≤3 erros HIGH |
| **LOW** | ❌ Não conforme | ≥1 erro CRITICAL ou >3 erros HIGH |

### Níveis de Severidade

- **CRITICAL** 🚨: Impede o deployment, quebra funcionalidade essencial
- **HIGH** ⚠️: Viola padrões obrigatórios, pode causar problemas
- **MEDIUM** ℹ️: Viola boas práticas, deve ser corrigido
- **LOW** 💡: Sugestões de melhoria, opcional

## 🔍 Validação 1: docker-compose.yaml

### CRITICAL Errors

#### 1.1 Arquivo não existe
```
SEVERITY: CRITICAL
MESSAGE: "Arquivo docker-compose.yaml não encontrado na raiz do projeto"
SOLUTION: "Criar docker-compose.yaml na raiz do projeto"
```

#### 1.2 Campo 'version' presente
```
SEVERITY: CRITICAL
MESSAGE: "Campo 'version' encontrado no docker-compose.yaml (obsoleto)"
SOLUTION: "Remover campo 'version' do início do arquivo"
```

#### 1.3 Network 'stack' não existe
```
SEVERITY: CRITICAL
MESSAGE: "Network 'stack' não declarada em 'networks:'"
SOLUTION: "Adicionar network externa 'stack' com name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}"
```

#### 1.4 Network 'stack' não é externa
```
SEVERITY: CRITICAL
MESSAGE: "Network 'stack' não está marcada como 'external: true'"
SOLUTION: "Adicionar 'external: true' na definição da network 'stack'"
```

#### 1.5 Nome da network incorreto
```
SEVERITY: CRITICAL
MESSAGE: "Network 'stack' deve ter name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}"
SOLUTION: "Corrigir o 'name' da network para usar as variáveis corretas"
```

### HIGH Errors

#### 1.6 Serviço não conectado à network 'stack'
```
SEVERITY: HIGH
MESSAGE: "Serviço '[service_name]' não está conectado à network 'stack'"
SOLUTION: "Adicionar 'stack' em 'networks:' do serviço"
```

#### 1.7 Uso de 'container_name' (PROIBIDO)
```
SEVERITY: HIGH
MESSAGE: "Serviço '[service_name]' usa 'container_name' (não permitido)"
SOLUTION: "Remover campo 'container_name' do serviço"
REASON: "O nome dos containers é automaticamente definido pelo COMPOSE_PROJECT_NAME, que é injetado pela plataforma Embrapa I/O. Usar container_name quebra a convenção de nomenclatura e pode causar conflitos entre ambientes."
```

**⚠️ IMPORTANTE**: O atributo `container_name` é **estritamente proibido** em todos os serviços do docker-compose.yaml. A plataforma Embrapa I/O utiliza a variável `COMPOSE_PROJECT_NAME` (definida no `.env.io`) para nomear automaticamente os containers seguindo o padrão `{IO_PROJECT}_{IO_APP}_{IO_STAGE}_{service}`. Definir `container_name` manualmente:
- Quebra a convenção de nomenclatura da plataforma
- Impede o correto isolamento entre ambientes (development, alpha, beta, release)
- Pode causar conflitos de nomes entre diferentes deploys
- Impossibilita a orquestração automatizada pela plataforma

#### 1.8 Volumes não externos
```
SEVERITY: HIGH
MESSAGE: "Volume '[volume_name]' não está marcado como 'external: true'"
SOLUTION: "Marcar volume como externo e definir 'name' com padrão correto"
```

#### 1.9 Serviço longa duração sem 'restart'
```
SEVERITY: HIGH
MESSAGE: "Serviço '[service_name]' de longa duração sem 'restart: unless-stopped'"
SOLUTION: "Adicionar 'restart: unless-stopped' ao serviço"
```

#### 1.10 Serviço longa duração sem 'healthcheck'
```
SEVERITY: HIGH
MESSAGE: "Serviço '[service_name]' de longa duração sem 'healthcheck'"
SOLUTION: "Implementar healthcheck adequado para o serviço"
```

### MEDIUM Errors

#### 1.11 Porta hardcoded
```
SEVERITY: MEDIUM
MESSAGE: "Serviço '[service_name]' usa porta hardcoded ao invés de variável"
SOLUTION: "Usar variável de ambiente para mapeamento de porta: ${SERVICE_PORT}:80"
```

#### 1.12 Serviço CLI sem 'profiles'
```
SEVERITY: MEDIUM
MESSAGE: "Serviço CLI '[service_name]' sem 'profiles: [cli]'"
SOLUTION: "Adicionar 'profiles: [cli]' ao serviço"
```

#### 1.13 Volume backup não encontrado
```
SEVERITY: MEDIUM
MESSAGE: "Volume de backup não declarado (recomendado: backup_data)"
SOLUTION: "Adicionar volume externo 'backup_data' com name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}_backup"
```

### LOW Errors

#### 1.14 Faltam serviços CLI recomendados
```
SEVERITY: LOW
MESSAGE: "Serviços CLI recomendados não encontrados: backup, restore, sanitize"
SOLUTION: "Implementar serviços CLI conforme embrapa-io-fundamentals.md"
```

## 🔍 Validação 2: Arquivos .env

### CRITICAL Errors

#### 2.1 Arquivo .env.io.example não existe
```
SEVERITY: CRITICAL
MESSAGE: "Arquivo .env.io.example não encontrado na raiz do projeto"
SOLUTION: "Criar .env.io.example com as variáveis da plataforma"
```

#### 2.2 Arquivo .env.example não existe
```
SEVERITY: CRITICAL
MESSAGE: "Arquivo .env.example não encontrado na raiz do projeto"
SOLUTION: "Criar .env.example com as variáveis da aplicação"
```

#### 2.3 Variável de .env.io repetida em .env
```
SEVERITY: CRITICAL
MESSAGE: "Variável '[var_name]' de .env.io está duplicada em .env.example"
SOLUTION: "Remover '[var_name]' de .env.example (pertence ao .env.io)"
```

### HIGH Errors

#### 2.4 Variável obrigatória ausente em .env.io
```
SEVERITY: HIGH
MESSAGE: "Variável obrigatória '[var_name]' ausente em .env.io.example"
REQUIRED_VARS: ["IO_PROJECT", "IO_APP", "IO_STAGE", "IO_VERSION"]
SOLUTION: "Adicionar variável obrigatória ao .env.io.example"
```

#### 2.5 Valor com espaços ou aspas em .env
```
SEVERITY: CRITICAL
MESSAGE: "Variável '[var_name]' contém espaços ou aspas (não permitido)"
SOLUTION: "Remover aspas e espaços. Para valores complexos, usar: Base64 (recomendado), URL encoding, ou substituição de caracteres"
EXAMPLES:
  INVALID: MY_VAR="valor com espaços"
  INVALID: MY_VAR='valor'
  INVALID: MY_VAR=valor com espaços
  VALID: MY_VAR=valor_sem_espacos
  VALID: MY_VAR=TWV1IFZhbG9y (Base64)
  VALID: MY_VAR=valor%20encoded (URL encoding)
```

#### 2.6 Convenção de nomenclatura incorreta
```
SEVERITY: HIGH
MESSAGE: "Variável '[var_name]' não segue convenção ${IO_PROJECT}_${IO_APP}_${IO_STAGE}_[nome]"
SOLUTION: "Renomear variável seguindo a convenção correta"
```

### MEDIUM Errors

#### 2.7 .gitignore não ignora .env
```
SEVERITY: MEDIUM
MESSAGE: "Arquivo .env não está no .gitignore"
SOLUTION: "Adicionar '.env' e '.env.io' ao .gitignore"
```

#### 2.8 Variável sensível sem indicação
```
SEVERITY: MEDIUM
MESSAGE: "Variável '[var_name]' parece sensível mas não tem comentário de aviso"
SOLUTION: "Adicionar comentário: # SENSITIVE: não commitar valor real"
```

## 🔍 Validação 3: .embrapa/settings.json

### CRITICAL Errors

#### 3.1 Arquivo não existe
```
SEVERITY: CRITICAL
MESSAGE: "Arquivo .embrapa/settings.json não encontrado"
SOLUTION: "Criar .embrapa/settings.json com estrutura base"
```

#### 3.2 JSON inválido
```
SEVERITY: CRITICAL
MESSAGE: "Arquivo .embrapa/settings.json contém JSON inválido"
SOLUTION: "Corrigir sintaxe JSON do arquivo"
```

#### 3.3 Campo obrigatório ausente
```
SEVERITY: CRITICAL
MESSAGE: "Campo obrigatório '[field]' ausente no settings.json"
REQUIRED_FIELDS: [
  "boilerplate",
  "platform",
  "label",
  "description",
  "references",
  "maintainers",
  "variables",
  "orchestrators"
]
SOLUTION: "Adicionar campo obrigatório ao settings.json"
```

### HIGH Errors

#### 3.4 Platform inválida
```
SEVERITY: HIGH
MESSAGE: "platform '[value]' inválida"
VALID_VALUES: ["android", "apple", "dart", "dotnet", "electron", "elixir", "flutter", "go", "java", "javascript", "kotlin", "native", "node", "php", "python", "react-native", "ruby", "rust", "unity", "unreal"]
SOLUTION: "Usar um dos valores válidos para platform"
```

#### 3.5 Variables.default ausente ou vazio
```
SEVERITY: HIGH
MESSAGE: "variables.default ausente ou vazio no settings.json"
SOLUTION: "Adicionar array variables.default com todas as variáveis do .env"
```

#### 3.6 Tipo de variável inválido
```
SEVERITY: HIGH
MESSAGE: "Tipo '[type]' inválido para variável '[name]'"
VALID_VALUES: ["TEXT", "PASSWORD", "SECRET", "PORT", "VOLUME", "EMPTY"]
SOLUTION: "Usar um dos tipos válidos de variável"
```

### MEDIUM Errors

#### 3.7 Variável com espaços ou aspas
```
SEVERITY: HIGH
MESSAGE: "Variável '[name]' contém espaços ou aspas no valor"
SOLUTION: "Remover espaços e aspas. Para valores complexos, usar: Base64 (recomendado), URL encoding, ou substituição de caracteres"
```

#### 3.8 References vazio
```
SEVERITY: MEDIUM
MESSAGE: "Array references está vazio"
SOLUTION: "Adicionar referências técnicas relevantes ao projeto"
```

#### 3.9 Formato de telefone inválido em maintainers
```
SEVERITY: MEDIUM
MESSAGE: "Campo 'phone' do mantenedor '[name]' não está no formato correto"
EXPECTED_FORMAT: "+DDI (DDD) X XXXX-XXXX"
REGEX: "^\+\d{1,3} \(\d{2}\) \d \d{4}-\d{4}$"
EXAMPLE: "+55 (67) 9 8111-8060"
SOLUTION: "Corrigir formato do telefone para: +DDI (DDD) X XXXX-XXXX"
NOTES:
  - DDI: Código internacional (1 a 3 dígitos, ex: 55 para Brasil)
  - DDD: Código de área entre parênteses (2 dígitos)
  - Espaços obrigatórios após DDI e após DDD
  - Formato do número: X XXXX-XXXX (9 dígitos com hífen)
```

## 🔍 Validação 4: Integrações

### HIGH Errors

#### 4.1 Sentry configurado mas sem DSN
```
SEVERITY: HIGH
MESSAGE: "Sentry habilitado no settings.json mas SENTRY_DSN não encontrado no código"
SOLUTION: "Implementar configuração do Sentry conforme embrapa-io-fundamentals.md"
```

#### 4.2 Matomo configurado mas sem tracking
```
SEVERITY: HIGH
MESSAGE: "Matomo habilitado mas código de tracking não encontrado"
SOLUTION: "Implementar tracking do Matomo conforme embrapa-io-fundamentals.md"
```

### MEDIUM Errors

#### 4.3 Logo da Embrapa não encontrada
```
SEVERITY: MEDIUM
MESSAGE: "Logo da Embrapa não encontrada em projeto com interface visual"
SOLUTION: "Adicionar logo da Embrapa conforme diretrizes de UI"
```

#### 4.4 SonarQube recomendado mas não configurado
```
SEVERITY: MEDIUM
MESSAGE: "Projeto [type] recomenda SonarQube mas não está configurado"
SOLUTION: "Configurar SonarQube ou documentar motivo da não-configuração"
```

### LOW Errors

#### 4.5 Grafana Loki não configurado
```
SEVERITY: LOW
MESSAGE: "Logs centralizados com Loki não configurados (recomendado)"
SOLUTION: "Considerar configurar Grafana Loki para logs centralizados"
```

## 🔍 Validação 5: Estrutura de Projeto

### MEDIUM Errors

#### 5.1 README.md ausente
```
SEVERITY: MEDIUM
MESSAGE: "Arquivo README.md não encontrado"
SOLUTION: "Criar README.md com documentação do projeto"
```

#### 5.2 .gitignore ausente
```
SEVERITY: MEDIUM
MESSAGE: "Arquivo .gitignore não encontrado"
SOLUTION: "Criar .gitignore adequado para a stack utilizada"
```

### LOW Errors

#### 5.3 Documentação de desenvolvimento ausente
```
SEVERITY: LOW
MESSAGE: "Documentação de setup de ambiente de desenvolvimento não encontrada"
SOLUTION: "Adicionar seção no README.md ou criar DEVELOPMENT.md"
```

## 📋 Formato do Relatório de Validação

O relatório de validação deve seguir este formato:

```json
{
  "project": {
    "name": "Nome do Projeto",
    "path": "/caminho/para/projeto",
    "type": "backend|frontend|mobile|fullstack"
  },
  "validation": {
    "timestamp": "2025-10-06T14:30:00Z",
    "score": "HIGH|MEDIUM|LOW",
    "summary": {
      "critical": 0,
      "high": 2,
      "medium": 5,
      "low": 3,
      "total": 10
    }
  },
  "results": [
    {
      "id": "1.6",
      "severity": "HIGH",
      "category": "docker-compose",
      "message": "Serviço 'api' não está conectado à network 'stack'",
      "location": "docker-compose.yaml:15",
      "solution": "Adicionar 'stack' em 'networks:' do serviço",
      "auto_fixable": true
    }
  ],
  "recommendations": [
    {
      "type": "integration",
      "message": "Considerar adicionar SonarQube para análise de qualidade de código",
      "priority": "medium"
    }
  ],
  "compliance_status": {
    "docker_compose": "compliant|partial|non-compliant",
    "env_files": "compliant|partial|non-compliant",
    "settings_json": "compliant|partial|non-compliant",
    "integrations": "compliant|partial|non-compliant",
    "structure": "compliant|partial|non-compliant"
  }
}
```

## 🤖 Auto-Fix

Alguns erros podem ser corrigidos automaticamente. Marcar com `"auto_fixable": true`:

- Adicionar network 'stack' ao docker-compose.yaml
- Remover campo 'version' do docker-compose.yaml
- Adicionar 'external: true' a volumes
- Criar arquivos .env.example ausentes
- Adicionar entradas ao .gitignore
- Criar .embrapa/settings.json com estrutura base

## ✅ Checklist de Validação Completa

Executar todas as 5 validações:

- [ ] **Validação 1**: docker-compose.yaml (14 regras)
- [ ] **Validação 2**: Arquivos .env (8 regras)
- [ ] **Validação 3**: .embrapa/settings.json (9 regras)
- [ ] **Validação 4**: Integrações (5 regras)
- [ ] **Validação 5**: Estrutura de Projeto (3 regras)

**Total**: 39 regras de validação

## 📊 Exemplo de Score Calculation

```javascript
function calculateComplianceScore(results) {
  const critical = results.filter(r => r.severity === 'CRITICAL').length;
  const high = results.filter(r => r.severity === 'HIGH').length;

  if (critical > 0 || high > 3) {
    return 'LOW';
  } else if (high > 0) {
    return 'MEDIUM';
  } else {
    return 'HIGH';
  }
}
```

---

**Versão**: 1.0
**Última atualização**: 2025-12-15
**Autor**: Módulo Embrapa I/O BMAD
