# sentinel

Plugin do Claude Code para tratar os relatórios da [Sentinela](https://embrapa.io/docs/sentinel/), o agente de
_insights_ da plataforma [Embrapa I/O](https://embrapa.io). A agente **Alice** busca os relatórios do seu projeto,
confere cada achado contra o código, registra o que procede como _issues_ no Kanban do grupo no GitLab (com
_milestones_, responsáveis e prazos pela capacidade da equipe), guia a correção _issue_ por _issue_ (_worktree_, teste
de regressão, MR, colunas Doing → Alpha → Beta pelas _tags_), mantém o Sentry e o SonarQube coerentes com o código e
devolve à Sentinela o que o relatório errou, pelos votos útil/ruído com veredito.

Nada é alterado sem a sua aprovação explícita: _issues_, _milestones_, _board_, MRs, votos e mudanças no Sentry e no
SonarQube passam antes por uma tabela de aprovação.

## Pré-requisitos

- Um projeto no Embrapa I/O com a Sentinela ativada e os clones das apps (remotos em `git.embrapa.io`).
- [MCP do Dashboard](https://embrapa.io/docs/mcp/io/) (`https://mcp.embrapa.io`), para ler os relatórios e registrar
  os votos. Sem ele, a Alice lê os relatórios do repositório `io-doc` do projeto.
- [MCP do GitLab](https://embrapa.io/docs/mcp/git/) (`https://git.embrapa.io/api/v4/mcp`), para as _issues_ e os MRs.
- Recomendado: a CLI [`glab`](https://gitlab.com/gitlab-org/cli) autenticada em git.embrapa.io
  (`glab auth login --hostname git.embrapa.io`), ou um token pessoal com escopo `api` em `GITLAB_TOKEN`. É o que
  permite criar _milestones_ de grupo e o _board_ e sincronizar as colunas com as _tags_; o MCP do GitLab não faz isso.
- Opcionais: [MCP do Sentry](https://embrapa.io/docs/mcp/bug/) e [MCP do SonarQube](https://embrapa.io/docs/mcp/code/)
  (ou `SONARQUBE_URL` e `SONARQUBE_TOKEN` no ambiente), para conferir os achados e manter as ferramentas em dia; a
  CLI `gws`, para ler os relatórios no e-mail quando não há MCP nem `io-doc`.
- Python 3 (só a biblioteca padrão) e `git`. Para validar correções, Docker.

## Instalação

```sh
claude plugin marketplace add embrapa-io/alice
claude plugin install sentinel@embrapa-io
```

## Uso

Na pasta do projeto (a que reúne os clones das apps) ou dentro do clone de uma app:

```
/sentinel:alice
```

A Alice se apresenta, mostra o menu e espera a escolha. Qualquer código vale a qualquer momento da conversa, e `MH`
mostra o menu de novo. Também dá para pedir direto: «trate o relatório desta semana», «qual a próxima issue?».

| Código | Descrição |
| --- | --- |
| MH | Reexibir o menu |
| TR | Tratar o relatório inteiro: revisar, organizar o Kanban, registrar votos e lições |
| RS | Revisar o relatório da Sentinela: buscar os relatórios e conferir cada achado contra o código |
| KB | Organizar o Kanban: MRs abertos, plano com _milestones_, responsáveis e prazos, aprovação e gravação |
| SC | Sincronizar as colunas do Kanban com as _tags_ alpha, beta e release |
| CI | Corrigir a próxima _issue_ (_worktree_, teste, MR) |
| SQ | Pôr o Sentry e o SonarQube coerentes com o código |
| BP | Levar ao _boilerplate_ a correção que nasceu nele |
| VT | Registrar útil/ruído (vereditos) no Dashboard |
| IS | Redigir _issue_ para a Sentinela sobre o que o relatório errou ou deixou de ver |
| DA | Dispensar a agente |

Os _milestones_ descontam os feriados nacionais. Para os estaduais e municipais da sua Unidade, a Alice pergunta onde a
equipe trabalha e grava em `~/.config/sentinel/local-holidays.json`; contribuições com a tabela de outras Unidades
(`skills/alice/references/local-holidays.json`) são bem-vindas.
