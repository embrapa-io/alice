# `LICENSE` — Substituição para MIT

## Por que substituir?

Em aplicações Embrapa I/O "normais" (repositórios de apps reais), o `LICENSE` costuma ser um _copyright all-rights-reserved_ da Embrapa, adequado para software institucional proprietário:

```
Copyright ⓒ <ano> Brazilian Agricultural Research Corporation (Embrapa). All rights reserved.
```

Esse modelo **não serve para boilerplates**. Um boilerplate é um template público, reutilizável por qualquer Unidade Descentralizada da Embrapa (e por qualquer desenvolvedor) para derivar software novo. Se o boilerplate carregar licença restritiva, ele **contamina** todo fork descendente — e esse não é o objetivo.

A licença **MIT** é permissiva, não-contaminante (não exige que derivados sejam MIT, não exige abertura do código derivado) e compatível com uso comercial, proprietário e open-source. É o padrão universal para templates/boilerplates.

## Código de terceiros: os avisos ficam em `THIRD-PARTY-NOTICES`

Se a app nasceu de código de terceiros com licença permissiva (um _template_ da comunidade, uma biblioteca
incorporada), **o aviso de _copyright_ e o texto da licença original não podem sair do repositório**: a MIT, por
exemplo, exige que «the above copyright notice and this permission notice shall be included in all copies». A Alice
já trata isso nas apps: move o `LICENSE` de terceiros para `THIRD-PARTY-NOTICES`, na raiz, antes de gravar o `LICENSE`
da Embrapa. Esta skill segue a mesma convenção:

| Situação | O que fazer |
| --- | --- |
| Existe `THIRD-PARTY-NOTICES` | **mantê-lo intacto** e substituir o `LICENSE` pela MIT da Embrapa |
| `LICENSE` atual é permissivo de terceiros (a app não passou pela Alice) | mover o conteúdo integral para `THIRD-PARTY-NOTICES`, com a linha `Código de terceiros incorporado a esta aplicação: <origem>`, e então gravar a MIT da Embrapa |
| `LICENSE` atual é _copyleft_ (GPL, AGPL, LGPL, MPL) ou sem licença | parar e avisar o usuário: o código não pode virar _boilerplate_ MIT sem análise |

Diga ao usuário, no _diff_ final, que os avisos de terceiros foram mantidos e onde.

## Quando aplicar

Durante a genericação, substitua o conteúdo do `LICENSE` pela licença MIT com o **ano atual** (ano de quando a genericação está sendo feita). Não use `%GENESIS_ACTUAL_YEAR%` aqui — o placeholder é processado em `README.md` pela plataforma, mas o `LICENSE` vai como literal no fork. Use o ano corrente obtido de `date +%Y` ou do contexto da conversa.

## Template canônico

Copie **exatamente** este conteúdo (substituindo `<ANO>` pelo ano atual):

```
MIT License

Copyright (c) <ANO> Brazilian Agricultural Research Corporation (Embrapa)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Regras

- **Titular do copyright é a Embrapa** (`Brazilian Agricultural Research Corporation`); os autores de código de terceiros ficam no `THIRD-PARTY-NOTICES`. Não mude o titular, não coloque nome pessoal, nem nome da Unidade Descentralizada. O boilerplate é propriedade institucional.
- **Ano** = ano corrente no momento da genericação. Não `1988`, não `%PLACEHOLDER%`, não o ano do primeiro commit do repo original.
- **Não traduza** o texto da licença para português. O texto canônico MIT precisa ficar em inglês por razões jurídicas (é a forma reconhecida internacionalmente).
- **Arquivo sem extensão** (`LICENSE`, não `LICENSE.md` nem `LICENSE.txt`) — convenção Embrapa I/O.
- **Final do arquivo**: terminar com quebra de linha final (`\n`). Evita o aviso "No newline at end of file" em diffs.

## Checagem pós-substituição

Depois de substituir, confirme com um `cat LICENSE` ou leitura que:

- [ ] Primeira linha é `MIT License` (literal)
- [ ] `THIRD-PARTY-NOTICES` (quando havia código de terceiros) continua no repositório, intacto
- [ ] Linha de copyright da Embrapa contém ano atual (4 dígitos) e `Brazilian Agricultural Research Corporation (Embrapa)`
- [ ] Texto canônico da MIT presente (parágrafos: "Permission is hereby granted", "The above copyright notice", "THE SOFTWARE IS PROVIDED")
- [ ] Arquivo termina com quebra de linha

## O que NÃO fazer

- ❌ Não use Apache 2.0, GPL, BSD ou outra licença sem alinhar com o usuário — MIT é a padrão do boilerplate.
- ❌ Não remova o `LICENSE` por achar que "a plataforma gera depois". Ela não gera.
- ❌ Não deixe o copyright antigo da Embrapa ("All rights reserved") no arquivo — substitua **integralmente**.
- ❌ Não apague nem edite o `THIRD-PARTY-NOTICES`: ele guarda os avisos de terceiros que as licenças exigem.
- ❌ Não adicione cabeçalho de licença em arquivos de código-fonte. O `LICENSE` raiz é suficiente.
