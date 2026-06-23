# Programação rica — 7º Caminhos do Contemporâneo

Design da nova apresentação da página de programação (`/eventos/caminhos-do-contemporaneo/2026/programacao/`), agora que existem ementas, participantes (conferencistas, palestrantes, ministrantes, mediadores, curadores), mini-currículos e fotografias.

- **Data:** 2026-06-18
- **Branch:** `feat/programacao-rica`
- **Fonte do conteúdo:** `ementas_programacao_7o_caminhos (1).docx` (31 atividades, dias 19–22/08/2026)

## Problema

A página atual é uma agenda cronológica enxuta: tipo, título, horário, local e modalidade por bloco, sem ementas nem pessoas. O conteúdo agora é denso — ementas longas, mesas com vários participantes (alguns com título individual de fala), e muitas pessoas que se repetem entre atividades. A agenda enxuta não comporta isso sem virar uma parede de texto, e os campos ainda incompletos ("a definir", sem bio, sem foto) não podem parecer quebrados.

## Objetivo

Uma **experiência integrada** em que a agenda é a espinha dorsal e o detalhe (ementa + participantes) é acessível a partir dela, na mesma página. Os nomes dos participantes públicos ficam visíveis já na capa de cada card; ementa, fotos e mini-currículos aparecem ao expandir.

## Decisões

1. **Acesso ao detalhe: expansão inline (acordeão).** A agenda continua escaneável (cards colapsados); cada card abre no lugar revelando ementa e participantes. Mantém uma jornada só, é robusto em site estático e lida bem com campos vazios.
2. **Nomes na capa do card.** O card colapsado mostra os nomes dos participantes públicos. A expansão acrescenta o que não cabe na capa.
3. **Sem vitrine de convidados no topo.** Os nomes nos cards bastam; não há faixa/galeria separada de conferencistas.
4. **"Responsável" é dado interno** — nunca vai ao ar. Os cards mostram apenas os participantes públicos (conferencistas, palestrantes, ministrantes, mediadores, curadores, coordenação quando pública).
5. **Oficinas e Mostra Audiovisual** aparecem na linha do tempo como as demais atividades (ementa + pessoas na expansão), com um link **"ver inscrição e materiais →"** apontando para as páginas dedicadas (`/2026/oficinas/` e `/2026/mostra-audiovisual/`), que continuam sendo o lugar das regras e da logística. Sem duplicar o texto pesado de inscrição.
6. **Coffee Break** entra como rótulo simples ("Coffee Break"), **sem expansão, ementa ou participantes** — a organização ainda está em aberto. Estruturado de modo a virar um card completo depois, sem retrabalho.
7. **Fotos:** fallback padrão é **círculo de iniciais colorido**. Quando a foto chega, substitui as iniciais sem mexer no resto. Fotos vêm aos poucos (6 disponíveis hoje no Drive do organizador, a serem baixadas para o repositório).
8. **Branch nova** (`feat/programacao-rica`); a `main` não é tocada até o resultado ser aprovado renderizado localmente.

## Arquitetura de dados

Hoje a programação é HTML escrito à mão. Passa a ser **orientada a dados**, com duas fontes normalizadas em `_data/`:

### `_data/pessoas.json`

Cada pessoa aparece **uma vez**, indexada por *slug*. Bios e fotos mantidas num único ponto, reaproveitadas em todas as atividades que a pessoa integra (ex.: Valdecir Babinski aparece em 4 atividades, Andrei Galkowski em 3, Mara Rúbia em várias).

Campos por pessoa:

- `slug` — identificador (ex.: `mario-barro`, `monica-fantin`)
- `nome` — nome com titulação como deve aparecer (ex.: "Prof. Dr. Mario Barro Hérnandez")
- `instituicao` — sigla/instituição (ex.: "UNAM"), opcional
- `bio` — mini-currículo; **omitido se "a definir" ou vazio**
- `foto` — nome do arquivo em `assets/img/convidados/` (ex.: `mario-barro.webp`); **opcional** — ausente → iniciais

### `_data/programacao.json`

Os 4 dias e suas atividades em ordem cronológica. Cada atividade referencia pessoas pelo *slug* e declara o papel **naquela** atividade.

Campos por atividade:

- `dia` (data) e agrupamento por dia (19, 20, 21, 22 ago 2026)
- `hora` — texto livre (ex.: "10h–12h", "17h30–19h")
- `tipo` — categoria/tag (ver taxonomia abaixo)
- `titulo` — título/tema; omitido quando "a definir"
- `modalidade` — `presencial` | `online` | `hibrido`
- `local` — texto livre (ex.: "Auditório", "Zoom – transmissão no ESPINE"); opcional
- `ementa` — texto; **omitido se "a definir" ou vazio**
- `participantes` — lista de `{ slug, papel?, titulo_fala? }`, onde `papel` é opcional (ex.: "mediador", "curadoria", "coordenação") e `titulo_fala` é o título da fala individual em mesas (coluna "Título" do documento), também opcional
- `paralela_com` (ou agrupamento) — para atividades simultâneas exibidas lado a lado (mesas/oficinas paralelas)
- `expansivel` — `false` para Coffee Break; `true` (padrão) para as demais
- `link` — opcional, `{ texto, href }` para "ver inscrição e materiais →" (oficinas, mostra)

*Alternativa considerada e descartada:* um único `programacao.json` com as pessoas embutidas em cada atividade — mais fácil de bater o olho num arquivo só, mas obriga a reescrever a mesma bio em vários lugares. A versão normalizada vence pela manutenção: preencher uma bio "a definir" ou encaixar uma foto é uma edição única que se propaga.

## Estrutura da página

Mantém o enquadramento atual: `layout.njk`, `event-header.njk`, cabeçalho da página (P1) e faixas por dia (19→22) alternando `section--ice`/`section--pink`. Dentro de cada dia, a lista de atividades em ordem de horário, gerada por loop Nunjucks sobre os dados. Atividades simultâneas continuam agrupadas no bloco "paralelo" (como hoje), agora também expansíveis.

### Taxonomia de tipos (tags)

Abertura · Conferência · Exposição · Mediação · Mostra · Mesa Temática · Coffee Break · Oficina · Comunicações Orais · Pôster · Cultural (apresentação musical, desfile) · Roda de Conversa · Encerramento. Reaproveitar as classes de tag existentes (`tag--red`, `tag--blue` etc.) e `modality-tag--presencial/online/hibrido`.

## Anatomia do card

**Fechado:**
- faixa de horário
- tag do tipo
- título/tema (omitido quando "a definir")
- nomes dos participantes públicos
- tag de modalidade + local
- chevron indicando que expande

**Aberto (acrescenta):**
- ementa (quando houver)
- lista de participantes: foto **ou** iniciais coloridas · nome · instituição · papel (quando houver) · mini-bio (quando houver) · título da fala individual (quando houver)
- oficinas/mostra: link "ver inscrição e materiais →" para a página dedicada

## Comportamento e casos de borda

- **Acordeão acessível em JS leve:** botão com `aria-expanded`, controla a região de detalhe. Em `js/main.js` ou módulo dedicado.
- **Degradação sem JS:** sem JavaScript, todos os detalhes ficam visíveis (HTML estático continua completo e legível).
- **Campos vazios não renderizam:** "a definir"/vazio em ementa, bio, foto, título, papel ou local simplesmente não geram markup — nada de placeholders.
- **Foto:** ausente → iniciais coloridas (cor derivada de forma estável a partir do slug/nome); presente → `<img>` WebP otimizado de `assets/img/convidados/`, com `alt` = nome e `loading="lazy"`.
- **Coffee Break:** renderiza só o rótulo, sem chevron, sem região expansível.

## Estilo

Reaproveitar tokens e componentes CSS existentes (`tokens.css` / `components.css`): tags, modality-tags, faixas de seção, `container`, `schedule-day`. Adicionar estilos novos só para: estado expansível do card, lista de participantes (avatar/iniciais + bio) e o link de inscrição. Seguir os padrões visuais das páginas `oficinas` e `mostra-audiovisual`.

## Entrega

- Toda a implementação na branch `feat/programacao-rica`.
- Validar renderização local (`npx @11ty/eleventy --serve`) antes de qualquer merge para `main`.
- As 6 fotos disponíveis entram em `assets/img/convidados/` (otimizadas para WebP), nomeadas por slug; as demais entram à medida que chegarem, sem alteração estrutural.

## Fora de escopo

- Galeria/página separada de convidados.
- Refatorar as páginas `oficinas` e `mostra-audiovisual` para também lerem dos novos dados (elas permanecem como estão; a programação apenas linka para elas).
- Conteúdo do Coffee Break (ementa/participantes), enquanto a organização não fecha.
- Regenerar PDFs de editais.
