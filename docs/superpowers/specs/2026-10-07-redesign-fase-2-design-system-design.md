# Spec — Redesign Fase 2: Design system

**Status:** Aprovada no brainstorming, aguardando plan
**Data:** 2026-10-07
**Dependência:** Fase 1 concluída (gate #23, PR #96).
**Issue:** #24

## Objetivo

Criar do zero o design system do site do LabMAES, sem herdar o CSS e os componentes atuais,
tendo como única regra visual o Manual de Marca do laboratório. O resultado é um catálogo em
HTML que é a fonte da verdade, publicado junto do site e consumido diretamente por ele.

## Escopo

- fundamentos visuais (cor, tipografia, forma, matéria, espaçamento, movimento);
- direção de arte das imagens geradas por IA;
- seis telas-chave e a home mobile, do mock ao HTML;
- catálogo `design-system.html` extraído das telas;
- integração com o Eleventy (publicação do catálogo, macros, layout v2);
- testes de sincronia e de acessibilidade na CI.

## Fora de escopo

- migrar páginas públicas para o novo sistema (Fases 3, 4 e 5);
- remover o `css/` e o `js/` atuais (Fase 7);
- textos das páginas e a declaração de uso de IA (Fase 3);
- modo escuro (só fica preparado);
- mocks das páginas Equipe/Pessoa e Contato, que serão montadas com os componentes;
- auditoria manual com leitor de tela (Fase 7, ADR 0005).

## 1. Conceito

### 1.1 Estrutura e matéria

O sistema tem duas camadas, que vêm das ideias de bloco de montar e de massinha de modelar:

- **Estrutura**: grid, módulos, encaixe, regra. Garante ordem, previsibilidade e
  acessibilidade, e predomina onde se lê e se busca.
- **Matéria**: massinha, papel, blocos de montar e tecido. Traz gesto, textura e volume, e
  traduz a estratégia dos saberes sensíveis.

Os quatro materiais têm **peso igual**. Nenhum deles representa uma área: Moda, Artes,
Ensino e Sociedade são tratadas de modo igual e transdisciplinar.

### 1.2 Manual de Marca como regra

Valem a paleta oficial, a Poppins como fonte principal, a Thunder como secundária e o
vocabulário modular (quadrado de canto arredondado, quarto de círculo, arco). O manual não é
reproduzido peça por peça; seus princípios são traduzidos para o meio digital.

O Caminhos do Contemporâneo continua como submarca, com tipografia e acentos próprios
(seção 2.6).

### 1.3 Intensidade

A dose de matéria é um parâmetro do sistema, aplicado por contexto com o atributo
`data-intensity`:

| Nível | Onde | O que entra |
|---|---|---|
| 1 | Repositório, leitura longa, página de item | Módulos chapados, grão leve de papel, no máximo um acento de matéria |
| 2 | Institucionais, eventos, 404 | Hero com uma composição de matéria contida |
| 3 | Home (só em toques sobre a base do nível 2) | Hero com vários materiais equilibrados e movimento mais presente |

Em todos os contextos, os pontos de interação têm volume sutil e "afundam" quando
pressionados (seção 2.5).

As calibragens que levaram a essa tabela estão em
`../redesign-fase2-referencias/2026-10-07-14-16-nivel-{1-sutil,2-medio,3-alto}.png`, fora do
repositório.

## 2. Fundamentos

### 2.1 Cor

Só a paleta do manual, num único tema claro. Os tokens semânticos ficam organizados para que
um modo escuro possa ser acrescentado depois sem retrabalho.

| Cor | Hex | Papel |
|---|---|---|
| Azul | `#302A66` | Texto, links, ações |
| Vermelho | `#B10000` | Texto, links, ações |
| Verde | `#00523C` | Texto, links, ações |
| Laranja | `#F44F21` | Matéria, formas, títulos muito grandes (contraste ≈ 3:1 sobre o gelo: nunca em texto comum) |
| Rosa | `#F4BEBE` | Superfícies e decoração, nunca em texto |
| Gelo | `#F0F0FF` | Fundo de papel |

A cor **não codifica significado**. Cada tipo de conteúdo (projeto, produção, evento,
pessoa, documento) tem só um pequeno ícone modular colorido, sempre acompanhado de rótulo. A
cor nunca é o único meio de identificar algo (WCAG 1.4.1).

### 2.2 Tipografia

| Família | Uso |
|---|---|
| Poppins | Interface, títulos e leitura longa. Na leitura longa, corpo maior e entrelinha mais generosa. |
| Thunder | Só títulos de impacto (home e aberturas), depois de confirmada a licença para web. |
| Poppins Black | Substitui a Thunder se a licença não for confirmada. |
| Cormorant Garamond + DM Mono | Só nas páginas da submarca Caminhos (seção 2.6). |

Os tamanhos são fluidos com `clamp()` e incluem um breakpoint de tablet (absorve a #27).
Nenhum texto traduzível usa `white-space: nowrap` (absorve a regra da #28).

**Pendência obrigatória:** o repositório tem `assets/fonts/Thunder-BoldHC.*` sem arquivo de
licença. A licença para web precisa ser confirmada antes que a Thunder entre no catálogo.

### 2.3 Forma

O vocabulário é o do manual: quadrado de canto arredondado, quarto de círculo e arco. Os
raios dos componentes e os ícones modulares derivam desses módulos. O grid é modular, como
uma base de montar.

### 2.4 Matéria

A matéria aparece em duas técnicas:

- **imagens geradas por IA**, só na camada expressiva (heroes, aberturas de seção, estados
  vazios, 404), seguindo o guia da seção 3;
- **código**, na camada sistêmica: grão de papel no fundo, volume dos botões, módulos
  chapados e movimento.

### 2.5 Movimento e interação

Princípios adaptados da filosofia de design engineering de Emil Kowalski para o nosso stack
(CSS puro; JavaScript e Web Animations API só quando necessário).

**Onde há movimento.** Mais presente no hero da home; nas outras páginas, só no hero e nos
pontos de interação. O movimento nunca atrasa a navegação nem bloqueia conteúdo.

**A frequência decide.**

| Frequência | Exemplos | Decisão |
|---|---|---|
| O tempo todo | Filtros e busca do repositório, paginação, menu aberto pelo teclado | Sem animação |
| Muitas vezes | Hover em cards e links | Mínima: cor ou sombra, cerca de 150 ms |
| De vez em quando | Menu mobile, acordeões da programação, avisos | Padrão: 200–250 ms |
| Raramente | Hero da home, 404, primeira visita | Pode ter prazer: a matéria "se assenta", com cascata leve |

Ações iniciadas pelo teclado nunca são animadas.

**Tokens de movimento** (Foundations do `styles.css`):

- `--ease-out: cubic-bezier(0.23, 1, 0.32, 1)` para entradas e respostas;
- `--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1)` para deslocamentos na tela;
- `ease-in` não é usado;
- durações: pressionar 120–160 ms, tooltip 150 ms, menus e acordeões 200–250 ms, nada de
  interface acima de 300 ms (só o hero da home pode passar disso);
- a saída é mais rápida que a entrada;
- cascatas com 30–80 ms entre itens, sem bloquear a interação.

**Pressionar.** Elementos pressionáveis vão a `scale(0.97)` e reduzem a sombra de volume. Nada
entra a partir de `scale(0)`: a entrada mais forte começa em `scale(0.95)` com opacidade zero.
O hover que muda forma só existe em `@media (hover: hover) and (pointer: fine)`.

**Desempenho.** Só se animam `transform`, `opacity` e `clip-path`. Tudo o que pode ser
acionado repetidamente usa transições (interrompíveis), não keyframes. Entradas usam
`@starting-style`. As imagens de matéria do hero se revelam com `clip-path` ao entrar na tela,
uma única vez.

**Personalidade.** Elasticidade leve (bounce de 0,1 a 0,2) só nas peças decorativas do hero
da home e da 404. Componentes funcionais não têm bounce.

**Movimento reduzido.** Com `prefers-reduced-motion: reduce`, saem deslocamentos, escala e
cascatas; ficam as transições de opacidade e cor que ajudam a entender a mudança de estado.

**Revisão.** Toda animação do catálogo é revista em câmera lenta (duração ×3 a ×5) e de novo
no dia seguinte, antes da aprovação.

### 2.6 Submarca Caminhos

A submarca é uma camada de tema, `data-brand="caminhos"`, que troca só a tipografia
(Cormorant Garamond + DM Mono) e os acentos de cor do evento. Os componentes são os mesmos;
não há fork.

## 3. Direção de arte das imagens geradas

**Uso.** Só a camada expressiva. Fotos de pessoas, registros de eventos e acervo continuam
sendo fotografias reais.

**Guia**, documentado no catálogo (Foundations → Matéria):

1. **Prompt-mestre fixo**, com:
   - o vocabulário da matéria: massinha fosca com marcas de dedo, papel de algodão
     levemente amassado, blocos de montar foscos, tecido de trama visível;
   - os seis hexadecimais da paleta;
   - luz difusa vinda de cima à esquerda, sombra curta e suave, câmera frontal ou em 30°;
   - fundo de papel gelo;
   - proibições: brilho plástico, cores fora da paleta, letras e logos inventados, mãos ou
     pessoas.
2. **Imagens-âncora:** de 3 a 5 imagens tiradas da primeira composição aprovada da home. São
   passadas como `--input-image` em toda geração nova.
3. **Parâmetros fixos:** Nano Banana Pro (`google/gemini-3-pro-image`) via OpenRouter,
   geração em 2K, depois recorte e exportação para WebP em tamanhos responsivos. Trocar de
   modelo exige regerar as âncoras e registrar um ADR.
4. **Checklist de aprovação:**
   - paleta conferida com conta-gotas;
   - nenhum texto ou logo inventado;
   - os quatro materiais equilibrados no conjunto;
   - luz e ângulo iguais aos das âncoras;
   - texto da interface só sobre área lisa;
   - peso dentro do orçamento.
5. **Orçamento de peso:** o hero da home fica abaixo de cerca de 200 KB no mobile, e as outras
   imagens expressivas abaixo de cerca de 120 KB. Tudo em WebP com `srcset`, e só o hero tem
   prioridade de carregamento.
6. **Texto alternativo:** imagens puramente decorativas usam `alt=""`. Quando a composição
   comunica algo (a 404, por exemplo), ganha uma descrição curta.
7. **Log:** cada geração aprovada é registrada (prompt, modelo, imagens de entrada, data,
   custo) em `design-systems/labmaes/assets/materia/log.md`.

**Onde ficam:** as imagens fixas do sistema (heroes das telas-chave, 404, estados vazios)
ficam em `design-systems/labmaes/assets/materia/`. Imagens de páginas específicas criadas
depois seguem o mesmo guia e entram pelo upload do CMS.

## 4. Fluxo de produção

O DS é produzido com as skills de `rtadewald/skills`:

1. `/plan-screen`: planeja cada tela (três propostas com wireframe);
2. `/to-img`: gera o mock aprovado em PNG;
3. `/img-to-html`: recria o mock em HTML, CSS e JS puros, etapa por etapa;
4. `/extract-ds`: extrai o catálogo `design-system.html` (Overview, Foundations, Components,
   Layouts).

As skills são usadas como estão, com três adaptações:

- no `/plan-screen`, o critério de impacto é o deste DS (estrutura e matéria, intensidade por
  contexto, saberes sensíveis), não o de conteúdo para redes sociais;
- no `/to-img`, o modelo padrão `gpt2` é substituído pelos parâmetros da seção 3;
- o `/extract-ds` aceita uma única entrada, então `design-systems/telas/index.html` liga as
  telas e serve de entrada para a extração.

Os gates de aprovação das skills valem integralmente.

### 4.1 Telas e ordem

| Ciclo | Telas | Nível |
|---|---|---|
| 1 | Home desktop | 3 |
| 1 | Home mobile | 3 |
| 1 | Listagem do repositório (Produções, com busca e filtros) | 1 |
| — | **Extração 1** → catálogo v1, ponto de revisão | — |
| 2 | Página de item (uma produção) | 1 |
| 2 | Página institucional (Sobre) | 1–2 |
| 2 | Edição de evento (Caminhos 2026) | 1–2, com `data-brand="caminhos"` |
| 2 | 404 | 2 |
| — | **Extração final** → catálogo completo, fonte da verdade | — |

O ciclo 1 junta os dois extremos para que os fundamentos não fiquem puxados para a matéria
nem para a estrutura. As imagens-âncora saem da home. No ciclo 2, cada tela parte do
`styles.css` do catálogo v1 e só acrescenta o que falta.

### 4.2 Estrutura no repositório

```text
design-systems/
  telas/
    index.html          # liga as telas; entrada do /extract-ds
    01-home/            # saída do /img-to-html: reference.png, wireframe.txt, index.html, assets/
    02-home-mobile/
    03-repositorio/
    04-item/
    05-sobre/
    06-evento/
    07-404/
  labmaes/              # saída do /extract-ds = fonte da verdade
    design-system.html
    styles.css
    interactions.js
    assets/
      materia/          # imagens geradas, âncoras e log.md
      fonts/
```

### 4.3 Regras

- Entre a extração 1 e a extração final, o catálogo não é editado à mão, porque a extração
  final o regenera. Ajustes finos só depois dela.
- Só entram no repositório os mocks aprovados (o `reference.png` de cada tela). As
  alternativas descartadas ficam em `../redesign-fase2-referencias/`, fora do repositório.
- Nenhum token fica em JSON ou outro arquivo paralelo ao `styles.css`.

## 5. Integração com o Eleventy

**Publicação.** O Eleventy ignora `design-systems/**` como fonte de templates e copia
`design-systems/labmaes/` sem transformação para `/design-system/`, com o
`design-system.html` copiado também como `/design-system/index.html`. O catálogo abre em
`/design-system/`, com `noindex` e fora do menu. O CSS e o JS ficam com URL estável:
`/design-system/styles.css` e `/design-system/interactions.js`.

**Layout v2.** `_includes/layout-v2.njk` carrega só o CSS e o JS do DS. As páginas atuais
continuam no `layout.njk` com o `css/` atual. Uma página nunca carrega os dois sistemas.

**Macros.** Cada componente do catálogo tem uma macro Nunjucks em `_includes/ds/`, com o mesmo
markup e as mesmas classes do preview correspondente.

**Teste de sincronia.** `npm run test:ds` (`node --test`, no padrão de `tools/eleventy/`)
verifica que todo `data-component` do catálogo tem uma macro e que a macro renderizada produz
as mesmas classes raiz do preview.

**Migração.** A Fase 2 não altera nenhuma página pública. As páginas migram para o layout v2
nas Fases 3, 4 e 5, e o `css/` e o `js/` antigos são removidos na Fase 7.

## 6. Acessibilidade e testes

Alvo: WCAG 2.2 AA (ADR 0005).

Um job novo no `.github/workflows/ci.yml` roda Playwright com `@axe-core/playwright` contra o
catálogo gerado pelo build:

1. regras WCAG 2.2 A e AA do axe;
2. a mesma checagem com `prefers-reduced-motion: reduce` emulado;
3. viewport de 320 px de largura, falhando se houver rolagem horizontal.

O catálogo mostra cada componente em todos os estados, então o job cobre o sistema inteiro.
As páginas migradas entram na mesma bateria nas fases seguintes.

## 7. Issues

| Issue | Destino |
|---|---|
| #24 | Fecha com esta spec e o plan |
| #26 | Reescrita: header e card saem do catálogo |
| #27 | Absorvida pelas Foundations (seção 2.2) |
| #28 | Regra do DS (seção 2.2); ainda pode ser corrigida no CSS atual |
| #33 | Fechada como substituída pelos mocks PNG e telas em HTML |
| #34 | Atendida pelo `design-system.html` |
| #35 | Atendida pelo job da seção 6 |

Issues novas: licença da Thunder, guia de direção de arte, uma por tela, extração 1, extração
final e integração com o Eleventy.

## 8. Critérios de saída

1. As seis telas e a home mobile estão aprovadas como mock e como HTML.
2. O catálogo saiu da extração final e cobre Foundations (com Matéria e Movimento),
   Components e Layouts, os três níveis de intensidade e `data-brand="caminhos"`.
3. O guia de direção de arte está no catálogo, com 3 a 5 âncoras e o log das gerações.
4. O catálogo está publicado em `/design-system/`; as macros de `_includes/ds/` e o
   `layout-v2.njk` existem; nenhuma página pública foi alterada.
5. `test:ds` e o job de acessibilidade estão verdes na CI.
6. A licença da Thunder está resolvida (confirmada, ou a Poppins Black adotada).
7. As issues foram reorganizadas, e `docs/roadmap.md` e `docs/architecture/README.md` estão
   atualizados.

## 9. Riscos

| Risco | Mitigação |
|---|---|
| A IA se desviar da direção de arte | Âncoras obrigatórias e checklist |
| O catálogo e as macros divergirem | `test:ds` na CI |
| A extração final sobrescrever ajustes | Nenhuma edição manual entre as extrações |
| Custo das gerações | Log com custo por imagem; saldo em 2026-10-07 de cerca de US$ 5,40 no OpenRouter |
| Thunder sem licença para web | Poppins Black como alternativa definida |
