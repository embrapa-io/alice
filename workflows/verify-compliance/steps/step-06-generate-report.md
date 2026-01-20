---
name: 'step-06-generate-report'
description: 'Gerar relatório final de conformidade em {project-root}/docs/embrapa-io-compliance.md'
---

# Step 6: Gerar Relatório de Conformidade

## STEP GOAL:

Consolidar todos os findings e gerar o relatório final de conformidade em `{project-root}/docs/embrapa-io-compliance.md` com action items claros para implementação por assistentes de codificação em IA.

## MANDATORY EXECUTION RULES:

- 🛑 MUST generate the complete report file
- 📖 Action items MUST be specific, implementable, and include code examples
- 📋 Code examples MUST be adapted to the project's technology stack
- 🎯 Report MUST be readable by both humans and AI coding assistants

## Sequence of Instructions

### 1. Calcular Compliance Score

**Fórmula:**
```
Se CRITICAL > 0 OR HIGH > 3 → LOW (🔴)
Se HIGH > 0 → MEDIUM (🟡)
Se HIGH = 0 AND CRITICAL = 0 → HIGH (🟢)
```

Calcular totais de cada severidade usando:
- `{docker_findings}`
- `{env_findings}`
- `{settings_findings}`
- `{integration_findings}`

### 2. Criar Diretório docs/ (se necessário)

Verificar se `{project-root}/docs/` existe. Se não, criar.

### 3. Gerar Relatório Completo

**Arquivo:** `{project-root}/docs/embrapa-io-compliance.md`

**Estrutura do relatório:**

```markdown
# Relatório de Conformidade Embrapa I/O

**Projeto:** {project_name}
**Data da Análise:** {current_date}
**Stack Detectada:** {detected_stack}
**Compliance Score:** {score} {emoji}

---

## 📊 Resumo Executivo

| Categoria | Status | CRITICAL | HIGH | MEDIUM | LOW |
|-----------|--------|----------|------|--------|-----|
| Docker Compose | {status} | {n} | {n} | {n} | {n} |
| Arquivos .env | {status} | {n} | {n} | {n} | {n} |
| settings.json | {status} | {n} | {n} | {n} | {n} |
| Integrações | {status} | {n} | {n} | {n} | {n} |
| **TOTAL** | **{overall}** | **{n}** | **{n}** | **{n}** | **{n}** |

### Interpretação do Score
- 🟢 **HIGH**: Projeto em conformidade. Pronto para deployment.
- 🟡 **MEDIUM**: Conformidade parcial. Requer ajustes antes do deployment.
- 🔴 **LOW**: Não conforme. Ajustes críticos necessários.

---

## 🎯 Action Items de Implementação

Os action items abaixo estão ordenados por prioridade (CRITICAL → HIGH → MEDIUM → LOW).
Cada item contém instruções específicas e exemplos de código adaptados à stack do projeto.

### 🚨 CRITICAL (Implementar Imediatamente)

{Para cada finding CRITICAL, gerar um action item detalhado}

#### AI-{number}: {título_curto}

**Severidade:** CRITICAL
**Categoria:** {docker|env|settings|integrations}
**Localização:** {file_path}:{line_number}
**Problema:** {descrição_detalhada}

**Ação Requerida:**
{descrição_imperativa_da_ação}

**Código a Implementar:**
```{language}
{código_exemplo_completo_adaptado_à_stack}
```

**Validação:**
- [ ] {critério_de_validação_1}
- [ ] {critério_de_validação_2}

---

### ⚠️ HIGH (Implementar Antes do Deployment)

{Para cada finding HIGH, gerar um action item detalhado}

---

### ℹ️ MEDIUM (Recomendado)

{Para cada finding MEDIUM, gerar um action item detalhado}

---

### 💡 LOW (Opcional)

{Para cada finding LOW, gerar um action item detalhado}

---

## 📁 Arquivos a Criar/Modificar

### Arquivos a Criar
{lista de arquivos que precisam ser criados}

### Arquivos a Modificar
{lista de arquivos que precisam ser modificados}

---

## 📝 Templates de Referência

### Template: .env.io.example
```ini
COMPOSE_PROJECT_NAME={io_project}_{io_app}_development
COMPOSE_PROFILES=development
IO_SERVER=localhost
IO_PROJECT={io_project}
IO_APP={io_app}
IO_STAGE=development
IO_VERSION=0.{YY}.{M}-dev.1
IO_DEPLOYER=first.surname@embrapa.br
SENTRY_DSN=GET_IN_DASHBOARD
MATOMO_ID={matomo_id}
MATOMO_TOKEN=
```

### Template: docker-compose.yaml (estrutura mínima)
```yaml
services:
  app:
    build: .
    restart: unless-stopped
    ports:
      - "${APP_PORT}:{internal_port}"
    environment:
      # variáveis específicas da aplicação
    networks:
      - stack
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:{internal_port}/{health_endpoint}"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

  # Serviços CLI (se aplicável)
  backup:
    image: {db_image}
    profiles: ['cli']
    restart: "no"
    volumes:
      - backup_data:/backup
    networks:
      - stack
    command: |
      sh -c "..."

  restore:
    image: {db_image}
    profiles: ['cli']
    restart: "no"
    volumes:
      - backup_data:/backup
    networks:
      - stack
    command: |
      sh -c "..."

  sanitize:
    image: {db_image}
    profiles: ['cli']
    restart: "no"
    networks:
      - stack
    command: |
      sh -c "..."

networks:
  stack:
    external: true
    name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}

volumes:
  backup_data:
    external: true
    name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}_backup
```

### Template: .embrapa/settings.json
```json
{
  "boilerplate": "_",
  "platform": "{detected_platform}",
  "label": "{project_label}",
  "description": "{project_description}",
  "references": [
    { "label": "{ref_label}", "url": "{ref_url}" }
  ],
  "maintainers": [
    {
      "name": "{maintainer_name}",
      "email": "{maintainer_email}",
      "phone": "+55 (XX) X XXXX-XXXX"
    }
  ],
  "variables": {
    "default": [
      { "name": "APP_PORT", "type": "PORT" }
    ],
    "alpha": [],
    "beta": [],
    "release": []
  },
  "orchestrators": ["DockerCompose"]
}
```

---

## 🚀 Próximos Passos

Após implementar todos os action items:

1. **Executar o workflow de Implementação (IA)**
   - O assistente de codificação irá executar os action items automaticamente

2. **Criar arquivos .env a partir dos examples**
   - Copiar `.env.io.example` para `.env.io`
   - Copiar `.env.example` para `.env`
   - Ajustar valores conforme necessário

3. **Executar bootstrap.sh**
   - Criar network e volumes externos
   - Testar a aplicação localmente

4. **Executar o workflow de Code Review (CR)**
   - Verificar se todas as implementações estão corretas

---

## 📚 Referências

- [Documentação Embrapa I/O](https://embrapa.io/docs)
- [Dashboard Embrapa I/O](https://dashboard.embrapa.io)
- [4 Verdades Fundamentais](knowledge/embrapa-io-fundamentals.md)
- [Regras de Validação](knowledge/embrapa-io-validation.md)

---

*Relatório gerado por Alice - Especialista em Conformidade Embrapa I/O*
*Data: {current_date}*
```

### 4. Salvar o Relatório

Salvar o arquivo em `{project-root}/docs/embrapa-io-compliance.md`.

### 5. Apresentar Resumo ao Usuário

```markdown
## ✅ Relatório de Conformidade Gerado

**Arquivo:** `docs/embrapa-io-compliance.md`

**Compliance Score:** {score} {emoji}

**Resumo:**
- CRITICAL: {n} items
- HIGH: {n} items
- MEDIUM: {n} items
- LOW: {n} items
- **TOTAL:** {n} action items

---

### 🎯 Próximos Passos

1. **Revise o relatório** em `docs/embrapa-io-compliance.md`
2. **Execute o workflow [IA] Implementar Ajustes** para aplicar as correções
3. **Execute o workflow [CR] Code Review** para validar a implementação

Para implementar os ajustes, selecione a opção **[IA]** no menu do agente Alice.
```

### 6. Present MENU OPTIONS

Display: "**Select an Option:** [M] Return to Main Menu [X] Exit"

#### Menu Handling Logic:

- IF M: Return to agent main menu
- IF X: End workflow gracefully with summary

## WORKFLOW COMPLETION

O workflow de verificação de conformidade está completo. O relatório foi gerado em `{project-root}/docs/embrapa-io-compliance.md` e contém todos os action items necessários para alcançar 100% de conformidade com a plataforma Embrapa I/O.
