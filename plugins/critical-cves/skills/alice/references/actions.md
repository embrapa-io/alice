# Roteiro por ação

Cada seção diz como confirmar, o que propor, como executar e como validar. O texto da ação que a equipe recebeu
no e-mail do alerta está em `action_text`; use-o como referência do que já foi dito a ela.

## Sumário

- [Gerar a tag de deploy](#tag)
- [A imagem nova já corrige?](#upstream)
- [bump_dependency](#bump_dependency)
- [bump_pinned](#bump_pinned)
- [pin_then_upgrade](#pin_then_upgrade)
- [restart_upgrade](#restart_upgrade)
- [releaser_upgrade, releaser_manual e releaser_stop](#releaser)
- [no_fix_restrict, no_fix_undeploy e stale_undeploy](#no_fix)

---

## Gerar a tag de deploy {#tag}

As ações que mudam o código só entram no ar com uma tag nova, criada **na branch do estágio** (`alpha`, `beta` ou
`release`). Uma tag fora do formato, ou criada fora da branch do estágio, é ignorada pela plataforma
(https://embrapa.io/docs/deploy).

- **Formato:** `macro.AA.M-<estágio>.patch` em alpha e beta (`2.26.10-beta.7`); em release, sem o estágio
  (`2.26.10-3`).
- **Próxima versão:** parta da `deployed_version` da build. Mantenha o macro e o milestone e some 1 ao patch:
  `2.26.9-beta.4` → `2.26.9-beta.5`. Antes, confira se a versão já existe:
  `git tag -l '<macro>.<milestone>-*' --sort=-v:refname | head`. Se o usuário quiser outro milestone, ele diz.
- **O que entra na branch do estágio.** O caminho normal é commit na `main` e merge da `main` no estágio. Mas, se a
  `main` estiver à frente da tag implantada com trabalho que ainda não deveria subir
  (`git log --oneline <deployed_version>..origin/main`), o merge levaria tudo junto para o ar. Nesse caso, proponha
  a correção mínima direto na branch do estágio (ou um cherry-pick do commit da correção) e o merge de volta na `main`
  depois. Mostre o `git log` ao usuário e deixe que ele escolha.
- **Sem bagunçar a cópia de trabalho:** faça a mudança num worktree
  (`git worktree add ../<app>-cve-<estágio> origin/<estágio>`) quando a cópia atual tiver alterações não commitadas
  ou estiver em outra branch.
- **Sequência**, cada push com confirmação: commit → `git push origin <branch>` → `git tag <versão>` na branch do
  estágio → `git push origin <versão>`. Depois do push da tag, a plataforma implanta a versão em alguns minutos.
- **Releaser:** a build também sobe por tag da branch do estágio; o Releaser do servidor busca a tag sozinho.

## A imagem nova já corrige? {#upstream}

Reiniciar com "Atualizar imagens" só resolve se a imagem mais nova publicada **na mesma tag** já traz o pacote na
versão corrigida. Nem sempre traz: é comum o fornecedor de uma imagem demorar semanas para publicar uma versão que
incorpore a dependência corrigida. Nesse caso o restart é inútil, e a saída pode ser trocar de tag ou desativar.

Antes de propor um restart (ou de dar por resolvido um bump de imagem), confira em Docker, na máquina local:

```sh
docker pull <imagem>:<tag>
# pacote do sistema (Debian/Ubuntu, Alpine) ou de linguagem
docker run --rm --entrypoint sh <imagem>:<tag> -c 'dpkg-query -W <pacote> 2>/dev/null || apk info -v <pacote> 2>/dev/null; pip show <pacote> 2>/dev/null | head -2'
# ou o veredito direto, para a CVE
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image --quiet --scanners vuln <imagem>:<tag> | grep <CVE>
```

- Versão corrigida presente: o restart (ou a tag nova) resolve; siga.
- Ainda vulnerável: diga ao usuário que reiniciar não adianta. Procure se há versão mais nova da imagem em outra tag
  (página de releases do fornecedor, Docker Hub) e trate como `bump_pinned` ou `pin_then_upgrade`; se não houver
  nenhuma, trate como `no_fix_*` (o fornecedor ainda não publicou a correção).

O `trivy` no Docker baixa a base de vulnerabilidades na primeira execução (algumas centenas de MB); avise antes.

## bump_dependency {#bump_dependency}

A versão vem do lockfile da app (`target`: `package-lock.json`, `composer.lock`, `poetry.lock`, `requirements.txt`…).
Reiniciar a build **não** corrige.

1. Localize a dependência no lock e no manifesto. Direta: suba a faixa no manifesto. Transitiva: descubra quem a puxa
   (`npm ls <pacote>`, `composer why <pacote>`, `pip show`/`pipdeptree`) e prefira atualizar o pai; se o pai ainda
   não liberou, use o mecanismo de override do ecossistema (`overrides` no npm, `resolutions` no yarn, restrição
   explícita no composer ou no pip).
2. Atualização **mínima** até `fixed` ou posterior. Se cruzar versão maior, leia o changelog e aponte as quebras de
   API que tocam o código da app (grep pelos usos).
3. Gere o lock em Docker, com a mesma imagem de base do Dockerfile da app (ex.:
   `docker run --rm -v "$PWD":/app -w /app node:24 npm install <pacote>@<versão>`), nunca com o toolchain instalado
   na máquina.
4. Valide: build da imagem (`docker compose build <serviço>`) e os testes da app, se houver. Mostre o diff do
   manifesto e o trecho do lock com a versão nova.
5. Siga para a [tag](#tag).

## bump_pinned {#bump_pinned}

A imagem tem versão exata fixada (`postgres:18.4`, `FROM python:3.12.3-slim`). Localize a linha no
`docker-compose.yaml` ou no Dockerfile e proponha a versão mais próxima que contenha a correção, no mesmo nível de
granularidade que a equipe escolheu (se ela fixou o patch, fixe o patch). Confira [se a imagem nova corrige](#upstream)
e então siga para a [tag](#tag). Em serviços com dados, mudar só o patch é seguro; mudar a versão maior não é: trate
como `pin_then_upgrade`.

## pin_then_upgrade {#pin_then_upgrade}

A imagem usa `latest` ou não tem tag. Um restart com "Atualizar imagens" puxaria o que estiver em `latest` hoje, que
pode ser uma versão maior nova, com mudanças incompatíveis, e num banco de dados pode deixar o volume ilegível.

1. Descubra a versão maior **em uso**: o campo `images` da build, `build_info`/`get_build_health` pelo MCP, a
   documentação ou o histórico do projeto. Na dúvida, pergunte ao usuário; não chute a versão de um banco.
2. Proponha fixar a versão maior (ou a menor, na série 0.x: `pocketbase:0.40`) no `docker-compose.yaml` ou no
   Dockerfile, conforme a política da plataforma (https://embrapa.io/docs/app).
3. Confira [se a imagem dessa versão maior já corrige](#upstream). Se a correção só existe numa versão maior nova,
   isso é uma migração: descreva o plano (backup, procedimento de upgrade do fornecedor, teste local com cópia dos
   dados) e não execute sem que o usuário peça explicitamente.
4. Siga para a [tag](#tag): o deploy da tag nova já puxa a imagem fixada.

## restart_upgrade {#restart_upgrade}

Tag parcial (`php:8.3-apache`, `postgres:18`) ou serviço com `build:` sobre base atualizável: a correção é puxar a
imagem de novo.

1. Confirme no código que a tag é parcial e que nada fixa o pacote no Dockerfile.
2. Confira [se a imagem nova corrige](#upstream). Num serviço com `build:`, olhe a imagem do `FROM`. Se ainda estiver
   vulnerável, **não reinicie**: volte ao usuário com as alternativas.
3. Mostre a chamada e espere o "pode": `restart_build` com `project`, `app`, `stage` e `upgrade: true`. Não use
   `remove: true`: ele recria os contêineres do zero e não é necessário para atualizar imagens.
4. Depois, confira com `get_build_health` se os serviços voltaram (estado running/healthy).

## releaser_upgrade, releaser_manual e releaser_stop {#releaser}

A build roda num servidor operado pela equipe local, pelo Releaser (https://embrapa.io/docs/releaser); o MCP não
reinicia nem desativa essas builds. Prepare para o usuário o comando e uma mensagem curta para quem opera o servidor
(`releaser.server`), em texto corrido, sem marcação, pronta para colar:

- `releaser_upgrade`: `io restart <projeto>/<app>@<estágio> --upgrade` (Releaser 1.26.10-10 ou mais novo).
- `releaser_manual`: Releaser antigo, sem `--upgrade`: `docker pull` das imagens da build, `io deploy --force` e, em
  seguida, atualizar o Releaser (https://embrapa.io/docs/releaser#update).
- `releaser_stop`: `io stop <projeto>/<app>@<estágio>`.

Se `releaser.seen` for antigo (o Releaser não dá notícias), avise que o dado de CVE pode estar desatualizado e que o
primeiro passo é saber se o servidor está de pé. As verificações de [imagem nova](#upstream) valem igual: peça a quem
opera o servidor que só reinicie depois de confirmada a correção na imagem.

## no_fix_restrict, no_fix_undeploy e stale_undeploy {#no_fix}

Não há versão corrigida (`fixed` vazio), ou a build está sem deploy há meses. Antes de tudo, confira se a correção
não saiu depois da última varredura (releases do pacote, a página da CVE no NVD ou no GitHub Advisory); se saiu,
trate pela ação correspondente.

- **Restringir** (`no_fix_restrict`, nível Alta): proponha o que é possível no código da app ou na frente dela
  (desligar o recurso vulnerável, bloquear a rota, exigir autenticação). Em alpha e beta, desativar costuma ser o
  mais simples.
- **Tirar do ar** (`no_fix_undeploy`, `stale_undeploy`, ou quando o usuário decide):
  1. **Backup**, se a build guarda dados: confira se o `docker-compose.yaml` tem o serviço `backup`. Se tiver, mostre
     a chamada `request_backup` e espere o "pode". O backup roda em segundo plano e o resultado chega por e-mail aos
     mantenedores; só siga quando o usuário confirmar que o e-mail chegou com sucesso. Sem serviço `backup`, diga que
     não há cópia pela plataforma e pergunte se segue assim mesmo.
  2. **Desativar**: mostre a chamada `undeploy_build` (`project`, `app`, `stage`) e espere o "pode". A configuração
     da build e os volumes são preservados; um deploy novo traz a build de volta.
  3. O episódio do alerta fecha como "desativado" na varredura seguinte.
- Manter no ar sem correção é decisão consciente da equipe; se for o caso, registre no relato final o motivo e o que
  vai disparar a revisão (ex.: "quando sair a versão do fornecedor").
