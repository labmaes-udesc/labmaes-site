# LabMAES site

Site estático do LabMAES e do 7º Caminhos do Contemporâneo, gerado com [Eleventy](https://www.11ty.dev/).

## Desenvolvimento local

Pré-requisitos: Node.js 18+

```bash
npm install
npm start        # preview em http://localhost:8080
npm run build    # gera _site/
```

## Publicar

Fazer push para `main`. O Cloudflare Pages executa o build automaticamente.

- Build command: `npx @11ty/eleventy`
- Output directory: `_site`
- Node.js version: 18 (variável de ambiente `NODE_VERSION=18`)

## Editar páginas

Cada página é um arquivo `.njk` na raiz ou nas subpastas.
O cabeçalho (front matter) de cada arquivo define:

- `title` — título da página (aparece na aba do navegador e no Google)
- `description` — texto para Google e redes sociais

Header, footer e navegação do evento ficam em `_includes/` — editar lá afeta todas as páginas de uma vez.

## Pendências

- **Atualizar o Edital 03 (Mostra Audiovisual)** — `assets/editais/Caminhos_edital_03_MA.pdf`. As cláusulas 2.6 e 2.7 ainda indicam que a inscrição da Mostra é feita pela Even3 ("Modalidade Mostra Audiovisual"). O fluxo mudou para inscrição no evento via Even3 + submissão da obra via Google Forms (refletido na página `/2026/mostra-audiovisual/`). O PDF precisa ser regenerado para evitar novas dúvidas.

### Melhorias mapeadas na análise crítica (2026-07-02)

**Antes da tradução FR/EN (estruturais):**

- **Internacionalização (i18n)** — extrair todo o texto dos templates para arquivos de dados por idioma (`_data/i18n/pt.json`, `fr.json`, `en.json`); estrutura de URLs `/fr/` e `/en/` com PT na raiz; `lang` dinâmico no `<html>`; `hreflang` recíprocos + `x-default`; `og:locale:alternate`; seletor de idioma no header ("Português · Français · English", sem bandeiras); campos multilíngues em `programacao.json`/`pessoas.json` (ex.: `titulo: { pt, fr, en }`).
- **Remover `white-space: nowrap`** de `.button` e `.tag` — textos em francês são 15–25% mais longos e vão estourar o layout. Testar com strings francesas.
- ~~**Auto-hospedar Poppins e DM Mono**~~ — **FEITO (2026-07-03):** Poppins 400/600/700 e DM Mono 400 convertidas para WOFF2 em `assets/fonts/`, declaradas via `@font-face` em `tokens.css`, com preload dos pesos críticos no `layout.njk`. Removido o `<link>` do Google Fonts e os domínios `fonts.googleapis.com`/`fonts.gstatic.com` da CSP (agora `style-src 'self'; font-src 'self'`). Resolve GDPR (CNIL) e elimina o render-blocking de terceiro.
- **Consolidar o CSS**: criar tokens semânticos (`--color-text-muted`, `--color-border`) substituindo os ~40 `rgba(48,42,102,X)` repetidos; unificar os 7 headers decorativos (`.areas-header`, `.modalidades-header`, `.oficinas-header`, `.prog-header`, `.contact-hero`, `.contact-location`, `.oficinas-section-intro`) num componente base; unificar os 7 cards brancos num `.card` base; remover código morto (`_includes/event-nav.njk` e o CSS `.schedule-*` legado, se confirmado que não são usados).

**SEO e assets:**

- **OG image própria do LabMAES** na home (hoje o preview do WhatsApp mostra o banner do Caminhos, não o laboratório) — o mecanismo `ogImage` já existe no layout.
- **Twitter Cards** (`twitter:card: summary_large_image`).
- **Favicons**: `favicon.ico` fallback, `apple-touch-icon`, `theme-color`.
- **Minificação + fingerprint de CSS/JS** — permitiria cache imutável de 1 ano (hoje `no-cache` no `_headers`).

**Acessibilidade e UX:**

- **Alvos de toque ≥44px** nos ícones sociais do rodapé (hoje 24×24px — adicionar padding na âncora).
- **Focus trap** no menu mobile aberto.
- **Chevron do `prog-card` visível no mobile** (hoje `display:none` remove a indicação de que o card expande).
- **"Inscrições ↗"** — envolver a seta em `<span aria-hidden="true">` e indicar que abre em nova aba.
- **Tipografia fluida** com `clamp()` nas escalas display/section + breakpoint tablet (768–1024px, grids de 4 colunas ficam apertados).

**Conteúdo:**

- **Completar as páginas "em construção"** (`/sobre/` e `/anais/`) — a página Sobre é a mais importante para o SEO institucional do laboratório.
