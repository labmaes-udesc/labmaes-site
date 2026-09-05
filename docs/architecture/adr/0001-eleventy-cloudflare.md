# ADR 0001 — Manter Eleventy e Cloudflare Pages

- Status: Aceito
- Data: 2026-09-04

## Contexto

O site atual já é gerado com Eleventy e publicado automaticamente pela Cloudflare
Pages. O redesign precisa ampliar robustez, conteúdo e governança sem introduzir
complexidade operacional desnecessária.

## Decisão

Manter Eleventy como gerador estático e Cloudflare Pages como plataforma de build e
deploy nesta etapa do redesign.

## Consequências

- preservamos baixo custo, boa performance e pequena superfície de ataque;
- o redesign será incremental, sem reescrita total;
- funcionalidades dinâmicas deverão ser justificadas antes de introduzir runtime
  adicional;
- uma futura troca de framework exigirá novo ADR.
