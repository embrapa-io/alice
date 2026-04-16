---
last-redoc-date: 2025-12-14
---

# Embrapa I/O Workflows

Coleção completa de workflows para setup e validação de projetos conformes com a plataforma Embrapa I/O.

Este módulo fornece 8 workflows especializados organizados em três categorias: **Alice** (3 workflows) para o fluxo principal de conformidade, **Setup** (4 workflows) para configuração inicial de projetos, e **Validate** (1 workflow legado) para verificação de conformidade.

## Categorias

### [Alice](.) - 3 workflows
Workflows principais da agente Alice para o ciclo completo de conformidade:

- **[verify-compliance](./verify-compliance/)**: Analisa o codebase e gera relatório detalhado de compliance com action items
- **[implement-compliance](./implement-compliance/)**: Executa os action items do relatório, cria `.env`, `.env.io` e `bootstrap.sh`
- **[code-review](./code-review/)**: Verifica se a implementação está 100% conforme e emite veredicto APPROVED/REJECTED

**Fluxo recomendado**: verify-compliance → implement-compliance → code-review (em nova sessão)

### [Setup](./setup/) - 4 workflows
Workflows para configuração inicial completa de projetos Embrapa I/O:

- **[generate-env-io](./setup/generate-env-io/)**: Gera `.env.io` e `.env.io.example` com variáveis obrigatórias (workflow interativo)
- **[generate-docker-compose](./setup/generate-docker-compose/)**: Cria `docker-compose.yaml` conforme com as 4 Verdades Fundamentais (auto-detecta stack)
- **[generate-settings-json](./setup/generate-settings-json/)**: Gera `.embrapa/settings.json` com metadados e configurações por ambiente
- **[generate-license](./setup/generate-license/)**: Cria arquivo `LICENSE` padrão da Embrapa (workflow autônomo)

**Ordem recomendada**: generate-env-io → generate-license → generate-settings-json → generate-docker-compose

### [Validate](./validate/) - 1 workflow (legado)
Workflows para validação de conformidade:

- **[validate-compliance](./validate/validate-compliance/)**: Validação completa contra 38 regras da plataforma, gera relatórios JSON e Markdown

> **Nota**: Para novos projetos, recomenda-se usar a agente Alice diretamente (verify-compliance → implement-compliance → code-review).

## Características

- **Detecção Automática**: Workflows detectam stack tecnológica (Node.js, Vue, React, PHP, .NET)
- **Validação Rigorosa**: Conformidade com as 4 Verdades Fundamentais e 38 regras da plataforma
- **Templates Especializados**: Templates adaptáveis para diferentes stacks e cenários
- **Knowledge Base**: 8 arquivos de conhecimento sobre fundamentals, validation, workflows, deployment, stacks, integrations, coding standards e integration guide
- **Relatórios Detalhados**: Saídas em JSON estruturado e Markdown formatado

## Quick Start

Para setup completo de um novo projeto:

```bash
# 1. Gerar variáveis de ambiente (interativo)
bmad run bmad/embrapa-io/workflows/setup/generate-env-io

# 2. Gerar licença (autônomo)
bmad run bmad/embrapa-io/workflows/setup/generate-license

# 3. Gerar settings (interativo)
bmad run bmad/embrapa-io/workflows/setup/generate-settings-json

# 4. Gerar docker-compose (interativo)
bmad run bmad/embrapa-io/workflows/setup/generate-docker-compose

# 5. Validar conformidade (opcional)
bmad run bmad/embrapa-io/workflows/validate/validate-compliance
```

## Files Generated

Após execução completa dos workflows de setup, o projeto terá:

- `.env.io` - Variáveis de ambiente locais (não commitar)
- `.env.io.example` - Template versionado de variáveis (commitar)
- `LICENSE` - Licença padrão Embrapa com copyright atualizado
- `.embrapa/settings.json` - Metadados e configurações da aplicação
- `docker-compose.yaml` - Configuração Docker conforme com a plataforma

## Compliance

Todos os workflows garantem conformidade com:

- **4 Verdades Fundamentais**: Sem `version`, network externa, volumes externos, sem `container_name`
- **38 Regras da Plataforma**: Cobertura completa de validações (14 Docker + 10 env + 8 settings + 6 integrations)
- **Padrões de Nomenclatura**: Nomes unix, versionamento `0.YY.M-dev.1`, concatenações obrigatórias
- **Boas Práticas Git**: Orientação sobre o que commitar e o que ignorar

## Total Workflows: 8
