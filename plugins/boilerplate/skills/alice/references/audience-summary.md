# Público do boilerplate: `audience` e `summary` no `.embrapa/settings.json`

Chaves oficiais desde nov/2026 (regras completas em https://embrapa.io/docs/boilerplate#audience). Elas decidem se o
boilerplate entra na **vitrine dos laboratórios virtuais do Forge** (https://forge.embrapa.io/lab), em que qualquer
pessoa da Unidade, sem conhecimento de TI, escolhe ferramentas prontas.

## 1. Classifique o boilerplate (pergunte ao usuário e confirme)

| `audience` | Quando | Exemplos |
| --- | --- | --- |
| `developer` (padrão; pode omitir a chave) | base para uma equipe **desenvolver** uma aplicação a partir do código | Vue + PocketBase, FastAPI + React, Laravel, Node.js |
| `end-user` | ferramenta **pronta**, usada como está pelo navegador por quem não é de TI | RStudio, JupyterLab, Joplin, Metabase, n8n, Open WebUI, GeoServer |

Sinais de `end-user`: imagem oficial de uma ferramenta de prateleira (sem código-fonte próprio, `.gitlab-io.yml` «de
prateleira»), interface web com login próprio, uso que não exige editar código. Na dúvida, é `developer`.

## 2. Se for `end-user`, o `summary` é obrigatório

Texto corrido em português do Brasil correto, **sem Markdown, sem quebra de linha e sem jargão**, de **120 a 600
caracteres**, em duas partes:

1. o que a ferramenta é, em uma ou duas frases, para leigos (nada de «container», «stack», «PostgreSQL», «deploy»);
2. `Exemplo:` e um uso concreto **na Embrapa** (pesquisa, gestão, comunicação, transferência de tecnologia).

```json
"audience": "end-user",
"summary": "Um laboratório de análise de dados em R que abre no navegador, sem instalar nada no computador. Exemplo: uma pesquisadora carrega a planilha de pesagens do experimento de suplementação, roda a análise de variância e gera os gráficos do relatório."
```

O `summary` não substitui a `description`, que continua falando com quem desenvolve (pilha, dependências).

## 3. Se for `end-user`, confira o que a vitrine promete

Cobre do usuário antes de fechar a genericação; o que faltar vai no diff final como pendência:

- [ ] **login próprio**, com a conta da dona criada na subida a partir de variáveis (ex.: `OWNER_EMAIL`, `OWNER_PASSWORD`
      ou o admin do próprio app), sem passo manual de cadastro;
- [ ] **backup íntegro**: serviços `backup` e `restore` no contrato da plataforma e o teste `test/backup-roundtrip.sh`;
- [ ] **nenhuma variável obrigatória que dependa de configuração manual** para a ferramenta funcionar (segredos de
      terceiros com `"mask": "empty"` só se a ferramenta funcionar sem eles);
- [ ] ícone da marca no catálogo (`si:<slug>` do Simple Icons ou Font Awesome).

Entrar na vitrine também exige a entrada da ferramenta no `lab-tools.json` do Forge (contas, primeiros passos, GPU):
avise o usuário, que pede isso à equipe do Forge.

## 4. Validação

O catálogo (`io/boilerplate/metadata`, `validate.py`) recusa `audience` fora de `developer`/`end-user` e `end-user` sem
`summary` válido. Rode antes de pedir a entrada no catálogo:

```bash
jq -e '(.audience // "developer") as $a | ($a == "developer" or $a == "end-user") and
  ($a == "developer" or ((.summary | type) == "string" and (.summary | length) >= 120 and (.summary | length) <= 600 and (.summary | contains("Exemplo:"))))' \
  .embrapa/settings.json && echo "✓ audience/summary" || echo "✗ audience/summary"
```
