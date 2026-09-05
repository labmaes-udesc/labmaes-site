# Plan — Redesign Fase 1: Content foundation

**Status:** Em andamento  
**Data:** 2026-09-04

## Pré-condição

A branch da Fase 1 deve conter a documentação final da Fase 0 (ADRs + spec + plan).

**Status: concluído.**

## Etapas

### 1. Reconciliar histórico — CONCLUÍDA

`redesign/fase-1-content-foundation` contém a Fase 0 e não há mais linhas arquiteturais paralelas.

### 2. Formalizar documentação — CONCLUÍDA

Presentes:
- ADRs 0001–0006;
- spec e plan da Fase 0;
- spec e plan da Fase 1;
- índice `docs/architecture/README.md`.

### 3. Validar foundation existente — AUDITADA; CORREÇÃO 01 PENDENTE DE COMMIT

Auditados:
- `.pages.yml`;
- `src/content/*`;
- `src/assets/uploads/*`;
- `tools/validate-content-foundation.mjs`;
- `package.json`;
- `eleventy.config.js`.

Correções da Auditoria 01:
- tokens explícitos `{fields.slug}` / `{fields.year}`;
- `editorialStatus` padronizado;
- operações destrutivas bloqueadas durante piloto;
- campos de texto alternativo;
- SVG removido dos uploads via CMS.

Ver:
`docs/superpowers/reviews/2026-09-04-fase-1-content-foundation-auditoria-01.md`.

### 4. Criar fixtures — PRÓXIMA ETAPA

Adicionar com garantia de não publicação:
- integrante atual;
- egresso;
- instituição;
- projeto de pesquisa;
- projeto de extensão;
- produção bibliográfica;
- produção audiovisual;
- produção `other`;
- evento;
- edição;
- documento.

### 5. Validar CMS

Testar referências, edição, mídia, traduções, erros e operações permitidas.

### 6. Evoluir validação

Substituir o validador estrutural mínimo por validação real de frontmatter/schema.

### 7. Gate de saída

Não conectar `src/content` ao Eleventy público até os critérios da spec da Fase 1 serem atendidos.
