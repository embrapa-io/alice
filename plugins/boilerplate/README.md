# Plugin `boilerplate` — a Alice criando boilerplates do Embrapa I/O

Transforma uma aplicação já aderente ao **Embrapa I/O** (validada pelo plugin `compliance`) em um _boilerplate_ do
catálogo da plataforma: palavras-chave `%GENESIS_*%` no lugar dos nomes reais, licença MIT com os avisos de terceiros,
`AGENTS.md`, `.gitlab-io.yml`, metadados e mantenedores, análise do SonarQube e a entrada no catálogo.

É para quem mantém _boilerplates_; quem só desenvolve aplicações precisa apenas do plugin `compliance`.

## Instalação (Claude Code)

```bash
claude plugin marketplace add embrapa-io/alice   # se ainda não adicionou o marketplace
claude plugin install boilerplate@embrapa-io
```

## Uso

Abra o Claude Code na pasta da aplicação (um clone no repositório `io/boilerplate/<nome>`, pedido à equipe da
plataforma) e chame `/boilerplate:alice` (digitar `/alice` lista as Alices instaladas).

| Código | Descrição |
| --- | --- |
| MH | Reexibir o menu |
| GB | Gerar o boilerplate (fluxo completo) |
| VS | Auditar versões e propor upgrades |
| GL | Gravar ou revisar o `.gitlab-io.yml` |
| SQ | SonarQube antes do catálogo |
| CT | Publicar no catálogo (`metadata/boilerplates.json`) |
| DA | Dispensar a agente |

Documentação: https://embrapa.io/docs/boilerplate
