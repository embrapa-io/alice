---
name: 'step-05-finalize'
description: 'Finalizar implementação e orientar próximos passos'
---

# Step 5: Finalizar Implementação

## STEP GOAL:

Finalizar o workflow de implementação, atualizar o relatório de conformidade com status dos action items, e orientar o usuário sobre os próximos passos.

## MANDATORY EXECUTION RULES:

- 🛑 MUST update the compliance report with completion status
- 📖 MUST provide clear next steps
- 📋 MUST emphasize the need for a NEW SESSION for code review

## Sequence of Instructions

### 1. Atualizar Relatório de Conformidade

Atualizar o arquivo `{output_folder}/embrapa-io-compliance.md`:

**Adicionar seção no início:**

```markdown
---

## 📋 Status da Implementação

**Data da Implementação:** {current_date}
**Implementado por:** Alice - Especialista em Conformidade Embrapa I/O

### Action Items Implementados

| # | Action Item | Severidade | Status |
|---|-------------|------------|--------|
| AI-1 | {título} | CRITICAL | ✅ Implementado |
| AI-2 | {título} | HIGH | ✅ Implementado |
| ... | ... | ... | ... |

**Resumo:**
- CRITICAL: {n}/{total} implementados
- HIGH: {n}/{total} implementados
- MEDIUM: {n}/{total} implementados
- LOW: {n}/{total} implementados (opcional)

---
```

### 2. Adicionar Seção de Conformidade ao README.md

Verificar se README.md existe e adicionar seção sobre conformidade Embrapa I/O:

```markdown
## 🔄 Embrapa I/O

Este projeto está em conformidade com a plataforma [Embrapa I/O](https://embrapa.io).

### Pré-requisitos

- Docker 20.x ou superior
- Docker Compose v2

### Iniciando o Ambiente de Desenvolvimento

1. **Execute o bootstrap**
   ```bash
   ./bootstrap.sh
   ```

2. **Inicie a aplicação**
   ```bash
   env $(cat .env.io) docker compose up --force-recreate --build --remove-orphans --wait
   ```

3. **Para parar a aplicação**
   ```bash
   env $(cat .env.io) docker compose down
   ```

### Comandos CLI

```bash
# Backup do banco de dados
env $(cat .env.io) docker compose run --rm backup

# Restore do banco de dados
env $(cat .env.io) BACKUP_FILE_TO_RESTORE=arquivo.sql docker compose run --rm restore

# Otimização do banco de dados
env $(cat .env.io) docker compose run --rm sanitize
```

### Documentação de Conformidade

Para detalhes sobre a conformidade com a plataforma Embrapa I/O, consulte:
- [Relatório de Conformidade]({output_folder}/embrapa-io-compliance.md)
```

### 3. Apresentar Resumo Final

```markdown
## ✅ Implementação Concluída!

### Arquivos Criados/Modificados

**Criados:**
- `.env.io` - Variáveis da plataforma
- `.env` - Variáveis da aplicação
- `bootstrap.sh` - Script de inicialização
- `.embrapa/settings.json` - Metadados do projeto (se não existia)
- `LICENSE` - Licença Embrapa (se não existia)

**Modificados:**
- `docker-compose.yaml` - Conformidade com 4 Verdades Fundamentais
- `.env.example` - Template de variáveis
- `.env.io.example` - Template de variáveis da plataforma
- `README.md` - Seção de conformidade adicionada
- `{output_folder}/embrapa-io-compliance.md` - Status atualizado

---

## 🚀 Próximos Passos Obrigatórios

### 1. Execute o bootstrap.sh

```bash
./bootstrap.sh
```

Este script irá:
- Validar Docker e Docker Compose
- Criar network externa
- Criar volumes externos

### 2. Inicie a aplicação

```bash
env $(cat .env.io) docker compose up --force-recreate --build --remove-orphans --wait
```

### 3. Teste a aplicação

Verifique se:
- [ ] A aplicação inicia sem erros
- [ ] Os health checks passam
- [ ] A funcionalidade básica está operando

### 4. Execute o Code Review

⚠️ **IMPORTANTE: Inicie uma NOVA SESSÃO do assistente de codificação**

O Code Review deve ser executado em uma nova sessão para garantir
uma análise imparcial das implementações realizadas.

Na nova sessão, execute:
1. Ative o agente Alice
2. Selecione a opção **[CR] Code Review**

O Code Review irá:
- Verificar se todas as implementações estão corretas
- Validar conformidade final
- Atualizar o relatório com o resultado da revisão

---

## ⚠️ Avisos Importantes

1. **Não commite arquivos sensíveis**
   Os arquivos `.env` e `.env.io` contêm valores sensíveis.
   Verifique se estão no `.gitignore`.

2. **Obtenha credenciais do Dashboard**
   - SENTRY_DSN: https://dashboard.embrapa.io
   - MATOMO_ID: https://dashboard.embrapa.io

3. **Secrets gerados automaticamente**
   Os valores de PASSWORD e SECRET foram gerados aleatoriamente.
   Anote-os em local seguro se necessário.

---

Implementação concluída por **Alice** - Especialista em Conformidade Embrapa I/O
Data: {current_date}
```

### 4. Present FINAL OPTIONS

Display: "**Select an Option:** [M] Return to Agent Menu [X] Exit Session"

#### Menu Handling Logic:

- IF M: Return to Alice's main menu
- IF X: End session with final message

**Final message on exit:**
```
Obrigada por usar o workflow de Implementação de Conformidade!

📋 Lembre-se:
1. Execute ./bootstrap.sh
2. Teste a aplicação
3. Inicie uma NOVA SESSÃO para o Code Review [CR]

Até a próxima! 👋
```

## WORKFLOW COMPLETION

O workflow de implementação está completo. Todas as modificações foram realizadas conforme o relatório de conformidade. O usuário deve executar o bootstrap.sh, testar a aplicação, e iniciar uma nova sessão para o Code Review.
