# Auditoria 05 — situação de publicação e clareza de `catalogStatus`

**Data:** 2026-09-16
**Status:** implementado; reteste no Pages CMS pendente

## Achados

Depois do reteste aprovado de `contributors` (bloqueio de produção sem nenhum contributor
funcionou), duas dúvidas de UX editorial surgiram:

1. `catalogStatus` ("Estado de catalogação") não deixava claro, para uma pessoa leiga, que o
   campo é sobre a confiança do **nosso cadastro** da produção (identificado/verificado/completo),
   não sobre a obra em si.
2. Não havia como registrar que uma obra está **no prelo** (aceita, ainda não publicada) ou **já
   publicada** — e isso é uma dimensão diferente de `editorialStatus`, que descreve só o fluxo de
   edição do nosso próprio site (se o registro já pode ficar público no LabMAES).

## Decisão

- `catalogStatus` ganhou `description` explicando os três estados e deixando explícito que não é
  sobre a obra.
- `editorial_status` (componente usado em todas as coleções) ganhou `description` reforçando que
  é sobre o registro no nosso site, não sobre a entidade em si.
- Produções ganham `publicationStatus` (opcional, independente de `editorialStatus`):
  - `in-press` — aceita, ainda não publicada;
  - `published` — já publicada.
  - Fica em branco quando o conceito não se aplica (ex.: exposição, produção audiovisual sem
    ciclo editorial formal).

ADR 0003 recebeu uma seção de refinamento registrando essa distinção.

## Armadilha de sintaxe YAML

A primeira tentativa de descrição do `publicationStatus` continha `(ex.: exposição...)` sem
aspas — a sequência `: ` (dois-pontos + espaço) dentro de um escalar plano é interpretada pelo
YAML como início de um mapeamento aninhado, e quebrava o parse (`bad indentation of a mapping
entry`). Corrigido citando a string inteira entre aspas simples, seguindo a convenção já usada em
outras descrições do arquivo (`'Ex.: ...'`). Validado programaticamente com `js-yaml` antes do
commit.

## Fixtures atualizados

- `2025-fixture-producao-bibliografica.md` → `publicationStatus: published` (já era
  `catalogStatus: verified`, com `lastVerifiedAt`);
- `2024-fixture-producao-audiovisual.md` → `publicationStatus: in-press`;
- `2026-fixture-producao-outros.md` → mantido sem `publicationStatus`, para testar que o campo
  opcional não impede salvar.

## Critério de aprovação

1. Os textos de ajuda de `catalogStatus`, `publicationStatus` e "Status editorial" aparecem no
   Pages CMS;
2. `publicationStatus` pode ficar em branco sem bloquear o salvamento;
3. os dois valores (`in-press`/`published`) aparecem com os rótulos em português.
