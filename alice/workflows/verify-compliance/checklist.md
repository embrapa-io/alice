---
last-redoc-date: 2026-01-20
---

# Checklist de Validação - Verify Compliance Workflow

## Validação Pré-Execução

- [ ] Conhecimento da plataforma Embrapa I/O carregado
- [ ] Arquivos de conhecimento acessíveis (embrapa-io-fundamentals.md, embrapa-io-validation.md)
- [ ] Diretório do projeto existe e é acessível

## Validação Durante Execução

### Detecção de Stack Tecnológica

- [ ] Stack tecnológica corretamente identificada (Node.js, Python, PHP, etc.)
- [ ] Estrutura de diretórios mapeada
- [ ] Endpoints de health check existentes detectados

### Validação docker-compose.yaml (14 regras)

- [ ] Arquivo existe
- [ ] Campo `version` ausente (obsoleto)
- [ ] Network `stack` externa declarada
- [ ] Nome da network: `${IO_PROJECT}_${IO_APP}_${IO_STAGE}`
- [ ] Todos os volumes são externos
- [ ] Nenhum serviço usa `container_name`
- [ ] Serviços de longa duração têm `restart: unless-stopped`
- [ ] Serviços de longa duração têm `healthcheck`
- [ ] Serviços CLI têm `profiles: ['cli']`
- [ ] Serviços CLI têm `restart: "no"`
- [ ] Portas do host usam variáveis de ambiente
- [ ] Todos os serviços conectados à network `stack`
- [ ] Serviços backup, restore, sanitize presentes (se aplicável)
- [ ] Healthchecks usam endpoints existentes

### Validação Arquivos .env (8 regras)

- [ ] `.env.io.example` existe
- [ ] `.env.example` existe
- [ ] Variáveis obrigatórias em `.env.io.example`
- [ ] `IO_VERSION` no formato `0.YY.M-dev.1`
- [ ] Sem duplicação de variáveis entre arquivos
- [ ] Sem espaços nos valores
- [ ] Sem aspas nos valores
- [ ] `.gitignore` inclui `.env`, `.env.io`, `.env.sh` e diretórios de agentes de IA

### Validação .embrapa/settings.json (9 regras)

- [ ] Arquivo existe
- [ ] JSON válido
- [ ] Campo `boilerplate` presente
- [ ] Campo `platform` com valor válido
- [ ] Campo `label` presente
- [ ] Campo `description` presente
- [ ] Campo `maintainers` com formato correto
- [ ] Campo `variables` com estrutura correta
- [ ] Campo `orchestrators` = `["DockerCompose"]`

### Validação Integrações (5 regras)

- [ ] Sentry configurado (se SENTRY_DSN presente)
- [ ] Matomo configurado (se MATOMO_ID presente e frontend)
- [ ] LICENSE presente
- [ ] Logo Embrapa presente (se frontend)
- [ ] README.md documenta comandos Embrapa I/O

## Validação de Outputs

### Relatório Gerado

- [ ] Arquivo `{output_folder}/embrapa-io-compliance.md` criado
- [ ] Compliance score calculado corretamente
- [ ] Todos os findings documentados
- [ ] Action items organizados por prioridade
- [ ] Exemplos de código adaptados à stack

### Estrutura do Relatório

- [ ] Header com projeto, data, score
- [ ] Resumo executivo
- [ ] Action items com severidade e instruções
- [ ] Exemplos de código completos
- [ ] Próximos passos claros

## Critérios de Sucesso

O workflow é considerado bem-sucedido quando:

1. ✅ Stack tecnológica detectada corretamente
2. ✅ Todas as validações executadas
3. ✅ Relatório gerado em `{output_folder}/embrapa-io-compliance.md`
4. ✅ Action items claros e implementáveis
5. ✅ Exemplos de código adaptados ao projeto
6. ✅ Comunicação em {communication_language}

---

**Versão:** 1.26.4-9
**Compatível com:** BMAD Core v6
**Última atualização:** 2026-03-30
