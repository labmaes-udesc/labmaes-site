# Roadmap do redesign

O redesign transforma o site, que nasceu para divulgar o 7º Caminhos do Contemporâneo, numa
plataforma institucional do LabMAES: durável, multilíngue, acessível e capaz de funcionar como
repositório das produções do laboratório.

Cada fase é uma **milestone** no GitHub, e o trabalho de cada uma está nas issues dela:
<https://github.com/labmaes-udesc/labmaes-site/milestones>.

Este documento é o mapa; o detalhe normativo está nos ADRs, nas specs e nos plans
(ver [architecture/README.md](architecture/README.md) para a ordem de precedência).
A divisão em fases vem de
[insumos-brainstorming/LabMAES-redesign-fase-0-v0.2.md](architecture/insumos-brainstorming/LabMAES-redesign-fase-0-v0.2.md), seção 16.

| Fase | Milestone | Estado | Referência |
| --- | --- | --- | --- |
| 0 | Arquitetura de informação e conteúdo | concluída (PR #7) | [spec](superpowers/specs/2026-09-04-redesign-fase-0-arquitetura-conteudo-design.md), ADRs 0001–0006 |
| 1 | Content foundation | em andamento | [spec](superpowers/specs/2026-09-04-redesign-fase-1-content-foundation-design.md), [plan](superpowers/plans/2026-09-04-redesign-fase-1-content-foundation.md), ADR 0007 |
| 2 | Design system | planejada | — |
| 3 | Institucional | planejada | — |
| 4 | Repositório de produções | planejada | — |
| 5 | Eventos | planejada | — |
| 6 | Internacionalização | planejada | ADR 0004 |
| 7 | Hardening e lançamento | planejada | ADR 0005 |
| — | Contínuo: manutenção e governança | permanente | — |

## Fases

**0 — Arquitetura de informação e conteúdo.** Princípios, arquitetura de informação, modelo de
conteúdo v1, estratégia de CMS e política de catalogação progressiva.

**1 — Content foundation.** Camada editorial paralela ao site atual: `.pages.yml`,
`src/content/`, fixtures, validação automática e teste do Pages CMS com bolsistas. O gate de
saída (Etapa 7) impede ligar `src/content` ao site público antes dos seis critérios da spec.

**2 — Design system.** Tokens, componentes, documentação, protótipos no Figma e testes de
acessibilidade dos componentes.

**3 — Institucional.** Home, Sobre, Equipe, Projetos, Redes e parceiros, Contato — as primeiras
páginas alimentadas por `src/content`.

**4 — Repositório.** Produções, documentos, coleções/acervo, busca, filtros e relações
automáticas entre pessoas, projetos e produções.

**5 — Eventos.** O Caminhos do Contemporâneo passa a ser um `event` com `eventEditions`,
preservando as URLs atuais e preparando as próximas edições.

**6 — Internacionalização.** Interface, fluxo de tradução, conteúdo prioritário em PT/EN/ES/FR,
revisão linguística e SEO internacional.

**7 — Hardening e lançamento.** Desempenho, segurança, regressão visual, auditoria manual de
acessibilidade, SEO técnico, redirects e documentação editorial final.

## Como atualizar

Quando uma fase começar, crie a spec e o plan dela em `docs/superpowers/` e atualize a coluna
"Referência". Quando terminar, feche a milestone e atualize o estado aqui e em
[architecture/README.md](architecture/README.md).
