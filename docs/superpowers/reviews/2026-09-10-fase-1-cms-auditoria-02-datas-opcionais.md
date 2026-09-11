# Auditoria 02 — datas opcionais no Pages CMS

**Data:** 2026-09-10  
**Status:** correção identificada; aplicação manual necessária por bloqueio 403 do conector.

## Achado

No primeiro teste real de criação de uma pessoa pelo Pages CMS, o registro foi salvo com:

`membershipEnd: 0001-09-01`

apesar de não haver uma data final válida.

## Decisão

Todos os campos de data opcionais devem declarar explicitamente:

`default: ''`

A data obrigatória das notícias permanece inalterada.

## Campos afetados

- people.membershipStart
- people.membershipEnd
- projects.startDate
- projects.endDate
- productions.date
- productions.lastVerifiedAt
- documents.date
- event_editions.startDate
- event_editions.endDate

## Critério de aprovação

Criar novo registro de pessoa no Pages CMS deixando `membershipEnd` vazio e confirmar que o
arquivo gerado não contém uma data artificial.
