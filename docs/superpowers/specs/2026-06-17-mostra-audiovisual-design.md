# Spec: Página Mostra Audiovisual — 7º Caminhos do Contemporâneo

**Data:** 2026-06-17
**Rota:** `/eventos/caminhos-do-contemporaneo/2026/mostra-audiovisual/`
**Arquivo novo:** `eventos/caminhos-do-contemporaneo/2026/mostra-audiovisual/index.njk`

---

## Objetivo

Criar uma página exclusiva para a Mostra Audiovisual "Narrativas em Movimento" (Edital 03),
respondendo às dúvidas recorrentes sobre a modalidade num único lugar: o que é a Mostra,
quais são os dois eixos/linhas de curadoria, quem coordena e faz a curadoria, a programação
das sessões de exibição e o **novo** processo de submissão em duas etapas (inscrição na Even3
+ submissão da obra via Google Forms).

**Mudança de estrutura:** diferente das outras modalidades (que submetem direto pela Even3),
a Mostra agora separa inscrição no evento (Even3) da submissão da obra (Google Forms).

---

## Abordagem escolhida

**Opção B — Página informativa por blocos temáticos.** Segue a jornada de quem chega com
dúvida e reaproveita o design system e os componentes já existentes no site (mesma lógica
visual de `submissoes` e `programacao`). Sem âncoras internas (descartado por sobreengenharia
para uma página de ~6 seções).

---

## Stack e convenções do projeto

- **Eleventy** (`.njk`). Os arquivos `.html` em `_site/` são build output — **não editar**.
- Frontmatter padrão: `layout: layout.njk`, `title`, `description`.
- Banner + navegação do evento vêm do include `{% include "event-header.njk" %}`.
- Estilos em `css/tokens.css` (tokens) e `css/components.css` (componentes).
- Build/preview local: ver `package.json` (Eleventy `--serve`).

---

## Estrutura de seções

| Seção | Fundo | Conteúdo |
|-------|-------|----------|
| M1 Cabeçalho + prazos | `section--ice` | H1 "Narrativas em Movimento" + intro + aside `prazo-card` + botão baixar edital |
| M2 Eixos (linhas de curadoria) | `section--pink` | 2 cards lado a lado, cada um com público, formato e curadoria |
| M3 Coordenação | `section--red` | 3 cards simples com a comissão coordenadora |
| M4 Programação | `section--ice` | `timeline` com as 4 sessões de exibição |
| M5 Como participar | `section--pink` | 2 passos numerados (Even3 → Google Forms) com CTAs |
| M6 Dúvidas | `section--red` | `event-callout` com e-mail de contato |

---

## Conteúdo por seção

### M1 — Cabeçalho e prazos (`section--ice`, layout `submissoes-header`)

- Tag `tag--red`: `MOSTRA AUDIOVISUAL`
- `<h1 class="section-title">`: **Narrativas em Movimento**
- `<p class="section-body">` (intro, adaptado do edital): "A Mostra Narrativas em Movimento
  convida estudantes da educação básica, estudantes universitários, educadores(as) e a
  comunidade do Brasil e da América Latina a colocar em circulação histórias que conectam
  pessoas, territórios e imaginários por meio do cinema. São aceitos curtas-metragens de
  ficção, experimental e documentário, com até 20 minutos."
- Aside `prazo-card` (tag `PRAZOS`):
  - Inscrições — 30 mai a 30 jun 2026
  - Resultado da seleção — 13 jul 2026
  - Exibições — 19 a 22 ago 2026
- Botão `button--primary`: **Baixar edital ↓** → `/assets/editais/Caminhos_edital_03_MA.pdf` (`download`)

### M2 — Os dois eixos (`section--pink`)

Cabeçalho da seção (tag `EIXOS` + `<h2>` "Linhas de curadoria" + intro curta: "A Mostra
subdivide-se em duas linhas, de acordo com o perfil dos(as) realizadores(as).").

Grid de 2 cards (novo modificador `.event-card-grid--2`). Cada card reutiliza `submissao-card`:

**Card 1 — Cinema Universitário e Comunitário Latino-Americano**
- Tag `tag--blue`: `EIXO 1`
- Descrição: "Obras produzidas por estudantes universitários e pela comunidade (Brasil e
  América Latina). Idade mínima de 18 anos para o(a) responsável pela inscrição."
- Curadoria (lista `.curadoria`): Andrei Galkowski (Udesc) · Mario Barro Hérnandez (UNAM)

**Card 2 — Olhares Sensíveis da Escola**
- Tag `tag--blue`: `EIXO 2`
- Descrição: "Obras produzidas por estudantes da educação básica, devidamente matriculados e
  representados por um(a) professor(a) responsável."
- Curadoria (lista `.curadoria`): Monica Rodrigues (IEMA) · Karine Joulie

### M3 — Coordenação (`section--red`)

- Tag `tag--ice`: `COORDENAÇÃO`
- `<h2 class="section-title section-title--inverse">`: **Comissão Coordenadora**
- Grid `event-card-grid--3` com 3 `event-card` (apenas nomes, sem bio):
  - Mara Rúbia Sant'Anna
  - Monica Rodrigues
  - Andrei Rafael Galkowski

### M4 — Programação (`section--ice`, componente `timeline`)

- Tag `tag--red`: `PROGRAMAÇÃO`
- `<h2 class="section-title">`: **Sessões de exibição**
- `<p class="section-body">`: "As obras selecionadas serão exibidas em duas sessões
  presenciais (UDESC CEART) e duas sessões online, cada uma seguida de debate."
- `timeline` com 4 `timeline-item`:

| Data | Título | Detalhe |
|------|--------|---------|
| 19 AGO | Cinema Universitário e Comunitário Latino-Americano | Presencial · 14h–15h · UDESC CEART |
| 20 AGO | Cinema Universitário e Comunitário Latino-Americano | Online · 14h–15h |
| 21 AGO | Olhares Sensíveis da Escola | Presencial · 14h–15h · UDESC CEART |
| 22 AGO | Olhares Sensíveis da Escola | Online · 14h–15h |

### M5 — Como participar (`section--pink`)

- Tag `tag--red`: `INSCRIÇÕES`
- `<h2 class="section-title">`: **Como participar**
- `<p class="section-body">`: "A participação é gratuita e ocorre em duas etapas. Leia o
  edital antes de iniciar."
- Grid de 2 passos (`.event-card-grid--2`), cada passo um `.passo-card`:

**Passo 1 — Inscrição no evento**
- Número "1" em destaque
- "Acesse a plataforma Even3 e faça sua inscrição gratuita no 7º Seminário Caminhos do
  Contemporâneo. A inscrição no evento é obrigatória antes de submeter a obra."
- Botão `button--secondary`: **Inscrever-se na Even3 ↗** →
  `https://www.even3.com.br/7-seminario-caminhos-do-contemporaneo-744454` (`target="_blank"`, `rel="noopener noreferrer"`)

**Passo 2 — Submissão da obra**
- Número "2" em destaque
- "Após a inscrição, preencha o formulário de submissão e envie: link da obra no YouTube ou
  Vimeo (com acesso liberado ou senha), ficha técnica, sinopse e, quando aplicável,
  comprovante de vínculo estudantil."
- Botão `button--secondary`: **Submeter obra ↗** →
  `https://docs.google.com/forms/d/e/1FAIpQLSd4HN7kAcVyDtVfSlyu4XMrmnPCp5jllsqSWz2Xj0Rv7mpLIg/viewform`
  (`target="_blank"`, `rel="noopener noreferrer"`)

### M6 — Dúvidas (`section--red`, componente `event-callout`)

- `<h2 class="event-callout__title">`: **Dúvidas?**
- `<p class="event-callout__body">`: "Informações adicionais sobre a Mostra podem ser
  obtidas pela Comissão Organizadora pelo e-mail labmaes.ceart@udesc.br."
- Link `mailto:labmaes.ceart@udesc.br` (pode ser inline no corpo ou botão `button--outline-ice`).

---

## Navegação

A página precisa ser descoberta (motivo do projeto: muitas dúvidas). Duas mudanças:

1. **Adicionar item "Mostra" à navegação do evento.** Inserir entre "Submissões" e "Oficinas"
   nos dois includes para manter consistência:
   - `_includes/event-header.njk` (nav usado pelas páginas)
   - `_includes/event-nav.njk` (variante standalone)
   - Seguir o padrão existente, incluindo o teste `aria-current` por `page.url`.

2. **Linkar a partir da página de submissões.** No card "Edital 3: Mostra Audiovisual"
   (`eventos/.../submissoes/index.njk`), adicionar um botão/link "Saiba mais →" apontando
   para a nova página, ao lado do botão de download do edital.

---

## CSS

Reaproveitamento máximo. Componentes já existentes usados sem alteração: `section`,
`section--ice/pink/red`, `container`, `submissoes-header`, `prazo-card`, `prazo-list`,
`prazo-item`, `event-card`, `event-card-grid`, `event-card-grid--3`, `timeline`,
`timeline-item`, `event-callout`, `tag` (variações), `button` (variações), `section-title`,
`section-title--inverse`, `section-body`, `section-content`.

**CSS novo a adicionar ao final de `css/components.css`:**

- `.event-card-grid--2` — `grid-template-columns: repeat(2, 1fr);` (hoje só existe `--3`;
  base é 4 colunas, `linha ~661` do components.css).
  **Importante (verificado):** no `@media (max-width: 767px)` a base `.event-card-grid`
  colapsa para `1fr 1fr` (2 colunas) e só `--3` vai para `1fr`. Portanto `.event-card-grid--2`
  **precisa ser adicionado explicitamente** à regra mobile (`grid-template-columns: 1fr;`),
  junto de `--3`, senão os cards ficam em 2 colunas apertadas no celular.
- `.curadoria` — lista pequena dentro do card do eixo: rótulo "Curadoria" + nomes
  (font-event/DM Mono, cor atenuada). Estilo leve, sem novo "componente" pesado.
- `.passo-card` + `.passo-card__numero` — card de passo com número grande em destaque
  (font-display, brand-red). Pode estender `.event-card`. `__numero` posicionado no topo.

---

## Responsivo

| Breakpoint | Ajuste |
|-----------|--------|
| ≥768px | Eixos e passos em 2 colunas; coordenação em 3 colunas |
| <768px | Todas as grids em 1 coluna; `submissoes-header` empilha texto + aside |

---

## Acessibilidade

- `aria-labelledby` em cada `<section>` apontando para o `<h2>`/`<h1>` correspondente
  (padrão já usado nas páginas existentes).
- `aria-current="page"` no item de nav "Mostra" quando ativo.
- Links externos com `target="_blank"` sempre acompanhados de `rel="noopener noreferrer"`.
- Botão de download do edital com `aria-label` descritivo.

---

## Arquivos a criar/modificar

1. **Criar** `eventos/caminhos-do-contemporaneo/2026/mostra-audiovisual/index.njk` — página completa.
2. **Modificar** `_includes/event-header.njk` — adicionar link "Mostra" na nav.
3. **Modificar** `_includes/event-nav.njk` — adicionar link "Mostra" na nav (consistência).
4. **Modificar** `eventos/caminhos-do-contemporaneo/2026/submissoes/index.njk` — link "Saiba mais →" no card da Mostra.
5. **Modificar** `css/components.css` — adicionar `.event-card-grid--2`, `.curadoria`, `.passo-card`.

---

## Fora de escopo

- Animações novas (a página reaproveita o IntersectionObserver existente para `.event-card`).
- Alteração do fluxo de submissão das outras modalidades (CO e Pôster continuam via Even3).
- Página de resultados/selecionados (será divulgada após 13 jul 2026 — outro ciclo).
- Especificações técnicas finais dos arquivos de exibição (informadas pela organização aos selecionados).

---

## Fonte dos dados

- **Edital 03** (`assets/editais/Caminhos_edital_03_MA.pdf`): eixos, categorias, cronograma,
  documentos exigidos, sessões de exibição, comissão coordenadora.
- **Curadoria por eixo** (informada pela organização, não consta no PDF):
  - Cinema Universitário e Comunitário Latino-Americano: Andrei Galkowski (Udesc), Mario Barro Hérnandez (UNAM)
  - Olhares Sensíveis da Escola: Monica Rodrigues (IEMA), Karine Joulie
- **Link do formulário de submissão (Google Forms):**
  `https://docs.google.com/forms/d/e/1FAIpQLSd4HN7kAcVyDtVfSlyu4XMrmnPCp5jllsqSWz2Xj0Rv7mpLIg/viewform`
