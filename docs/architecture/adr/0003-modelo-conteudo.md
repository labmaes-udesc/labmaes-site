# ADR 0003 — Modelo de conteúdo estruturado e relacional

- Status: Aceito
- Data: 2026-09-04

## Contexto

O novo site será também um repositório das produções e da memória institucional do
LabMAES. Páginas isoladas e conteúdo hardcoded não escalam para esse objetivo.

## Decisão

Adotar entidades estruturadas e relacionáveis como base do site.

Entidades iniciais:

- page;
- person;
- institution;
- project;
- production;
- document;
- collection;
- event;
- eventEdition;
- news.

Projetos de pesquisa, ensino e extensão são uma única entidade `project`, diferenciada
por tipo.

Pessoas mantêm histórico de vínculo. Egressos não são removidos do acervo.

Produções usam macro categorias públicas:

- bibliográficas;
- artísticas;
- audiovisuais;
- educacionais;
- documentais;
- outros.

`other` é escape controlado e deve registrar `otherTypeLabel`.

## Consequências

- relações substituem duplicação de nomes e metadados;
- páginas de autor, projeto, produção e evento poderão ser geradas automaticamente;
- slugs passam a funcionar como identificadores estáveis;
- alterações de taxonomia devem preservar compatibilidade ou prever migração.
