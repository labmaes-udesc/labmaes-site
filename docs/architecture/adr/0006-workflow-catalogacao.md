# ADR 0006 — Workflow editorial e catalogação progressiva

- Status: Aceito
- Data: 2026-09-04

## Contexto

Não existe hoje uma base consolidada das produções do LabMAES. O acervo será construído
progressivamente e precisa distinguir informação apenas identificada de informação
verificada.

## Decisão

Usar estados editoriais:

- `draft`;
- `review`;
- `published`.

Para produções, usar adicionalmente estados de catalogação:

- `identified`;
- `verified`;
- `complete`.

Registros podem guardar `sourceNotes` e `lastVerifiedAt` como metadados internos de
proveniência.

## Consequências

- não será necessário completar todo o histórico antes do lançamento;
- dados duvidosos não devem ser apresentados como confirmados;
- a primeira carga prioriza produções recentes, verificáveis e vinculadas aos projetos
  atuais;
- o workflow por branch/PR será preferido enquanto for operacionalmente viável.
