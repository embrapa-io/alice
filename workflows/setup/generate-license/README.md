---
last-redoc-date: 2025-12-03
---

# Generate LICENSE Workflow

Workflow autônomo que gera o arquivo `LICENSE` padrão da Embrapa com copyright atualizado automaticamente, executando silenciosamente sem interação do usuário.

Este é o workflow mais simples do módulo, projetado para execução completamente autônoma. Calcula dinamicamente o ano atual e gera o arquivo LICENSE contendo `Copyright ⓒ YYYY Brazilian Agricultural Research Corporation (Embrapa). All rights reserved.` Garante encoding UTF-8 para preservar corretamente o símbolo de copyright ⓒ (U+24D2) e inclui quebra de linha final conforme padrões de arquivo texto.

Se o arquivo LICENSE já existir, será sobrescrito silenciosamente - comportamento intencional para manter o ano sempre atualizado. A única interação com o usuário é uma mensagem de confirmação final informando o caminho do arquivo criado e o ano do copyright aplicado.

## Usage

```xml
<invoke-workflow>
  <path>{project-root}/_bmad/embrapa-io/workflows/setup/generate-license/workflow.yaml</path>
  <description>Gera LICENSE da Embrapa (execução silenciosa)</description>
</invoke-workflow>
```

Este é um workflow **AUTÔNOMO** - não requer interação do usuário.

## Inputs

Nenhum - workflow completamente autônomo.

## Outputs

- **File**: `{project-root}/LICENSE`
- **Content**: `Copyright ⓒ YYYY Brazilian Agricultural Research Corporation (Embrapa). All rights reserved.`
- **Encoding**: UTF-8 com quebra de linha final
- **Year**: Calculado automaticamente da data de execução
