---
name: Backup Roundtrip
description: Testa, no computador do desenvolvedor, se o serviço restore desfaz exatamente o backup (regra 1.19)
communication_language: "{communication_language}"
document_output_language: "{document_output_language}"
web_bundle: true
---

# Backup Roundtrip Workflow — [BR] Testar Backup e Restore

**Goal:** Provar, executando, que o arquivo gerado pelo serviço `backup` da aplicação é restaurado por inteiro pelo
serviço `restore`: lê os dados, faz o backup, apaga os volumes de dados, restaura e lê de novo; as duas leituras têm de
ser iguais. É a garantia de que os backups podem ir para o Backup S3 da plataforma e servir para migrar dados entre
servidores (a plataforma executa o `restore` com `BACKUP_FILE_TO_RESTORE`).

**Your Role:** além da persona, você é quem executa o teste com cuidado: ele **apaga os volumes de dados da aplicação**
e só pode rodar no ambiente de desenvolvimento do próprio computador.

Referência completa (sondas por pilha, o roteiro e o que fazer quando falha):
`./workflows/references/backup-restore-roundtrip.md` (caminhos relativos à raiz da skill). O roteiro executável é `./scripts/roundtrip.sh`.

---

## Sequência (não pule etapas)

### 1. Conferir o ambiente

- `.env.io` existe e tem `IO_STAGE=development`; senão, **pare** e explique (o teste apaga volumes).
- O `docker-compose.yaml` tem os serviços `backup` e `restore` (perfil `cli`); senão, recomende o **[IA]** e pare.
- Se a rede ou os volumes externos não existem, rode `./bootstrap.sh`.
- Suba a aplicação: `env $(cat .env.io) docker compose up -d --wait`. Se uma porta do `.env` estiver ocupada por outro
  projeto, troque-a só no `.env` local (não versionado) e diga ao usuário qual trocou.

### 2. Escolher a sonda

- A sonda é um comando que imprime um retrato determinístico dos dados (contagens por tabela, títulos ordenados,
  _hashes_ dos arquivos). Escolha pela pilha, na tabela da referência, e adapte aos nomes reais do `docker-compose.yaml`
  e do `.env` (serviço do banco, usuário, banco). Apps com banco e arquivos combinam duas sondas.
- Rode a sonda. Se ela não imprimir nada (base vazia), grave **dados de exemplo pela própria aplicação** (API, _seed_ ou
  migração com dados), poucos e fictícios, e diga quais.

### 3. Rodar o teste

- Copie `./scripts/roundtrip.sh` (deste módulo) para a raiz da aplicação, se ainda não estiver lá.
- Execute: `ROUNDTRIP_PROBE='<sonda>' ./roundtrip.sh --yes`.

### 4. Relatar

- **OK** («os dados voltaram iguais»): diga quantas linhas a sonda comparou e o nome do arquivo de backup gerado.
- **FALHA**: mostre o _diff_, diga o que o `restore` deixou de trazer (um banco, um volume, um diretório) e proponha a
  correção no `restore` (ou rode o **[IA]**). Nunca «corrija» o teste para passar.
- Lembre que o `roundtrip.sh` pode ficar no repositório (só roda em `development`) e que vale repetir o teste sempre
  que o modelo de dados ou os volumes mudarem.

---

## HEADLESS MODE

Se `{headless_mode}=true`: execute as etapas sem perguntas (dados de exemplo mínimos quando a base estiver vazia) e
termine com `{"workflow": "backup-roundtrip", "result": "OK" | "FALHA", "probe_lines": N, "backup_file": "…"}`.
