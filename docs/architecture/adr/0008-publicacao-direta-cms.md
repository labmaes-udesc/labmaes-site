# ADR 0008 — Edições do CMS vão direto para a `main`; a `main` só é protegida contra reescrita

- Status: Aceito
- Data: 2026-10-06
- Refina: ADR 0006 (última consequência)

## Contexto

O ADR 0006 previa que "o workflow por branch/PR será preferido enquanto for operacionalmente
viável". Ao configurar a proteção da `main` (issue #70), ficou claro que exigir pull request ou CI
verde antes de cada mudança na `main` faria de cada edição no Pages CMS um PR à espera de alguém com
acesso técnico ao GitHub. O objetivo do ADR 0002 é o oposto: a equipe do LabMAES atualizar o site
com autonomia.

## Decisão

- O Pages CMS grava diretamente na `main`.
- A `main` tem um ruleset ("Proteger main") com só duas regras, que valem para todas as pessoas:
  - impedir *force-push* (reescrever o histórico);
  - impedir apagar a branch.
- Não se exige PR nem CI verde antes de mudanças na `main`.
- Mudanças de código, templates, CSS, configuração e schema (`.pages.yml`) continuam passando por
  PR, por convenção (`CONTRIBUTING.md`), não por trava técnica.

## Por que é seguro

- O fluxo editorial do ADR 0006 continua sendo a porta de publicação: um registro só aparece no
  site quando está como `published`. Rascunhos e registros em revisão podem estar na `main` sem
  ficar públicos.
- A CI roda o validador de conteúdo (ADR 0007) e o build a cada push na `main`. Uma edição que
  quebre uma regra marca o commit como falho e notifica, sem bloquear quem edita.
- Com o histórico protegido, qualquer edição pode ser desfeita por um novo commit.

## Consequências

- A autonomia editorial do LabMAES não depende de quem administra o GitHub.
- Uma edição inválida pode chegar à `main` antes de ser corrigida. Isso só vira problema público se
  o registro estiver como `published`, e é detectado pela CI no mesmo push.
- Se o volume ou o risco editorial crescer, a alternativa registrada é: o CMS grava numa branch
  editorial e uma automação mescla na `main` sempre que a CI passar, sem aprovação humana. Adotar
  essa alternativa exige um novo ADR.
- Para alterar ou remover o ruleset, é preciso registrar a mudança aqui ou num ADR que o substitua.
