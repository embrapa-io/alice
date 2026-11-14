# Servidor MCP oficial ligado por padrão (`mcp` no `.embrapa/settings.json`)

Regra da plataforma (decisão de 14/11/2026): **se a ferramenta do boilerplate tem servidor MCP oficial, o boilerplate sobe
com ele ligado**, para que a configuração das instâncias (e o trabalho com os dados delas) seja feita por agentes de IA
via MCP, e não por cliques. Documentação pública: https://embrapa.io/docs/boilerplate#mcp. O catálogo
(`io/boilerplate/metadata`, `validate.py`) recusa uma declaração `mcp` fora destas regras.

## 1. Existe MCP oficial?

Pesquise na documentação e no GitHub **da própria ferramenta** (não em agregadores). Conta como oficial o servidor
mantido pelo projeto ou pela empresa da ferramenta: embutido na aplicação (n8n, Metabase), plugin oficial (WordPress
`mcp-adapter`) ou pacote oficial (Posit `mcptools` para o R). Servidor da comunidade **não** entra no boilerplate, mesmo
que popular: sem garantia de manutenção nem de correção de falhas. Registre a pesquisa no diff final (o que achou, URL).

Se não houver oficial, não declare `mcp` e diga isso no diff final. Se o oficial exigir licença paga no self-hosted ou
for só local (stdio, sem como chegar pela rede), também não ligue; anote o motivo.

## 2. Como ligar

- **Mesmo endereço da aplicação**, num caminho (`/mcp` de preferência). Nada de porta nova: o MCP passa pelo roteador
  da plataforma e pelo _firewall_ dos _clusters_ como o resto.
- **Sempre com token.** Variável nova do tipo `SECRET` (sorteada na criação da _build_), em geral `MCP_TOKEN`. Todo
  pedido exige `Authorization: Bearer <token>`; sem ele, ou com o errado, `401` e nada chega à ferramenta. Quando a
  ferramenta não autentica o MCP por um token fixo, ponha na frente um proxy (nginx) que confira o cabeçalho, como o
  boilerplate `rstudio` faz. Valide o formato do token na subida e nunca o escreva em log.
- **Teste automatizado** em `test/mcp.py` (só biblioteca padrão, token pelo ambiente, nunca na linha de comando):
  `401` sem token e com token errado; com o token, `initialize` e `tools/list`; uma chamada real a uma _tool_.
- O MCP não pode mudar o que o backup guarda: rode de novo o `test/backup-roundtrip.sh`.

## 3. Declarar no `.embrapa/settings.json`

```json
"mcp": {
  "port": "PORT",
  "path": "/mcp",
  "token": "MCP_TOKEN",
  "server": "mcptools (Posit)",
  "docs": "https://posit-dev.github.io/mcptools/"
}
```

`port` é o **nome** de uma variável `PORT`; `token`, o **nome** de uma variável `SECRET`; `docs`, endereço `https`.
Nenhum outro atributo é aceito.

## 4. README e aviso de dados

No README, uma seção «MCP» com o endereço, como usar o token num cliente MCP e o aviso: o MCP entrega ao agente os
dados da instância; com um modelo externo (Claude, Gemini, ChatGPT), os dados saem da Embrapa. Para dado interno ou
sigiloso, use um agente ligado aos GPU Servers da plataforma (por exemplo, o Hermes).

## Conferência rápida

```sh
jq -e '(.mcp // null) as $m | if $m == null then true else
  ([.variables | if type=="object" then .[] else . end | .[]] ) as $v
  | ($v | map(select(.name==$m.port and .type=="PORT")) | length > 0)
  and ($v | map(select(.name==$m.token and .type=="SECRET")) | length > 0)
  and ($m.path | startswith("/")) and ($m.docs | startswith("https://")) end' .embrapa/settings.json
```
