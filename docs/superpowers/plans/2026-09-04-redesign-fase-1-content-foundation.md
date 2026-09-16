# Plan — Redesign Fase 1: Content foundation

**Status:** Em andamento  
**Data:** 2026-09-15

## Etapas

### 1. Reconciliar histórico — CONCLUÍDA

A branch da Fase 1 contém a Fase 0 e está sincronizada com `main`.

### 2. Formalizar documentação — CONCLUÍDA

Presentes:
- ADRs 0001–0006;
- spec e plan da Fase 0;
- spec e plan da Fase 1;
- índice `docs/architecture/README.md`.

### 3. Validar foundation existente — CONCLUÍDA

Auditoria 01 aplicada:
- filenames com tokens explícitos de campos;
- `editorialStatus` padronizado;
- operações destrutivas bloqueadas durante piloto;
- campos de texto alternativo;
- SVG removido do upload editorial inicial.

Auditoria 02 aplicada:
- datas opcionais usam `default: ''`;
- valores artificiais em datas vazias deixaram de ser aceitos como comportamento esperado.

### 4. Criar fixtures — CONCLUÍDA

Conjunto criado em `src/content/**`, inteiramente marcado como fixture e mantido fora do build
público. Inclui pessoas, instituição, projetos, produções, evento/edição, documento e página
institucional de teste.

Ver:
`docs/superpowers/fixtures/2026-09-10-fase-1-fixtures-editoriais.md`.

### 5. Validar CMS — EM ANDAMENTO

#### Criação de registros — APROVADA

O Pages CMS criou registros na branch corretamente e preservou o formato de frontmatter.

#### Datas opcionais — CORRIGIDAS

O primeiro teste encontrou data artificial em campo vazio. A Correção 02 foi aplicada.

#### Referências relacionais — FUNCIONAIS; CORREÇÃO 03 PENDENTE DE RETESTE

Teste real confirmou:
- múltiplas referências;
- armazenamento por slug;
- preservação da ordem.

Problema de UX identificado:
- seletor exibia nomes de arquivo (`*.md`) em vez de nomes/títulos legíveis.

Correção 03:
- `value: '{fields.slug}'`;
- `label: '{primary}'`.

Ver:
`docs/superpowers/reviews/2026-09-15-fase-1-cms-auditoria-03-referencias.md`.

#### Modelo de autoria — DECISÃO TOMADA; IMPLEMENTAÇÃO PENDENTE

Produções adotarão `contributors` em lista ordenada, aceitando:
- pessoa interna por referência;
- pessoa externa por nome/metadados mínimos.

Ainda testar:
- `contributors`;
- mídia;
- traduções;
- workflow editorial;
- mensagens de erro e campos obrigatórios;
- ergonomia com uma pessoa não técnica.

### 6. Evoluir validação

Substituir o validador estrutural mínimo por validação real de frontmatter/schema e referências.

### 7. Gate de saída

Não conectar `src/content` ao Eleventy público até os critérios da spec da Fase 1 serem atendidos.
