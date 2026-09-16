# ADR 0003 — Modelo de conteúdo estruturado e relacional

- Status: Aceito
- Data: 2026-09-04
- Refinamento: 2026-09-16

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

### Refinamento — autoria e contribuições

Produções usam uma lista ordenada `contributors` para representar autoria e outros créditos.

Cada item é de um dos seguintes tipos:

- `internal`: referencia uma entidade `person` existente por slug;
- `external`: registra nominalmente uma pessoa que não precisa fazer parte do cadastro institucional.

O bloco externo pode registrar, além do nome, função/crédito, afiliação institucional e ORCID.
O bloco interno pode registrar função/crédito junto à referência da pessoa.

A ordem dos itens em `contributors` é semanticamente significativa e representa a ordem oficial
de autoria/crédito.

Não devem ser criados perfis `person` artificiais apenas para permitir o registro de coautores ou
colaboradores externos.

## Consequências

- relações substituem duplicação de nomes e metadados quando a pessoa integra o cadastro;
- colaboradores externos podem ser registrados sem inflar artificialmente a coleção `people`;
- páginas de autor, projeto, produção e evento poderão ser geradas automaticamente;
- slugs passam a funcionar como identificadores estáveis;
- a ordem de `contributors` deve ser preservada por CMS, validação e templates públicos;
- alterações de taxonomia devem preservar compatibilidade ou prever migração.
