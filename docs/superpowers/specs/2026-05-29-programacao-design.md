# Spec: Página Programação — 7º Caminhos do Contemporâneo

**Data:** 2026-05-29  
**Rota:** `/eventos/caminhos-do-contemporaneo/2026/programacao/`  
**Arquivo:** `labmaes-site/eventos/caminhos-do-contemporaneo/2026/programacao/index.njk`

---

## Objetivo

Substituir o placeholder "EM CONSTRUÇÃO" pela programação completa do evento, respeitando o design system existente e filtrando informações de controle interno.

---

## Informações públicas vs. internas

### Incluir
- Horário, nome da atividade, local (simplificado), modalidade
- Nomes dos conferencistas principais (Myriam Lemonchois, Mario Barro Hérnandez, Mónica Faria)
- Títulos das mesas temáticas e eixos
- Nomes das oficinas e ministrantes já definidos
- Atividade cultural noturna dia 22 (Desfile Rotfather — confirmado para divulgação)

### Omitir
- Coluna "Responsável" inteira (controle interno)
- Notas de confirmação: "(a confirmar)", "aceite confirmado"
- Notas de produção: "Colocar no canal LabMAES", "Proposta: ...", "fazer convites"
- Lista de convidadas com status de aceite das mesas temáticas
- Curadoria pendente de confirmação

---

## Estrutura de seções

| Seção | Fundo | Conteúdo |
|-------|-------|----------|
| P1 Header | `section--ice` | Nav + H1 "Programação" + intro |
| P2 Dia 19 | `section--pink` | Quarta-feira, 19/08 — abertura, conferência, mesas, oficinas, cultural |
| P3 Dia 20 | `section--ice` | Quinta-feira, 20/08 — conferência, C.O., mesas, oficinas, pôster |
| P4 Dia 21 | `section--pink` | Sexta-feira, 21/08 — conferência, mostra, mesas, encerramento presencial |
| P5 Dia 22 | `section--ice` | Sábado, 22/08 · online — roda de conversa, C.O., mostra, Desfile Rotfather |
| P6 Callout | `section--red` | CTA para inscrição via Even3 |

---

## Programação pública por dia

### Dia 19 de agosto — Quarta-feira

| Horário | Atividade | Local | Modalidade |
|---------|-----------|-------|------------|
| 9h | Abertura | Auditório | Presencial + Online |
| 9h30 | Conferência de abertura — Prof. Dra. Myriam Lemonchois | Auditório | Presencial + Online |
| 11h30 | Mediação sensível | Hall | Presencial |
| 14h | Abertura da Mostra Audiovisual — Cinema Universitário e Comunitário Latino-Americano (1ª sessão) | Auditório | Presencial |
| 14h | Abertura da Exposição "The Rotfather: experimentações têxteis para figurinos anímicos" | Hall – Básica 02 | Presencial |
| 15–17h | Mesa Temática (sessão 1) — Economia Criativa | Auditório | Presencial |
| 15–17h | Mesa Temática (sessão 2) — Tessituras Sensíveis do Ensino de Arte na Educação Básica Contemporânea | Lab | Online |
| 17–18h30 | Oficina 1 — Composição visual para figurinos cênicos | BC 102 | Presencial |
| 17–18h30 | Oficina 2 — Do texto ao têxtil | BC 101 | Presencial |
| 19h | Atividade cultural | Arena | Presencial |
| 19h30 | Coffee break | Básica 2 | Presencial |

### Dia 20 de agosto — Quinta-feira

| Horário | Atividade | Local | Modalidade |
|---------|-----------|-------|------------|
| 9h30 | Mediação artística | Hall | Presencial |
| 10–12h | Conferência — Prof. Dr. Mario Barro Hérnandez | Auditório | Presencial + Online |
| 13h30 | Sessão de Comunicações Orais (presencial) | Auditório | Presencial |
| 14–15h | Mostra Audiovisual — sessão online | Zoom | Online |
| 15–17h | Mesa Temática (sessão 3) — Educação Básica | Auditório | Presencial |
| 15–17h | Mesa Temática (sessão 4) — Economia Criativa | Lab/Zoom | Online |
| 17–17h30 | Apresentação musical | Auditório | Presencial |
| 17h30–19h | Oficina 3 | BC 101 | Presencial |
| 17h30–19h | Oficina 4 — Desenhando com linhas | BC 102 | Presencial |
| 17h30–19h | Sessão de Pôster Digital | Lab/Zoom | Online |

### Dia 21 de agosto — Sexta-feira

| Horário | Atividade | Local | Modalidade |
|---------|-----------|-------|------------|
| 9h30 | Mediação | — | Presencial |
| 10h30 | Conferência — Prof. Dra. Mónica Faria | Auditório | Presencial + Online |
| 14–15h | Mostra Audiovisual — Olhares Sensíveis da Escola (2ª sessão) | Auditório | Presencial + Online |
| 15–17h | Mesa Redonda (sessão 5) — Criação | Auditório | Presencial |
| 15–17h | Mesa Redonda (sessão 6) — Educação Básica | Lab/Zoom | Online |
| 17h30 | Encerramento presencial | Auditório | Presencial |

### Dia 22 de agosto — Sábado · Sessão Online

| Horário | Atividade | Local | Modalidade |
|---------|-----------|-------|------------|
| 9h30 | Atividade de percepção | Zoom | Online |
| 10h30 | Roda de conversa com professores da Educação Básica | Zoom | Online |
| 14–16h | Sessão de Comunicações Orais | Zoom | Online |
| 14–15h | Mostra Audiovisual — Olhares Sensíveis da Escola | Zoom | Online |
| 21h | Desfile Rotfather | Cervejaria Nefasta | Presencial |

---

## Componentes novos (CSS)

### `.schedule-day`
Cabeçalho de cada dia dentro da seção. Contém badge de data + nome do dia da semana.

```
.schedule-day            — flex, align-items: baseline, gap
.schedule-day__date      — "19 AGO" em font-display, cor brand-red, grande
.schedule-day__weekday   — "quarta-feira" em font-event, menor
.schedule-day__badge     — tag opcional "ONLINE" para dia 22
```

### `.schedule-list`
Container da lista de atividades. `display: grid; gap: 16px`.

### `.schedule-item`
Cada linha da programação: grid `120px 1fr`.

```
.schedule-item                 — grid, fundo branco, border-radius, padding
.schedule-item--featured       — conferências: borda esquerda brand-red 3px, fundo levemente tintado
.schedule-item__slot           — horário à esquerda, DM Mono, color brand-red
.schedule-item__content        — conteúdo à direita
.schedule-item__title          — nome da atividade, font-weight 600
.schedule-item__speaker        — nome do palestrante (só conferências), italic ou DM Mono
.schedule-item__meta           — flex row: .modality-tag + local (font-event pequeno)
```

### `.schedule-parallel`
Wrapper para duas atividades simultâneas. `display: grid; grid-template-columns: 1fr 1fr; gap: 12px`.  
No mobile: `grid-template-columns: 1fr`.

### `.modality-tag`
Badge inline pequeno (sem borda, fundo com opacidade baixa).

```
.modality-tag             — inline-flex, padding 3px 8px, border-radius pill, font 11px
.modality-tag--presencial — bg brand-blue/10, color brand-blue
.modality-tag--online     — bg support-green/10, color support-green
.modality-tag--hibrido    — bg support-orange/10, color support-orange
```

---

## Animações

- **Stagger nos schedule-items**: IntersectionObserver existente no site já cobre `.event-card`. Para `schedule-item`, adicionar ao observer em `main.js` com delay de 40ms entre itens.
- **Entrada do dia**: `@starting-style` com `opacity: 0; transform: translateY(8px)` em `.schedule-day__date`.
- `prefers-reduced-motion` já coberto pelo reset global no CSS.
- Sem animações em ações de teclado.

---

## Responsivo

| Breakpoint | Ajuste |
|-----------|--------|
| ≥768px | schedule-item: 120px + 1fr; schedule-parallel: 2 colunas |
| <768px | schedule-item: 1 coluna (slot acima do content); schedule-parallel: 1 coluna |

---

## Arquivos a modificar

1. `eventos/caminhos-do-contemporaneo/2026/programacao/index.njk` — substituição completa
2. `css/components.css` — adicionar classes novas ao final
