# ADR 0007 — Validação de conteúdo derivada do `.pages.yml`

- Status: Aceito
- Data: 2026-10-05

## Contexto

O `.pages.yml` já descreve o schema de todas as coleções de `src/content/`: tipos de campo,
`required`, opções de `select`, `pattern`, coleção alvo de cada `reference` e os blocos de
`contributors`. A spec da Fase 1 exige validação automática de frontmatter/schema, slugs únicos,
referências existentes, `other` + `otherTypeLabel` e datas coerentes. O validador anterior só
conferia os nomes das pastas.

Uma biblioteca de schema (Zod, Ajv) exigiria uma segunda descrição dos mesmos campos, que
divergiria do CMS a cada ajuste. Nenhuma biblioteca resolve as regras que cruzam campos ou
arquivos.

## Decisão

Validar o conteúdo com um validador próprio que **lê o `.pages.yml` como fonte única do schema**:

- `gray-matter` lê o frontmatter e `js-yaml` lê o `.pages.yml` (ambos já eram dependências
  transitivas do Eleventy; passam a ser `devDependencies` explícitas);
- as checagens por campo são derivadas do `.pages.yml`: obrigatoriedade, tipo, `select`,
  `pattern`, listas, objetos, blocos, referências por slug e arquivos de mídia existentes;
- campos fora do schema são erro (pegam erros de digitação);
- um tipo de campo ou chave do `.pages.yml` que o validador não conhece **falha de forma
  explícita** em vez de ser ignorado;
- as regras que cruzam campos ou arquivos ficam em código próprio, separado:
  slugs únicos por coleção, nome de arquivo igual ao `filename.template`,
  `other` exige `otherTypeLabel`, datas coerentes, `contributors` sem a mesma pessoa interna
  repetida;
- o comando continua sendo `npm run validate:content`; saída com código 1 se houver erro.

## Consequências

- uma mudança no CMS passa a ser validada sem editar um segundo schema;
- um tipo de campo novo no `.pages.yml` exige uma linha nova no validador, e o validador avisa
  quando isso acontece;
- o interpretador só cobre o dialeto do Pages CMS que o projeto usa; o que não é usado não é
  validado;
- o validador garante coerência do conteúdo, não que o CMS grave corretamente (isso foi testado
  na Etapa 5);
- a regra de compatibilidade entre `productionCategory` e `productionType` não é validada,
  porque nenhum ADR a define;
- se o projeto passar a consumir `src/content` com TypeScript, schemas Zod podem ser gerados a
  partir do mesmo `.pages.yml` sem reabrir esta decisão.
