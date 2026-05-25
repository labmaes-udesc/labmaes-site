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
