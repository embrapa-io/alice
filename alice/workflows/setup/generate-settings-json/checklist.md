---
last-redoc-date: 2025-12-03
---

# Checklist de Validação - Generate .embrapa/settings.json

## ✅ Estrutura do Arquivo

- [ ] Arquivo criado em `{project-root}/.embrapa/settings.json`
- [ ] Diretório `.embrapa/` criado se não existia
- [ ] JSON válido (sem erros de sintaxe)
- [ ] Encoding UTF-8

## ✅ Campos Obrigatórios

- [ ] Campo `boilerplate` presente (valor: "_")
- [ ] Campo `platform` presente (node, python, php, dotnet, etc.)
- [ ] Campo `label` presente e descritivo
- [ ] Campo `description` presente
- [ ] Campo `references` presente (array)
- [ ] Campo `maintainers` presente (array com pelo menos 1 item)
- [ ] Campo `variables` presente (objeto com default, alpha, beta, release)
- [ ] Campo `orchestrators` presente (array com "DockerCompose")

## ✅ Mantenedores

- [ ] Pelo menos 1 mantenedor configurado
- [ ] Campo `name` preenchido
- [ ] Campo `email` preenchido e válido
- [ ] Campo `phone` presente (pode estar vazio)

## ✅ Variáveis de Ambiente

### Estrutura
- [ ] Objeto `variables` possui: default, alpha, beta, release
- [ ] `default` é array de objetos variável
- [ ] Cada variável possui: name, type
- [ ] Campo `value` opcional dependendo do type

### Tipos Válidos
- [ ] Tipos usados: TEXT, PORT, SECRET, PASSWORD, VOLUME, EMPTY
- [ ] Nenhum tipo inválido presente

### Variáveis Padrão Mínimas
- [ ] ENVIRONMENT (default: test, release: production)
- [ ] PORT ou equivalente
- [ ] BASE_URL ou equivalente
- [ ] SECRET presente

## ✅ Integração com Git

- [ ] Diretório `.embrapa/` NÃO está no .gitignore
- [ ] Arquivo `settings.json` deve ser versionado
- [ ] Não contém dados sensíveis hardcoded

## 🎯 Critérios de Sucesso

1. ✅ Arquivo JSON válido criado
2. ✅ Todos os campos obrigatórios presentes
3. ✅ Pelo menos 1 mantenedor configurado
4. ✅ Variáveis padrão configuradas
5. ✅ Platform correta identificada
6. ✅ Arquivo versionado no git

---

**Checklist Version**: 1.26.4-8
**Módulo**: embrapa-io/setup/generate-settings-json
