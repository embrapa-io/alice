# Roadmap de Componentes - Módulo Embrapa I/O

**Versão do Módulo**: 1.26.4-5
**Atualizado em**: 2026-03-30
**Status Geral**: 🟢 Core Completo (85% completo)

## 📊 Visão Geral do Progresso

| Categoria | Total | Completos | Pendentes | % Completo |
|-----------|-------|-----------|-----------|------------|
| **Conhecimento** | 7 | 7 | 0 | 100% ✅ |
| **Templates** | 6 | 6 | 0 | 100% ✅ |
| **Workflows Core** | 5 | 5 | 0 | 100% ✅ |
| **Workflows Avançados** | 13 | 0 | 13 | 0% 🔴 |
| **Config & Docs** | 4 | 4 | 0 | 100% ✅ |
| **TOTAL** | 35 | 22 | 13 | 63% 🟢 |

> **Nota**: O core do módulo (conhecimento, templates, workflows de setup/validação) está 100% completo. Os workflows avançados (CREATE, ADD, MIGRATE) são extensões futuras planejadas.

---

## 🎯 Fase 1: Core Validation (Prioridade ALTA) ✅ COMPLETA

**Objetivo**: Sistema de validação completo e funcional

**Status**: ✅ COMPLETO (Dezembro 2025)

**Componentes**: 22 itens implementados

### ✅ Completos (22/22)

**Conhecimento (7/7):**
- [x] knowledge/embrapa-io-fundamentals.md
- [x] knowledge/embrapa-io-validation.md
- [x] knowledge/embrapa-io-workflows.md
- [x] knowledge/embrapa-io-deployment.md
- [x] knowledge/embrapa-io-stacks.md
- [x] knowledge/embrapa-io-integrations.md
- [x] knowledge/embrapa-io-integration-guide.md

**Workflows Setup (4/4):**
- [x] workflows/setup/generate-env-io/ (3 steps)
- [x] workflows/setup/generate-docker-compose/ (5 steps)
- [x] workflows/setup/generate-settings-json/ (4 steps)
- [x] workflows/setup/generate-license/ (1 step)

**Workflow Validate (1/1):**
- [x] workflows/validate/validate-compliance/ (5 steps)

**Templates (6/6):**
- [x] templates/docker-compose/base.yaml
- [x] templates/env/.env.example
- [x] templates/env/.env.io.example
- [x] templates/settings/settings-base.json
- [x] templates/settings/settings-nodejs.json
- [x] templates/settings/settings-frontend.json

**Config & Docs (4/4):**
- [x] config.yaml
- [x] embrapa-io-setup/ (skill de setup BMad-compliant)
- [x] README.md
- [x] ROADMAP.md

### 📝 Nota sobre Validações Granulares

As validações específicas (docker-compose, env-files, settings, integrations) foram consolidadas no workflow único `validate-compliance`, que executa todas as 40 regras de validação em 5 steps sequenciais. Esta abordagem simplifica o uso e mantém a coerência do sistema.

---

## 🚀 Fase 2: Scaffolding Node.js (Prioridade ALTA)

**Objetivo**: Criar projetos Node.js API conformes do zero

**Prazo Estimado**: 3 semanas

**Componentes**: 8 itens

### 🔨 Pendentes (8/8)

#### Templates (2)

- [ ] **templates/docker-compose/nodejs-api.yaml**
  - Services: api, db (MongoDB/PostgreSQL), backup, restore, sanitize
  - Healthchecks completos
  - **Prioridade**: ALTA
  - **Tempo estimado**: 2 dias

- [ ] **templates/env/.env.nodejs.example**
  - Variáveis específicas Node.js + Express
  - Variáveis de banco de dados
  - **Prioridade**: ALTA
  - **Tempo estimado**: 1 dia

#### Workflows CREATE (1)

- [ ] **workflows/create/create-nodejs-api/**
  - [ ] workflow.yaml
  - [ ] instructions.md
  - [ ] templates/ (código base)
    - [ ] src/index.js
    - [ ] src/routes/api.routes.js
    - [ ] src/config/sentry.js
    - [ ] src/config/matomo.js
    - [ ] package.json
    - [ ] Dockerfile
  - **Prioridade**: ALTA
  - **Depende de**: Tasks scaffolding
  - **Tempo estimado**: 5 dias

#### Tasks SCAFFOLDING (3)

- [ ] **tasks/scaffolding/scaffold-project-structure.xml**
  - Criar estrutura de diretórios
  - Copiar templates base
  - **Prioridade**: ALTA
  - **Tempo estimado**: 2 dias

- [ ] **tasks/scaffolding/apply-template.xml**
  - Substituir variáveis em templates
  - Aplicar configurações específicas
  - **Prioridade**: ALTA
  - **Tempo estimado**: 2 dias

- [ ] **tasks/scaffolding/configure-integrations.xml**
  - Instalar SDKs (Sentry, Matomo)
  - Gerar código de configuração
  - **Prioridade**: ALTA
  - **Tempo estimado**: 3 dias

**Total Fase 2**: 15 dias úteis (~3 semanas)

---

## 🎨 Fase 3: Frontend Scaffolding (Prioridade MÉDIA)

**Objetivo**: Criar projetos Vue.js e React conformes

**Prazo Estimado**: 3 semanas

**Componentes**: 8 itens

### 🔨 Pendentes (8/8)

#### Templates (4)

- [ ] **templates/docker-compose/vuejs-frontend.yaml**
- [ ] **templates/env/.env.vuejs.example**
- [ ] **templates/docker-compose/react-frontend.yaml**
- [ ] **templates/env/.env.react.example**
- **Prioridade**: MÉDIA
- **Tempo estimado**: 2 dias cada (8 dias total)

#### Workflows CREATE (2)

- [ ] **workflows/create/create-vuejs-frontend/**
  - Código base Vue.js 3 + Vuetify
  - Tema verde Embrapa
  - Logo integrada
  - **Prioridade**: MÉDIA
  - **Tempo estimado**: 4 dias

- [ ] **workflows/create/create-react-frontend/**
  - Código base React 18
  - UI library configurada
  - **Prioridade**: MÉDIA
  - **Tempo estimado**: 3 dias

#### Templates de Integração (2)

- [ ] **templates/integrations/sentry-config.js**
  - Configuração para Node.js, Vue.js, React
  - **Prioridade**: MÉDIA
  - **Tempo estimado**: 1 dia

- [ ] **templates/integrations/matomo-tracking.js**
  - Tracking code para frontends
  - Custom dimensions
  - **Prioridade**: MÉDIA
  - **Tempo estimado**: 1 dia

**Total Fase 3**: 15 dias úteis (~3 semanas)

---

## ➕ Fase 4: Add Compliance Workflows (Prioridade MÉDIA)

**Objetivo**: Adicionar conformidade a projetos existentes

**Prazo Estimado**: 3 semanas

**Componentes**: 9 itens

### 🔨 Pendentes (9/9)

#### Workflows ADD (5)

- [ ] **workflows/add/add-embrapa-compliance/**
  - Analisar projeto existente
  - Gerar docker-compose conforme
  - Criar .env files sem conflitos
  - **Prioridade**: MÉDIA
  - **Tempo estimado**: 5 dias

- [ ] **workflows/add/add-sentry-integration/**
  - Detectar stack
  - Instalar SDK apropriado
  - Configurar código
  - **Prioridade**: MÉDIA
  - **Tempo estimado**: 3 dias

- [ ] **workflows/add/add-matomo-integration/**
  - Frontend ou backend
  - Implementar tracking
  - **Prioridade**: MÉDIA
  - **Tempo estimado**: 2 dias

- [ ] **workflows/add/add-sonarqube-integration/**
  - Criar sonar-project.properties
  - Configurar CI/CD
  - **Prioridade**: BAIXA
  - **Tempo estimado**: 2 dias

- [ ] **workflows/add/add-loki-integration/**
  - Configurar logging driver
  - Definir labels
  - **Prioridade**: BAIXA
  - **Tempo estimado**: 2 dias

#### Tasks MIGRATION (3)

- [ ] **tasks/migration/analyze-existing-project.xml**
  - Detectar stack, banco, estrutura
  - **Prioridade**: MÉDIA
  - **Tempo estimado**: 3 dias

- [ ] **tasks/migration/generate-migration-plan.xml**
  - Plano de correções priorizadas
  - **Prioridade**: MÉDIA
  - **Tempo estimado**: 2 dias

- [ ] **tasks/migration/apply-compliance-changes.xml**
  - Aplicar mudanças com backup
  - **Prioridade**: MÉDIA
  - **Tempo estimado**: 3 dias

#### Templates de Integração (1)

- [ ] **templates/integrations/sonarqube-properties**
  - Template para diferentes stacks
  - **Prioridade**: BAIXA
  - **Tempo estimado**: 1 dia

**Total Fase 4**: 23 dias úteis (~4.5 semanas)

---

## 🔄 Fase 5: Migration Workflows (Prioridade MÉDIA)

**Objetivo**: Migrar projetos entre estados

**Prazo Estimado**: 2 semanas

**Componentes**: 2 itens

### 🔨 Pendentes (2/2)

#### Workflows MIGRATE (2)

- [ ] **workflows/migrate/migrate-to-compliance/**
  - Usar análise + plano + apply
  - Validação pós-migração
  - **Prioridade**: MÉDIA
  - **Tempo estimado**: 3 dias

- [ ] **workflows/migrate/migrate-stage/**
  - Atualizar variáveis de ambiente
  - Criar tag git
  - Checklist de deploy
  - **Prioridade**: MÉDIA
  - **Tempo estimado**: 2 dias

**Total Fase 5**: 5 dias úteis (~1 semana)

---

## 🌟 Fase 6: Stacks Adicionais (Prioridade BAIXA)

**Objetivo**: Suporte para React Native, .NET, PHP

**Prazo Estimado**: 4 semanas

**Componentes**: 12 itens

### 🔨 Pendentes (12/12)

#### Templates (6)

- [ ] templates/docker-compose/reactnative-mobile.yaml (2 dias)
- [ ] templates/env/.env.react.example (1 dia)
- [ ] templates/docker-compose/dotnet-app.yaml (2 dias)
- [ ] templates/env/.env.dotnet.example (1 dia)
- [ ] templates/docker-compose/php-app.yaml (2 dias)
- [ ] templates/env/.env.php.example (1 dia)

#### Workflows CREATE (3)

- [ ] workflows/create/create-reactnative-mobile/ (4 dias)
- [ ] workflows/create/create-dotnet-app/ (4 dias)
- [ ] workflows/create/create-php-app/ (3 dias)

#### Templates Settings (2)

- [ ] templates/settings/settings-nodejs.json (1 dia)
- [ ] templates/settings/settings-frontend.json (1 dia)

#### Templates de Integração (1)

- [ ] templates/integrations/loki-config.yaml (1 dia)

**Total Fase 6**: 20 dias úteis (~4 semanas)

---

## 🛠️ Fase 7: Tooling & Automation (Prioridade MÉDIA)

**Objetivo**: Ferramentas de instalação e automação

**Prazo Estimado**: 1 semana

**Componentes**: 4 itens

### 🔨 Pendentes (4/4)

- [ ] **install.sh**
  - Copiar conhecimento para agentes
  - Adicionar menu items
  - Registrar workflows
  - **Tempo estimado**: 2 dias

- [ ] **uninstall.sh**
  - Remover conhecimento
  - Remover menu items
  - Opção de manter templates
  - **Tempo estimado**: 1 dia

- [ ] **Testes de validação**
  - Suite de testes para 38 regras
  - **Tempo estimado**: 3 dias

- [ ] **Tutorial interativo**
  - Modo tutorial para Dev Júnior
  - **Tempo estimado**: 2 dias

**Total Fase 7**: 8 dias úteis (~1.5 semanas)

---

## 📅 Cronograma Geral

| Fase | Prazo | Dependências | Status |
|------|-------|--------------|--------|
| **Fase 1**: Core Validation | 3 semanas | Nenhuma | ✅ Completa (100%) |
| **Fase 2**: Scaffolding Node.js | 3 semanas | Fase 1 | 🔴 Pendente |
| **Fase 3**: Frontend Scaffolding | 3 semanas | Fase 2 | 🔴 Pendente |
| **Fase 4**: Add Compliance | 4.5 semanas | Fase 1 | 🔴 Pendente |
| **Fase 5**: Migration | 1 semana | Fase 4 | 🔴 Pendente |
| **Fase 6**: Stacks Adicionais | 4 semanas | Fase 2, 3 | 🔴 Pendente |
| **Fase 7**: Tooling | 1.5 semanas | Fase 1-5 | 🔴 Pendente |

**Tempo Total Estimado**: 20 semanas (~5 meses)

**Data de Conclusão Prevista (v1.0 completo)**: Março 2026

---

## 🎯 Próximas Ações (Fases Futuras)

### Fase 2: Scaffolding (Quando Necessário)

Os workflows CREATE são extensões opcionais para scaffolding completo de novos projetos. O core atual permite que qualquer agente BMAD crie projetos conformes usando:

1. **Conhecimento** para entender as regras
2. **Workflows Setup** para gerar arquivos obrigatórios
3. **Templates** como base para adaptação
4. **Workflow Validate** para verificar conformidade

### Prioridades para Extensões Futuras

1. ⏳ **create-nodejs-api** - Scaffolding completo Node.js
2. ⏳ **create-vuejs-frontend** - Scaffolding Vue.js + Vuetify
3. ⏳ **add-embrapa-compliance** - Adicionar conformidade a projetos existentes
4. ⏳ **migrate-to-compliance** - Migração assistida de projetos legados

---

## 📊 Métricas de Sucesso

### Versão 1.0 Core (Completa ✅)

- [x] 7 arquivos de conhecimento ✅
- [x] 5 workflows core funcionais ✅
- [x] 6 templates completos ✅
- [x] 100% das 38 regras validáveis ✅
- [x] Documentação técnica completa ✅
- [x] Suporte para 7 stacks (via conhecimento) ✅
- [x] 4 integrações documentadas (Sentry, Matomo, SonarQube, Loki) ✅

### Versão 1.1 (Extensões Futuras)

- [ ] Workflows CREATE (scaffolding completo)
- [ ] Workflows ADD (adicionar conformidade)
- [ ] Workflows MIGRATE (migração assistida)
- [ ] Auto-fix avançado
- [ ] Modo tutorial interativo

### Versão 1.2 (Melhorias Avançadas)

- [ ] Dashboard consolidado
- [ ] Testes automatizados (cobertura >80%)
- [ ] Integração MCP avançada
- [ ] Instalador/Desinstalador automáticos

---

**Última atualização**: 2025-12-14
**Responsável**: Camilo Carromeu / BMAD Team
**Status Geral**: 🟢 Core 100% Completo | Extensões 0%
