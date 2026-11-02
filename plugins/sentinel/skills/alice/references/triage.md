# Modelo do arquivo de triagem

Um arquivo por triagem, `sentinel-AAAA-MM-DD.md`, na pasta do projeto que reúne os clones (ou na pasta-mãe do clone
da app), **fora** dos repositórios das apps: o arquivo cita versões vulneráveis e falhas abertas e não vai para git
nenhum. É o registro da triagem e a entrada da votação. Siga a estrutura abaixo, sempre igual, para que triagens de
projetos diferentes possam ser somadas.

## Vereditos

| Veredito | Quando | Voto (`vote`) |
| --- | --- | --- |
| `ok` | procede e a ação serve (do app, do boilerplate ou fora do código) | `useful` |
| `wrong_action` | o problema existe, mas a ação sugerida não serve como escrita | `useful` |
| `partial` | parte procede, parte já estava resolvida no código ou não se aplica | `useful` |
| `stale` | era verdade em algum momento, mas não no momento do relatório | sem voto (`noise` silenciaria o achado para sempre) |
| `noise` | falso positivo, dado mal lido, observação sem ação | `noise` |
| `unverified` | a fonte não estava acessível na triagem | sem voto |

O veredito é o campo `verdict` da tool `vote_sentinel_findings` do MCP do Dashboard: o JSON do fim do arquivo vira
direto a chamada (passo 9 do SKILL.md).

## Estrutura

```markdown
---
project: <slug> (<nome>)
reports:
  - <caminho no io-doc ou "prévia AAAAMMDDTHHMMSSZ"> (gerado DD/MM/AAAA HH:MM, período …, modelo <provedor/modelo>)
reviewed: AAAA-MM-DD, contra <branch e commit de cada app>, fontes: <Sentry, SonarQube, Dashboard, GitLab…>
limitations: <fonte que não estava acessível e o que ficou sem conferir; "nenhuma">
kanban: https://git.embrapa.io/groups/<projeto>/-/boards (<N> issues criadas)
sentinel_issues: <issues redigidas ou comentadas para a Sentinela; "nenhuma">
votes_recorded: <yes | no (motivo)>
---

# Triagem da Sentinela · <nome>, relatório de DD/MM/AAAA

## Placar

| Veredito | Quantidade | Identificadores |
(uma linha por veredito, inclusive os zerados de ok, wrong_action, partial e noise)

## Achados

| ID | App | Título curto | Veredito | Voto | Issue na app | Lição para a Sentinela |

### `<id>` · <título do relatório> (<app>, <severidade>)

- **Relatório:** o que disse e a ação sugerida, em uma ou duas frases.
- **Conferência:** o que o código e as fontes mostraram, com arquivo e linha, versão, data.
- **Onde errou:** (só em wrong_action, partial, stale e noise) o que a Sentinela não viu ou leu errado.
- **Lição:** a regra que evitaria o erro, e a issue que a registra (se houver).

## Sentry e SonarQube

| Ferramenta | Item | Mudança | Justificativa (arquivo:linha, versão) | Gravado |
| --- | --- | --- | --- | --- |

Só o que foi aprovado; «Gravado» é `sim`, `não` (recusado) ou `manual` (sem permissão, com o link).

## Lacunas

| Lacuna | Evidência | Virou |
(o que o código mostrou e o relatório não viu)

## Lições para a Sentinela

| Regra proposta | Achados | Issue (nova, comentada ou texto entregue à equipe do Embrapa I/O) |

## Votos (JSON)

{"project": "<slug>", "report": "<caminho ou stamp>", "reviewed_at": "AAAA-MM-DD",
 "votes": [{"fingerprint": "<id>", "vote": "useful|noise|null", "verdict": "ok|wrong_action|partial|stale|noise|unverified", "reason": "<uma linha>"}]}
```

O JSON vai num bloco ```json no arquivo. `reason` em uma linha (até 300 caracteres), sem nome de pessoa, segredo,
IP, e-mail nem versão vulnerável: vai para o banco da plataforma e, nos vereditos `wrong_action` e `partial`, também
para o modelo da Sentinela na execução seguinte (ver o passo 9 do SKILL.md). Nesses dois, escreva a orientação, não
o julgamento: «a ação certa é X» ou «só Y procede; Z já foi corrigido em <commit>».
