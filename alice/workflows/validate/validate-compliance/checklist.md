---
last-redoc-date: 2025-12-03
---

# Checklist de Validação - Validate Compliance Workflow

## Validação Pré-Execução

- [ ] Conhecimento da plataforma Embrapa I/O carregado
- [ ] Arquivos de conhecimento acessíveis (embrapa-io-fundamentals.md, embrapa-io-validation.md, embrapa-io-workflows.md)
- [ ] Parâmetros de validação coletados (project_path, severity_levels, auto_fix)
- [ ] Diretório do projeto existe e é acessível

## Validação Durante Execução

### Detecção de Tipo de Projeto

- [ ] Arquivos docker-compose.yaml, .embrapa/settings.json, .env.io.example verificados
- [ ] Tipo de projeto corretamente identificado (ALREADY_COMPLIANT, EXISTING, NEW)

### Validação docker-compose.yaml (14 regras)

- [ ] Todas as 14 regras de validação executadas
- [ ] Erros categorizados por severidade (CRITICAL, HIGH, MEDIUM, LOW)
- [ ] Status da categoria calculado (compliant/partial/non-compliant)

### Validação Arquivos .env (8 regras)

- [ ] .env.io.example e .env.example verificados
- [ ] Variáveis obrigatórias validadas (IO_PROJECT, IO_APP, IO_STAGE, IO_VERSION, IO_DEPLOYER)
- [ ] Convenções de nomenclatura verificadas (UPPER_SNAKE_CASE)

### Validação .embrapa/settings.json (8 regras)

- [ ] Arquivo existe e é JSON válido
- [ ] Campos obrigatórios presentes (boilerplate, platform, label, description, references, maintainers, variables, orchestrators)
- [ ] Platform possui valor válido
- [ ] Tipos de variáveis são válidos (TEXT, PASSWORD, SECRET, PORT, VOLUME, EMPTY)

### Validação Integrações (5 regras)

- [ ] Sentry configurado (se aplicável)
- [ ] Matomo tracking implementado (se aplicável)
- [ ] Logo Embrapa presente
- [ ] SonarQube configurado (se backend)
- [ ] Grafana Loki configurado (opcional)

### Cálculo de Compliance Score

- [ ] Todos os erros consolidados
- [ ] Contagem por severidade calculada (critical, high, medium, low)
- [ ] Score de conformidade determinado (LOW/MEDIUM/HIGH)

## Validação de Outputs

### Relatórios Gerados

- [ ] Relatório JSON gerado em {output_folder}/validation-report-{project_name}-{date}.json
- [ ] Relatório Markdown gerado em {output_folder}/compliance-summary-{project_name}-{date}.md
- [ ] Ambos os relatórios contêm informações completas e corretas

### Estrutura do Relatório JSON

- [ ] Seção project com name, path, type
- [ ] Seção validation com timestamp, score, summary
- [ ] Seção results com docker_compose, env_files, settings_json, integrations
- [ ] Array all_errors com todos os erros consolidados

### Estrutura do Relatório Markdown

- [ ] Cabeçalho com projeto, data, score com emoji
- [ ] Resumo executivo com contagem de validações
- [ ] Detalhamento por categoria com status e erros
- [ ] Próximos passos priorizados por severidade
- [ ] Referências para conhecimento e workflows relacionados

## Correções Automáticas (se auto_fix = true)

- [ ] Backups criados para todos os arquivos modificados (.bak)
- [ ] Correções aplicadas com sucesso
- [ ] Sintaxe validada após modificações (YAML/JSON parse)
- [ ] Log de mudanças registrado
- [ ] Usuário informado sobre correções aplicadas

## Validação Pós-Execução

### Confirmação de Sucesso

- [ ] Resultado final apresentado ao usuário em {communication_language}
- [ ] Score de conformidade comunicado com emoji apropriado (🟢 HIGH / 🟡 MEDIUM / 🔴 LOW)
- [ ] Paths dos relatórios fornecidos
- [ ] Próximos passos recomendados apresentados

### Qualidade dos Outputs

- [ ] Relatórios acessíveis e legíveis
- [ ] Informações precisas e completas
- [ ] Recomendações claras e acionáveis
- [ ] Priorização adequada por severidade

## Checklist de Conformidade do Próprio Workflow

- [ ] Workflow segue estrutura BMAD v6
- [ ] Config block completo (config_source, output_folder, user_name, communication_language, date)
- [ ] Web bundle inclui todos os arquivos necessários
- [ ] Instruções usam tags corretas (<action>, <check>, <ask>)
- [ ] Comunicação em {communication_language}
- [ ] Uso apropriado de {user_name} para personalização

---

## Critérios de Sucesso

O workflow é considerado bem-sucedido quando:

1. ✅ Todas as 48 regras de validação foram aplicadas corretamente
2. ✅ Relatórios JSON e Markdown gerados com informações completas
3. ✅ Score de conformidade calculado corretamente baseado em severidades
4. ✅ Erros apresentados com ID, severidade, mensagem, localização e solução
5. ✅ Correções automáticas aplicadas com segurança (se habilitadas)
6. ✅ Usuário informado em {communication_language} com próximos passos claros

---

**Versão:** 1.26.4-8
**Compatível com:** BMAD Core v6
**Última atualização:** 2026-03-30
