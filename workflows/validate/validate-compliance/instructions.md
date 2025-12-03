# Validate Compliance - Instruções de Validação Completa

<critical>The workflow execution engine is governed by: {project-root}/.bmad/core/tasks/workflow.xml</critical>
<critical>You MUST have already loaded and processed: {project-root}/.bmad/embrapa-io/workflows/validate/validate-compliance/workflow.yaml</critical>
<critical>This is an INTERACTIVE workflow - requires user input and generates reports</critical>
<critical>Communicate in {communication_language} throughout execution</critical>
<critical>Read knowledge files before starting validation</critical>

<workflow>

<step n="1" goal="Carregar conhecimento necessário">
<action>Carregar e compreender os seguintes arquivos de conhecimento:</action>
<action>- {project-root}/.bmad/embrapa-io/knowledge/embrapa-io-fundamentals.md → As 4 verdades fundamentais da plataforma</action>
<action>- {project-root}/.bmad/embrapa-io/knowledge/embrapa-io-validation.md → Todas as 47 regras de validação organizadas (incluindo NO-FALLBACK, Volumes via .env, Portas via .env, e Linter)</action>
<action>- {project-root}/.bmad/embrapa-io/knowledge/embrapa-io-workflows.md → Adaptação por tipo de projeto</action>

<check if="arquivos carregados com sucesso">
<action>Informar {user_name}: Conhecimento da plataforma Embrapa I/O carregado</action>
<action>Listar quantas regras de validação foram identificadas</action>
</check>

<check if="erro ao carregar conhecimento">
<action>Reportar erro em {communication_language}</action>
<action>Encerrar workflow pois validação não pode ser executada sem conhecimento</action>
</check>

<action>Store validation rules count as internal variable</action>
</step>

<step n="2" goal="Coletar parâmetros de validação">
<ask>Qual o caminho absoluto do projeto a ser validado?</ask>
<action>Armazenar como {{project_path}}</action>
<action>Validar que o diretório existe e é acessível</action>

<check if="diretório não existe ou não é acessível">
<action>Solicitar novo caminho explicando o problema</action>
<action>Repetir até receber caminho válido</action>
</check>

<ask>Quais níveis de severidade validar? Digite: CRITICAL, HIGH, MEDIUM, LOW ou ALL para todos</ask>
<action>Armazenar como {{severity_levels}} (array)</action>
<action>Se "ALL", expandir para: ["CRITICAL", "HIGH", "MEDIUM", "LOW"]</action>

<ask>Aplicar correções automáticas quando possível? Digite: y para sim, n para não</ask>
<action>Armazenar como {{auto_fix}} (boolean)</action>

<action>Extrair nome do projeto do caminho (último segmento)</action>
<action>Armazenar como {{project_name}}</action>

<action>Informar {user_name} os parâmetros coletados:</action>
<action>- Projeto: {{project_name}}</action>
<action>- Caminho: {{project_path}}</action>
<action>- Severidades: {{severity_levels}}</action>
<action>- Auto-fix: {{auto_fix}}</action>

<action>Store project_path as internal variable</action>
<action>Store project_name as internal variable</action>
<action>Store severity_levels as internal variable</action>
<action>Store auto_fix as internal variable</action>
</step>

<step n="3" goal="Detectar tipo de projeto">
<action>Verificar existência dos arquivos no {{project_path}}:</action>
<action>- docker-compose.yaml → armazenar resultado em {{hasDockerCompose}}</action>
<action>- .embrapa/settings.json → armazenar resultado em {{hasSettings}}</action>
<action>- .env.io.example → armazenar resultado em {{hasEnvIo}}</action>

<action>Determinar tipo do projeto baseado nos arquivos encontrados</action>

<check if="hasSettings AND hasEnvIo">
<action>{{project_type}} = "ALREADY_COMPLIANT" (projeto já possui arquivos Embrapa I/O)</action>
</check>

<check if="hasDockerCompose AND NOT (hasSettings AND hasEnvIo)">
<action>{{project_type}} = "EXISTING" (projeto existente, precisa adaptação)</action>
</check>

<check if="NOT hasDockerCompose">
<action>{{project_type}} = "NEW" (projeto novo, sem Docker Compose)</action>
</check>

<check if="project_type == NEW">
<action>Informar {user_name} em {communication_language}:</action>
<action>⚠️ Projeto novo detectado - validação de conformidade não aplicável</action>
<action>💡 Sugestão: Use workflows create-* apropriados para iniciar projeto Embrapa I/O</action>
<action>Encerrar workflow</action>
</check>

<action>Informar {user_name}: Tipo de projeto detectado: {{project_type}}</action>
<action>Listar arquivos relevantes encontrados no projeto</action>

<action>Store project_type as internal variable</action>
<action>Store hasDockerCompose as internal variable</action>
<action>Store hasSettings as internal variable</action>
<action>Store hasEnvIo as internal variable</action>
</step>

<step n="4" goal="Validar docker-compose.yaml">
<action>Ler arquivo {{project_path}}/docker-compose.yaml completo</action>
<action>Executar 14 validações conforme embrapa-io-validation.md seção "Validação 1 - Docker Compose"</action>

<action>Validações CRITICAL (IDs 1.1-1.5):</action>
<action>- 1.1: Arquivo docker-compose.yaml existe no diretório raiz</action>
<action>- 1.2: Campo 'version' está ausente (Compose v2+ não usa mais)</action>
<action>- 1.3: Network 'stack' está definida na seção networks</action>
<action>- 1.4: Network 'stack' possui 'external: true'</action>
<action>- 1.5: Nome da network segue padrão: ${IO_PROJECT}_${IO_APP}_stack</action>

<action>Validações HIGH (IDs 1.6-1.10):</action>
<action>- 1.6: Todos os serviços estão conectados à network 'stack'</action>
<action>- 1.7: Nenhum serviço possui 'container_name' definido</action>
<action>- 1.8: Todos os volumes possuem 'external: true'</action>
<action>- 1.9: Todos os serviços possuem 'restart: unless-stopped'</action>
<action>- 1.10: Todos os serviços possuem 'healthcheck' configurado</action>

<action>Validações MEDIUM (IDs 1.11-1.14):</action>
<action>- 1.11: Portas são definidas via variáveis de ambiente (${PORT:-3000})</action>
<action>- 1.12: Serviços CLI possuem profiles corretos (cli, development)</action>
<action>- 1.13: Volume de backup existe e está configurado</action>
<action>- 1.14: Volumes de serviços (exceto backup) usam variáveis do .env (formato: name: ${SERVICE_VOLUME})</action>

<action>Validações LOW (IDs 1.15-1.17):</action>
<action>- 1.15: Serviços CLI estão presentes (backup, restore, sanitize)</action>
<action>- 1.16: Volume de backup tem nome hardcoded: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}_backup (não usa variável do .env)</action>
<action>- 1.17: 🚨 CRÍTICO - Portas do host (lado esquerdo) JAMAIS hardcoded, sempre via variável (formato: "${PORT_VAR}:container_port")</action>

<action>Para cada erro encontrado, criar objeto estruturado:</action>

**Estrutura de erro**:
```json
{
  "id": "1.6",
  "severity": "HIGH",
  "category": "docker-compose",
  "message": "Serviço 'api' não está conectado à network 'stack'",
  "location": "docker-compose.yaml:15",
  "solution": "Adicionar 'stack' na seção 'networks:' do serviço",
  "auto_fixable": true
}
```

<action>Armazenar todos os erros encontrados em {{docker_compose_errors}} (array)</action>
<action>Calcular status da categoria:</action>
<action>- "compliant": 0 erros</action>
<action>- "partial": apenas erros MEDIUM/LOW</action>
<action>- "non-compliant": erros CRITICAL ou HIGH presentes</action>

<action>Store docker_compose_errors as internal variable</action>
<action>Store docker_compose_status as internal variable</action>
</step>

<step n="5" goal="Validar arquivos .env e variáveis de volume">
<action>Executar validações conforme embrapa-io-validation.md seção "Validação 2 - Arquivos .env"</action>

<action>Validações CRITICAL (IDs 2.1-2.3):</action>
<action>- 2.1: Arquivo .env.io.example existe no diretório raiz</action>
<action>- 2.2: Arquivo .env.example existe no diretório raiz</action>
<action>- 2.3: Não há duplicação de variáveis entre .env.io e .env</action>

<action>Validações HIGH (IDs 2.4-2.7):</action>
<action>- 2.4: Variáveis obrigatórias presentes (IO_PROJECT, IO_APP, IO_STAGE, IO_VERSION, IO_DEPLOYER)</action>
<action>- 2.5: Valores sem espaços ou aspas desnecessárias</action>
<action>- 2.6: Variáveis seguem convenção UPPER_SNAKE_CASE</action>
<action>- 2.7: Variáveis de volume presentes no .env para todos os volumes (exceto backup) declarados no docker-compose.yaml</action>

<action>Validações MEDIUM (IDs 2.8-2.10):</action>
<action>- 2.8: .gitignore ignora arquivos .env mas não .env.*.example</action>
<action>- 2.9: Variáveis sensíveis possuem comentários de documentação</action>
<action>- 2.10: Variáveis de volume seguem padrão: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}_[a-z0-9]+</action>

<action>Armazenar todos os erros em {{env_files_errors}} (array)</action>
<action>Calcular status da categoria (compliant/partial/non-compliant)</action>

<action>Store env_files_errors as internal variable</action>
<action>Store env_files_status as internal variable</action>
</step>

<step n="6" goal="Validar .embrapa/settings.json">
<action>Ler arquivo {{project_path}}/.embrapa/settings.json completo</action>
<action>Executar 8 validações conforme embrapa-io-validation.md seção "Validação 3 - Settings JSON"</action>

<action>Validações CRITICAL (IDs 3.1-3.3):</action>
<action>- 3.1: Arquivo .embrapa/settings.json existe</action>
<action>- 3.2: Conteúdo é JSON válido (parse sem erros)</action>
<action>- 3.3: Campos obrigatórios presentes: boilerplate, platform, label, description, references, maintainers, variables, orchestrators</action>

<action>Validações HIGH (IDs 3.4-3.6):</action>
<action>- 3.4: Campo 'platform' possui valor válido (nodejs|python|php|java|golang|ruby|dotnet)</action>
<action>- 3.5: Campo 'variables.default' está presente e não-vazio</action>
<action>- 3.6: Tipos de variáveis são válidos (TEXT, PASSWORD, SECRET, PORT, VOLUME, EMPTY)</action>

<action>Validações MEDIUM (IDs 3.7-3.8):</action>
<action>- 3.7: Valores default sem espaços ou aspas desnecessárias</action>
<action>- 3.8: Array 'references' não está vazio (possui documentação)</action>

<action>Armazenar erros em {{settings_errors}} (array)</action>
<action>Calcular status da categoria</action>

<action>Store settings_errors as internal variable</action>
<action>Store settings_status as internal variable</action>
</step>

<step n="7" goal="Validar integrações">
<action>Executar 5 validações conforme embrapa-io-validation.md seção "Validação 4 - Integrações"</action>

<action>Validações HIGH (IDs 4.1-4.2):</action>
<action>- 4.1: Sentry configurado (SENTRY_DSN em .env + código de inicialização presente)</action>
<action>- 4.2: Matomo tracking implementado (MATOMO_ID presente + código de tracking)</action>

<action>Validações MEDIUM (IDs 4.3-4.4):</action>
<action>- 4.3: Logo Embrapa presente em assets/public do projeto</action>
<action>- 4.4: SonarQube configurado se projeto backend (sonar-project.properties ou config)</action>

<action>Validações LOW (ID 4.5):</action>
<action>- 4.5: Grafana Loki configurado (opcional mas recomendado para logs)</action>

<action>Armazenar erros em {{integrations_errors}} (array)</action>
<action>Calcular status da categoria</action>

<action>Store integrations_errors as internal variable</action>
<action>Store integrations_status as internal variable</action>
</step>

<step n="7.5" goal="Validar NO-FALLBACK no codebase (REGRA CRÍTICA)">
<action>🚨 Esta é uma validação CRÍTICA da plataforma Embrapa I/O</action>

<action>Escanear arquivos de código do projeto em busca de padrões de fallback proibidos:</action>

**Validações CRITICAL (IDs 5.1-5.4):**

<action>ID 5.1: Buscar padrões JavaScript/TypeScript de fallback:</action>
<action>- Buscar regex: `process\.env\.\w+\s*\|\|`</action>
<action>- Buscar regex: `process\.env\.\w+\s*\?\?`</action>
<action>- Padrão proibido: `process.env.PORT || 3000`</action>
<action>- Arquivos: *.js, *.ts, *.jsx, *.tsx</action>

<action>ID 5.2: Buscar padrões Python de fallback:</action>
<action>- Buscar regex: `os\.environ\.get\(['"]\w+['"],\s*.+\)`</action>
<action>- Buscar regex: `os\.getenv\(['"]\w+['"],\s*.+\)`</action>
<action>- Padrão proibido: `os.environ.get('PORT', 3000)`</action>
<action>- Arquivos: *.py</action>

<action>ID 5.3: Buscar padrões Shell/Bash de fallback:</action>
<action>- Buscar regex: `\$\{\w+:-[^}]+\}`</action>
<action>- Padrão proibido: `${PORT:-3000}`</action>
<action>- Arquivos: *.sh, *.bash, Dockerfile, docker-compose.yaml</action>

<action>ID 5.4: Buscar padrões Docker Compose de fallback:</action>
<action>- Buscar no docker-compose.yaml: padrão `${VAR:-default}`</action>
<action>- Padrão proibido em environment ou ports</action>
<action>- Arquivo: docker-compose.yaml</action>

**Ações para cada ocorrência encontrada:**
<action>Criar erro estruturado com:</action>
```json
{
  "id": "5.X",
  "severity": "CRITICAL",
  "category": "no-fallback",
  "message": "Fallback detectado em variável de ambiente: {VAR_NAME}",
  "location": "{file_path}:{line_number}",
  "pattern_found": "{código encontrado}",
  "solution": "Remover fallback. Use apenas: {correção sugerida}",
  "auto_fixable": false,
  "explanation": "Plataforma Embrapa I/O sempre injeta variáveis. Fallback mascara erros de configuração."
}
```

<action>Informar {user_name} em {communication_language}:</action>
<action>Se nenhum fallback encontrado: ✅ Código conforme - sem fallbacks detectados</action>
<action>Se fallbacks encontrados: 🚨 CRÍTICO - {count} fallbacks proibidos detectados</action>

<action>Armazenar erros em {{no_fallback_errors}} (array)</action>
<action>Calcular status da categoria</action>

<action>Store no_fallback_errors as internal variable</action>
<action>Store no_fallback_status as internal variable</action>
</step>

<step n="7.6" goal="Validar presença de Linter configurado (REGRA DE QUALIDADE)">
<action>🔍 Esta é uma validação de QUALIDADE da plataforma Embrapa I/O</action>

<action>Detectar linguagem/framework do projeto:</action>
<action>- Procurar package.json → JavaScript/TypeScript</action>
<action>- Procurar composer.json → PHP</action>
<action>- Procurar requirements.txt/pyproject.toml → Python</action>
<action>- Procurar go.mod → Go</action>
<action>- Procurar Gemfile → Ruby</action>
<action>- Procurar pom.xml/build.gradle → Java</action>
<action>- Procurar *.csproj → .NET</action>
<action>- Procurar Cargo.toml → Rust</action>

<action>Armazenar linguagem detectada como {{detected_language}}</action>

**Validações MEDIUM (IDs 6.1-6.2):**

<action>ID 6.1: Verificar se Linter está instalado (dependências):</action>

<check if="detected_language == JavaScript/TypeScript">
<action>Verificar se package.json possui eslint nas devDependencies ou dependencies</action>
<action>Se não encontrado, criar erro:</action>
```json
{
  "id": "6.1",
  "severity": "MEDIUM",
  "category": "linter",
  "message": "ESLint não configurado. JavaScript/TypeScript requer Linter.",
  "location": "package.json",
  "solution": "npm install --save-dev eslint eslint-config-standard",
  "auto_fixable": false,
  "explanation": "Plataforma Embrapa I/O exige Linter para qualidade de código."
}
```
</check>

<check if="detected_language == PHP">
<action>Verificar se composer.json possui squizlabs/php_codesniffer ou phpstan</action>
<action>Se não encontrado, criar erro com sugestão: composer require --dev squizlabs/php_codesniffer</action>
</check>

<check if="detected_language == Python">
<action>Verificar se requirements.txt ou pyproject.toml possui ruff, flake8, pylint ou black</action>
<action>Se não encontrado, criar erro com sugestão: pip install ruff</action>
</check>

<check if="detected_language == Go">
<action>Verificar se existe .golangci.yml ou Makefile com golangci-lint</action>
<action>Se não encontrado, criar WARNING (Go possui gofmt built-in mas golangci-lint recomendado)</action>
</check>

<check if="detected_language == Ruby">
<action>Verificar se Gemfile possui rubocop</action>
<action>Se não encontrado, criar erro com sugestão: gem install rubocop</action>
</check>

<check if="detected_language == Java">
<action>Verificar se pom.xml possui checkstyle ou spotbugs plugin</action>
<action>Se não encontrado, criar erro</action>
</check>

<check if="detected_language == .NET">
<action>Verificar se *.csproj possui StyleCop.Analyzers ou possui .editorconfig</action>
<action>Se não encontrado, criar erro</action>
</check>

<check if="detected_language == Rust">
<action>Rust possui Clippy built-in - marcar como conforme automaticamente</action>
</check>

<action>ID 6.2: Verificar se comandos lint e lint:fix estão definidos:</action>

<check if="detected_language == JavaScript/TypeScript">
<action>Verificar se package.json possui scripts "lint" e "lint:fix" (ou "fix")</action>
<action>Se não encontrado, criar erro:</action>
```json
{
  "id": "6.2",
  "severity": "LOW",
  "category": "linter",
  "message": "Scripts lint/lint:fix não definidos em package.json",
  "location": "package.json:scripts",
  "solution": "Adicionar: \"lint\": \"eslint .\", \"lint:fix\": \"eslint . --fix\"",
  "auto_fixable": false
}
```
</check>

<check if="detected_language == PHP">
<action>Verificar se composer.json possui scripts "lint" e "lint:fix"</action>
<action>Se não encontrado, criar erro com sugestão de scripts phpcs/phpcbf</action>
</check>

<check if="detected_language == Python">
<action>Verificar se pyproject.toml possui [tool.scripts] ou se existe Makefile com target lint</action>
<action>Se não encontrado, criar WARNING</action>
</check>

<action>Informar {user_name} em {communication_language}:</action>
<action>Se Linter encontrado: ✅ Linter configurado - {{linter_name}}</action>
<action>Se Linter não encontrado: ⚠️ WARNING - Linter não configurado para {{detected_language}}</action>

<action>Armazenar erros em {{linter_errors}} (array)</action>
<action>Calcular status da categoria</action>

<action>Store linter_errors as internal variable</action>
<action>Store linter_status as internal variable</action>
</step>

<step n="8" goal="Calcular compliance score">
<action>Consolidar todos os erros encontrados:</action>
<action>{{all_errors}} = docker_compose_errors + env_files_errors + settings_errors + integrations_errors + no_fallback_errors + linter_errors</action>

<action>Contar erros por severidade:</action>
<action>- {{critical_count}}: count onde severity == "CRITICAL"</action>
<action>- {{high_count}}: count onde severity == "HIGH"</action>
<action>- {{medium_count}}: count onde severity == "MEDIUM"</action>
<action>- {{low_count}}: count onde severity == "LOW"</action>
<action>- {{total_errors}}: soma de todos os erros</action>

<action>Calcular {{compliance_score}} baseado nas severidades:</action>

<check if="critical_count > 0 OR high_count > 3">
<action>{{compliance_score}} = "LOW" 🔴 (projeto não-conforme)</action>
</check>

<check if="high_count > 0 AND high_count <= 3 AND critical_count == 0">
<action>{{compliance_score}} = "MEDIUM" 🟡 (conformidade parcial)</action>
</check>

<check if="high_count == 0 AND critical_count == 0">
<action>{{compliance_score}} = "HIGH" 🟢 (alta conformidade)</action>
</check>

<action>Informar {user_name}: Score de conformidade calculado: {{compliance_score}}</action>
<action>Informar resumo: {{total_errors}} erros (C:{{critical_count}}, H:{{high_count}}, M:{{medium_count}}, L:{{low_count}})</action>

<action>Store all_errors as internal variable</action>
<action>Store critical_count as internal variable</action>
<action>Store high_count as internal variable</action>
<action>Store medium_count as internal variable</action>
<action>Store low_count as internal variable</action>
<action>Store total_errors as internal variable</action>
<action>Store compliance_score as internal variable</action>
</step>

<step n="9" goal="Gerar relatório JSON">
<action>Criar estrutura completa do relatório JSON:</action>

**Estrutura do relatório**:
```json
{
  "project": {
    "name": "{{project_name}}",
    "path": "{{project_path}}",
    "type": "{{project_type}}"
  },
  "validation": {
    "timestamp": "{{date}}",
    "score": "{{compliance_score}}",
    "summary": {
      "critical": {{critical_count}},
      "high": {{high_count}},
      "medium": {{medium_count}},
      "low": {{low_count}},
      "total": {{total_errors}}
    }
  },
  "results": {
    "docker_compose": {
      "status": "{{docker_compose_status}}",
      "errors": [...]
    },
    "env_files": {
      "status": "{{env_files_status}}",
      "errors": [...]
    },
    "settings_json": {
      "status": "{{settings_status}}",
      "errors": [...]
    },
    "integrations": {
      "status": "{{integrations_status}}",
      "errors": [...]
    },
    "no_fallback": {
      "status": "{{no_fallback_status}}",
      "errors": [...]
    },
    "linter": {
      "status": "{{linter_status}}",
      "errors": [...]
    }
  },
  "all_errors": [...]
}
```

<action>Salvar JSON completo em {validation_report_json}</action>
<action>Informar {user_name}: Relatório JSON salvo em {{validation_report_json}}</action>

<action>Store report_json_path as internal variable</action>
</step>

<step n="10" goal="Gerar relatório Markdown">
<action>Criar relatório humanizado em Markdown seguindo template padrão</action>

<action>Incluir seções obrigatórias:</action>
<action>1. Cabeçalho: projeto, data, score com emoji (🟢 HIGH / 🟡 MEDIUM / 🔴 LOW)</action>
<action>2. Resumo executivo: contagem de validações e estatísticas</action>
<action>3. Detalhamento por categoria: status, lista de erros com ID, severidade, mensagem, solução</action>
<action>4. Próximos passos: ações priorizadas (CRITICAL → HIGH → MEDIUM → LOW)</action>
<action>5. Referências: links para conhecimento e workflows relacionados</action>

<action>Salvar Markdown completo em {validation_report_md}</action>
<action>Informar {user_name}: Relatório Markdown salvo em {{validation_report_md}}</action>

<action>Store report_md_path as internal variable</action>
</step>

<step n="11" goal="Apresentar sugestões de correção">
<action>Para cada erro em {{all_errors}}, apresentar em {communication_language}:</action>
<action>- ID e severidade do erro</action>
<action>- Descrição clara do problema encontrado</action>
<action>- Solução específica com exemplo de código quando aplicável</action>
<action>- Indicação se é auto_fixable (correção automática possível)</action>
<action>- Referência a workflow BMAD relacionado se aplicável</action>

<action>Agrupar sugestões por prioridade:</action>
<action>1. CRITICAL: ação imediata obrigatória</action>
<action>2. HIGH: alta prioridade, corrigir antes de deploy</action>
<action>3. MEDIUM: média prioridade, melhorias importantes</action>
<action>4. LOW: baixa prioridade, sugestões opcionais</action>

<action>Apresentar lista priorizada completa para {user_name}</action>
</step>

<step n="12" goal="Aplicar correções automáticas" if="auto_fix == true AND existem erros auto_fixable">
<action>Filtrar {{all_errors}} para obter apenas erros com auto_fixable == true</action>
<action>Armazenar em {{fixable_errors}}</action>

<check if="fixable_errors está vazio">
<action>Informar {user_name}: Nenhum erro possui correção automática disponível</action>
<action>Pular para Step 13</action>
</check>

<action>Para cada erro em {{fixable_errors}}:</action>
<action>1. Criar backup do arquivo original: {{arquivo}}.bak</action>
<action>2. Aplicar correção específica baseada no tipo de erro</action>
<action>3. Validar sintaxe do arquivo modificado (YAML/JSON parse)</action>
<action>4. Registrar ação no log de mudanças</action>

<action>Correções automáticas implementadas:</action>
<action>- Remover campo 'version' do docker-compose.yaml</action>
<action>- Adicionar 'external: true' a networks e volumes</action>
<action>- Criar .env.example ausente com estrutura base</action>
<action>- Adicionar entradas ao .gitignore (.env, .env.io)</action>
<action>- Criar .embrapa/settings.json com estrutura mínima se ausente</action>

<action>Informar {user_name}: {{count}} correções automáticas aplicadas com sucesso</action>
<action>Listar arquivos modificados e respectivos backups criados</action>

<ask>Deseja re-executar validação para verificar as correções aplicadas? (y/n)</ask>

<check if="resposta == y">
<action>Informar: Reiniciando validação desde o Step 3 (detecção de tipo)</action>
<action>Retornar para Step 3</action>
</check>

<check if="resposta == n">
<action>Continuar para apresentação de resultados finais</action>
</check>
</step>

<step n="13" goal="Finalizar e apresentar resultados">
<action>Apresentar resumo final para {user_name} em {communication_language}:</action>

**🎯 Validação de Conformidade Embrapa I/O - Resultado Final**

📂 **Projeto**: {{project_name}}
📍 **Caminho**: {{project_path}}
🏷️ **Tipo**: {{project_type}}
📊 **Score**: {{compliance_score_emoji}} {{compliance_score}}

📈 **Resumo de Validações**:
- ❌ Erros CRITICAL: {{critical_count}}
- ⚠️ Erros HIGH: {{high_count}}
- ⚡ Avisos MEDIUM: {{medium_count}}
- ℹ️ Sugestões LOW: {{low_count}}
- 📋 Total: {{total_errors}} problemas identificados

📝 **Relatórios gerados**:
- JSON: {{validation_report_json}}
- Markdown: {{validation_report_md}}

<check if="auto_fix == true">
<action>🔧 **Correções automáticas**: {{fixes_applied}} correções aplicadas</action>
</check>

💡 **Próximos passos recomendados**:

<check if="critical_count > 0">
<action>1. 🚨 URGENTE: Corrigir {{critical_count}} erros CRITICAL imediatamente</action>
</check>

<check if="high_count > 0">
<action>2. ⚠️ ALTA PRIORIDADE: Corrigir {{high_count}} erros HIGH antes de deploy</action>
</check>

<check if="medium_count > 0">
<action>3. ⚡ MÉDIA PRIORIDADE: Implementar {{medium_count}} melhorias MEDIUM</action>
</check>

<check if="low_count > 0">
<action>4. ℹ️ BAIXA PRIORIDADE: Considerar {{low_count}} sugestões LOW</action>
</check>

<check if="total_errors == 0">
<action>✅ **PARABÉNS!** Projeto 100% conforme com Embrapa I/O!</action>
</check>

<action>Perguntar se {user_name} deseja mais detalhes sobre alguma categoria específica</action>
</step>

</workflow>

## 📋 Notas Importantes

**Princípios de Execução**:
- **SEMPRE** ler arquivos completos antes de validar (não assumir estruturas)
- **SEMPRE** seguir as 38 regras de validação documentadas em embrapa-io-validation.md
- **SEMPRE** gerar relatórios nos dois formatos (JSON para automação + Markdown para humanos)
- **SEMPRE** indicar próximos passos priorizados por severidade
- **SEMPRE** criar backups antes de aplicar correções automáticas

**Restrições**:
- **NUNCA** inventar regras de validação não documentadas
- **NUNCA** aplicar auto-fix sem criar arquivo .bak
- **NUNCA** modificar arquivos sem validar sintaxe após correção
- **NUNCA** prosseguir validação se conhecimento não foi carregado

**Correções Automáticas Suportadas**:
1. Remover campo 'version' do docker-compose.yaml (ID 1.2)
2. Adicionar 'external: true' a networks (ID 1.4)
3. Adicionar 'external: true' a volumes (ID 1.8)
4. Criar .env.example com estrutura base (ID 2.2)
5. Atualizar .gitignore com .env e .env.io (ID 2.7)
6. Criar .embrapa/settings.json mínimo (ID 3.1)

## 🔧 Uso por Agentes

Este workflow deve ser invocado para validar conformidade de projetos:

```xml
<step n="X" goal="Validar conformidade Embrapa I/O">
  <invoke-workflow>
    <path>{project-root}/.bmad/embrapa-io/workflows/validate/validate-compliance/workflow.yaml</path>
    <description>Valida projeto contra 38 regras Embrapa I/O e gera relatórios (workflow interativo)</description>
  </invoke-workflow>
</step>
```

**Características**:
- Workflow interativo (requer parâmetros do usuário)
- Validação baseada em 38 regras documentadas
- Gera relatórios JSON e Markdown
- Suporta correções automáticas com backup
- Pode re-executar após correções
- Score: LOW/MEDIUM/HIGH baseado em severidades

---

**Versão**: 3.0.0 (BMAD Core v6 compliant)
**Atualizado**: 2025-10-21
**Autor**: Módulo Embrapa I/O BMAD
