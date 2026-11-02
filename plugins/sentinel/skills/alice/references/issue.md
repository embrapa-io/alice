# Issue para a Sentinela

Para quem mantém a Sentinela (`automaton-sentinel`), não para a equipe da app. O objetivo é que o próximo relatório,
deste e de qualquer projeto, saia melhor. O repositório (`github.com/embrapa-io/automaton-sentinel`) é privado: quem
tem acesso abre a issue lá; quem não tem entrega o texto à equipe do Embrapa I/O por e-mail (io@embrapa.br) ou no Discord (https://discord.embrapa.io).

## Modelo

Título: o que a Sentinela deve passar a fazer, numa frase. Por exemplo: «Google Play: anexar a pilha do crash aos
erros agrupados (errorReports:search)».

```markdown
## Contexto

O relatório <semanal|diário> de <projeto> (<data>) trouxe o achado "<título>" (`<identificador>`), com a ação
sugerida "<ação>". <O que a equipe precisou fazer para descobrir que não era bem isso.>

<A evidência do código ou da fonte, curta: o trecho, a pilha, a configuração. Só o mínimo, sem dado pessoal.>

<A conclusão: por que o achado ou a ação não serviam.>

## Proposta

<A mudança na coleta dos dados, nas instruções ao modelo (runbook) ou na renderização do relatório.>

1. <passo>
2. <passo>

<Custo: chamadas a mais, tokens, permissões.>

## Referência

<Commit, script ou documento que ajuda, quando houver.>
```

## Exemplo

> **Google Play: anexar a pilha do crash aos erros agrupados (errorReports:search)**
>
> **Contexto.** O relatório semanal de um app Android trouxe o achado «Crash isolado em
> WindowManagerGlobal.addView» (`IllegalStateException`, 9 relatos de 1 usuário, numa só versão), com a ação
> sugerida «checar `isFinishing` antes de mostrar o diálogo». A equipe não soube se a versão nova resolvia e teve de
> abrir o Console. A pilha mostrou que não havia nada a corrigir: `window count is over max!!`, só frames de
> `android.*`. Era o limite de janelas da interface de um fabricante, num único aparelho, num único dia.
>
> **Proposta.** Para cada grupo de erro da Google Play, buscar um relato em `errorReports:search`, guardar a mensagem,
> o início da pilha e o aparelho, contar as linhas do app (`app_frames`) e, nas instruções ao modelo, proibir sugestão
> de mudança no código quando `app_frames = 0`. Mostrar a pilha no achado.

## Antes de abrir

- Procure uma issue parecida (`gh issue list --repo embrapa-io/automaton-sentinel --state all --search "<termos>"`):
  havendo, comente nela com o caso novo. Procure de novo **imediatamente antes** de criar: outras pessoas podem estar
  triando outros projetos ao mesmo tempo.
- Nada de segredo, token, IP, e-mail, nome de pessoa, URL interna ou dado de usuário. Credencial ou dependência
  vulnerável achada numa app no ar entra só de forma genérica, sem arquivo, tipo nem versão. Pilha de framework e
  mensagem de exceção podem ir; código proprietário, só o mínimo.
- Português do Brasil, frases completas, sem exagero. Uma issue por proposta: dois problemas diferentes viram duas
  issues.
- Só depois do «sim» do usuário.
