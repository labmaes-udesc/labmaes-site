# Plan — Redesign Fase 1: Content foundation

**Status:** Em andamento  
**Data:** 2026-09-04

## Pré-condição

A branch da Fase 1 deve conter a documentação final da Fase 0 (ADRs + spec + plan).
Como a branch `redesign/fase-1-content-foundation` foi criada originalmente a partir de
`main`, ela deve receber a Fase 0 antes de novos commits de implementação.

## Etapas

### 1. Reconciliar histórico

Incorporar `redesign/fase-0-arquitetura-conteudo` à branch da Fase 1.

Resultado:
- Fase 1 contém os insumos e documentos normativos da Fase 0;
- não existem duas linhas arquiteturais paralelas.

### 2. Formalizar documentação

Adicionar:
- ADRs 0001–0006;
- spec e plan da Fase 0;
- spec e plan da Fase 1;
- índice `docs/architecture/README.md`.

### 3. Validar foundation existente

Revisar:
- `.pages.yml`;
- `src/content/*`;
- `src/assets/uploads/*`;
- `tools/validate-content-foundation.mjs`;
- alterações em `package.json`;
- `eleventy.config.js`.

### 4. Criar fixtures

Adicionar somente em branch/pasta de teste ou com garantia de não publicação:
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

Substituir o validador estrutural mínimo por validação real do frontmatter/schema.

### 7. Gate de saída

Não conectar `src/content` ao Eleventy público até os critérios da spec da Fase 1 serem
atendidos.
