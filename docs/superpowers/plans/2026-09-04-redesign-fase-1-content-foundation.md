# Plan — Redesign Fase 1: Content foundation

**Status:** Em andamento  
**Data:** 2026-09-10

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

### 4. Criar fixtures — CONCLUÍDA

Conjunto criado em `src/content/**`, inteiramente marcado como fixture e mantido fora do build
público. Inclui pessoas, instituição, projetos, produções, evento/edição, documento e página
institucional de teste.

Ver:
`docs/superpowers/fixtures/2026-09-10-fase-1-fixtures-editoriais.md`.

### 5. Validar CMS — PRÓXIMA ETAPA

Testar no Pages CMS:
- descoberta das coleções;
- referências;
- edição;
- mídia;
- traduções;
- mensagens de erro;
- operações permitidas;
- ergonomia com uma pessoa não técnica.

### 6. Evoluir validação

Substituir o validador estrutural mínimo por validação real de frontmatter/schema e referências.

### 7. Gate de saída

Não conectar `src/content` ao Eleventy público até os critérios da spec da Fase 1 serem atendidos.
