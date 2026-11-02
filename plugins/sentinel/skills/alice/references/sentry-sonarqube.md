# Sentry e SonarQube: contexto na triagem, mudanças com aprovação

A triagem já lê o Sentry e o SonarQube para conferir um achado. Esta referência diz o que a skill também **muda**
nessas ferramentas, para que elas fiquem coerentes com o código e com o Kanban: um erro corrigido continuar «não
resolvido» no Sentry, ou um hotspot seguro continuar «a revisar» no SonarQube, faz a Sentinela repetir o achado toda
semana e esconde o que é novo.

Todas as mudanças saem com as credenciais do usuário (MCPs do Sentry e do SonarQube) e aparecem como feitas por ele.
Por isso, nada é gravado sem passar pela mesma tabela de aprovação do Kanban (passo 5). Se a credencial recusar a
escrita (401/403), a mudança vira passo manual na resposta final, com o link.

## Sentry (bug.embrapa.io)

Organização = slug do projeto; projeto = app. Consultas na sintaxe do Sentry (`is:unresolved`,
`environment:production`, `lastSeen:-7d`) em `search_issues`, `get_issue_details` e `search_issue_events`. A instância
registra só erros e crashes: não há sessões, traces nem release health.

| Situação conferida no código | Mudança | Como |
| --- | --- | --- |
| A issue do GitLab que corrige o erro chegou a uma tag **release** (passo 6) | resolver | `update_issue(status="resolved", reason="Corrigido em <tag> (MR !N, issue #M)")` |
| MR da correção mesclado, mas a release ainda não saiu | resolver na próxima versão | `update_issue(status="resolvedInNextRelease", reason=…)`; o Sentry reabre sozinho se o erro voltar numa versão posterior |
| Ruído confirmado: pilha sem nenhuma linha do app (sistema, fabricante, extensão do navegador, bot) | ignorar até escalar | `update_issue(status="ignored", ignoreMode="untilEscalating", reason="<por quê>")`; nunca `forever` sem o usuário pedir |
| Erro que ainda ocorre na versão atual | nada | nunca resolver o que ainda acontece: confira `lastSeen` e a `release` dos últimos eventos |

- A issue do GitLab leva o link do Sentry na evidência; o `reason` do Sentry leva o da issue do GitLab.
- Vários erros com a mesma causa: uma issue no GitLab, todos citados nela, cada um resolvido junto.

## SonarQube (code.embrapa.io)

Sem o MCP do SonarQube na sessão, use `scripts/sonar.py`, que lê `SONARQUBE_URL` e `SONARQUBE_TOKEN` do ambiente (ou
da configuração do MCP `sonarqube` no `~/.claude.json`): assim «revisar como seguro» não vira passo manual. Antes de
revisar um hotspot de código, leia o trecho (`sonar.py lines`): a regra genérica do SonarQube não diz se a entrada é
validada.

Chave do projeto: `<projeto>_<app>` (o `sonar.projectKey` do pipeline da plataforma). Para achar um item:
`search_security_hotspots` e `show_security_hotspot` (hotspots), `search_sonar_issues_in_projects` e `show_rule`
(issues).

| Situação conferida no código | Mudança | Como |
| --- | --- | --- |
| Hotspot seguro: `Math.random` fora de segurança, regex sem entrada externa ou com entrada limitada, `eval` de código fixo, `http` só para recurso público | revisar como seguro | `change_security_hotspot_status(status="REVIEWED", resolution="SAFE", comment="<arquivo:linha: por que é seguro>")` |
| Hotspot que a correção da issue elimina | nada agora | a próxima análise fecha; só `FIXED` se o código mudou e a análise ainda não rodou, citando o MR |
| Hotspot com risco real que a equipe decidiu aceitar | aceitar o risco | `ACKNOWLEDGED` só com a decisão explícita do usuário, e o motivo no comentário |
| Issue que o código mostra ser falso positivo (regra que não se aplica ao caso) | falso positivo | `change_sonar_issue_status(status="falsepositive")`; o motivo vai no arquivo de triagem, porque a ferramenta não aceita comentário |
| Issue verdadeira, mas a equipe decidiu não corrigir | aceitar | `accept` só com a decisão explícita do usuário |
| Issue verdadeira | nada no SonarQube | vira issue no GitLab; o SonarQube fecha sozinho quando a análise não a encontrar mais |

- Nunca revisar hotspot ou fechar issue só para melhorar a nota: cada mudança tem de ter o trecho de código que a
  justifica no arquivo de triagem.
- Arquivo gerado ou de terceiros (build, bundle, vendor) não se revisa item por item: a ação é `sonar.exclusions`,
  numa issue da app (costuma ser do boilerplate).
- Análise antiga (`stale_analysis`) ou cobertura não medida (`coverage_not_measured`): não há o que mudar no
  SonarQube.

## Cobertura de testes

A cobertura só sobe com testes, e só aparece no SonarQube quando o pipeline importa o relatório deles. O pipeline da
plataforma (`.gitlab-io.yml`) roda o `sonar-scanner`; enquanto ele não importar o relatório de cobertura, a app mostra
0% ou «não medida», com ou sem testes. Por isso, a skill:

- **não** trata cobertura como achado nem tenta subi-la numa execução;
- inclui um **teste de regressão** em toda correção (passo 7), quando a app já tem estrutura de testes;
- numa app sem estrutura de testes, propõe **uma** issue `Request` «Estrutura de testes» (tamanho M): runner em
  Docker, relatório de cobertura e os primeiros testes da lógica pura (cálculo, simulação, validação), que é o que mais
  vale e o mais fácil de testar. Uma vez por app, não a cada relatório.
