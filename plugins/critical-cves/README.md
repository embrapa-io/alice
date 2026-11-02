# Embrapa I/O — CVEs críticos (agente Alice)

Plugin do Claude Code que trata os alertas de CVEs críticos da plataforma [Embrapa I/O](https://embrapa.io/docs/cve):
vulnerabilidades em exploração ativa, segundo catálogos KEV, exploráveis sem login e sem ação de usuário.

A agente **Alice** roda dentro do repositório da app, lista as builds afetadas pelo MCP do Dashboard, confere cada CVE
no código da versão implantada e executa, build a build e sempre com confirmação explícita, a ação indicada pelo
alerta: atualizar a dependência no lockfile, subir ou fixar a versão da imagem (com commit e tag de deploy), reiniciar
com atualização de imagens, preparar os comandos do Releaser ou, quando não há correção, fazer backup e desativar o
estágio.

Regras de segurança que a Alice segue sempre:

- nada sai da máquina (push, tag, restart, backup, desativação) sem o seu "pode", uma build por vez;
- antes de reiniciar, confere se a imagem nova do fornecedor já traz a versão corrigida;
- antes de desativar uma build com dados, faz o backup e espera a confirmação de que ele terminou;
- nunca dá salto de versão maior em banco de dados sem plano de migração.

## Pré-requisitos

- MCP **Embrapa I/O - Dashboard** conectado ao Claude Code ([como conectar](https://embrapa.io/docs/mcp)).
- Papel de **arquiteto** no projeto do Embrapa I/O.
- Clone da app (`git.embrapa.io/<projeto>/<app>`) e Docker na máquina local.

## Instalação

```bash
claude plugin marketplace add embrapa-io/alice
claude plugin install critical-cves@embrapa-io
```

## Uso

Abra o Claude Code na pasta da app (ou numa pasta com os clones das apps do projeto) e digite:

```
/critical-cves:alice
```

A Alice se apresenta, mostra o menu e espera a sua escolha. Qualquer código vale a qualquer momento da conversa; `MH`
reexibe o menu.

| Código | Descrição |
| --- | --- |
| FC | Fluxo completo: do panorama ao fechamento, build a build |
| LC | Listar as builds com CVE crítico |
| VC | Verificar um CVE no código da versão implantada |
| VI | Verificar se a imagem nova do fornecedor já corrige |
| AT | Atualizar dependência ou imagem (commit e tag de deploy) |
| RU | Reiniciar com atualização de imagens |
| RL | Preparar os comandos para o servidor do Releaser |
| BD | Sem correção: restringir o acesso, ou fazer backup e desativar o estágio |
| CF | Conferir se o alerta fechou e fazer o relato final |
| MH | Reexibir o menu |
| DA | Dispensar a Alice |
