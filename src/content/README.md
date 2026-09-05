# Fundação de conteúdo do redesign

Esta árvore é a nova camada editorial do LabMAES.

## Estado

Durante a Fase 1, ela é **paralela** ao site Eleventy atual. Nenhuma rota pública depende destes
arquivos até que schemas, CMS, validações e templates tenham sido testados.

## Regras

- não mover o conteúdo atual para `src/content/` nesta etapa;
- não remover `_data/` nem páginas Nunjucks existentes;
- não publicar fixtures de teste em produção;
- referências entre entidades usam slugs estáveis;
- egressos permanecem no acervo;
- `productionType: other` exige `otherTypeLabel`;
- itens de produção usam `catalogStatus: identified | verified | complete`;
- traduções só devem ser preenchidas quando revisadas.

A configuração editorial está em `/.pages.yml`.
