# Análise do SonarQube antes de publicar no catálogo

Um boilerplate com código-fonte próprio só deve entrar no catálogo (`io/boilerplate/metadata`, arquivo `boilerplates.json`) **depois** de a análise do SonarQube dele estar limpa. O motivo é o mesmo que justifica analisar boilerplates: o código dele se replica em toda app criada a partir dele, e um defeito na origem vira um defeito em cada projeto derivado (o ReDoS na validação de e-mail, em 2026, exigiu dezenas de MRs). Corrigir antes de publicar custa uma vez; depois, custa uma vez por app.

Boilerplate **de prateleira** (o `.gitlab-io.yml` declara não haver pipeline): não há análise; pule esta etapa.

## 1. O projeto no SonarQube

Depois que o repositório existir em `io/boilerplate/<nome>` com o `.gitlab-io.yml` de análise na `main`, o automaton-sonarqube (comando `boilerplate`, de hora em hora) cria o projeto `boilerplate_<nome>` (rótulo `boilerplate/<nome>`), liga o CI, aponta o projeto para o `.gitlab-io.yml` e dá acesso aos membros do projeto no GitLab. Para não esperar a próxima hora, quem administra a plataforma roda no core:

```sh
cd ~/embrapa.io/automaton-sonarqube
docker compose exec automaton php /app/run.php boilerplate --apply
```

## 2. Disparar a análise

Não precisa de commit: em `io/boilerplate/<nome>`, **Build › Pipelines › Run pipeline** na `main`, ou pela API:

```sh
GITLAB_HOST=git.embrapa.io glab api -X POST "projects/io%2Fboilerplate%2F<nome>/pipeline?ref=main"
```

Não reexecute um pipeline antigo: ele usa a configuração da época dele. Se o arquivo da pilha restringir a regra a `push` (era o caso do .NET), inclua `web` e `api` em `$CI_PIPELINE_SOURCE`.

## 3. Ligar o MCP do SonarQube no Claude Code

**Sempre oriente o usuário a fazer isto ao final do desenvolvimento**, se o MCP `sonarqube` ainda não estiver disponível na sessão (ferramentas `mcp__sonarqube__*`):

1. Gerar um token de usuário em https://code.embrapa.io › *My Account* › *Security* › *Generate Tokens* (tipo *User Token*).
2. Registrar o servidor oficial da SonarSource (roda em Docker; nada é instalado na máquina):

   ```sh
   claude mcp add sonarqube --scope user \
     -e SONARQUBE_URL=https://code.embrapa.io \
     -e SONARQUBE_TOKEN=<token> \
     -- docker run -i --rm -e SONARQUBE_TOKEN -e SONARQUBE_URL mcp/sonarqube
   ```

3. Reiniciar a sessão do Claude Code (ou conferir com `/mcp`).

O token é pessoal: não o registre em arquivo versionado nem em mensagem.

## 4. Usar a análise para corrigir

Com o MCP ativo, na própria sessão:

- `get_project_quality_gate_status` com `projectKey: boilerplate_<nome>` — o quality gate.
- `get_component_measures` — bugs, vulnerabilidades, *code smells*, *security hotspots*, duplicação e notas.
- `search_sonar_issues_in_projects` (projeto `boilerplate_<nome>`) e `search_security_hotspots` — a lista do que corrigir, com arquivo e linha; `show_rule` explica cada regra.

Ordem: **vulnerabilidades e *security hotspots* → bugs → duplicação → *code smells***. Corrija no código do boilerplate, mantendo os placeholders `%GENESIS_*%` e a conformidade da Alice; rode a análise de novo (passo 2) até o quality gate passar e não restar vulnerabilidade nem bug. Problemas que não fizerem sentido corrigir (falso positivo, regra que não se aplica à pilha) devem ser marcados no SonarQube com a justificativa, e não ignorados em silêncio.

## 5. Só então, o catálogo

Com a análise limpa, inclua o boilerplate em `boilerplates.json` do repositório `io/boilerplate/metadata` (via MR). Registre no diff final ao usuário o estado da análise: quality gate, e quantos bugs, vulnerabilidades e hotspots restaram (idealmente zero).
