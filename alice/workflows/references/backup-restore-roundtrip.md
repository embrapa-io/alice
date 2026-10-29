# Teste de ida e volta: backup → apagar → restore → comparar

A regra 1.19 confere, por leitura do `docker-compose.yaml`, se o serviço `restore` desfaz o `backup`. A garantia de
verdade é executar o ciclo e comparar os dados: é o que este roteiro descreve. Ele importa porque a plataforma
**executa o `restore`** (Backup S3 dos clusters compartilhados, restore pelo *Health Check*, com
`BACKUP_FILE_TO_RESTORE`): um restore incompleto traz a aplicação de volta sem um banco, um volume ou um diretório, e
ninguém percebe até precisar dos dados.

## A sonda

Comparar os arquivos dos volumes não funciona para bancos: depois de `pg_dump` e `psql`, os arquivos internos mudam
mesmo com os mesmos dados. Por isso o teste usa uma **sonda**: um comando que imprime um retrato determinístico dos
dados da app, rodado antes do backup e depois do restore. As duas saídas têm de ser iguais.

Boas sondas, por pilha:

| Pilha | Sonda (`ROUNDTRIP_PROBE`) |
| --- | --- |
| PostgreSQL | `exec -T db psql -U "$DB_USER" -d "$DB_NAME" -At -c "SELECT table_name, (xpath('/row/c/text()', query_to_xml('SELECT count(*) AS c FROM '||table_name, false, true, '')))[1]::text FROM information_schema.tables WHERE table_schema='public' ORDER BY 1"` |
| MySQL/MariaDB | `exec -T db mysql -u"$DB_USER" -p"$DB_PASSWORD" -N -e "CHECKSUM TABLE $(tabelas)" "$DB_NAME"` |
| MongoDB | `exec -T db mongosh --quiet "$MONGO_URL" --eval 'db.getCollectionNames().sort().forEach(c => print(c, db[c].countDocuments()))'` |
| PocketBase/SQLite | `exec -T pocketbase sh -c 'sqlite3 /pb_data/data.db "SELECT name FROM sqlite_master WHERE type=\"table\" ORDER BY 1" \| while read t; do echo "$t $(sqlite3 /pb_data/data.db "SELECT count(*) FROM \"$t\"")"; done'` |
| Arquivos (uploads, plugins) | `exec -T app sh -c 'cd /app/uploads && find . -type f -exec sha256sum {} + \| sort'` |

Apps com banco **e** arquivos combinam duas sondas (`sonda1; sonda2`). Antes do backup, o teste grava dados
conhecidos pela própria app (seed, migração com dados de exemplo ou um cadastro feito à mão), para a sonda não comparar
duas bases vazias.

## O roteiro (`roundtrip.sh`)

Roda **só em desenvolvimento** e **apaga os volumes de dados da app** no meio do caminho: por isso exige `--yes` e
recusa rodar se o `.env.io` não for de `development`. Copie para a raiz da app, ajuste `ROUNDTRIP_PROBE` e rode com
`./roundtrip.sh --yes`.

```bash
#!/usr/bin/env bash
# Teste de ida e volta do backup/restore da app (Alice, regra 1.19). Só em desenvolvimento: APAGA os volumes de dados.
#   ROUNDTRIP_PROBE='exec -T db psql ...' ./roundtrip.sh --yes
set -euo pipefail

[ "${1:-}" = "--yes" ] || { echo "Uso: ROUNDTRIP_PROBE='...' $0 --yes (apaga os volumes de dados da app)"; exit 1; }
[ -n "${ROUNDTRIP_PROBE:-}" ] || { echo "Defina ROUNDTRIP_PROBE (veja a tabela de sondas)"; exit 1; }
grep -q '^IO_STAGE=development$' .env.io || { echo "Recusado: o .env.io não é de development"; exit 1; }

dc () { env $(cat .env.io) docker compose "$@"; }
cli () { env $(cat .env.io) COMPOSE_PROFILES=cli docker compose "$@"; }

PREFIX=$(grep '^COMPOSE_PROJECT_NAME=' .env.io | cut -d= -f2)
BACKUP_VOLUME="${PREFIX}_backup"
# Volumes de dados = externos da app, exceto o de backup
DATA_VOLUMES=$(dc config --format json | python3 -c 'import json,sys; v=json.load(sys.stdin).get("volumes",{}); print(" ".join(x.get("name",k) for k,x in v.items() if x.get("external") and not x.get("name",k).endswith("_backup")))')

echo "1/6 subindo a app"; dc up -d --wait
echo "2/6 sonda antes";   dc $ROUNDTRIP_PROBE > /tmp/roundtrip-before.txt
[ -s /tmp/roundtrip-before.txt ] || { echo "A sonda não imprimiu nada: grave dados de exemplo antes"; exit 1; }

echo "3/6 backup"; cli run --rm --no-deps backup
FILE=$(docker run --rm -v "$BACKUP_VOLUME":/backup:ro alpine sh -c 'ls -t /backup/*.tar.gz | head -1 | xargs basename')
echo "    arquivo: $FILE"

echo "4/6 apagando os volumes de dados: $DATA_VOLUMES"
dc down
for v in $DATA_VOLUMES; do docker volume rm "$v" > /dev/null && docker volume create "$v" > /dev/null; done
dc up -d --wait

echo "5/6 restore"; cli run --rm --no-deps -e BACKUP_FILE_TO_RESTORE="$FILE" restore
dc restart && dc up -d --wait

echo "6/6 sonda depois"; dc $ROUNDTRIP_PROBE > /tmp/roundtrip-after.txt

if diff -u /tmp/roundtrip-before.txt /tmp/roundtrip-after.txt; then
  echo "OK: os dados voltaram iguais ($(wc -l < /tmp/roundtrip-after.txt) linhas da sonda)"
else
  echo "FALHA: o restore não devolveu os mesmos dados (diff acima)"; exit 1
fi
```

## Quando usar

- **Workflow `implement-compliance`:** depois de criar ou corrigir `backup`/`restore`, propor a sonda da app e rodar o
  roteiro; anotar o resultado no relatório.
- **Boilerplates:** cada boilerplate com dados guarda o `roundtrip.sh` e a sonda (ex.: no `README.md`, seção de
  backup) e roda o teste a cada mudança no `backup`/`restore`. Correção de restore incompleto é correção de bug: vai
  aos forks pelo fluxo de propagação.
- **Migração para a plataforma:** a estrutura do `.tar.gz` que o `restore` espera é a que o `backup` gera; o roteiro
  mostra essa estrutura na prática (`tar -tzf` no arquivo do passo 3). Documente-a no `README.md` da app: quem migra dados de fora monta
  o arquivo nesse formato, envia à pasta `<projeto>/<app>/upload/` do bucket do Backup S3 e o restaura pelo Health
  Check (https://embrapa.io/docs/s3#clusters-upload).
