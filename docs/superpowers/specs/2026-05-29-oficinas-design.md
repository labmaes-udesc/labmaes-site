# Spec: Página /eventos/caminhos-do-contemporaneo/2026/oficinas

**Data:** 2026-05-29  
**Status:** Aprovado  
**Arquivo alvo:** `src/eventos/caminhos-do-contemporaneo/2026/oficinas/index.html`  
(ou `_site/eventos/caminhos-do-contemporaneo/2026/oficinas/index.html` se gerado por 11ty)

---

## 1. Contexto

A página `/oficinas` atualmente exibe um placeholder ("Em construção"). O Edital 04 do 7º Seminário Caminhos do Contemporâneo foi publicado em 29 de maio de 2026 e as inscrições abrem em 30 de maio. O objetivo é substituir o placeholder por uma página completa com todas as informações do edital.

**Stack:** HTML estático · `tokens.css` · `components.css` · `main.js`  
**Hospedagem:** Cloudflare Pages (push para `main` → deploy automático)

---

## 2. Estrutura da página

A página segue exatamente o padrão das demais páginas do evento (programação, submissões): header do site → hero banner → event-nav → `<main class="site-page">` com seções → footer.

### 2.1 `<head>`

- `<title>` → `Oficinas — 7º Caminhos do Contemporâneo | LabMAES`
- `<meta name="description">` → `Três oficinas simultâneas, gratuitas e presenciais no 7º Seminário Caminhos do Contemporâneo 2026 — inscrições até 1º de agosto pela plataforma Even3.`
- Open Graph completo (título, descrição, imagem, URL, locale)
- Links para Google Fonts (Poppins + DM Mono), `tokens.css`, `components.css`, favicon SVG
- `aria-current="true"` em Eventos no `site-nav`

### 2.2 Header + hero + event-nav

Idêntico ao padrão das outras páginas do evento:
- `<header class="site-header">` com logo, mobile-menu-toggle e site-nav
- `<section class="event-hero">` com `<picture>` (banner mobile + desktop)
- `<nav class="event-nav">` com `aria-current="page"` no botão **Oficinas**

### 2.3 Seção 1 — Cabeçalho da página (`section--ice`)

**Layout:** `oficinas-header-grid` — grid 2 colunas: `1fr 280px`

**Coluna esquerda (`oficinas-header-text`):**
- `<span class="tag tag--red">OFICINAS</span>`
- `<h1 class="section-title">Três oficinas simultâneas</h1>`
- `<p class="section-body">` — descrição geral (presencial, gratuito, 12 vagas, Even3)
- Dois botões em `oficinas-header-actions`:
  - `button--primary` → Even3 (target blank)
  - `button--outline button--pdf` → `/assets/editais/Caminhos_edital_04_OF.pdf` (target blank)

**Coluna direita — sidebar (`<aside>`):**
- `<div class="prazo-card">` com `tag--blue` "CRONOGRAMA" e `prazo-list`:

| Label | Data |
|---|---|
| Abertura das inscrições | 30 mai 2026 |
| Prazo final | 1º ago 2026 |
| Lista de inscritos | 10 ago 2026 |
| Oficinas 1 e 2 | 19 ago · 17h–18h30 |
| Oficina 3 | 20 ago · 17h30–19h |

- Datas passadas/neutras: `prazo-item__date` com `color: var(--color-brand-blue)`
- Data de prazo final (1º ago): cor padrão `var(--color-brand-red)`

**Gráfico decorativo:** pseudo-elemento `::before` no `.oficinas-header-graphic` usando `module-labmaes-block-2x2-a.svg`, `rotate(-8deg)`, `opacity: 0.13`, cor `var(--color-brand-red)`. Oculto em mobile.

### 2.4 Seção 2 — As três oficinas (`section--pink`)

**Cabeçalho da seção (`oficinas-section-intro`):** flex row com:
- `.oficinas-section-intro__content`: `tag--blue` "PROGRAMAÇÃO · PRESENCIAL", `<h2 class="section-title">As oficinas</h2>`, `section-body` com instrução sobre escolha única e entrega de materiais
- `.oficinas-section-intro__graphic`: pseudo-elemento decorativo — `module-labmaes-block-2x2-b.svg`, `rotate(10deg)`, `opacity: 0.18`, cor `var(--color-brand-blue)`. Oculto em mobile.

**Grid:** `event-card-grid event-card-grid--3`

Cada `<article class="oficina-card">` contém (em ordem):
1. `tag--blue` ou `tag--red` com data e horário
2. `<h3>` — título da oficina
3. `.oficina-card__ministrante` — nomes em DM Mono, `font-size: 12px`, separados por ` · `
4. `.oficina-card__ementa` — texto completo da ementa do edital
5. Bloco de materiais: `.oficina-card__materiais-label` ("MATERIAIS NECESSÁRIOS") + `.oficina-card__materiais` (fundo `--color-brand-ice`, itens separados por ` · `)
6. `.oficina-card__meta` — local e nº de vagas em DM Mono

**Oficinas:**

| # | Tag | Título | Ministrantes | Data/Hora | Local |
|---|-----|--------|-------------|-----------|-------|
| 1 | `tag--blue` | Composição visual para figurinos cênicos: exercícios de representação | Valdecir Babinski Júnior (prof.) · Pietra Eurich Martins · Poliana Cardoso da Silva · Maria Gabriela Rodrigues Zoldan (UEM) | 19 AGO · 17h–18h30 | Sala BC 102 – UDESC CEART |
| 2 | `tag--blue` | Do texto ao têxtil | Janaina Nascimento | 19 AGO · 17h–18h30 | Sala BC 101 – UDESC CEART |
| 3 | `tag--red` | Desenhando com linhas | Camila França · Emanoela Mardula (IFSC-JAR) · M. E. Mariquito Gonçalves · M. H. Cano Garbin · G. N. Martines · Valdecir Babinski Júnior (UEM) | 20 AGO · 17h30–19h | Sala BC 101 – UDESC CEART |

**Materiais completos por oficina:**
- Oficina 1: Lápis de cor · nanquim · marcadores · grafite · esfuminho
- Oficina 2: Poemas · tesouras · linhas · agulhas · tecidos/retalhos · fios/cordões · lã e similares
- Oficina 3: Linhas de costura · fios de tricô e crochê (lãs e barbantes) · cordões e fios têxteis variados · retalhos lineares (debruns e aviamentos em rolo) · linhas de pesca · meadas · fio de nylon (diferentes espessuras, cores e texturas) · arames · pedrarias e aviamentos · tesouras · fita crepe · materiais simples de fixação

### 2.5 Seção 3 — Como participar (`section--ice`)

**Cabeçalho:** `tag--red` "INFORMAÇÕES" + `<h2 class="section-title">Como participar</h2>` + `section-body`

**Grid:** `normas-grid` (3 colunas, reutiliza classe existente) com 3 `event-card` / `regra-card`:

| Card | Tag | Título | Conteúdo (lista `<ul>`) |
|---|---|---|---|
| 1 | `tag--blue` | 12 vagas por oficina | Inscrições só pelo Even3 · Inscreva-se no evento primeiro · Ordem de inscrição · Prazo 1º ago · Vagas remanescentes: presencialmente em 19/08 até 16h |
| 2 | `tag--blue` | Traga seus materiais | Inscrição gratuita · Materiais de responsabilidade do participante · Sacola identificada com nome · Entrega até 17/08 18h na sala do LabMAES · Fora de Florianópolis: labmaes.ceart@udesc.br |
| 3 | `tag--red` | 20% para vulnerabilidade social | ≈ 2 vagas reservadas por oficina · Documento comprobatório exigido · Materiais fornecidos pelos oficineiros nessa modalidade · Ordem de inscrição |

### 2.6 Seção 4 — Callout CTA (`section--red`)

Componente `event-callout` padrão:
- **Conteúdo:** `tag--ice` "INSCRIÇÕES ABERTAS" + `<h2 class="event-callout__title">Inscreva-se nas oficinas</h2>` + `event-callout__body` com prazo e instrução para se inscrever no evento primeiro + e-mail de contato
- **Botões** (coluna flex, `flex-shrink: 0`):
  - `button--secondary` → Even3 (target blank)
  - `button--outline-ice` → `/assets/editais/Caminhos_edital_04_OF.pdf` (target blank, `↓ Edital 04 — PDF`)

---

## 3. CSS novo necessário

Todos os componentes reutilizados já existem no `components.css`. São necessários apenas os seguintes blocos novos, a serem adicionados ao final do `components.css` (ou em seção nomeada):

```css
/* ═══════════════════════════════════════════════════════════
   OFICINAS
   ═══════════════════════════════════════════════════════════ */

/* ─── Cabeçalho da página ───────────────────────────────── */
.oficinas-header-grid {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: var(--space-48);
  align-items: start;
}

.oficinas-header-text {
  display: flex;
  flex-direction: column;
  gap: var(--space-24);
}

.oficinas-header-actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-12);
  align-items: center;
}

/* Botão PDF — variante outline vermelho */
.button--pdf {
  color: var(--color-brand-red);
  border-color: var(--color-brand-red);
}

/* Gráfico decorativo do cabeçalho */
.oficinas-header-graphic {
  flex-shrink: 0;
  position: relative;
  width: 120px;
  height: 240px;
  align-self: center;
}

.oficinas-header-graphic::before {
  content: '';
  position: absolute;
  top: 50%; left: 50%;
  width: 240px; height: 240px;
  transform: translate(-50%, -50%) rotate(-8deg);
  background-color: var(--color-brand-red);
  -webkit-mask-image: url('/assets/graphics/module-labmaes-block-2x2-a.svg');
  mask-image: url('/assets/graphics/module-labmaes-block-2x2-a.svg');
  -webkit-mask-size: contain; mask-size: contain;
  -webkit-mask-repeat: no-repeat; mask-repeat: no-repeat;
  -webkit-mask-position: center; mask-position: center;
  opacity: 0.13;
}

/* ─── Intro da seção de oficinas ────────────────────────── */
.oficinas-section-intro {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-32);
}

.oficinas-section-intro__content {
  display: flex;
  flex-direction: column;
  gap: var(--space-16);
  max-width: 560px;
}

.oficinas-section-intro__graphic {
  flex-shrink: 0;
  position: relative;
  width: 160px;
  height: 160px;
  align-self: center;
}

.oficinas-section-intro__graphic::before {
  content: '';
  position: absolute;
  top: 50%; left: 50%;
  width: 200px; height: 200px;
  transform: translate(-50%, -50%) rotate(10deg);
  background-color: var(--color-brand-blue);
  -webkit-mask-image: url('/assets/graphics/module-labmaes-block-2x2-b.svg');
  mask-image: url('/assets/graphics/module-labmaes-block-2x2-b.svg');
  -webkit-mask-size: contain; mask-size: contain;
  -webkit-mask-repeat: no-repeat; mask-repeat: no-repeat;
  -webkit-mask-position: center; mask-position: center;
  opacity: 0.18;
}

/* ─── Card de oficina enriquecido ───────────────────────── */
.oficina-card__ministrante {
  margin: 0;
  font-family: var(--font-event);
  font-size: 12px;
  line-height: 1.6;
  color: rgba(48, 42, 102, 0.52);
  padding-bottom: var(--space-12);
  border-bottom: 1px solid rgba(48, 42, 102, 0.08);
}

.oficina-card__ementa {
  margin: 0;
  font-size: var(--text-body-size);
  line-height: var(--text-body-line);
  color: rgba(48, 42, 102, 0.72);
  flex-grow: 1;
}

.oficina-card__materiais-label {
  margin: var(--space-8) 0 6px;
  font-family: var(--font-event);
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.7px;
  color: rgba(48, 42, 102, 0.42);
}

.oficina-card__materiais {
  background: var(--color-brand-ice);
  border-radius: var(--radius-sm);
  padding: 10px 14px;
  font-size: 13px;
  line-height: 1.65;
  color: rgba(48, 42, 102, 0.70);
}

/* ─── Regras (reutiliza normas-grid do components.css) ──── */
.regra-card {
  background: var(--color-white);
  border: 1px solid rgba(48, 42, 102, 0.12);
  border-radius: var(--radius-lg);
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: var(--space-12);
}

.regra-card h3 {
  margin: 0 0 var(--space-8);
  font-size: 17px;
  font-weight: 700;
  color: var(--color-brand-blue);
  line-height: 1.3;
}

.regra-card ul {
  margin: 0; padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.regra-card li {
  font-size: var(--text-body-size);
  line-height: var(--text-body-line);
  color: rgba(48, 42, 102, 0.72);
  padding-left: 16px;
  position: relative;
}

.regra-card li::before {
  content: '–';
  position: absolute;
  left: 0;
  color: var(--color-brand-red);
  font-weight: 700;
}

/* ─── Responsivo: oficinas ──────────────────────────────── */
@media (max-width: 767px) {
  .oficinas-header-grid {
    grid-template-columns: 1fr;
  }

  .oficinas-header-graphic {
    display: none;
  }

  .oficinas-section-intro {
    flex-direction: column;
  }

  .oficinas-section-intro__graphic {
    display: none;
  }
}
```

> **Nota:** `.oficina-card` (container flex-column com gap e `.oficina-card__meta`) já existe no `components.css`. Os novos seletores acima são extensões desse card.

---

## 4. Arquivos a modificar

| Arquivo | Ação |
|---|---|
| `eventos/caminhos-do-contemporaneo/2026/oficinas/index.html` | Substituir conteúdo do placeholder pela estrutura descrita |
| `css/components.css` | Adicionar bloco `/* OFICINAS */` ao final |

> **Atenção:** verificar se o projeto usa `src/` + build (11ty) ou edita diretamente os arquivos em `_site/`. Editar apenas os arquivos-fonte corretos.

---

## 5. Checklist de QA

- [ ] Página carrega com header, hero banner, event-nav e footer corretos
- [ ] `aria-current="page"` em "Oficinas" no event-nav
- [ ] `aria-current="true"` em "Eventos" no site-nav
- [ ] Módulos gráficos decorativos visíveis (pseudo-elementos com SVG mask)
- [ ] Botão "↓ Edital 04 — PDF" abre `/assets/editais/Caminhos_edital_04_OF.pdf` em nova aba
- [ ] Botões Even3 abrem `https://www.even3.com.br/7-seminario-caminhos-do-contemporaneo-744454` em nova aba
- [ ] Sidebar de cronograma renderiza corretamente com prazos corretos
- [ ] 3 cards de oficina com ementa completa, ministrantes e caixa de materiais
- [ ] Tag da Oficina 3 é `tag--red` (dia diferente das Oficinas 1 e 2)
- [ ] Seção "Como participar" com 3 cards e `normas-grid`
- [ ] Callout CTA fundo vermelho com dois botões empilhados
- [ ] Mobile: sidebar empilha abaixo do texto, gráficos decorativos ocultos, `event-nav` scroll horizontal
- [ ] Scroll reveal de cards funciona via `main.js` (IntersectionObserver)
