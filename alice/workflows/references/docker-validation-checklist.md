# Docker Compose Validation Checklist

Shared reference for verify-compliance and code-review workflows.

## Pre-Computed Validation

If `validate-compliance.py` JSON output is available, use `checks.docker` results directly instead of manual inspection. The script covers all checks below.

```bash
uv run ./scripts/validate-compliance.py --project-path {project-root} --checks docker --output json
```

## 4 Verdades Fundamentais

### VF1: Sem campo 'version'
- docker-compose.yaml NÃO deve ter campo `version` no topo
- Arquivo deve iniciar diretamente com `services:`

### VF2: Network Externa
- DEVE existir seção `networks:` com rede `stack` marcada como `external: true`
- Nome da rede: `${IO_PROJECT}_${IO_APP}_${IO_STAGE}`
- TODOS os serviços (exceto CLI) devem estar na rede `stack`

### VF3: Volumes Externos
- Volumes de dados persistentes DEVEM ser `external: true`
- Nome do volume: `${IO_PROJECT}_${IO_APP}_${IO_STAGE}_{volume_name}`
- Volume de backup: `${IO_PROJECT}_${IO_APP}_${IO_STAGE}_backup`

### VF4: Sem container_name
- NENHUM serviço deve ter `container_name` definido
- Docker Compose gerencia nomes automaticamente

## Serviços de Longa Duração

Para cada serviço não-CLI:
- [ ] `restart: unless-stopped`
- [ ] `env_file:` com `.env` e `.env.io`
- [ ] `networks:` inclui `stack`
- [ ] `healthcheck:` configurado (test, interval, timeout, retries, start_period)
- [ ] Portas usam variáveis (`${APP_PORT}:{internal}`) — sem hardcoding

## Serviços CLI (backup, restore, sanitize)

Para cada serviço CLI:
- [ ] `profiles: ['cli']`
- [ ] `restart: "no"`
- [ ] `networks:` inclui `stack`
- [ ] Backup gera **UM** `.tar.gz` na **RAIZ** de `/backup` (não `.sql` solto, não em subdiretório)
- [ ] Nome EXATO: `${IO_PROJECT}_${IO_APP}_${IO_STAGE}_${IO_VERSION}_$$(date +'%Y-%m-%d_%H-%M-%S').tar.gz` (data como SUFIXO, `$$` para o Compose)
- [ ] Sem extensão dupla (`.sql.tar.gz`, `.dump.tar.gz` são proibidos — o dump fica DENTRO do tar)
- [ ] Diretório temporário removido após compactar (`rm -rf` ou `trap`); só `.tar.gz` na raiz do volume
- [ ] `restore` recebe `BACKUP_FILE_TO_RESTORE` (nome relativo a `/backup`) e valida com `test -f`
- Motivo: o Doctor publica apenas `*.tar.gz` da raiz do volume e o Releaser (`cleaner`) lê a data do nome para a retenção 7 diários / 4 semanais / 3 mensais — sem data no nome, o arquivo fica no volume para sempre

## Resultado

```
### Status: {COMPLIANT | PARTIAL | NON-COMPLIANT}
- VF1 (version): {PASS/FAIL}
- VF2 (network): {PASS/FAIL}
- VF3 (volumes): {PASS/FAIL}
- VF4 (container_name): {PASS/FAIL}
- Serviços longa duração: {PASS/FAIL}
- Serviços CLI: {PASS/FAIL}
- Portas: {PASS/FAIL}
```
