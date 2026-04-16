# Workflows Embrapa I/O

## 🎯 Visão Geral

Este documento define os workflows BMAD para garantir conformidade com a plataforma Embrapa I/O. Os workflows são organizados em 4 categorias e adaptam-se ao tipo de projeto.

## 🔄 Adaptação por Tipo de Projeto

### Tipos de Projeto

1. **NEW** 🆕 - Projeto novo do zero
   - **Característica**: Não tem docker-compose.yaml ou .embrapa/settings.json
   - **Abordagem**: Scaffolding completo com todas as decisões
   - **Workflows aplicáveis**: CREATE workflows

2. **EXISTING** 📦 - Projeto existente sem conformidade
   - **Característica**: Tem código mas não está conforme Embrapa I/O
   - **Abordagem**: Adicionar camada de conformidade ao código existente
   - **Workflows aplicáveis**: ADD workflows + VALIDATE workflows

3. **ALREADY_COMPLIANT** ✅ - Projeto já conforme
   - **Característica**: Tem .embrapa/settings.json com validation_score
   - **Abordagem**: Validação e sugestões de melhoria
   - **Workflows aplicáveis**: VALIDATE workflows

### Detecção Automática de Tipo

```javascript
function detectProjectType(projectPath) {
  const hasDockerCompose = fs.existsSync(`${projectPath}/docker-compose.yaml`);
  const hasSettings = fs.existsSync(`${projectPath}/.embrapa/settings.json`);
  const hasEnvIo = fs.existsSync(`${projectPath}/.env.io.example`);

  if (hasSettings && hasEnvIo) {
    return 'ALREADY_COMPLIANT';
  } else if (hasDockerCompose) {
    return 'EXISTING';
  } else {
    return 'NEW';
  }
}
```

## 📋 CATEGORIA 1: VALIDATE Workflows (Prioridade #1)

### 1.1 validate-compliance

**Objetivo**: Validação completa de conformidade Embrapa I/O

**Entrada**:
- Caminho do projeto
- Opções de validação (níveis de severidade)

**Saída**:
- Relatório JSON completo
- Compliance score (HIGH/MEDIUM/LOW)
- Lista de erros por severidade
- Sugestões de correção

**Processo**:
1. Detectar tipo de projeto
2. Executar todas as 5 validações
3. Calcular compliance score
4. Gerar relatório detalhado
5. Sugerir próximos passos

**Tipos de projeto**: EXISTING, ALREADY_COMPLIANT

---

### 1.2 validate-docker-compose

**Objetivo**: Validação específica do docker-compose.yaml

**Entrada**:
- Caminho do docker-compose.yaml

**Saída**:
- Lista de erros de docker-compose
- Status: compliant|partial|non-compliant

**Validações**:
- Ausência de campo 'version'
- Network 'stack' externa com nome correto
- Volumes externos
- Serviços conectados à network
- Ausência de container_name
- Healthchecks em serviços de longa duração
- Serviços CLI com profiles

**Tipos de projeto**: EXISTING, ALREADY_COMPLIANT

---

### 1.3 validate-env-files

**Objetivo**: Validação dos arquivos .env

**Entrada**:
- Caminhos .env.io.example e .env.example

**Saída**:
- Lista de erros de variáveis
- Variáveis duplicadas
- Variáveis ausentes

**Validações**:
- Existência dos dois arquivos
- Variáveis obrigatórias em .env.io
- Não duplicação entre arquivos
- Convenção de nomenclatura
- Ausência de espaços/aspas
- .gitignore correto

**Tipos de projeto**: EXISTING, ALREADY_COMPLIANT

---

### 1.4 validate-settings

**Objetivo**: Validação do .embrapa/settings.json

**Entrada**:
- Caminho .embrapa/settings.json

**Saída**:
- Lista de erros de estrutura
- Campos ausentes
- Valores inválidos

**Validações**:
- Existência do arquivo
- JSON válido
- Campos obrigatórios presentes
- Valores dentro dos enumerados
- Data de validação atualizada
- Configurações de integração completas

**Tipos de projeto**: EXISTING, ALREADY_COMPLIANT

---

### 1.5 validate-integrations

**Objetivo**: Validação das integrações (Sentry, Matomo, etc.)

**Entrada**:
- Caminho do projeto
- Lista de integrações habilitadas

**Saída**:
- Status de cada integração
- Configurações ausentes
- Recomendações

**Validações**:
- Sentry: DSN configurado, release correto
- Matomo: Tracking implementado, custom dimensions
- SonarQube: sonar-project.properties existente
- Loki: Logging driver configurado

**Tipos de projeto**: EXISTING, ALREADY_COMPLIANT

---

### 1.6 generate-compliance-report

**Objetivo**: Gerar relatório de conformidade para humanos

**Entrada**:
- Resultados da validate-compliance

**Saída**:
- README de conformidade em Markdown
- Dashboard visual (opcional)
- Relatório executivo

**Formato**:
```markdown
# Relatório de Conformidade Embrapa I/O

**Projeto**: Nome do Projeto
**Data**: 2025-10-06
**Score**: 🟢 HIGH | 🟡 MEDIUM | 🔴 LOW

## Resumo Executivo
- ✅ 25 validações passaram
- ⚠️ 3 erros HIGH encontrados
- ℹ️ 5 sugestões de melhoria

## Detalhamento por Categoria
### docker-compose.yaml: 🟢 Compliant
### Arquivos .env: 🟡 Parcial
...
```

**Tipos de projeto**: EXISTING, ALREADY_COMPLIANT

---

## 📋 CATEGORIA 2: CREATE Workflows (Prioridade #2)

### 2.1 create-nodejs-api

**Objetivo**: Scaffolding completo de API Node.js + Express

**Entrada**:
- Nome do projeto
- Tipo de banco (mongodb|postgresql)
- Portas desejadas
- Integrações opcionais

**Saída**:
- Estrutura de projeto completa
- docker-compose.yaml configurado
- .env files
- .embrapa/settings.json
- Código base com endpoints de exemplo

**Estrutura gerada**:
```
projeto/
├── docker-compose.yaml
├── .env.io.example
├── .env.example
├── .gitignore
├── .embrapa/
│   └── settings.json
├── src/
│   ├── index.js
│   ├── routes/
│   ├── models/
│   ├── controllers/
│   └── config/
│       ├── sentry.js
│       └── matomo.js
├── package.json
└── README.md
```

**Stack**:
- Node.js 20.x LTS
- Express 4.x
- MongoDB + Mongoose OU PostgreSQL + Sequelize
- Sentry + Matomo integrados

**Tipos de projeto**: NEW

---

### 2.2 create-vuejs-frontend

**Objetivo**: Scaffolding de frontend Vue.js + Vuetify

**Entrada**:
- Nome do projeto
- API backend URL
- Recursos opcionais (PWA, i18n)

**Saída**:
- Estrutura Vue.js 3.x
- docker-compose.yaml com Nginx
- .env files
- Tema verde Embrapa
- Logo da Embrapa integrada

**Estrutura gerada**:
```
projeto/
├── docker-compose.yaml
├── .env.io.example
├── .env.example
├── .embrapa/
│   └── settings.json
├── src/
│   ├── main.js
│   ├── App.vue
│   ├── router/
│   ├── store/
│   ├── views/
│   ├── components/
│   └── assets/
│       └── logo-embrapa.png
├── public/
├── package.json
└── vite.config.js
```

**Stack**:
- Vue.js 3.x
- Vuetify 3.x
- Vite
- Axios + Dexie.js (PWA)
- Sentry + Matomo integrados

**Tipos de projeto**: NEW

---

### 2.3 create-react-frontend

**Objetivo**: Scaffolding de frontend React

**Entrada**:
- Nome do projeto
- UI library (MUI|Ant Design|none)
- API backend URL

**Saída**:
- Estrutura React 18.x
- docker-compose.yaml
- Tema verde Embrapa

**Stack**:
- React 18.x
- UI library escolhida
- Vite
- Sentry + Matomo integrados

**Tipos de projeto**: NEW

---

### 2.4 create-reactnative-mobile

**Objetivo**: Scaffolding de app React Native

**Entrada**:
- Nome do projeto
- Plataformas (iOS|Android|both)
- API backend URL

**Saída**:
- Estrutura React Native
- docker-compose.yaml para backend de suporte
- Configurações iOS/Android

**Stack**:
- React Native latest
- Expo (opcional)
- Sentry integrado

**Tipos de projeto**: NEW

---

### 2.5 create-dotnet-app

**Objetivo**: Scaffolding de app .NET Blazor

**Entrada**:
- Nome do projeto
- Tipo (Server|WebAssembly|Hybrid)
- Banco de dados

**Saída**:
- Estrutura .NET 8.x
- docker-compose.yaml
- Integração Sentry

**Stack**:
- .NET 8.x
- Blazor
- Entity Framework Core

**Tipos de projeto**: NEW

---

### 2.6 create-php-app

**Objetivo**: Scaffolding de app PHP

**Entrada**:
- Nome do projeto
- Framework (Laravel|none)
- Banco de dados

**Saída**:
- Estrutura PHP 8.x
- docker-compose.yaml
- Nginx + PHP-FPM

**Stack**:
- PHP 8.2
- Laravel (opcional)
- Composer

**Tipos de projeto**: NEW

---

## 📋 CATEGORIA 3: ADD Workflows (Prioridade #3)

### 3.1 add-embrapa-compliance

**Objetivo**: Adicionar conformidade Embrapa I/O a projeto existente

**Entrada**:
- Caminho do projeto existente
- Tipo detectado automaticamente

**Saída**:
- docker-compose.yaml ajustado/criado
- .env files criados
- .embrapa/settings.json criado
- README atualizado

**Processo**:
1. Analisar projeto existente (stack, estrutura)
2. Detectar banco de dados e serviços
3. Gerar docker-compose.yaml conformante
4. Criar .env files sem conflitos
5. Gerar .embrapa/settings.json com metadados
6. Validar resultado
7. Gerar relatório de mudanças

**Adaptações**:
- Preserva código existente
- Adiciona apenas camada de conformidade
- Sugere refactorings opcionais

**Tipos de projeto**: EXISTING

---

### 3.2 add-sentry-integration

**Objetivo**: Adicionar integração Sentry a projeto existente

**Entrada**:
- Caminho do projeto
- Stack detectada

**Saída**:
- Código Sentry integrado
- SENTRY_DSN em .env.io
- Configuração em settings.json

**Suporte**:
- Node.js: @sentry/node
- React: @sentry/react
- Vue.js: @sentry/vue
- .NET: Sentry.AspNetCore
- PHP: sentry/sentry

**Tipos de projeto**: EXISTING, ALREADY_COMPLIANT

---

### 3.3 add-matomo-integration

**Objetivo**: Adicionar analytics Matomo

**Entrada**:
- Caminho do projeto
- Tipo (frontend|backend)

**Saída**:
- Código de tracking
- MATOMO_ID e MATOMO_TOKEN em .env.io
- Custom dimensions configuradas

**Tipos de projeto**: EXISTING, ALREADY_COMPLIANT

---

### 3.4 add-sonarqube-integration

**Objetivo**: Adicionar análise SonarQube

**Entrada**:
- Caminho do projeto
- Stack detectada

**Saída**:
- sonar-project.properties
- Integração com CI/CD
- Configuração em settings.json

**Tipos de projeto**: EXISTING, ALREADY_COMPLIANT

---

### 3.5 add-loki-integration

**Objetivo**: Adicionar logs centralizados Grafana Loki

**Entrada**:
- Caminho do projeto
- docker-compose.yaml

**Saída**:
- Logging driver configurado
- Labels externos definidos
- Documentação de acesso

**Tipos de projeto**: EXISTING, ALREADY_COMPLIANT

---

## 📋 CATEGORIA 4: MIGRATE Workflows (Prioridade #4)

### 4.1 migrate-to-compliance

**Objetivo**: Migração assistida de projeto não-conforme

**Entrada**:
- Caminho do projeto
- Resultados de validação

**Saída**:
- Plano de migração passo-a-passo
- Backup do estado atual
- Migração executada
- Validação pós-migração

**Processo**:
1. Executar validate-compliance
2. Gerar plano de correções
3. Criar backup do projeto
4. Aplicar correções por severidade (CRITICAL → LOW)
5. Validar após cada correção
6. Gerar relatório de migração

**Tipos de projeto**: EXISTING

---

### 4.2 migrate-stage

**Objetivo**: Migrar projeto entre stages

**Entrada**:
- Stage origem (development|alpha|beta)
- Stage destino (alpha|beta|release)

**Saída**:
- Configurações atualizadas
- .env.io atualizado
- settings.json atualizado
- Tag git criada

**Processo**:
1. Validar conformidade no stage atual
2. Verificar requisitos do stage destino
3. Atualizar variáveis de ambiente
4. Atualizar settings.json
5. Criar tag de versão
6. Gerar checklist de deploy

**Tipos de projeto**: ALREADY_COMPLIANT

---

## 🔀 Matriz de Compatibilidade

| Workflow | NEW | EXISTING | ALREADY_COMPLIANT |
|----------|-----|----------|-------------------|
| validate-compliance | ❌ | ✅ | ✅ |
| validate-docker-compose | ❌ | ✅ | ✅ |
| validate-env-files | ❌ | ✅ | ✅ |
| validate-settings | ❌ | ✅ | ✅ |
| validate-integrations | ❌ | ✅ | ✅ |
| generate-compliance-report | ❌ | ✅ | ✅ |
| create-nodejs-api | ✅ | ❌ | ❌ |
| create-vuejs-frontend | ✅ | ❌ | ❌ |
| create-react-frontend | ✅ | ❌ | ❌ |
| create-reactnative-mobile | ✅ | ❌ | ❌ |
| create-dotnet-app | ✅ | ❌ | ❌ |
| create-php-app | ✅ | ❌ | ❌ |
| add-embrapa-compliance | ❌ | ✅ | ❌ |
| add-sentry-integration | ❌ | ✅ | ✅ |
| add-matomo-integration | ❌ | ✅ | ✅ |
| add-sonarqube-integration | ❌ | ✅ | ✅ |
| add-loki-integration | ❌ | ✅ | ✅ |
| migrate-to-compliance | ❌ | ✅ | ❌ |
| migrate-stage | ❌ | ❌ | ✅ |

## 🎭 Integração com Personas

### Developer Júnior
- **Preferência**: CREATE workflows com modo tutorial
- **Características**: Step-by-step detalhado, explicações inline
- **Workflow recomendado**: create-nodejs-api com tutorial mode

### Tech Lead
- **Preferência**: VALIDATE workflows com relatórios executivos
- **Características**: Visão consolidada, priorização automática
- **Workflow recomendado**: generate-compliance-report

### DevOps Engineer
- **Preferência**: MIGRATE workflows e ADD integrations
- **Características**: Automação, CI/CD, monitoramento
- **Workflow recomendado**: add-loki-integration, migrate-stage

---

**Versão**: 1.0
**Última atualização**: 2025-12-15
**Autor**: Módulo Embrapa I/O BMAD
