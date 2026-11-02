# `AGENTS.md` do boilerplate

Todo boilerplate do catálogo traz na raiz um `AGENTS.md`: as diretrizes da plataforma para os assistentes de IA
(Claude Code, Gemini CLI, Copilot, Codex…) de quem fizer _fork_. A Alice **não** gera esse arquivo: ele nasce aqui,
na genericação, e acompanha o modelo.

## Como gerar

1. Escolha um boilerplate de referência da mesma família (código próprio com banco: `nodejs-postgresql`,
   `bun-postgresql`, `php-slim-postgresql`; ferramenta de prateleira: `gitea`, `leantime`) e leia o `AGENTS.md` dele,
   que é público:
   `https://git.embrapa.io/io/boilerplate/<referência>/-/raw/main/AGENTS.md`
2. Mantenha a estrutura e as regras da plataforma (as seções «Diretrizes da Plataforma Embrapa I/O», de 1 a 10, e
   «Comportamentos do Agente») e **reescreva o que é da pilha**:
   - «Sobre este Codebase»: nome do boilerplate, tecnologias, tipo (SOURCE ou TOOL), plataforma, propósito;
   - estrutura de pastas, comandos (instalar, testar, migrar), exemplos de código de variáveis de ambiente sem
     _fallback_ na linguagem da app (ex.: `os.environ["X"]` em Python), integrações Sentry e Matomo como estão no
     código, serviços `backup`, `restore` e `sanitize` como estão no `docker-compose.yaml`;
   - linting e formatação das ferramentas que a app usa de fato.
3. Nada de nome do projeto de origem, _slugs_ reais, DSN, IDs do Matomo ou e-mails pessoais. Onde o nome do projeto
   ou da app for útil, use as _keywords_ (`%GENESIS_PROJECT_UNIX%`, `%GENESIS_APP_UNIX%`): o Genesis as substitui em
   todo arquivo que não começa com ponto, inclusive este.
4. Português brasileiro com acentos; nomes de arquivos, variáveis e comandos como no código.
5. Mostre ao usuário as seções que mudaram em relação à referência.
