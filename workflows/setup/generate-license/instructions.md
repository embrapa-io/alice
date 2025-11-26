# Generate LICENSE - Instruções de Geração Automática

<critical>The workflow execution engine is governed by: {project-root}/.bmad/core/tasks/workflow.xml</critical>
<critical>You MUST have already loaded and processed: {project-root}/.bmad/embrapa-io/workflows/setup/generate-license/workflow.yaml</critical>
<critical>This is an AUTONOMOUS workflow - executes silently without user interaction</critical>
<critical>Communicate in {communication_language} for final confirmation only</critical>

<workflow>

<step n="1" goal="Calcular ano atual automaticamente">
<action>Obter data atual do sistema</action>
<action>Extrair ano no formato YYYY (4 dígitos)</action>
<action>Armazenar em variável {{current_year}}</action>

**Exemplo**: Se data atual é 2025-10-21, então {{current_year}} = 2025

**Importante**: NÃO usar ano fixo - deve ser calculado dinamicamente a cada execução
</step>

<step n="2" goal="Gerar conteúdo do arquivo LICENSE">
<action>Carregar template de: {installed_path}/template.LICENSE</action>
<action>Substituir variável {{current_year}} pelo ano calculado no Step 1</action>

**Conteúdo esperado**:
```
Copyright ⓒ 2025 Brazilian Agricultural Research Corporation (Embrapa). All rights reserved.
```

(onde 2025 é substituído pelo ano atual)

<action>Armazenar conteúdo completo pronto para salvar</action>

<template-output>license_content</template-output>
</step>

<step n="3" goal="Salvar arquivo LICENSE">
<action>Criar arquivo em {default_output_file} (que resolve para {project-root}/LICENSE)</action>
<action>Escrever conteúdo gerado no Step 2</action>
<action>Garantir encoding UTF-8 para preservar símbolo ⓒ</action>

**Importante**:
- Este workflow é AUTÔNOMO - NÃO solicitar confirmação do usuário
- Se arquivo LICENSE já existir, sobrescrever silenciosamente
- Garantir quebra de linha final

<check if="arquivo salvo com sucesso">
<action>Confirmar criação para {user_name} em {communication_language}:</action>

**Mensagem de confirmação**:
```
✅ Arquivo LICENSE criado com sucesso!

Localização: {project-root}/LICENSE
Ano do copyright: {{current_year}}
Conteúdo: Copyright ⓒ {{current_year}} Brazilian Agricultural Research Corporation (Embrapa). All rights reserved.
```
</check>

<check if="erro ao salvar">
<action>Reportar erro em {communication_language}</action>
<action>Informar caminho tentado e motivo da falha</action>
</check>
</step>

</workflow>

## 📋 Validação Pós-Geração

Este workflow deve resultar em:

- ✅ Arquivo `LICENSE` na raiz do projeto
- ✅ Conteúdo: `Copyright ⓒ YYYY Brazilian Agricultural Research Corporation (Embrapa). All rights reserved.`
- ✅ Ano (YYYY) corresponde ao ano atual de execução
- ✅ Símbolo ⓒ (U+24D2) renderizado corretamente
- ✅ Encoding UTF-8
- ✅ Arquivo com quebra de linha final
- ✅ Execução silenciosa (sem prompts ao usuário)

## 🔧 Uso por Agentes

Este workflow deve ser invocado automaticamente durante setup inicial do projeto:

```xml
<step n="X" goal="Gerar arquivo LICENSE da Embrapa">
  <invoke-workflow>
    <path>{project-root}/.bmad/embrapa-io/workflows/setup/generate-license/workflow.yaml</path>
    <description>Cria LICENSE com copyright da Embrapa (execução silenciosa)</description>
  </invoke-workflow>
</step>
```

**Características**:
- Workflow autônomo (sem interação)
- Ano calculado dinamicamente
- Sobrescreve LICENSE existente
- Confirmação final apenas
