# Plan — Redesign Fase 0: Arquitetura de informação e conteúdo

**Status:** Concluído  
**Data:** 2026-09-04

## Entregáveis

1. Inventário técnico do repositório atual.
2. Diagnóstico de arquitetura e manutenção.
3. Arquitetura de informação v1.
4. Modelo de conteúdo v1.
5. Estratégia de CMS Git-based.
6. Estratégia i18n.
7. Critério WCAG 2.2 AA.
8. Estratégia de SEO por tipo de conteúdo.
9. Política de catalogação progressiva.
10. ADRs 0001–0006.
11. Spec formal da Fase 0.

## Decisões fechadas

- manter Eleventy;
- manter Cloudflare Pages;
- manter GitHub como fonte da verdade;
- validar Pages CMS;
- preservar egressos;
- usar uma entidade única `project`;
- adotar “Outros” como escape controlado em produções;
- construir o catálogo de produções progressivamente.

## Encerramento

Os arquivos de `docs/architecture/insumos-brainstorming/` permanecem preservados como
histórico, mas deixam de ser normativos.

A Fase 1 só deve avançar tomando esta spec e os ADRs como base.
