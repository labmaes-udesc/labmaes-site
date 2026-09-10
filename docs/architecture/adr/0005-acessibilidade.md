# ADR 0005 — WCAG 2.2 AA como requisito do projeto

- Status: Aceito
- Data: 2026-09-04

## Contexto

Acessibilidade é requisito imperativo do redesign e precisa orientar componentes,
conteúdo e validação, não ser uma revisão posterior.

## Decisão

Adotar WCAG 2.2 nível AA como referência mínima de acessibilidade.

Combinar:

- HTML semântico;
- operação completa por teclado;
- foco visível e gerenciamento de foco;
- contraste e escalabilidade tipográfica;
- suporte a `prefers-reduced-motion`;
- textos alternativos e política editorial de mídia;
- testes automatizados;
- testes manuais periódicos.

## Consequências

- novos componentes só são considerados prontos após critérios de acessibilidade;
- o CI deverá ganhar verificações automatizáveis;
- PDFs/documentos deverão registrar limitações e, quando possível, oferecer alternativa
  HTML acessível;
- conformidade automatizada não substitui avaliação manual.
