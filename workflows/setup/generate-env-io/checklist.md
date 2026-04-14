---
last-redoc-date: 2025-12-03
---

# Checklist de Validação - Generate .env.io

## ✅ Arquivo .env.io

- [ ] Arquivo criado em `{project-root}/.env.io`
- [ ] Variável `COMPOSE_PROJECT_NAME` presente e no formato correto
- [ ] Variável `IO_PROJECT` presente e validada (somente lowercase, números, hífen)
- [ ] Variável `IO_APP` presente e validada (somente lowercase, números, hífen)
- [ ] Variável `IO_VERSION` presente e no formato correto (0.YY.M-dev.1)
- [ ] Variável `IO_DEPLOYER` presente e é email válido
- [ ] Variável `IO_STAGE` presente com valor padrão `development`
- [ ] Todas as variáveis obrigatórias da plataforma incluídas
- [ ] Formato de arquivo correto (KEY=value, sem espaços)
- [ ] Arquivo salvo com encoding UTF-8

## ✅ Arquivo .env.io.example

- [ ] Arquivo criado em `{project-root}/.env.io.example`
- [ ] Contém mesmas variáveis que `.env.io`
- [ ] Valores são placeholders descritivos (sem dados reais)
- [ ] Exemplo: `IO_PROJECT=nome-do-projeto` (não valor real)
- [ ] Exemplo: `IO_DEPLOYER=seu-email@embrapa.br` (placeholder)
- [ ] Comentários explicativos presentes (se aplicável)
- [ ] Formato consistente com .env.io

## ✅ Validação de Conformidade

### Nomenclatura Unix
- [ ] `IO_PROJECT` usa apenas: lowercase, números, hífen (a-z, 0-9, -)
- [ ] `IO_APP` usa apenas: lowercase, números, hífen (a-z, 0-9, -)
- [ ] Nenhum uso de underscore, espaços ou caracteres especiais
- [ ] Nomes começam com letra (não número ou hífen)
- [ ] Nomes não terminam com hífen

### Formato de Versão
- [ ] `IO_VERSION` segue padrão: `0.YY.M-dev.N`
- [ ] YY = últimos 2 dígitos do ano corrente
- [ ] M = mês atual (1-12)
- [ ] Sufixo `-dev.1` presente para stage development
- [ ] Exemplo válido: `0.25.10-dev.1` (outubro de 2025)

### Email do Deployer
- [ ] `IO_DEPLOYER` é email válido
- [ ] Formato: `usuario@dominio.ext`
- [ ] Preferencialmente email @embrapa.br

### COMPOSE_PROJECT_NAME
- [ ] Calculado automaticamente como `{IO_PROJECT}_{IO_APP}_development`
- [ ] Usa apenas lowercase, números, underscore
- [ ] Exemplo: se IO_PROJECT=api-catalogo e IO_APP=backend → COMPOSE_PROJECT_NAME=api-catalogo_backend_development

### 🚨 Valores Sem Aspas e Espaços (CRÍTICO)
- [ ] Nenhum valor contém aspas simples (`'`)
- [ ] Nenhum valor contém aspas duplas (`"`)
- [ ] Nenhum valor contém espaços (` `)
- [ ] Valores com caracteres especiais estão codificados (Base64, URL encoding, ou substituição)
- [ ] Formato sempre: `KEY=valor_sem_espacos_ou_aspas`

## ✅ Integração com Git

- [ ] `.env.io` está listado no `.gitignore` (não versionar valores reais)
- [ ] `.env.sh` está listado no `.gitignore`
- [ ] `.env.io.example` NÃO está no `.gitignore` (versionar template)
- [ ] Diretórios de agentes de IA estão no `.gitignore` (`.claude/`, `_bmad/`, etc.)
- [ ] Se `.gitignore` não existe, criar com entradas completas
- [ ] Arquivo `.env.io` não deve ser commitado no repositório

## ✅ Documentação

- [ ] Usuário foi informado sobre localização dos arquivos
- [ ] Usuário foi instruído sobre diferença entre .env.io e .env.io.example
- [ ] Instruções sobre edição de valores fornecidas (se aplicável)
- [ ] Próximos passos comunicados claramente

## 🎯 Critérios de Sucesso

**O workflow é considerado bem-sucedido quando:**

1. ✅ Ambos os arquivos (.env.io e .env.io.example) foram criados
2. ✅ Todas as validações de nomenclatura Unix passaram
3. ✅ Versão está no formato correto (0.YY.M-dev.1)
4. ✅ Email do deployer é válido
5. ✅ COMPOSE_PROJECT_NAME foi calculado corretamente
6. ✅ .env.io está protegido no .gitignore
7. ✅ .env.io.example está versionado (não no .gitignore)
8. ✅ Usuário confirmou entendimento dos arquivos gerados

## ⚠️ Casos de Falha Comum

### Nomenclatura Inválida
- ❌ `IO_PROJECT=api_catalogo` (underscore não permitido)
- ✅ `IO_PROJECT=api-catalogo` (correto)

### Versão Incorreta
- ❌ `IO_VERSION=1.0.0` (formato semver não é usado)
- ❌ `IO_VERSION=0.25.10` (falta sufixo de stage)
- ✅ `IO_VERSION=0.25.10-dev.1` (correto)

### Email Inválido
- ❌ `IO_DEPLOYER=nome` (não é email)
- ❌ `IO_DEPLOYER=@embrapa.br` (falta usuário)
- ✅ `IO_DEPLOYER=nome.sobrenome@embrapa.br` (correto)

### Git Ignore
- ❌ `.env.io.example` no .gitignore (template deve ser versionado)
- ❌ `.env.io` versionado (valores reais não devem ir para git)
- ✅ `.env.io`, `.env.sh` e diretórios de agentes de IA no .gitignore (correto)

### 🚨 Valores com Aspas ou Espaços (CRÍTICO)
- ❌ `MY_VAR="valor com espaços"` (aspas e espaços não permitidos)
- ❌ `MY_VAR='valor'` (aspas simples não permitidas)
- ❌ `MY_VAR=valor com espaços` (espaços não permitidos)
- ✅ `MY_VAR=valor_sem_espacos` (correto)
- ✅ `MY_VAR=TWV1IFZhbG9y` (Base64 para valores complexos - correto)
- ✅ `MY_VAR=valor%20encoded` (URL encoding - correto)

---

**Checklist Version**: 1.1.0
**Última atualização**: 2025-11-25
**Módulo**: embrapa-io/setup/generate-env-io
