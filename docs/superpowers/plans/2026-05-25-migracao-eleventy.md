# Migração para Eleventy — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrar o site estático do LabMAES para Eleventy (11ty), resolvendo os 18 problemas de qualidade identificados na auditoria (fontes, duplicação de HTML, CSS, acessibilidade, SEO e segurança).

**Architecture:** Eleventy como SSG com templates Nunjucks. Partials em `_includes/` eliminam duplicação de header/footer. Dados globais em `_data/site.json`. Output em `_site/` (HTML estático puro, invisível para SEO e leitores de tela).

**Tech Stack:** Node.js 18+, Eleventy 3.x (`@11ty/eleventy`), Nunjucks (`.njk`), Cloudflare Pages

---

## Mapa de arquivos

| Arquivo | Ação | Responsabilidade |
|---|---|---|
| `package.json` | criar | dependências e scripts de build |
| `eleventy.config.js` | criar | configuração do Eleventy |
| `.gitignore` | modificar | ignorar `_site/` e `node_modules/` |
| `implementation-report.json` | remover | arquivo interno sem valor no repo |
| `_data/site.json` | criar | dados globais (nome, url, descrição padrão) |
| `_includes/layout.njk` | criar | esqueleto HTML base: head, meta tags, fontes, scripts |
| `_includes/header.njk` | criar | cabeçalho com logo e navegação principal |
| `_includes/footer.njk` | criar | rodapé com logo, endereço |
| `_includes/event-nav.njk` | criar | navegação interna das páginas do evento |
| `assets/fonts/Thunder-BoldHC.woff2` | criar | fonte Thunder auto-hospedada (formato principal) |
| `assets/fonts/Thunder-BoldHC.otf` | criar | fonte Thunder auto-hospedada (fallback) |
| `css/tokens.css` | modificar | reformatar + adicionar `@font-face` para Thunder |
| `css/components.css` | modificar | desminificar + `:focus-visible` + aria-current + logo + `.section-content` |
| `js/main.js` | modificar | + fechar menu no Esc, clique fora e clique em link |
| `index.njk` | criar (substitui `index.html`) | página inicial |
| `sobre/index.njk` | criar (substitui `sobre/index.html`) | página sobre |
| `contato/index.njk` | criar (substitui `contato/index.html`) | página contato |
| `eventos/.../2026/index.njk` | criar (substitui `.html`) | página do evento |
| `eventos/.../2026/programacao/index.njk` | criar | programação |
| `eventos/.../2026/submissoes/index.njk` | criar | submissões |
| `eventos/.../2026/oficinas/index.njk` | criar | oficinas |
| `eventos/.../2026/anais/index.njk` | criar | anais |
| `_headers` | modificar | + CSP, HSTS, cache para CSS/JS |

---

## Task 1: Limpeza inicial do repositório

**Files:**
- Modify: `.gitignore`
- Delete: `implementation-report.json`

- [ ] **Passo 1: Atualizar .gitignore**

Abrir `.gitignore` e adicionar ao final:

```
# Eleventy output
_site/

# Node
node_modules/

# Brainstorming visual companion (gerado em sessões de trabalho com IA)
.superpowers/
```

- [ ] **Passo 2: Remover arquivo interno**

```bash
git rm implementation-report.json
```

- [ ] **Passo 3: Commit**

```bash
git add .gitignore
git commit -m "chore: limpar repositório e atualizar .gitignore"
```

Saída esperada: `2 files changed` (`.gitignore` modificado, `implementation-report.json` deletado).

---

## Task 2: Inicializar Eleventy

**Files:**
- Create: `package.json`
- Create: `eleventy.config.js`

- [ ] **Passo 1: Criar package.json**

```json
{
  "name": "labmaes-site",
  "version": "1.0.0",
  "description": "Site estático do LabMAES e do Caminhos do Contemporâneo",
  "scripts": {
    "build": "npx @11ty/eleventy",
    "start": "npx @11ty/eleventy --serve"
  },
  "devDependencies": {
    "@11ty/eleventy": "^3.0.0"
  }
}
```

- [ ] **Passo 2: Criar eleventy.config.js**

```js
export default function (eleventyConfig) {
  // Copiar assets estáticos para _site/ sem processar
  eleventyConfig.addPassthroughCopy("assets");
  eleventyConfig.addPassthroughCopy("css");
  eleventyConfig.addPassthroughCopy("js");
  eleventyConfig.addPassthroughCopy("_headers");
  eleventyConfig.addPassthroughCopy("_redirects");

  return {
    dir: {
      input: ".",
      output: "_site",
      includes: "_includes",
      data: "_data",
    },
    // Arquivos e pastas que o Eleventy deve ignorar ao processar
    // (evita processar o próprio output e dependências)
  };
}
```

- [ ] **Passo 3: Adicionar type: module ao package.json**

O `eleventy.config.js` usa `export default` (ES Modules). Adicionar ao `package.json`:

```json
{
  "name": "labmaes-site",
  "version": "1.0.0",
  "type": "module",
  "description": "Site estático do LabMAES e do Caminhos do Contemporâneo",
  "scripts": {
    "build": "npx @11ty/eleventy",
    "start": "npx @11ty/eleventy --serve"
  },
  "devDependencies": {
    "@11ty/eleventy": "^3.0.0"
  }
}
```

- [ ] **Passo 4: Instalar dependências**

```bash
npm install
```

Saída esperada: `added N packages` e criação de `node_modules/` e `package-lock.json`.

- [ ] **Passo 5: Verificar que o build roda**

```bash
npm run build
```

Saída esperada: `[11ty] Wrote 0 files in ...` (zero arquivos por enquanto — ainda não há templates `.njk`). Não deve haver erros.

- [ ] **Passo 6: Commit**

```bash
git add package.json package-lock.json eleventy.config.js
git commit -m "feat: inicializar Eleventy 3.x"
```

---

## Task 3: Adicionar fontes

**Files:**
- Create: `assets/fonts/Thunder-BoldHC.woff2`
- Create: `assets/fonts/Thunder-BoldHC.otf`
- Modify: `css/tokens.css`

- [ ] **Passo 1: Converter Thunder-BoldHC.otf para WOFF2**

O arquivo fonte está em `C:\Users\Windows 10\Downloads\thunder-font\thunder-font\THUNDER\Fonts\OpenType-PS\Thunder-BoldHC.otf`.

**Conversão via Transfonter (recomendado — sem instalação):**
1. Acessar https://transfonter.org
2. Adicionar o arquivo `Thunder-BoldHC.otf`
3. Marcar apenas "WOFF2" em formatos
4. Clicar em "Convert"
5. Baixar o arquivo `.woff2` gerado

- [ ] **Passo 2: Copiar arquivos de fonte para o repositório**

```bash
# Criar diretório
mkdir -p assets/fonts

# Copiar OTF original
cp "C:\Users\Windows 10\Downloads\thunder-font\thunder-font\THUNDER\Fonts\OpenType-PS\Thunder-BoldHC.otf" assets/fonts/Thunder-BoldHC.otf

# Mover WOFF2 convertido (ajustar caminho conforme onde foi salvo o download)
cp "C:\Users\Windows 10\Downloads\Thunder-BoldHC.woff2" assets/fonts/Thunder-BoldHC.woff2
```

- [ ] **Passo 3: Adicionar @font-face ao tokens.css**

Abrir `css/tokens.css` e adicionar no topo do arquivo, antes do `:root {`:

```css
/* ─── Fontes auto-hospedadas ─────────────────────────────── */
@font-face {
  font-family: "Thunder";
  src:
    url("/assets/fonts/Thunder-BoldHC.woff2") format("woff2"),
    url("/assets/fonts/Thunder-BoldHC.otf") format("opentype");
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}
```

- [ ] **Passo 4: Verificar que o build inclui as fontes**

```bash
npm run build
ls _site/assets/fonts/
```

Saída esperada: `Thunder-BoldHC.otf  Thunder-BoldHC.woff2`

- [ ] **Passo 5: Commit**

```bash
git add assets/fonts/ css/tokens.css
git commit -m "feat: adicionar fonte Thunder BoldHC auto-hospedada"
```

---

## Task 4: Reformatar e atualizar CSS

**Files:**
- Modify: `css/tokens.css`
- Modify: `css/components.css`

### tokens.css

- [ ] **Passo 1: Reformatar tokens.css**

Substituir o conteúdo atual de `css/tokens.css` pelo conteúdo abaixo (o `@font-face` do Task 3 já está no topo; aqui reformatamos o `:root`):

```css
/* ─── Fontes auto-hospedadas ─────────────────────────────── */
@font-face {
  font-family: "Thunder";
  src:
    url("/assets/fonts/Thunder-BoldHC.woff2") format("woff2"),
    url("/assets/fonts/Thunder-BoldHC.otf") format("opentype");
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}

/* ─── Tokens globais ─────────────────────────────────────── */
:root {
  /* Cores de marca */
  --color-brand-red: #B10000;
  --color-brand-ice: #F0F0FF;
  --color-brand-blue: #302A66;

  /* Cores de suporte */
  --color-support-orange: #F44F21;
  --color-support-green: #00523C;
  --color-support-pink: #F4BEBE;

  /* Neutros */
  --color-white: #FFFFFF;
  --color-black: #111111;

  /* Semânticos */
  --color-background-default: var(--color-brand-ice);
  --color-background-inverse: var(--color-brand-red);
  --color-text-primary: var(--color-brand-blue);
  --color-text-inverse: var(--color-brand-ice);
  --color-action-primary: var(--color-brand-red);
  --color-action-secondary: var(--color-brand-blue);

  /* Espaçamento */
  --space-8: 8px;
  --space-12: 12px;
  --space-16: 16px;
  --space-24: 24px;
  --space-32: 32px;
  --space-48: 48px;
  --space-64: 64px;
  --space-80: 80px;
  --space-120: 120px;

  /* Bordas arredondadas */
  --radius-sm: 8px;
  --radius-md: 16px;
  --radius-lg: 28px;
  --radius-xl: 36px;
  --radius-pill: 999px;

  /* Layout */
  --container-max: 1280px;
  --desktop-margin: 80px;
  --mobile-margin: 20px;

  /* Tipografia — famílias */
  --font-sans: "Poppins", system-ui, sans-serif;
  --font-display: "Thunder", "Poppins", system-ui, sans-serif;
  --font-event: "DM Mono", "Poppins", monospace;

  /* Tipografia — escalas */
  --text-button-size: 16px;
  --text-button-line: 20px;
  --text-tag-size: 13px;
  --text-tag-line: 16px;
  --text-body-size: 18px;
  --text-body-line: 28px;
  --text-body-large-size: 22px;
  --text-body-large-line: 32px;
  --text-h3-size: 28px;
  --text-h3-line: 36px;
  --text-section-size: 56px;
  --text-hero-size: 88px;
}

/* Escala responsiva */
@media (max-width: 767px) {
  :root {
    --desktop-margin: 20px;
    --text-body-size: 16px;
    --text-body-line: 25px;
    --text-body-large-size: 18px;
    --text-body-large-line: 28px;
    --text-h3-size: 22px;
    --text-h3-line: 30px;
    --text-section-size: 42px;
    --text-hero-size: 54px;
  }
}
```

### components.css

- [ ] **Passo 2: Substituir components.css pelo conteúdo reformatado e atualizado**

Substituir o conteúdo inteiro de `css/components.css`:

```css
/* ─── Reset ──────────────────────────────────────────────── */
* {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  margin: 0;
  font-family: var(--font-sans);
  background: var(--color-background-default);
  color: var(--color-text-primary);
}

a {
  color: inherit;
  text-decoration: none;
}

img {
  display: block;
  max-width: 100%;
}

/* ─── Acessibilidade ─────────────────────────────────────── */
.skip-link {
  position: absolute;
  left: -999px;
  top: 12px;
  z-index: 999;
  background: var(--color-brand-blue);
  color: var(--color-brand-ice);
  padding: 8px 12px;
  border-radius: var(--radius-sm);
}

.skip-link:focus {
  left: 12px;
}

/* Foco visível para navegação por teclado */
:focus-visible {
  outline: 2.5px solid var(--color-brand-red);
  outline-offset: 3px;
  border-radius: var(--radius-sm);
}

/* ─── Layout ─────────────────────────────────────────────── */
.site-page {
  min-height: 100vh;
  background: var(--color-background-default);
}

.container {
  width: min(100% - (2 * var(--desktop-margin)), var(--container-max));
  margin-inline: auto;
}

/* ─── Cabeçalho ──────────────────────────────────────────── */
.site-header {
  background: var(--color-brand-ice);
  padding: 16px var(--desktop-margin);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-24);
}

.logo {
  width: 180px;
  height: auto;
}

/* ─── Navegação principal ────────────────────────────────── */
.site-nav,
.event-nav__row {
  display: flex;
  align-items: center;
  gap: var(--space-12);
}

.site-nav [aria-current="page"] {
  color: var(--color-brand-red);
  font-weight: 700;
}

.mobile-menu-toggle {
  display: none;
  border: 0;
  background: transparent;
  color: var(--color-brand-blue);
  font: 600 16px/20px var(--font-sans);
  cursor: pointer;
}

/* ─── Botões ─────────────────────────────────────────────── */
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 46px;
  padding: 13px 24px;
  border-radius: var(--radius-lg) var(--radius-pill) var(--radius-pill) var(--radius-lg);
  font-size: var(--text-button-size);
  line-height: var(--text-button-line);
  font-weight: 600;
  white-space: nowrap;
  border: 1.5px solid transparent;
  cursor: pointer;
  transition:
    transform 0.16s ease,
    background-color 0.16s ease,
    color 0.16s ease,
    border-color 0.16s ease;
}

.button:hover {
  transform: translateY(-1px);
}

.button--primary {
  background: var(--color-action-primary);
  color: var(--color-text-inverse);
}

.button--secondary {
  background: var(--color-action-secondary);
  color: var(--color-text-inverse);
}

.button--outline {
  background: transparent;
  color: var(--color-brand-blue);
  border-color: var(--color-brand-blue);
}

.button--ghost {
  background: transparent;
  color: var(--color-brand-blue);
}

/* ─── Tags ───────────────────────────────────────────────── */
.tag {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: fit-content;
  min-height: 28px;
  padding: 6px 16px;
  border-radius: var(--radius-pill) var(--radius-sm) var(--radius-pill) var(--radius-sm);
  font-size: var(--text-tag-size);
  line-height: var(--text-tag-line);
  font-weight: 700;
  white-space: nowrap;
}

.tag--red {
  color: var(--color-brand-red);
  border: 1.25px solid var(--color-brand-red);
}

.tag--blue {
  color: var(--color-brand-blue);
  border: 1.25px solid var(--color-brand-blue);
}

/* ─── Seções ─────────────────────────────────────────────── */
.section {
  padding: 72px var(--desktop-margin);
}

.section--ice {
  background: var(--color-brand-ice);
}

.section--pink {
  background: var(--color-support-pink);
}

.section--red {
  background: var(--color-brand-red);
}

.section-title {
  margin: 0;
  font-family: var(--font-display);
  font-size: var(--text-section-size);
  line-height: 1;
  color: var(--color-brand-blue);
}

.section-title--inverse {
  color: var(--color-brand-ice);
}

.section-body {
  margin: 0;
  font-size: var(--text-body-large-size);
  line-height: var(--text-body-large-line);
  color: rgba(48, 42, 102, 0.84);
}

/* Utilitário para espaçamento superior em conteúdo de seção */
.section-content {
  margin-top: var(--space-32);
}

/* ─── Cards de evento ────────────────────────────────────── */
.event-card,
.event-placeholder-card {
  background: var(--color-white);
  border: 1px solid rgba(48, 42, 102, 0.12);
  border-radius: var(--radius-lg);
  padding: 28px;
}

.event-placeholder-card {
  border-color: rgba(177, 0, 0, 0.18);
}

.event-card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
}

/* ─── Callout do evento ──────────────────────────────────── */
.event-callout {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-32);
  width: 100%;
  background: var(--color-brand-red);
  color: var(--color-brand-ice);
  border-radius: var(--radius-xl);
  padding: 36px 40px;
}

.event-callout__content {
  max-width: 840px;
}

.event-callout__title {
  margin: 0 0 24px;
  font-size: 34px;
  line-height: 40px;
  font-weight: 700;
}

.event-callout__body {
  margin: 0;
  font-size: var(--text-body-large-size);
  line-height: var(--text-body-large-line);
  color: rgba(240, 240, 255, 0.88);
}

/* ─── Navegação do evento ────────────────────────────────── */
.event-nav {
  background: var(--color-brand-blue);
  padding: 24px 10px;
}

.event-nav__row {
  justify-content: center;
  gap: var(--space-48);
}

.event-nav--mobile {
  width: 100%;
  overflow-x: auto;
  overflow-y: hidden;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
  background: var(--color-white);
  padding: 14px 20px;
}

.event-nav--mobile::-webkit-scrollbar {
  display: none;
}

.event-nav--mobile .event-nav__row {
  width: max-content;
  gap: 10px;
  justify-content: flex-start;
}

/* ─── Timeline ───────────────────────────────────────────── */
.timeline {
  display: grid;
  gap: var(--space-24);
}

.timeline-item {
  display: grid;
  grid-template-columns: 160px 1fr;
  gap: 28px;
  padding: 28px;
  background: var(--color-white);
  border: 1px solid rgba(48, 42, 102, 0.12);
  border-radius: var(--radius-lg);
}

.timeline-item__date {
  margin: 0;
  color: var(--color-brand-red);
  font-weight: 600;
  font-size: var(--text-h3-size);
  line-height: var(--text-h3-line);
}

/* ─── Rodapé ─────────────────────────────────────────────── */
.site-footer {
  background: var(--color-brand-blue);
  color: var(--color-brand-ice);
  border-radius: var(--radius-lg);
  padding: 40px 48px;
  margin: 24px 10px 10px;
}

/* ─── Responsivo ─────────────────────────────────────────── */
@media (max-width: 767px) {
  .site-header {
    padding: 18px var(--mobile-margin);
  }

  .logo {
    width: 140px;
  }

  .site-nav {
    display: none;
  }

  .mobile-menu-toggle {
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }

  .site-nav[data-open="true"] {
    display: flex;
    position: absolute;
    inset: 64px 20px auto 20px;
    z-index: 20;
    flex-direction: column;
    align-items: stretch;
    gap: 8px;
    padding: 16px;
    background: var(--color-white);
    border: 1px solid rgba(48, 42, 102, 0.12);
    border-radius: var(--radius-lg);
    box-shadow: 0 12px 32px rgba(48, 42, 102, 0.16);
  }

  .site-nav[data-open="true"] .button {
    width: 100%;
  }

  .section {
    padding: 56px var(--mobile-margin);
  }

  .container {
    width: calc(100% - (2 * var(--mobile-margin)));
  }

  .event-callout {
    flex-direction: column;
    align-items: flex-start;
  }

  .event-callout__title {
    font-size: 26px;
    line-height: 32px;
  }

  .event-card-grid {
    grid-template-columns: 1fr;
  }

  .timeline-item {
    grid-template-columns: 1fr;
    gap: 8px;
  }
}
```

- [ ] **Passo 3: Verificar build**

```bash
npm run build
ls _site/css/
```

Saída esperada: `components.css  tokens.css`

- [ ] **Passo 4: Commit**

```bash
git add css/tokens.css css/components.css
git commit -m "style: reformatar CSS e adicionar focus-visible, aria-current, logo responsivo"
```

---

## Task 5: Corrigir main.js

**Files:**
- Modify: `js/main.js`

- [ ] **Passo 1: Substituir main.js**

```js
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector("[data-mobile-menu-toggle]");
  const nav = document.querySelector("[data-site-nav]");
  if (!toggle || !nav) return;

  function closeMenu() {
    nav.setAttribute("data-open", "false");
    toggle.setAttribute("aria-expanded", "false");
  }

  function openMenu() {
    nav.setAttribute("data-open", "true");
    toggle.setAttribute("aria-expanded", "true");
  }

  // Abrir/fechar ao clicar no botão
  toggle.addEventListener("click", () => {
    const isOpen = nav.getAttribute("data-open") === "true";
    isOpen ? closeMenu() : openMenu();
  });

  // Fechar ao pressionar Esc
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && nav.getAttribute("data-open") === "true") {
      closeMenu();
      toggle.focus(); // Devolver foco ao botão para acessibilidade
    }
  });

  // Fechar ao clicar fora do menu
  document.addEventListener("click", (e) => {
    if (
      nav.getAttribute("data-open") === "true" &&
      !nav.contains(e.target) &&
      !toggle.contains(e.target)
    ) {
      closeMenu();
    }
  });

  // Fechar ao clicar em qualquer link dentro da nav
  nav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", closeMenu);
  });
});
```

- [ ] **Passo 2: Verificar build**

```bash
npm run build
ls _site/js/
```

Saída esperada: `main.js`

- [ ] **Passo 3: Commit**

```bash
git add js/main.js
git commit -m "feat: fechar menu mobile no Esc, clique fora e clique em link"
```

---

## Task 6: Criar dados globais e partials

**Files:**
- Create: `_data/site.json`
- Create: `_includes/layout.njk`
- Create: `_includes/header.njk`
- Create: `_includes/footer.njk`
- Create: `_includes/event-nav.njk`

- [ ] **Passo 1: Criar _data/site.json**

```json
{
  "name": "LabMAES",
  "description": "Laboratório de Moda, Artes, Ensino e Sociedade da UDESC CEART.",
  "url": "https://labmaes.com.br"
}
```

- [ ] **Passo 2: Criar _includes/layout.njk**

```html
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% if title == 'LabMAES' %}LabMAES{% else %}{{ title }} | LabMAES{% endif %}</title>
  <meta name="description" content="{{ description or site.description }}">

  <!-- Open Graph (preview em redes sociais e WhatsApp) -->
  <meta property="og:title" content="{% if title == 'LabMAES' %}LabMAES{% else %}{{ title }} | LabMAES{% endif %}">
  <meta property="og:description" content="{{ description or site.description }}">
  <meta property="og:image" content="{{ site.url }}{% if ogImage %}{{ ogImage }}{% else %}/assets/banners/banner-caminhos-desktop.webp{% endif %}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{{ site.url }}{{ page.url }}">

  <!-- Fontes: Poppins e DM Mono via Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=DM+Mono:ital,wght@0,400&display=swap">

  <!-- Estilos -->
  <link rel="stylesheet" href="/css/tokens.css">
  <link rel="stylesheet" href="/css/components.css">

  <!-- Favicon -->
  <link rel="icon" href="/assets/logos/logo-labmaes-vermelho.svg" type="image/svg+xml">
</head>
<body>
  <a class="skip-link" href="#conteudo">Pular para o conteúdo</a>
  {% include "header.njk" %}
  {{ content | safe }}
  {% include "footer.njk" %}
  <script src="/js/main.js"></script>
</body>
</html>
```

- [ ] **Passo 3: Criar _includes/header.njk**

```html
<header class="site-header">
  <a href="/" aria-label="LabMAES">
    <img class="logo" src="/assets/logos/logo-labmaes-vermelho.svg" alt="LabMAES">
  </a>
  <button class="mobile-menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" data-mobile-menu-toggle>Menu</button>
  <nav id="site-nav" class="site-nav" aria-label="Navegação principal" data-site-nav data-open="false">
    <a class="button button--ghost" href="/sobre/"
       {% if page.url == '/sobre/' %}aria-current="page"{% endif %}>Sobre nós</a>
    <a class="button button--ghost" href="/eventos/caminhos-do-contemporaneo/2026/"
       {% if '/eventos/caminhos-do-contemporaneo/2026/' in page.url %}aria-current="page"{% endif %}>Eventos</a>
    <a class="button button--ghost" href="/contato/"
       {% if page.url == '/contato/' %}aria-current="page"{% endif %}>Contato</a>
  </nav>
</header>
```

- [ ] **Passo 4: Criar _includes/footer.njk**

```html
<footer class="site-footer">
  <img class="logo" src="/assets/logos/logo-labmaes-branco.svg" alt="LabMAES">
  <p>Laboratório de Moda, Artes, Ensino e Sociedade · UDESC · CEART</p>
  <p>Avenida Madre Benvenuta, 1907 - Sala 06 DDE DMO<br>Florianópolis - SC</p>
</footer>
```

- [ ] **Passo 5: Criar _includes/event-nav.njk**

```html
<nav class="event-nav event-nav--mobile" aria-label="Navegação do evento">
  <div class="event-nav__row">
    <a class="button button--primary" href="/eventos/caminhos-do-contemporaneo/2026/"
       {% if page.url == '/eventos/caminhos-do-contemporaneo/2026/' %}aria-current="page"{% endif %}>Edição atual</a>
    <a class="button button--primary" href="/eventos/caminhos-do-contemporaneo/2026/programacao/"
       {% if page.url == '/eventos/caminhos-do-contemporaneo/2026/programacao/' %}aria-current="page"{% endif %}>Programação</a>
    <a class="button button--primary" href="/eventos/caminhos-do-contemporaneo/2026/submissoes/"
       {% if page.url == '/eventos/caminhos-do-contemporaneo/2026/submissoes/' %}aria-current="page"{% endif %}>Submissões</a>
    <a class="button button--primary" href="/eventos/caminhos-do-contemporaneo/2026/oficinas/"
       {% if page.url == '/eventos/caminhos-do-contemporaneo/2026/oficinas/' %}aria-current="page"{% endif %}>Oficinas</a>
    <a class="button button--primary" href="/eventos/caminhos-do-contemporaneo/2026/anais/"
       {% if page.url == '/eventos/caminhos-do-contemporaneo/2026/anais/' %}aria-current="page"{% endif %}>Anais</a>
  </div>
</nav>
```

- [ ] **Passo 6: Verificar build**

```bash
npm run build
```

Saída esperada: `[11ty] Wrote 0 files` (ainda sem páginas `.njk`). Sem erros.

- [ ] **Passo 7: Commit**

```bash
git add _data/ _includes/
git commit -m "feat: criar layout base e partials (header, footer, event-nav)"
```

---

## Task 7: Converter páginas para Nunjucks

**Files:**
- Delete + Create: todos os 8 arquivos `.html` → `.njk`

Cada página recebe um bloco de front matter no topo com `layout`, `title` e `description`. O corpo fica só com o `<main>` — sem `<html>`, `<head>`, `<body>`, header, footer ou `<script>`.

- [ ] **Passo 1: Converter index.html → index.njk**

Deletar `index.html`. Criar `index.njk`:

```njk
---
layout: layout.njk
title: LabMAES
description: Laboratório de Moda, Artes, Ensino e Sociedade da UDESC CEART.
---

<main id="conteudo" class="site-page">
  <section class="section section--ice">
    <div class="container">
      <span class="tag tag--red">LABORATÓRIO · UDESC CEART</span>
      <h1 class="section-title">Moda, Artes, Ensino e Sociedade</h1>
      <p class="section-body">Investigações, ações formativas e experiências sensíveis que aproximam universidade, escola, cultura e sociedade.</p>
      <p>
        <a class="button button--primary" href="/sobre/">Conheça o LabMAES</a>
        <a class="button button--outline" href="/eventos/caminhos-do-contemporaneo/2026/">Acesse o 7º Caminhos</a>
      </p>
    </div>
  </section>

  <section class="event-hero" aria-label="7º Caminhos do Contemporâneo">
    <a href="/eventos/caminhos-do-contemporaneo/2026/">
      <picture>
        <source media="(max-width: 767px)" srcset="/assets/banners/banner-caminhos-mobile.webp">
        <img src="/assets/banners/banner-caminhos-desktop.webp" alt="7º Seminário Caminhos do Contemporâneo 2026" width="1440" height="600">
      </picture>
    </a>
  </section>

  <section class="section section--ice">
    <div class="container">
      <span class="tag tag--blue">ATUAÇÃO TRANSDISCIPLINAR</span>
      <h2 class="section-title">Ensino, pesquisa, extensão e publicações</h2>
      <p class="section-body">O LabMAES articula moda, artes, design e educação como campos interdependentes de criação, formação e produção de conhecimento.</p>
      <div class="event-card-grid section-content">
        <article class="event-card">
          <h3>Ensino</h3>
          <p>Atuação da educação básica à pós-graduação, articulando práticas pedagógicas, formação docente e experiências sensíveis de aprendizagem.</p>
        </article>
        <article class="event-card">
          <h3>Pesquisa</h3>
          <p>Investigações em iniciação científica, pós-graduação e grupo de pesquisa, com formações conjuntas e produção coletiva de conhecimento.</p>
        </article>
        <article class="event-card">
          <h3>Extensão</h3>
          <p>Ações educativas em diálogo com a sociedade, com formação continuada e práticas em contextos de ensino não formal.</p>
        </article>
      </div>
    </div>
  </section>
</main>
```

> Nota: `width="1440" height="600"` são valores aproximados do banner — ajustar para as dimensões reais do arquivo se necessário.

- [ ] **Passo 2: Converter sobre/index.html → sobre/index.njk**

Deletar `sobre/index.html`. Criar `sobre/index.njk`:

```njk
---
layout: layout.njk
title: Sobre o LabMAES
description: Conheça o Laboratório de Moda, Artes, Ensino e Sociedade da UDESC CEART — pesquisa, ensino e extensão em moda, artes e educação.
---

<main id="conteudo" class="site-page">
  <section class="section section--ice">
    <div class="container">
      <span class="tag tag--red">EM CONSTRUÇÃO</span>
      <h1 class="section-title">Sobre o LabMAES</h1>
      <p class="section-body">Conteúdo institucional do laboratório a ser consolidado.</p>
    </div>
  </section>
</main>
```

- [ ] **Passo 3: Converter contato/index.html → contato/index.njk**

Deletar `contato/index.html`. Criar `contato/index.njk`:

```njk
---
layout: layout.njk
title: Contato
description: Entre em contato com o LabMAES — Laboratório de Moda, Artes, Ensino e Sociedade da UDESC CEART.
---

<main id="conteudo" class="site-page">
  <section class="section section--ice">
    <div class="container">
      <span class="tag tag--red">EM CONSTRUÇÃO</span>
      <h1 class="section-title">Contato</h1>
      <p class="section-body">Informações de contato e canais oficiais do LabMAES.</p>
    </div>
  </section>
</main>
```

- [ ] **Passo 4: Converter eventos/caminhos-do-contemporaneo/2026/index.html → index.njk**

Deletar o `.html`. Criar `eventos/caminhos-do-contemporaneo/2026/index.njk`:

```njk
---
layout: layout.njk
title: 7º Caminhos do Contemporâneo 2026
description: 7º Seminário Caminhos do Contemporâneo — Criação, tessituras sensíveis e narrativas em movimento. UDESC CEART, agosto de 2026.
---

<main id="conteudo" class="site-page">
  <section class="event-hero">
    <picture>
      <source media="(max-width: 767px)" srcset="/assets/banners/banner-caminhos-mobile.webp">
      <img src="/assets/banners/banner-caminhos-desktop.webp" alt="7º Seminário Caminhos do Contemporâneo 2026" width="1440" height="600">
    </picture>
  </section>

  {% include "event-nav.njk" %}

  <section class="section section--ice">
    <div class="container">
      <span class="tag tag--blue">SOBRE O EVENTO</span>
      <h1 class="section-title">Criação, tessituras sensíveis e narrativas em movimento</h1>
      <p class="section-body">O 7º Seminário Caminhos do Contemporâneo reúne pesquisas, práticas formativas e experiências estéticas em torno da criação em artes, moda e design, dos saberes sensíveis e das narrativas em movimento.</p>
    </div>
  </section>

  <section class="section section--pink">
    <div class="container">
      <div class="event-callout">
        <div class="event-callout__content">
          <h2 class="event-callout__title">Inscrições e submissões</h2>
          <p class="event-callout__body">As inscrições, submissões e chamadas serão organizadas pela plataforma do evento. Algumas informações ainda estão em atualização.</p>
        </div>
        <a class="button button--secondary" href="/eventos/caminhos-do-contemporaneo/2026/submissoes/">Acompanhe as chamadas</a>
      </div>
    </div>
  </section>

  <section class="section section--ice">
    <div class="container">
      <h2 class="section-title">Programação</h2>
      <p class="section-body">As atividades previstas incluem conferências, mesas, mostra audiovisual, exposição, oficinas, comunicações, pôsteres e atividades culturais.</p>
      <div class="timeline section-content">
        <article class="timeline-item">
          <p class="timeline-item__date">19 AGO</p>
          <div>
            <h3>Abertura e conferência</h3>
            <p>Abertura institucional, conferência de abertura, mostra audiovisual, exposição e primeiras mesas temáticas.</p>
          </div>
        </article>
        <article class="timeline-item">
          <p class="timeline-item__date">20 AGO</p>
          <div>
            <h3>Mesas, comunicações e pôsteres</h3>
            <p>Conferência, comunicações orais presenciais, mesas temáticas, oficinas e sessão de pôster digital.</p>
          </div>
        </article>
        <article class="timeline-item">
          <p class="timeline-item__date">21 AGO</p>
          <div>
            <h3>Conferência e encerramento presencial</h3>
            <p>Conferência, mostra audiovisual, mesas temáticas e encerramento das atividades presenciais.</p>
          </div>
        </article>
        <article class="timeline-item">
          <p class="timeline-item__date">22 AGO</p>
          <div>
            <h3>Atividades online</h3>
            <p>Roda de conversa, comunicações orais online e atividade cultural prevista.</p>
          </div>
        </article>
      </div>
    </div>
  </section>
</main>
```

- [ ] **Passo 5: Converter as 4 páginas "em construção" do evento**

Deletar os quatro `.html`. Criar cada `.njk` com o padrão abaixo:

**`eventos/caminhos-do-contemporaneo/2026/programacao/index.njk`:**
```njk
---
layout: layout.njk
title: Programação — 7º Caminhos do Contemporâneo
description: Programação completa do 7º Seminário Caminhos do Contemporâneo 2026.
---

<main id="conteudo" class="site-page">
  {% include "event-nav.njk" %}
  <section class="section section--ice">
    <div class="container">
      <span class="tag tag--red">EM CONSTRUÇÃO</span>
      <h1 class="section-title">Programação</h1>
      <p class="section-body">A programação completa será confirmada nas próximas etapas.</p>
    </div>
  </section>
</main>
```

**`eventos/caminhos-do-contemporaneo/2026/submissoes/index.njk`:**
```njk
---
layout: layout.njk
title: Submissões — 7º Caminhos do Contemporâneo
description: Chamadas e informações de submissão para o 7º Seminário Caminhos do Contemporâneo 2026.
---

<main id="conteudo" class="site-page">
  {% include "event-nav.njk" %}
  <section class="section section--ice">
    <div class="container">
      <span class="tag tag--red">EM CONSTRUÇÃO</span>
      <h1 class="section-title">Submissões</h1>
      <p class="section-body">As chamadas e links de submissão serão atualizados quando a operação acadêmica estiver fechada.</p>
    </div>
  </section>
</main>
```

**`eventos/caminhos-do-contemporaneo/2026/oficinas/index.njk`:**
```njk
---
layout: layout.njk
title: Oficinas — 7º Caminhos do Contemporâneo
description: Oficinas do 7º Seminário Caminhos do Contemporâneo 2026.
---

<main id="conteudo" class="site-page">
  {% include "event-nav.njk" %}
  <section class="section section--ice">
    <div class="container">
      <span class="tag tag--red">EM CONSTRUÇÃO</span>
      <h1 class="section-title">Oficinas</h1>
      <p class="section-body">As oficinas serão divulgadas nas próximas etapas.</p>
    </div>
  </section>
</main>
```

**`eventos/caminhos-do-contemporaneo/2026/anais/index.njk`:**
```njk
---
layout: layout.njk
title: Anais — 7º Caminhos do Contemporâneo
description: Anais do 7º Seminário Caminhos do Contemporâneo 2026.
---

<main id="conteudo" class="site-page">
  {% include "event-nav.njk" %}
  <section class="section section--ice">
    <div class="container">
      <span class="tag tag--red">EM CONSTRUÇÃO</span>
      <h1 class="section-title">Anais</h1>
      <p class="section-body">Os anais serão disponibilizados após o evento.</p>
    </div>
  </section>
</main>
```

- [ ] **Passo 6: Verificar build completo**

```bash
npm run build
find _site -name "*.html" | sort
```

Saída esperada (8 arquivos):
```
_site/contato/index.html
_site/eventos/caminhos-do-contemporaneo/2026/anais/index.html
_site/eventos/caminhos-do-contemporaneo/2026/index.html
_site/eventos/caminhos-do-contemporaneo/2026/oficinas/index.html
_site/eventos/caminhos-do-contemporaneo/2026/programacao/index.html
_site/eventos/caminhos-do-contemporaneo/2026/submissoes/index.html
_site/index.html
_site/sobre/index.html
```

- [ ] **Passo 7: Verificar conteúdo do output**

```bash
# Verificar título da home
grep -o "<title>.*</title>" _site/index.html

# Verificar título de subpágina
grep -o "<title>.*</title>" _site/sobre/index.html

# Verificar meta description
grep "meta name=\"description\"" _site/sobre/index.html

# Verificar Open Graph
grep "og:image" _site/index.html

# Verificar aria-current na nav da página sobre
grep "aria-current" _site/sobre/index.html

# Verificar font Thunder no CSS
grep "@font-face" _site/css/tokens.css

# Verificar :focus-visible no CSS
grep "focus-visible" _site/css/components.css
```

Saídas esperadas:
```
<title>LabMAES</title>
<title>Sobre o LabMAES | LabMAES</title>
<meta name="description" content="Conheça o Laboratório...">
<meta property="og:image" content="https://labmaes.com.br/assets/...">
aria-current="page"
@font-face {
:focus-visible {
```

- [ ] **Passo 7b: Nota sobre lazy loading**

Os banners são as únicas imagens reais do site e ficam acima da dobra (above the fold) — por isso **não** recebem `loading="lazy"` (isso atrasaria a imagem mais importante da página). Quando páginas de conteúdo forem criadas com imagens internas (ex: fotos de palestrantes, galeria), adicionar `loading="lazy"` nessas imagens.

- [ ] **Passo 8: Commit**

```bash
git add index.njk sobre/ contato/ eventos/
git rm index.html sobre/index.html contato/index.html
git rm eventos/caminhos-do-contemporaneo/2026/index.html
git rm eventos/caminhos-do-contemporaneo/2026/programacao/index.html
git rm eventos/caminhos-do-contemporaneo/2026/submissoes/index.html
git rm eventos/caminhos-do-contemporaneo/2026/oficinas/index.html
git rm eventos/caminhos-do-contemporaneo/2026/anais/index.html
git commit -m "feat: converter todas as páginas para Nunjucks com layout, meta tags e aria-current"
```

---

## Task 8: Atualizar _headers

**Files:**
- Modify: `_headers`

- [ ] **Passo 1: Substituir _headers**

```
/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  X-Frame-Options: SAMEORIGIN
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Content-Security-Policy: default-src 'self'; style-src 'self' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; script-src 'self'; connect-src 'self'

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/css/*
  Cache-Control: public, max-age=86400

/js/*
  Cache-Control: public, max-age=86400
```

- [ ] **Passo 2: Verificar que o arquivo aparece no output**

```bash
npm run build
cat _site/_headers
```

Saída esperada: conteúdo idêntico ao arquivo fonte.

- [ ] **Passo 3: Commit**

```bash
git add _headers
git commit -m "feat: adicionar CSP, HSTS e cache de CSS/JS nos headers"
```

---

## Task 9: Verificação final e configuração do Cloudflare Pages

- [ ] **Passo 1: Build limpo de verificação**

```bash
rm -rf _site
npm run build
```

Saída esperada: `[11ty] Wrote 8 files in ...ms` sem erros ou warnings.

- [ ] **Passo 2: Preview local**

```bash
npm start
```

Abrir http://localhost:8080 e verificar:
- [ ] Home carrega com fonte Thunder nos títulos
- [ ] Navegação mobile abre e fecha (botão, Esc, clique fora)
- [ ] Página "Sobre nós" tem "Sobre nós" destacado em vermelho no header
- [ ] Inspetor do navegador → Network → Fonts mostra Thunder carregando de `/assets/fonts/`
- [ ] `<title>` da home é "LabMAES" (sem sufixo)
- [ ] `<title>` de subpágina é "Sobre o LabMAES | LabMAES"

- [ ] **Passo 3: Configurar Cloudflare Pages**

No painel do Cloudflare Pages, editar as configurações do projeto `labmaes-site`:

| Configuração | Valor |
|---|---|
| Build command | `npx @11ty/eleventy` |
| Build output directory | `_site` |
| Environment variable | `NODE_VERSION` = `18` |

- [ ] **Passo 4: Push e verificar deploy**

```bash
git push origin main
```

Acompanhar o deploy no painel do Cloudflare Pages. Aguardar o build completar com sucesso.

- [ ] **Passo 5: Commit final de documentação**

```bash
git add .
git commit -m "docs: atualizar README com instruções de desenvolvimento local" 
```

Atualizar o `README.md` com:

```markdown
# LabMAES site

Site estático do LabMAES e do 7º Caminhos do Contemporâneo, gerado com Eleventy.

## Desenvolvimento local

Pré-requisitos: Node.js 18+

```bash
npm install
npm start        # preview em http://localhost:8080
npm run build    # gera _site/
```

## Publicar

Fazer push para `main`. O Cloudflare Pages executa o build automaticamente.
Build command: `npx @11ty/eleventy` · Output: `_site`

## Editar páginas

Cada página é um arquivo `.njk` na raiz ou nas subpastas.
O cabeçalho (front matter) de cada página define:
- `title` — título da página
- `description` — texto para Google e redes sociais

Header, footer e navegação do evento ficam em `_includes/` — editar lá afeta todas as páginas.
```
