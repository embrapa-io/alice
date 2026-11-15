# Público do boilerplate e a entrada no Hub do Forge

O Hub do Forge (https://forge.embrapa.io/hub) é onde um setor ou uma comissão monta, sem conhecimento de TI, o seu
conjunto de ferramentas prontas (o título por extenso de cada hub é como «Hub de Automação — CNPGC/CSST»; no resto, só
«Hub»). Regras completas em https://embrapa.io/docs/boilerplate#hub.

Cada boilerplate do Hub tem **todas** as suas informações em só dois lugares:

- **`.embrapa/settings.json` do boilerplate**: o contrato técnico (variáveis com tipo, `mcp`). **Não grave `audience`
  nem `summary` nele**: essas chaves saíram em 15/11/2026, e o validador do catálogo acusa quem ainda as tem.
- **`hub.json` de `io/boilerplate/metadata`**: a curadoria e a orquestração da ferramenta (resumo, exemplo, papel,
  ícone, endereços, variáveis que o Forge preenche, acesso, primeiros passos). Entra **por MR** naquele repositório.

## 1. Classifique o boilerplate (pergunte ao usuário e confirme)

| Público | Quando | Exemplos |
| --- | --- | --- |
| desenvolvimento | base para uma equipe **desenvolver** uma aplicação a partir do código | Vue + PocketBase, FastAPI + React, Laravel, Node.js |
| público final (Hub) | ferramenta **pronta**, usada como está pelo navegador por quem não é de TI | RStudio, JupyterLab, Joplin, Metabase, n8n, NocoDB, GeoServer |

Sinais de público final: imagem oficial de uma ferramenta de prateleira (sem código-fonte próprio, `.gitlab-io.yml` «de
prateleira»), interface web com login próprio, uso que não exige editar código. Na dúvida, é de desenvolvimento, e nada
muda no `settings.json`.

## 2. Se for de público final, confira o que o Hub promete

Cobre do usuário antes de fechar a genericação; o que faltar vai no diff final como pendência:

- [ ] **login próprio**, com a conta de quem cria o hub gerada na subida a partir de variáveis (ex.: `OWNER_EMAIL`,
      `OWNER_PASSWORD` ou o admin do próprio app), sem passo manual de cadastro;
- [ ] **backup íntegro**: serviços `backup` e `restore` no contrato da plataforma e o teste `test/backup-roundtrip.sh`;
- [ ] **nenhuma variável obrigatória que dependa de configuração manual** para a ferramenta funcionar (segredos de
      terceiros com `"mask": "empty"` só se a ferramenta funcionar sem eles);
- [ ] variáveis que o Forge vai preencher com tipo `TEXT` (URL pública, e-mail e nome de quem cria o hub, fuso `TZ`,
      SMTP), senhas iniciais `PASSWORD` ou `SECRET` e endereços `PORT`;
- [ ] ícone da marca no catálogo (`si:<slug>` do Simple Icons ou Font Awesome).

## 3. Proponha a entrada no `hub.json` (por MR no `io/boilerplate/metadata`)

Escreva com o usuário a entrada da ferramenta e abra o MR no metadata **depois** de o boilerplate estar na `main` e no
`boilerplates.json`. Copie a estrutura de uma entrada parecida do `hub.json` e siga a referência de cada campo no README
do metadata (seção «`hub.json`»). O essencial:

- `summary`: texto corrido em português do Brasil correto, **sem Markdown, sem quebra de linha e sem jargão** (nada de
  «container», «stack», «PostgreSQL», «deploy»), de 60 a 400 caracteres, dizendo o que a ferramenta é para leigos;
- `example`: um uso concreto **na Embrapa** (pesquisa, gestão, comunicação, transferência de tecnologia), sem pessoa com
  gênero («Montar o painel…», e não «a pesquisadora monta…»);
- `role`: `is` (quando é a escolha) e `not` (quando não é, citando a ferramenta do Hub que serve no lugar);
- `icon`: nome Lucide em PascalCase (`ChartLine`; o `boilerplates.json` usa outro formato, Font Awesome ou Simple Icons);
- `apps`: `hosts` (variável `PORT` e subdomínio), `fixed` (com `{url:VAR}`, `{owner}`, `{person}`, `{timezone}`…),
  `smtp`, `access` (usuário e variável da senha inicial), `external`, `first_steps` e, quando há, `ready`.

Linguagem neutra em todo texto visível: «Conta de administração do …», «quem criou o hub», «você»; nunca «dona»,
«dono» ou «administradora».

## 4. Validação

No clone do metadata, com a entrada nova:

```bash
python3 -m unittest test_validate
GITLAB_TOKEN=$(glab config get token --host git.embrapa.io) python3 -I validate.py
```

O `validate.py` confere a estrutura do `hub.json` e cada variável citada contra o `settings.json` do boilerplate na
`main` (existe e tem o tipo certo). No boilerplate, confira que as chaves antigas não voltaram:

```bash
jq -e 'has("audience") or has("summary") | not' .embrapa/settings.json && echo "✓ sem audience/summary" || echo "✗ tire audience/summary (vão para o hub.json)"
```
