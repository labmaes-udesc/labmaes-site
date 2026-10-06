# Fixtures editoriais — Fase 1

**Status:** conjunto de teste da Etapa 4  
**Data:** 2026-09-10

## Objetivo

Validar o schema e a experiência editorial do Pages CMS sem usar dados reais nem publicar
conteúdo fictício no site.

Todos os fixtures:

- usam prefixo `fixture-` no slug;
- têm `editorialStatus: draft`;
- usam títulos explicitamente marcados com `[FIXTURE]`;
- permanecem sob `src/**`, atualmente ignorado pelo Eleventy;
- devem ser removidos antes da primeira carga editorial real.

## Cobertura

1. pessoa integrante atual;
2. pessoa egressa;
3. instituição;
4. projeto de pesquisa;
5. projeto de extensão;
6. produção bibliográfica;
7. produção audiovisual;
8. produção `other` com `otherTypeLabel`;
9. evento recorrente;
10. edição de evento;
11. documento com PDF de teste;
12. página institucional com `body`, SEO e traduções EN/ES/FR.

## Relações exercitadas

- pessoa → instituição;
- projeto → coordenação / participantes / instituições;
- produção → autoria / projeto;
- edição → evento / organizadores / instituições.

## Checklist para a Etapa 5

Confirmar no Pages CMS que uma pessoa editora consegue:

- localizar todos os fixtures;
- alterar campos e salvar sem editar YAML;
- selecionar referências pelo nome exibido;
- distinguir `editorialStatus` de `status`;
- editar e preservar traduções;
- anexar/substituir mídia;
- entender a ajuda do campo `slug`;
- preencher `otherTypeLabel`;
- perceber que rename/delete estão bloqueados.

## Limpeza

Antes da primeira carga real, remover os registros com `slug` iniciado por `fixture-` e o PDF
`src/assets/uploads/documents/fixture-documento.pdf`.
