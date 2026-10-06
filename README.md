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

## Validar conteúdo

O conteúdo estruturado do redesign fica em `src/content/` e é editado pelo Pages CMS
(`.pages.yml`). Antes de abrir um PR:

```bash
npm run validate:content
```

A CI roda o build e essa validação em todo pull request.

## Roadmap e tarefas

- [Roadmap do redesign](docs/roadmap.md) — fases 0 a 7 e onde está o detalhe de cada uma.
- [Milestones](https://github.com/labmaes-udesc/labmaes-site/milestones) — uma por fase, mais
  a de manutenção contínua.
- [Issues](https://github.com/labmaes-udesc/labmaes-site/issues) — pendências, bugs e
  melhorias. As que estavam listadas neste README desde 2026-07 viraram issues.
- [Decisões de arquitetura](docs/architecture/README.md) — ADRs, com a ordem de precedência
  entre ADR, spec e plan.

## Contribuir

Leia o [guia de contribuição](CONTRIBUTING.md) e o [código de conduta](CODE_OF_CONDUCT.md).
Falhas de segurança ou exposição de dados pessoais: siga o [SECURITY.md](SECURITY.md), sem
abrir issue pública.

## Licença

Ainda não definida. Até a decisão, o código e o conteúdo não têm licença aberta. A discussão
está na [issue #69](https://github.com/labmaes-udesc/labmaes-site/issues/69).
