# `.gitlab-io.yml` do boilerplate

## O que é e por quê

O GitLab da Embrapa (git.embrapa.io) lê a configuração de pipeline das aplicações em **`.gitlab-io.yml`**, na raiz do repositório, e não no `.gitlab-ci.yml` (decisão de outubro de 2026). É a mesma lógica do `.env` × `.env.io`: os dois arquivos ficam lado a lado e o `.io` é o da plataforma. O `.gitlab-ci.yml` é **da equipe**: a plataforma não o lê, não o cria e não o exige.

O `.gitlab-io.yml` do boilerplate é o **modelo** copiado para toda app criada a partir dele (o Genesis cria a app por *fork*). Por isso o boilerplate precisa trazer o arquivo certo para a pilha dele. Se faltar, a app recebe do automaton-sonarqube um arquivo genérico com a análise — inadequado para pilhas com necessidades próprias (o .NET, por exemplo) e indevido em boilerplates de ferramenta.

## 1. Classificar a app

| Tipo | Como reconhecer | `.gitlab-io.yml` |
|---|---|---|
| **Com código-fonte próprio** | arquivos de código fora de `docker/`, `.embrapa/` e `docs/` (`.js`, `.ts`, `.vue`, `.py`, `.php`, `.cs`, `.java`, `.go`, `.dart`…) e/ou manifesto de dependências (`package.json`, `composer.json`, `requirements.txt`, `pyproject.toml`, `*.csproj`, `go.mod`) | com a análise do SonarQube |
| **De prateleira** (ferramenta de terceiros) | só sobe uma imagem pronta (banco, servidor de e-mail, armazenamento de objetos, ferramenta *no-code*): `docker-compose.yaml`, configuração e documentação, sem código próprio | sem pipeline |

Proponha a classificação com a evidência (contagem de arquivos de código, manifestos encontrados) e **confirme com o usuário**. Casos de fronteira: um boilerplate feito para a equipe *gerar* código (ex.: `vibe-coding`) é «com código», mesmo vazio; uma ferramenta com uma pasta de extensões de exemplo (ex.: `directus`) é decisão do usuário.

## 2. Gravar o arquivo

**Com código-fonte próprio** — parta de `assets/gitlab-io.yml`. Se a app já tem um `.gitlab-io.yml` ajustado à pilha (o .NET usa `dotnet sonarscanner`, com imagem do SDK e `before_script` próprios), **preserve-o** e só confira a chave do projeto. A chave tem de ser calculada pelo **último nível do grupo**:

```
-Dsonar.projectKey="${CI_PROJECT_NAMESPACE##*/}_${CI_PROJECT_NAME}"
```

Nas apps (grupo de um nível) isso dá `<projeto>_<app>`, a chave de sempre; no repositório do próprio boilerplate, cujo grupo é `io/boilerplate`, dá `boilerplate_<nome>` (a barra não é aceita em chave do SonarQube). Troque qualquer `"${CI_PROJECT_NAMESPACE}_${CI_PROJECT_NAME}"` por essa forma, inclusive no `export SONAR_PROJECT_KEY=...` do .NET.

**De prateleira** — use `assets/gitlab-io-sem-analise.yml`: `workflow: rules: - when: never` (nenhum pipeline é criado) e um job mínimo, porque o GitLab recusa configuração sem nenhum job visível. O arquivo tem de existir mesmo assim: é ele que diz à plataforma que a ausência de análise é escolha, e não esquecimento.

## 3. O `.gitlab-ci.yml`

O boilerplate **não deve trazer `.gitlab-ci.yml`**: ele iria para toda app nova como se fosse da equipe.

- Se for o antigo da plataforma (tem `sonar-scanner` ou `dotnet sonarscanner`): remova-o — o conteúdo vive agora no `.gitlab-io.yml`.
- Se for um pipeline próprio da app (build, testes): **pergunte ao usuário** antes de remover. Se ele quiser que esse pipeline rode nas apps derivadas, o caminho é incluí-lo no `.gitlab-io.yml` (`include: - local: .gitlab-ci.yml`) e o job da análise passa a ter `stage: .post`, `needs: []` e `inherit: { default: false, variables: false }`, para não herdar imagem, `before_script`, tags e variáveis globais do arquivo da equipe — mas aí o `.gitlab-ci.yml` tem de ir junto, e isso é decisão dele.

## 4. Conferência

- A Alice (regra 5.5) acusa a falta do `.gitlab-io.yml` e aceita as duas variantes; o aviso 5.5b aparece se o arquivo existe sem o scanner e sem declarar «sem pipeline».
- No README do boilerplate, a árvore de arquivos deve citar o `.gitlab-io.yml` (pipeline da plataforma) e nunca o `.gitlab-ci.yml`.
- Depois de publicado em `io/boilerplate`, o automaton-sonarqube (comando `boilerplate`, de hora em hora) cria o projeto `boilerplate_<nome>` no SonarQube para os boilerplates com análise, liga o CI, aponta o projeto para o `.gitlab-io.yml` e dá acesso aos membros do projeto no GitLab. Antes de o boilerplate entrar no catálogo, a análise tem de estar limpa: ver `references/sonarqube-antes-do-catalogo.md`.
