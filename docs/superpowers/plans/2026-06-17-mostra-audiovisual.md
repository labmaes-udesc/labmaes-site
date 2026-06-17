# Página Mostra Audiovisual — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar a página exclusiva `/eventos/caminhos-do-contemporaneo/2026/mostra-audiovisual/` apresentando a Mostra Audiovisual "Narrativas em Movimento", seus dois eixos de curadoria, a coordenação, a programação de exibições e o novo fluxo de submissão (Even3 → Google Forms).

**Architecture:** Site estático Eleventy (`.njk` → `_site/`). A página reaproveita o design system existente (`css/tokens.css` + `css/components.css`) e os includes do evento. Verificação por build do Eleventy + inspeção do HTML gerado e preview no navegador — não há framework de testes unitários neste projeto.

**Tech Stack:** Eleventy 3.x (Nunjucks), HTML estático, CSS (tokens + components), hospedagem Cloudflare Pages.

---

## Verificação neste projeto

Não existe test runner. Cada tarefa é verificada assim:
- **Build:** `npm run build` deve terminar sem erro.
- **HTML gerado:** conferir o arquivo correspondente em `_site/...` para o conteúdo esperado.
- **Preview visual:** `npm run start` serve em `http://localhost:8080`; usar as ferramentas de preview para checar layout, console e responsivido.

Os arquivos em `_site/` são build output — **nunca editar à mão**; sempre editar a fonte `.njk`/`.css` e rebuildar.

---

## Estrutura de arquivos

| Arquivo | Ação | Responsabilidade |
|---------|------|------------------|
| `eventos/caminhos-do-contemporaneo/2026/mostra-audiovisual/index.njk` | Criar | Página completa (6 seções) |
| `_includes/event-header.njk` | Modificar | Adicionar item "Mostra" à nav (variante com banner) |
| `_includes/event-nav.njk` | Modificar | Adicionar item "Mostra" à nav (variante standalone) |
| `eventos/caminhos-do-contemporaneo/2026/submissoes/index.njk` | Modificar | Link "Saiba mais →" no card da Mostra |
| `css/components.css` | Modificar | `.event-card-grid--2`, `.curadoria`, `.passo-card` + colapso mobile |

---

## Task 1: Esqueleto da página + cabeçalho (M1)

**Files:**
- Create: `eventos/caminhos-do-contemporaneo/2026/mostra-audiovisual/index.njk`

- [ ] **Step 1: Criar o arquivo com frontmatter, include do header e a seção M1**

Conteúdo inicial do arquivo (será expandido nas próximas tasks):

```njk
---
layout: layout.njk
title: Mostra Audiovisual — 7º Caminhos do Contemporâneo
description: Mostra Audiovisual "Narrativas em Movimento" do 7º Caminhos do Contemporâneo — eixos de curadoria, coordenação, programação de exibições e inscrição via Even3 e formulário.
---

<main id="conteudo" class="site-page">

  {% include "event-header.njk" %}

  <!-- M1: Cabeçalho e prazos -->
  <section class="section section--ice">
    <div class="container">
      <div class="submissoes-header">
        <div class="submissoes-header__text">
          <span class="tag tag--red">MOSTRA AUDIOVISUAL</span>
          <h1 class="section-title">Narrativas em Movimento</h1>
          <p class="section-body">A Mostra Narrativas em Movimento convida estudantes da educação básica, estudantes universitários, educadores(as) e a comunidade do Brasil e da América Latina a colocar em circulação histórias que conectam pessoas, territórios e imaginários por meio do cinema. São aceitos curtas-metragens de ficção, experimental e documentário, com até 20 minutos.</p>
        </div>
        <aside class="submissoes-header__side" aria-label="Prazos importantes">
          <div class="prazo-card">
            <span class="tag tag--blue">PRAZOS</span>
            <ul class="prazo-list" role="list">
              <li class="prazo-item">
                <span class="prazo-item__label">Inscrições</span>
                <span class="prazo-item__date">30 mai – 30 jun 2026</span>
              </li>
              <li class="prazo-item">
                <span class="prazo-item__label">Resultado da seleção</span>
                <span class="prazo-item__date">13 jul 2026</span>
              </li>
              <li class="prazo-item">
                <span class="prazo-item__label">Exibições</span>
                <span class="prazo-item__date">19 – 22 ago 2026</span>
              </li>
            </ul>
          </div>
          <a class="button button--primary"
             href="/assets/editais/Caminhos_edital_03_MA.pdf"
             download
             aria-label="Baixar Edital 03 — Mostra Audiovisual">
            Baixar edital ↓
          </a>
        </aside>
      </div>
    </div>
  </section>

</main>
```

- [ ] **Step 2: Buildar e verificar que não há erro**

Run: `npm run build`
Expected: build conclui sem erro; cria `_site/eventos/caminhos-do-contemporaneo/2026/mostra-audiovisual/index.html`.

- [ ] **Step 3: Verificar o HTML gerado**

Conferir em `_site/eventos/caminhos-do-contemporaneo/2026/mostra-audiovisual/index.html` que o `<h1>` "Narrativas em Movimento", o `prazo-card` e o botão "Baixar edital ↓" (href para o PDF) estão presentes.

- [ ] **Step 4: Commit**

```bash
git add eventos/caminhos-do-contemporaneo/2026/mostra-audiovisual/index.njk
git commit -m "feat: página Mostra Audiovisual — cabeçalho e prazos (M1)"
```

---

## Task 2: Seção dos dois eixos (M2)

**Files:**
- Modify: `eventos/caminhos-do-contemporaneo/2026/mostra-audiovisual/index.njk`

- [ ] **Step 1: Inserir a seção M2 antes do fechamento `</main>`**

Inserir imediatamente após a seção M1 (antes de `</main>`):

```njk
  <!-- M2: Eixos / linhas de curadoria -->
  <section class="section section--pink" aria-labelledby="eixos-heading">
    <div class="container">
      <span class="tag tag--red">EIXOS</span>
      <h2 id="eixos-heading" class="section-title">Linhas de curadoria</h2>
      <p class="section-body">A Mostra subdivide-se em duas linhas, de acordo com o perfil dos(as) realizadores(as).</p>
      <div class="event-card-grid event-card-grid--2 section-content">

        <article class="submissao-card" aria-labelledby="eixo-1-title">
          <div class="submissao-card__header">
            <span class="tag tag--blue">EIXO 1</span>
            <h3 id="eixo-1-title">Cinema Universitário e Comunitário Latino-Americano</h3>
          </div>
          <p class="submissao-card__desc">Obras produzidas por estudantes universitários e pela comunidade (Brasil e América Latina). Idade mínima de 18 anos para o(a) responsável pela inscrição.</p>
          <div class="curadoria">
            <span class="curadoria__label">Curadoria</span>
            <p class="curadoria__names">Andrei Galkowski (Udesc) · Mario Barro Hérnandez (UNAM)</p>
          </div>
        </article>

        <article class="submissao-card" aria-labelledby="eixo-2-title">
          <div class="submissao-card__header">
            <span class="tag tag--blue">EIXO 2</span>
            <h3 id="eixo-2-title">Olhares Sensíveis da Escola</h3>
          </div>
          <p class="submissao-card__desc">Obras produzidas por estudantes da educação básica, devidamente matriculados e representados por um(a) professor(a) responsável.</p>
          <div class="curadoria">
            <span class="curadoria__label">Curadoria</span>
            <p class="curadoria__names">Monica Rodrigues (IEMA) · Karine Joulie</p>
          </div>
        </article>

      </div>
    </div>
  </section>
```

- [ ] **Step 2: Buildar**

Run: `npm run build`
Expected: build sem erro.

- [ ] **Step 3: Verificar HTML gerado**

Conferir que os dois cards de eixo, com os nomes de curadoria corretos, aparecem em `_site/.../mostra-audiovisual/index.html`. (O estilo de `.curadoria` e o grid de 2 colunas vêm na Task 6 — aqui só conferir o conteúdo.)

- [ ] **Step 4: Commit**

```bash
git add eventos/caminhos-do-contemporaneo/2026/mostra-audiovisual/index.njk
git commit -m "feat: Mostra Audiovisual — seção de eixos e curadoria (M2)"
```

---

## Task 3: Coordenação (M3) + Programação (M4)

**Files:**
- Modify: `eventos/caminhos-do-contemporaneo/2026/mostra-audiovisual/index.njk`

- [ ] **Step 1: Inserir as seções M3 e M4 antes de `</main>`**

```njk
  <!-- M3: Coordenação -->
  <section class="section section--red" aria-labelledby="coordenacao-heading">
    <div class="container">
      <span class="tag tag--ice">COORDENAÇÃO</span>
      <h2 id="coordenacao-heading" class="section-title section-title--inverse">Comissão Coordenadora</h2>
      <div class="event-card-grid event-card-grid--3 section-content">
        <article class="event-card">
          <h3>Mara Rúbia Sant'Anna</h3>
        </article>
        <article class="event-card">
          <h3>Monica Rodrigues</h3>
        </article>
        <article class="event-card">
          <h3>Andrei Rafael Galkowski</h3>
        </article>
      </div>
    </div>
  </section>

  <!-- M4: Programação -->
  <section class="section section--ice" aria-labelledby="programacao-heading">
    <div class="container">
      <span class="tag tag--red">PROGRAMAÇÃO</span>
      <h2 id="programacao-heading" class="section-title">Sessões de exibição</h2>
      <p class="section-body">As obras selecionadas serão exibidas em duas sessões presenciais (UDESC CEART) e duas sessões online, cada uma seguida de debate.</p>
      <div class="timeline section-content">
        <article class="timeline-item">
          <p class="timeline-item__date">19 AGO</p>
          <div>
            <h3>Cinema Universitário e Comunitário Latino-Americano</h3>
            <p>Presencial · 14h–15h · UDESC CEART</p>
          </div>
        </article>
        <article class="timeline-item">
          <p class="timeline-item__date">20 AGO</p>
          <div>
            <h3>Cinema Universitário e Comunitário Latino-Americano</h3>
            <p>Online · 14h–15h</p>
          </div>
        </article>
        <article class="timeline-item">
          <p class="timeline-item__date">21 AGO</p>
          <div>
            <h3>Olhares Sensíveis da Escola</h3>
            <p>Presencial · 14h–15h · UDESC CEART</p>
          </div>
        </article>
        <article class="timeline-item">
          <p class="timeline-item__date">22 AGO</p>
          <div>
            <h3>Olhares Sensíveis da Escola</h3>
            <p>Online · 14h–15h</p>
          </div>
        </article>
      </div>
    </div>
  </section>
```

- [ ] **Step 2: Buildar**

Run: `npm run build`
Expected: build sem erro.

- [ ] **Step 3: Verificar HTML gerado**

Conferir que os 3 cards de coordenação e os 4 itens da timeline (datas e modalidades corretas) aparecem em `_site/.../mostra-audiovisual/index.html`.

- [ ] **Step 4: Commit**

```bash
git add eventos/caminhos-do-contemporaneo/2026/mostra-audiovisual/index.njk
git commit -m "feat: Mostra Audiovisual — coordenação e programação (M3, M4)"
```

---

## Task 4: Como participar (M5) + Dúvidas (M6)

**Files:**
- Modify: `eventos/caminhos-do-contemporaneo/2026/mostra-audiovisual/index.njk`

- [ ] **Step 1: Inserir as seções M5 e M6 antes de `</main>`**

```njk
  <!-- M5: Como participar -->
  <section class="section section--pink" aria-labelledby="participar-heading">
    <div class="container">
      <span class="tag tag--red">INSCRIÇÕES</span>
      <h2 id="participar-heading" class="section-title">Como participar</h2>
      <p class="section-body">A participação é gratuita e ocorre em duas etapas. Leia o edital antes de iniciar.</p>
      <div class="event-card-grid event-card-grid--2 section-content">

        <article class="passo-card">
          <span class="passo-card__numero" aria-hidden="true">1</span>
          <h3>Inscrição no evento</h3>
          <p>Acesse a plataforma Even3 e faça sua inscrição gratuita no 7º Seminário Caminhos do Contemporâneo. A inscrição no evento é obrigatória antes de submeter a obra.</p>
          <a class="button button--secondary"
             href="https://www.even3.com.br/7-seminario-caminhos-do-contemporaneo-744454"
             target="_blank" rel="noopener noreferrer">
            Inscrever-se na Even3 ↗
          </a>
        </article>

        <article class="passo-card">
          <span class="passo-card__numero" aria-hidden="true">2</span>
          <h3>Submissão da obra</h3>
          <p>Após a inscrição, preencha o formulário de submissão e envie: link da obra no YouTube ou Vimeo (com acesso liberado ou senha), ficha técnica, sinopse e, quando aplicável, comprovante de vínculo estudantil.</p>
          <a class="button button--secondary"
             href="https://docs.google.com/forms/d/e/1FAIpQLSd4HN7kAcVyDtVfSlyu4XMrmnPCp5jllsqSWz2Xj0Rv7mpLIg/viewform"
             target="_blank" rel="noopener noreferrer">
            Submeter obra ↗
          </a>
        </article>

      </div>
    </div>
  </section>

  <!-- M6: Dúvidas -->
  <section class="section section--red" aria-label="Dúvidas">
    <div class="container">
      <div class="event-callout">
        <div class="event-callout__content">
          <h2 class="event-callout__title">Dúvidas?</h2>
          <p class="event-callout__body">Informações adicionais sobre a Mostra podem ser obtidas com a Comissão Organizadora pelo e-mail labmaes.ceart@udesc.br.</p>
        </div>
        <a class="button button--outline-ice" href="mailto:labmaes.ceart@udesc.br">Enviar e-mail</a>
      </div>
    </div>
  </section>
```

- [ ] **Step 2: Buildar**

Run: `npm run build`
Expected: build sem erro.

- [ ] **Step 3: Verificar HTML gerado**

Conferir os dois `passo-card` com os botões apontando para Even3 (passo 1) e Google Forms (passo 2), e o callout de dúvidas com `mailto:`.

- [ ] **Step 4: Commit**

```bash
git add eventos/caminhos-do-contemporaneo/2026/mostra-audiovisual/index.njk
git commit -m "feat: Mostra Audiovisual — fluxo de inscrição e dúvidas (M5, M6)"
```

---

## Task 5: Navegação — adicionar item "Mostra"

**Files:**
- Modify: `_includes/event-header.njk`
- Modify: `_includes/event-nav.njk`
- Modify: `eventos/caminhos-do-contemporaneo/2026/submissoes/index.njk`

- [ ] **Step 1: Adicionar link "Mostra" em `event-header.njk`**

Em `_includes/event-header.njk`, inserir entre o link de "Submissões" e o de "Oficinas" (após a linha do link de submissões):

```njk
    <a class="button button--outline event-nav__link" href="/eventos/caminhos-do-contemporaneo/2026/mostra-audiovisual/"
       {% if page.url == '/eventos/caminhos-do-contemporaneo/2026/mostra-audiovisual/' %}aria-current="page"{% endif %}>Mostra</a>
```

- [ ] **Step 2: Adicionar link "Mostra" em `event-nav.njk`**

Em `_includes/event-nav.njk`, inserir entre "Submissões" e "Oficinas". Note que este arquivo usa `button--primary` (não `button--outline`):

```njk
    <a class="button button--primary" href="/eventos/caminhos-do-contemporaneo/2026/mostra-audiovisual/"
       {% if page.url == '/eventos/caminhos-do-contemporaneo/2026/mostra-audiovisual/' %}aria-current="page"{% endif %}>Mostra</a>
```

- [ ] **Step 3: Adicionar link "Saiba mais →" no card da Mostra em submissões**

Em `eventos/caminhos-do-contemporaneo/2026/submissoes/index.njk`, localizar o bloco `submissao-card__actions` dentro do card "Edital 3: Mostra Audiovisual" (o que contém apenas o botão "Edital 3 ↓"). Adicionar, após o link de download do edital e dentro do mesmo `<div class="submissao-card__actions">`:

```njk
            <a class="button button--outline"
               href="/eventos/caminhos-do-contemporaneo/2026/mostra-audiovisual/"
               aria-label="Saiba mais sobre a Mostra Audiovisual">
              Saiba mais →
            </a>
```

- [ ] **Step 4: Buildar**

Run: `npm run build`
Expected: build sem erro.

- [ ] **Step 5: Verificar HTML gerado**

- Em qualquer página do evento gerada (ex.: `_site/.../2026/index.html`), confirmar que o link "Mostra" aparece na nav entre "Submissões" e "Oficinas".
- Em `_site/.../mostra-audiovisual/index.html`, confirmar que o item "Mostra" da nav tem `aria-current="page"`.
- Em `_site/.../submissoes/index.html`, confirmar o botão "Saiba mais →" no card da Mostra.

- [ ] **Step 6: Commit**

```bash
git add _includes/event-header.njk _includes/event-nav.njk eventos/caminhos-do-contemporaneo/2026/submissoes/index.njk
git commit -m "feat: adicionar Mostra Audiovisual à navegação do evento"
```

---

## Task 6: CSS — grid de 2 colunas, curadoria e passo-card

**Files:**
- Modify: `css/components.css`

- [ ] **Step 1: Adicionar o grid de 2 colunas ao final de `css/components.css`**

```css
/* ─── Grid 2 colunas (eixos, passos) ─────────────────────── */
.event-card-grid--2 {
  grid-template-columns: repeat(2, 1fr);
}
```

- [ ] **Step 2: Adicionar estilos de `.curadoria` ao final de `css/components.css`**

```css
/* ─── Curadoria dentro do card de eixo ───────────────────── */
.curadoria {
  margin-top: auto;
  padding-top: var(--space-16);
  border-top: 1px solid rgba(48, 42, 102, 0.12);
}

.curadoria__label {
  display: block;
  font-family: var(--font-event, 'DM Mono', monospace);
  font-size: 12px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--color-brand-red);
  margin-bottom: var(--space-8);
}

.curadoria__names {
  margin: 0;
  font-size: var(--text-body-size);
  line-height: var(--text-body-line);
  color: rgba(48, 42, 102, 0.72);
}
```

> Nota: `.submissao-card` já usa `display: flex; flex-direction: column;` (components.css ~849), então `margin-top: auto` empurra a curadoria para a base do card alinhando os dois eixos.

- [ ] **Step 3: Adicionar estilos de `.passo-card` ao final de `css/components.css`**

```css
/* ─── Passo (fluxo de inscrição) ─────────────────────────── */
.passo-card {
  position: relative;
  background: var(--color-white);
  border: 1px solid rgba(48, 42, 102, 0.12);
  border-radius: var(--radius-lg);
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: var(--space-12);
}

.passo-card__numero {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: 999px;
  background: var(--color-brand-red);
  color: var(--color-white);
  font-weight: 700;
  font-size: 20px;
}

.passo-card .button {
  margin-top: auto;
  align-self: flex-start;
}
```

- [ ] **Step 4: Adicionar o colapso mobile dos novos grids**

Localizar a regra `.event-card-grid--3 { grid-template-columns: 1fr; }` dentro do `@media (max-width: 767px)` (components.css ~1087) e adicionar `.event-card-grid--2` à mesma regra:

```css
  .event-card-grid--2,
  .event-card-grid--3 {
    grid-template-columns: 1fr;
  }
```

- [ ] **Step 5: Buildar**

Run: `npm run build`
Expected: build sem erro (o Eleventy copia o CSS via passthrough).

- [ ] **Step 6: Verificar no preview**

Run: `npm run start`
Abrir `http://localhost:8080/eventos/caminhos-do-contemporaneo/2026/mostra-audiovisual/`. Verificar:
- Eixos (M2) e passos (M5) em 2 colunas no desktop; curadoria alinhada na base dos cards de eixo.
- Número do passo em círculo vermelho; botões alinhados na base dos passo-cards.
- Em viewport <768px, eixos, passos e coordenação colapsam para 1 coluna.
- Console sem erros.

- [ ] **Step 7: Commit**

```bash
git add css/components.css
git commit -m "feat: estilos da Mostra Audiovisual — grid 2col, curadoria, passo-card"
```

---

## Task 7: Verificação final e revisão visual

**Files:** nenhum (verificação).

- [ ] **Step 1: Build limpo**

Run: `npm run build`
Expected: sem erro.

- [ ] **Step 2: Revisão completa no preview**

Run: `npm run start`
Percorrer a página inteira em desktop e mobile:
- Ordem das seções: M1 ice → M2 pink → M3 red → M4 ice → M5 pink → M6 red.
- Todos os links funcionam: edital (PDF), Even3, Google Forms, mailto.
- Navegação do evento mostra "Mostra" com estado ativo na página.
- A partir de `/submissoes/`, o botão "Saiba mais →" leva à nova página.
- Console limpo; sem imagens quebradas.

- [ ] **Step 3: Verificar acessibilidade básica**

- Cada `<section>` com `aria-labelledby`/`aria-label`.
- Links externos com `rel="noopener noreferrer"`.
- Botão de download com `aria-label`.

- [ ] **Step 4: Commit final (se houver ajustes)**

```bash
git add -A
git commit -m "fix: ajustes finais da página Mostra Audiovisual"
```

(Se não houver ajustes, pular este commit.)

---

## Self-review (cobertura do spec)

- M1 cabeçalho + prazos + edital → Task 1 ✓
- M2 dois eixos + curadoria → Task 2 (conteúdo) + Task 6 (`.curadoria`, grid 2col) ✓
- M3 coordenação → Task 3 ✓
- M4 programação/timeline → Task 3 ✓
- M5 dois passos (Even3 → Google Forms) → Task 4 (conteúdo) + Task 6 (`.passo-card`) ✓
- M6 dúvidas/callout → Task 4 ✓
- Navegação (event-header, event-nav, link em submissões) → Task 5 ✓
- CSS novo (`.event-card-grid--2`, `.curadoria`, `.passo-card`, colapso mobile) → Task 6 ✓
- Responsivo / acessibilidade → Task 6 (preview) + Task 7 ✓

Nomes/classes consistentes entre tasks: `event-card-grid--2`, `curadoria` / `curadoria__label` / `curadoria__names`, `passo-card` / `passo-card__numero` usados de forma idêntica nas Tasks 2/4 (HTML) e Task 6 (CSS).
