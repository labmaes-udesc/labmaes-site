# ADR 0009 — A macro categoria da produção é derivada do tipo específico

- Status: Aceito
- Data: 2026-10-06
- Refina: ADR 0003 (macro categorias das produções); resolve a pendência registrada no ADR 0007

## Contexto

O ADR 0003 definiu seis macro categorias públicas de produção (bibliográficas, artísticas,
audiovisuais, educacionais, documentais, outros) e, no schema v1, cada produção tinha dois campos
escolhidos de forma independente: "Macro categoria" e "Tipo específico". Nada impedia combinações
sem sentido, como categoria Audiovisual com tipo Artigo. O ADR 0007 deixou a regra de
compatibilidade sem validar, porque nenhum ADR a definia (issue #16).

## Decisão

- Quem cadastra escolhe **só o Tipo específico**. O campo "Macro categoria" (`productionCategory`)
  sai do CMS e do frontmatter.
- A categoria é **derivada do tipo** por uma tabela única em
  `tools/content-model/categorias-producao.mjs`, que também guarda os nomes públicos das
  categorias:

| Categoria | Tipos |
| --- | --- |
| Bibliográficas | artigo, livro, capítulo de livro, organização de livro, trabalho em evento, tese / dissertação / TCC |
| Artísticas | produção artística, exposição, catálogo |
| Audiovisuais | produção audiovisual, podcast / áudio |
| Educacionais | material didático |
| Documentais | relatório / documento técnico |
| Outros | software / recurso digital, outro |

- O validador recusa um tipo sem categoria na tabela, e um teste confere que todo tipo do
  `.pages.yml` está nela.
- "Se “Outro”, qual?" (`otherTypeLabel`) passa a ser obrigatório só quando o tipo é "Outro".

## Consequências

- Um campo a menos para a bolsista, e nenhuma combinação incoerente possível.
- Cada tipo pertence a exatamente uma categoria. Os tipos ambíguos foram fixados pela coordenação:
  catálogo vai para Artísticas, e software / recurso digital vai para Outros.
- Mudar a categoria de um tipo muda a de todas as produções desse tipo. É uma alteração de
  taxonomia, e por isso exige revisão deste ADR.
- Acrescentar um tipo exige mudar o `.pages.yml` e a tabela no mesmo PR; a CI falha se faltar a
  tabela.
- Templates e filtros públicos (Fase 4) usam `categoriaDe()` em vez de ler um campo do registro.
