---
last-redoc-date: 2026-01-20
---

# Checklist de Validação - Code Review Workflow

## Pré-Requisitos

- [ ] Executar em NOVA SESSÃO (sem contexto de implementação anterior)
- [ ] Relatório `{output_folder}/embrapa-io-compliance.md` existe
- [ ] Action items foram implementados (workflow [IA])
- [ ] Conhecimento Embrapa I/O carregado

## Validação Durante Execução

### Step 1: Verificar docker-compose.yaml

#### 4 Verdades Fundamentais

- [ ] Campo `version` AUSENTE
- [ ] Network `stack` declarada como `external: true`
- [ ] Network name = `${IO_PROJECT}_${IO_APP}_${IO_STAGE}`
- [ ] TODOS os volumes são `external: true`
- [ ] NENHUM serviço usa `container_name`

#### Configuração de Serviços

- [ ] Serviços de longa duração têm `restart: unless-stopped`
- [ ] Serviços de longa duração têm `healthcheck` configurado
- [ ] Serviços CLI têm `profiles: ['cli']`
- [ ] Serviços CLI têm `restart: "no"`
- [ ] Portas do host usam variáveis de ambiente
- [ ] Todos os serviços conectados à network `stack`

**Resultado Step 1:** PASS ✅ / FAIL ❌

### Step 2: Verificar Arquivos .env

#### Presença de Arquivos

- [ ] `.env.io.example` existe
- [ ] `.env.io` existe
- [ ] `.env.example` existe
- [ ] `.env` existe

#### .env.io.example - Variáveis Obrigatórias

- [ ] `COMPOSE_PROJECT_NAME` presente
- [ ] `COMPOSE_PROFILES` presente
- [ ] `IO_SERVER` presente
- [ ] `IO_PROJECT` presente
- [ ] `IO_APP` presente
- [ ] `IO_STAGE` presente
- [ ] `IO_VERSION` presente
- [ ] `IO_DEPLOYER` presente
- [ ] `SENTRY_DSN` presente
- [ ] `MATOMO_ID` presente

#### .env.io - Valores Válidos

- [ ] `IO_VERSION` formato correto (`0.YY.M-dev.1`)
- [ ] `COMPOSE_PROJECT_NAME` = `{IO_PROJECT}_{IO_APP}_development`
- [ ] Valores sem espaços
- [ ] Valores sem aspas

#### .env.example - Validações

- [ ] Sem duplicatas do `.env.io`
- [ ] Sem valores com espaços
- [ ] Sem valores com aspas

#### .gitignore

- [ ] `.env` listado
- [ ] `.env.io` listado
- [ ] `.env.sh` listado
- [ ] Diretórios de agentes de IA listados

**Resultado Step 2:** PASS ✅ / FAIL ❌

### Step 3: Verificar .embrapa/settings.json

#### Estrutura

- [ ] Arquivo existe
- [ ] JSON válido

#### Campos Obrigatórios

- [ ] `boilerplate` (string)
- [ ] `platform` (valor válido)
- [ ] `label` (string não vazia)
- [ ] `description` (string não vazia)
- [ ] `references` (array)
- [ ] `maintainers` (array não vazio)
- [ ] `variables` (objeto)
- [ ] `orchestrators` (array)

#### Validações Específicas

- [ ] `platform` é valor válido da lista
- [ ] Cada maintainer tem `name`, `email`, `phone`
- [ ] `phone` no formato `+DDI (DDD) X XXXX-XXXX`
- [ ] `variables.default`, `.alpha`, `.beta`, `.release` existem
- [ ] `orchestrators` = `["DockerCompose"]`
- [ ] `orchestrators` NÃO contém `"DockerSwarm"`

**Resultado Step 3:** PASS ✅ / FAIL ❌

### Step 4: Verificar Integrações e Bootstrap

#### bootstrap.sh

- [ ] Arquivo existe
- [ ] Arquivo é executável
- [ ] Valida pré-requisitos (Docker, Docker Compose)
- [ ] Cria network externa
- [ ] Cria volumes externos
- [ ] Usa variáveis do `.env.io`

#### LICENSE

- [ ] Arquivo existe
- [ ] Contém copyright Embrapa

#### README.md

- [ ] Arquivo existe
- [ ] Documenta comando de inicialização Embrapa I/O
- [ ] Comando inclui `env $(cat .env.io) docker compose up ...`

#### Integrações (se aplicável)

- [ ] Sentry: pacote instalado, DSN de variável, release com IO_VERSION
- [ ] Matomo: código presente, host = `https://hit.embrapa.io`, site ID de variável

**Resultado Step 4:** PASS ✅ / FAIL ❌

### Step 5: Resultado Final

- [ ] Todos os steps anteriores verificados
- [ ] Resultado consolidado calculado
- [ ] Relatório de conformidade atualizado

## Critérios de Aprovação

### APPROVED ✅

- Todas as 4 categorias passaram
- 0 falhas em verificações obrigatórias
- Integrações N/A não contam como falha

### REJECTED ❌

- Uma ou mais categorias falharam
- Qualquer verificação obrigatória falhou
- Retornar ao workflow [IA] para correções

## Validação de Outputs

### Se APPROVED

- [ ] Relatório atualizado com "✅ Conformidade Verificada"
- [ ] Todos os action items marcados como "✅ Completo"
- [ ] Data e resultado do code review registrados
- [ ] Seção "🎉 Projeto em Conformidade" adicionada

### Se REJECTED

- [ ] Relatório atualizado com "❌ Code Review - Falhas Encontradas"
- [ ] Lista detalhada de falhas documentada
- [ ] Instruções de correção fornecidas
- [ ] Próximos passos indicados

## Critérios de Sucesso do Workflow

O workflow é considerado bem-sucedido quando:

1. ✅ Todas as verificações executadas sem erros
2. ✅ Resultado final claramente determinado (APPROVED/REJECTED)
3. ✅ Relatório de conformidade atualizado corretamente
4. ✅ Falhas documentadas com instruções de correção (se REJECTED)
5. ✅ Comunicação em {communication_language}

---

**Versão:** 1.26.4-5
**Compatível com:** BMAD Core v6
**Última atualização:** 2026-03-30
