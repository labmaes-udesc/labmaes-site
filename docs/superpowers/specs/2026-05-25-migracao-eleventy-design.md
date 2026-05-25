# Migração para Eleventy — Design Spec

**Data:** 2026-05-25  
**Status:** Aprovado  
**Repositório:** https://github.com/labmaes-udesc/labmaes-site

---

## Contexto

O site estático do LabMAES e do 7º Caminhos do Contemporâneo foi construído como HTML puro por praticidade inicial. Uma auditoria identificou 18 problemas divididos em três categorias:

- **4 críticos:** fontes não carregadas, header/footer duplicado em 8 arquivos, CSS semi-minificado, sem foco visível para teclado
- **8 atenção:** sem estado ativo na nav, meta tags ausentes em 5 páginas, sem favicon, menu mobile incompleto, títulos inconsistentes, estilos inline, headers de segurança faltando, imagens sem lazy load
- **6 melhorias:** tokens.css em uma linha, font-display swap, logo sem CSS responsivo, cache faltando em CSS/JS, arquivo interno no repo, menu não fecha ao clicar em link

A abordagem escolhida é migrar para **Eleventy (11ty)** como gerador de site estático, resolvendo todos os 18 problemas de forma estruturada.

---

## Decisões de Arquitetura

### Por que Eleventy

- Gera **HTML estático puro** no output — SEO e leitores de tela não percebem diferença
- Templates em Nunjucks são quase HTML normal — editáveis por equipe não-técnica com suporte de IA
- Cloudflare Pages já suporta o build nativamente (plano gratuito, 500 builds/mês)
- Zero custo financeiro (open source, MIT)

### Fontes

- **Thunder:** auto-hospedada em `assets/fonts/`. Usar peso **BoldHC** — único peso usado nos títulos de seção. O arquivo `Thunder-BoldHC.otf` está disponível localmente em `Downloads/thunder-font/`. Converter para WOFF2 usando a ferramenta online [Transfonter](https://transfonter.org) ou o pacote npm `woff2` — o WOFF2 é o formato principal, o OTF fica como fallback.
- **Poppins:** Google Fonts via `<link rel="preconnect">` + `<link rel="stylesheet">` (pesos 400, 600, 700)
- **DM Mono:** Google Fonts, mesmo método (peso 400)

---

## Estrutura de Arquivos

```
labmaes-site/
├── package.json                        # novo — @11ty/eleventy
├── package-lock.json                   # gerado pelo npm install
├── eleventy.config.js                  # novo — configuração do build
├── _headers                            # modificado — + CSP, HSTS, cache CSS/JS
├── _redirects                          # sem mudança
├── .gitignore                          # modificado — + _site/, node_modules/
│
├── _includes/                          # novo diretório
│   ├── layout.njk                      # esqueleto HTML base (head, body, scripts)
│   ├── header.njk                      # partial — cabeçalho do site
│   ├── footer.njk                      # partial — rodapé do site
│   └── event-nav.njk                   # partial — navegação interna do evento
│
├── _data/                              # novo diretório
│   └── site.json                       # nome do site, url base, descrição padrão
│
├── assets/
│   ├── fonts/                          # novo
│   │   ├── Thunder-BoldHC.woff2        # convertido do OTF para web
│   │   └── Thunder-BoldHC.otf          # fallback
│   ├── logos/                          # sem mudança
│   ├── banners/                        # sem mudança
│   ├── graphics/                       # sem mudança
│   └── images/                         # sem mudança
│
├── css/
│   ├── tokens.css                      # modificado — reformatado, legível
│   └── components.css                  # modificado — desminificado, :focus-visible,
│                                       #   aria-current styles, logo CSS, sem inline styles
│
├── js/
│   └── main.js                         # modificado — + fechar menu no Esc/fora/link
│
├── index.njk                           # renomeado de index.html
├── sobre/index.njk
├── contato/index.njk
├── eventos/caminhos-do-contemporaneo/2026/index.njk
├── eventos/caminhos-do-contemporaneo/2026/programacao/index.njk
├── eventos/caminhos-do-contemporaneo/2026/submissoes/index.njk
├── eventos/caminhos-do-contemporaneo/2026/oficinas/index.njk
├── eventos/caminhos-do-contemporaneo/2026/anais/index.njk
│
└── _site/                              # gerado pelo build, não commitado
```

**Removidos do repositório:**
- `implementation-report.json`

---

## Templates e Partials

### `_includes/layout.njk`

Layout base herdado por todas as páginas via front matter (`layout: layout.njk`). Contém:

```html
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ title }} | LabMAES</title>
  <meta name="description" content="{{ description or site.description }}">
  <!-- Open Graph -->
  <meta property="og:title" content="{{ title }} | LabMAES">
  <meta property="og:description" content="{{ description or site.description }}">
  <meta property="og:image" content="{{ site.url }}{{ ogImage or '/assets/banners/banner-caminhos-desktop.webp' }}">
  <meta property="og:type" content="website">
  <!-- Fontes -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=DM+Mono:wght@400&display=swap">
  <link rel="stylesheet" href="/css/tokens.css">
  <link rel="stylesheet" href="/css/components.css">
  <link rel="icon" href="/assets/logos/favicon.svg" type="image/svg+xml">
</head>
<body>
  {% include "header.njk" %}
  {{ content | safe }}
  {% include "footer.njk" %}
  <script src="/js/main.js"></script>
</body>
</html>
```

### Front matter por página

Cada página `.njk` declara suas próprias variáveis:

```yaml
---
layout: layout.njk
title: Sobre o LabMAES
description: Conheça o Laboratório de Moda, Artes, Ensino e Sociedade da UDESC CEART.
---
```

A página `index.njk` (home) usa `title: LabMAES` para que o `<title>` fique apenas "LabMAES" sem o sufixo " | LabMAES". O layout usa:

```html
<title>{% if title == 'LabMAES' %}LabMAES{% else %}{{ title }} | LabMAES{% endif %}</title>
```

### `aria-current` automático

O `header.njk` usa `page.url` do Eleventy para marcar a página ativa:

```html
<a class="button button--ghost" href="/sobre/"
   {% if page.url == '/sobre/' %}aria-current="page"{% endif %}>
  Sobre nós
</a>
```

### `_data/site.json`

```json
{
  "name": "LabMAES",
  "description": "Laboratório de Moda, Artes, Ensino e Sociedade da UDESC CEART.",
  "url": "https://labmaes.com.br"
}
```

---

## CSS

### `tokens.css` — reformatação
Separar cada grupo de tokens em linhas individuais com comentários de seção. Nenhum valor muda — só legibilidade.

### `components.css` — desminificação e adições

**Adições necessárias:**

1. **`:focus-visible` global** — anel de foco visível em todos os elementos interativos:
```css
:focus-visible {
  outline: 2.5px solid var(--color-brand-red);
  outline-offset: 3px;
  border-radius: var(--radius-sm);
}
```

2. **Estado ativo na navegação:**
```css
.site-nav [aria-current="page"] {
  color: var(--color-brand-red);
  font-weight: 700;
}
```

3. **Logo responsivo:**
```css
.logo {
  width: 180px;
  height: auto;
}
@media (max-width: 767px) {
  .logo { width: 140px; }
}
```

4. **Remover necessidade de inline styles** — adicionar classe utilitária `.section-content` com `margin-top: var(--space-32)` para substituir os dois casos de `style="margin-top:32px"` no HTML.

### `_headers` — segurança e cache

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

---

## JavaScript — `main.js`

Adições ao comportamento existente do menu mobile:

1. **Fechar ao pressionar Esc:**
```js
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && nav.getAttribute('data-open') === 'true') {
    closeMenu();
  }
});
```

2. **Fechar ao clicar fora:**
```js
document.addEventListener('click', (e) => {
  if (!nav.contains(e.target) && !toggle.contains(e.target)) {
    closeMenu();
  }
});
```

3. **Fechar ao clicar em link da nav:**
```js
nav.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', closeMenu);
});
```

Extrair lógica de fechar para função `closeMenu()` reutilizada pelos três casos.

---

## Imagens

- Adicionar `loading="lazy"` nas imagens que não são above the fold (banner na home é acima da dobra — manter sem lazy; imagens de conteúdo interno recebem lazy)
- Adicionar `width` e `height` explícitos no elemento `<picture>` do banner para prevenir CLS
- Favicon: usar `logo-labmaes-vermelho.svg` existente como `favicon.svg` referenciado no layout

---

## Workflow de deploy

| Etapa | Comando |
|---|---|
| Preview local | `npx @11ty/eleventy --serve` |
| Build manual | `npx @11ty/eleventy` |
| Publicar | `git commit + git push origin main` |
| Build automático | Cloudflare Pages detecta o push |

**Configuração no Cloudflare Pages:**
- Build command: `npx @11ty/eleventy`
- Build output directory: `_site`
- Node.js version: 18 ou superior (via variável de ambiente `NODE_VERSION=18`)

---

## O que NÃO muda

- Design visual (cores, tipografia, componentes) — nenhuma alteração
- Estrutura de URLs — todas as rotas permanecem idênticas
- Imagens e assets — apenas movimentação dos arquivos de fonte
- `_redirects` — sem mudança
- Hospedagem no Cloudflare Pages — apenas atualização da config de build
