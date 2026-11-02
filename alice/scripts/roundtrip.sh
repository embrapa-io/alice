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
# eval: a sonda traz argumentos entre aspas (o SQL do psql); sem ele, o shell a quebra em palavras
echo "2/6 sonda antes";   eval "dc $ROUNDTRIP_PROBE" > /tmp/roundtrip-before.txt
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

echo "6/6 sonda depois"; eval "dc $ROUNDTRIP_PROBE" > /tmp/roundtrip-after.txt

if diff -u /tmp/roundtrip-before.txt /tmp/roundtrip-after.txt; then
  echo "OK: os dados voltaram iguais ($(wc -l < /tmp/roundtrip-after.txt) linhas da sonda)"
else
  echo "FALHA: o restore não devolveu os mesmos dados (diff acima)"; exit 1
fi
