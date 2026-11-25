# Spec — Redesign Fase 2: Design system

**Status:** Revisada em 2026-11-24 (brainstorming); o plan de 2026-10-12 precisa ser reescrito
**Data:** 2026-10-07 · **Revisão 1:** 2026-11-24
**Dependência:** Fase 1 concluída (gate #23, PR #96).
**Issue:** #24

## Revisões

**Revisão 1 (2026-11-24).** A versão de 2026-10-07 propunha uma nova linguagem visual,
"estrutura + matéria", com cenas 3D de massinha, papel, blocos e tecido geradas por IA e três
níveis de intensidade. Ao retomar a fase, o usuário julgou ousado demais mudar o branding junto
com o site novo. Decisões desta revisão:

1. **Layout novo, marca igual.** As páginas e os componentes são redesenhados, mas a identidade
   é a do Manual de Marca, 2D e chapada. Saem o par estrutura/matéria e o `data-intensity`.
2. **Textura como detalhe:** grão e trama em CSS e, onde fizer falta, amostras chapadas de
   material geradas por IA, aplicadas dentro dos módulos do manual. Nada de cena 3D.
3. **A skill `design-taste-frontend` constrói as telas**, com uma camada de marca por cima do
   kit dela e uma lista explícita de exceções às suas regras (seção 4.2). Saem o `/to-img` e o
   `/img-to-html`; o `/plan-screen` fica opcional e o `/extract-ds` continua gerando o catálogo.

As seções 1 a 4 foram reescritas; as seções 5 a 10 receberam só os ajustes decorrentes.

## Objetivo

Criar o design system do novo site do LabMAES dentro da marca atual, tendo o Manual de Marca
como regra visual. O CSS e os componentes do site atual não são herdados como código, mas a
identidade que eles expressam é mantida. O resultado é um catálogo em HTML que é a fonte da
verdade, publicado junto do site e consumido diretamente por ele.

## Escopo

- fundamentos visuais (cor, tipografia, forma, textura, espaçamento, movimento);
- guia das texturas e imagens de apoio geradas por IA;
- seis telas-chave e a home mobile, construídas em HTML;
- catálogo `design-system.html` extraído das telas;
- integração com o Eleventy (publicação do catálogo, macros, layout v2);
- testes de sincronia e de acessibilidade na CI;
- aprovação da coordenadora do LabMAES antes de qualquer publicação.

## Fora de escopo

- mudar a marca do LabMAES (logotipo, paleta, tipografia ou vocabulário de formas);
- migrar páginas públicas para o novo sistema (Fases 3, 4 e 5);
- remover o `css/` e o `js/` atuais (Fase 7);
- textos das páginas e a declaração de uso de IA (Fase 3);
- modo escuro (só fica preparado);
- telas das páginas Equipe/Pessoa e Contato, que serão montadas com os componentes;
- auditoria manual com leitor de tela (Fase 7, ADR 0005).

## 1. Conceito

### 1.1 Site novo, mesma marca

O LabMAES ganha um site novo, com a arquitetura de informação das Fases 0 e 1 (repositório de
produções, itens, pessoas, eventos), mas quem o visita reconhece a mesma identidade do site
atual e das peças do laboratório. O visual é **2D e chapado**, como no manual.

A expressão vem do **vocabulário modular** do manual (quadrado de canto arredondado, quarto de
círculo, arco), compondo heroes e aberturas de seção, na linha do cabeçalho decorativo que o
site atual já usa. A **textura entra como detalhe**, em pontos contados (seção 2.4), e nunca
como camada visual própria.

Papel, tecido, massinha e blocos de montar, quando aparecem como textura, têm **peso igual**.
Nenhum deles representa uma área: Moda, Artes, Ensino e Sociedade são tratadas de modo igual e
transdisciplinar, na estratégia dos saberes sensíveis.

### 1.2 Manual de Marca como regra

Valem a paleta oficial, a Poppins como fonte principal, a Thunder como secundária e o
vocabulário modular. O manual não é reproduzido peça por peça; seus princípios são traduzidos
para o meio digital.

O Caminhos do Contemporâneo continua como submarca, com tipografia e acentos próprios
(seção 2.6).

## 2. Fundamentos

### 2.1 Cor

Só a paleta do manual, num único tema claro. Os tokens semânticos ficam organizados para que
um modo escuro possa ser acrescentado depois sem retrabalho.

| Cor | Hex | Papel |
|---|---|---|
| Azul | `#302A66` | Texto, links, ações |
| Vermelho | `#B10000` | Texto, links, ações |
| Verde | `#00523C` | Texto, links, ações |
| Laranja | `#F44F21` | Formas, títulos muito grandes (contraste ≈ 3:1 sobre o gelo: nunca em texto comum) |
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

O vocabulário é o do manual: quadrado de canto arredondado, quarto de círculo e arco. É o
principal recurso expressivo do sistema. Os raios dos componentes e os ícones modulares
derivam desses módulos; os heroes e as aberturas de seção são composições de módulos chapados
na paleta. O grid é modular.

### 2.4 Textura como detalhe

Dois meios, ambos em pontos contados:

- **CSS:** grão leve de papel no fundo e trama sutil, aplicados em poucos lugares (fundo de
  página, uma superfície de destaque). Nunca atrás de texto de leitura longa.
- **IA:** só **amostras chapadas de material**, vistas de cima, sem volume nem perspectiva
  (papel, tecido, massinha, blocos de montar, com peso igual), usadas **dentro de um módulo**
  do manual (por exemplo, um quarto de círculo preenchido com trama de tecido); e imagens de
  apoio 2D onde faltar conteúdo (estados vazios, 404). Guia na seção 3.

Fotos de pessoas, registros de eventos e acervo são sempre fotografias reais. Nenhuma imagem
gerada ou de banco é apresentada como se fosse do laboratório.

### 2.5 Movimento e interação

Princípios adaptados da filosofia de design engineering de Emil Kowalski para o nosso stack
(CSS puro; JavaScript e Web Animations API só quando necessário), somados à camada de hover e
pressão da `design-taste-frontend` (seção 4.2).

**Onde há movimento.** O hero de cada página entra uma única vez ao carregar. Os "momentos" da
skill só valem se forem tipográficos ou feitos com os módulos da marca, e só na home, no Sobre,
na edição de evento e na 404; nunca nas páginas de leitura e busca. O movimento nunca atrasa a
navegação nem bloqueia conteúdo.

**A frequência decide.**

| Frequência | Exemplos | Decisão |
|---|---|---|
| O tempo todo | Filtros e busca do repositório, paginação, menu aberto pelo teclado | Sem animação |
| Muitas vezes | Hover em cards e links | Mínima: cor, sombra ou elevação de 2 px, cerca de 150 ms |
| De vez em quando | Menu mobile, acordeões da programação, avisos | Padrão: 200–250 ms |
| Raramente | Hero, 404, primeira visita | Pode ter prazer: os módulos "se encaixam", com cascata leve |

Ações iniciadas pelo teclado nunca são animadas.

**Tokens de movimento** (Foundations do `styles.css`):

- `--ease-out: cubic-bezier(0.23, 1, 0.32, 1)` para entradas e respostas;
- `--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1)` para deslocamentos na tela;
- `ease-in` não é usado;
- durações: pressionar 120–160 ms, tooltip 150 ms, menus e acordeões 200–250 ms, nada de
  interface acima de 300 ms (só o hero da home pode passar disso);
- a saída é mais rápida que a entrada;
- cascatas com 30–80 ms entre itens, sem bloquear a interação.

**Pressionar.** Elementos pressionáveis vão a `scale(0.97)`. Nada entra a partir de
`scale(0)`: a entrada mais forte começa em `scale(0.95)` com opacidade zero. O hover que muda
forma só existe em `@media (hover: hover) and (pointer: fine)`.

**Desempenho.** Só se animam `transform`, `opacity` e `clip-path`. Tudo o que pode ser
acionado repetidamente usa transições (interrompíveis), não keyframes. Entradas usam
`@starting-style`.

**Personalidade.** Elasticidade leve (bounce de 0,1 a 0,2) só nos módulos decorativos do hero
da home e da 404. Componentes funcionais não têm bounce.

**Movimento reduzido.** Com `prefers-reduced-motion: reduce`, saem deslocamentos, escala e
cascatas; ficam as transições de opacidade e cor que ajudam a entender a mudança de estado.
Nada fica escondido.

**Revisão.** Toda animação do catálogo é revista em câmera lenta (duração ×3 a ×5) e de novo
no dia seguinte, antes da aprovação.

### 2.6 Submarca Caminhos

A submarca é uma camada de tema, `data-brand="caminhos"`, que troca só a tipografia
(Cormorant Garamond + DM Mono) e os acentos de cor do evento. Os componentes são os mesmos;
não há fork.

## 3. Guia das imagens geradas por IA

**Uso.** Só as amostras de textura e as imagens de apoio da seção 2.4. Documentado no catálogo
(Foundations → Textura).

1. **Prompt fixo**, com: amostra de material vista de cima, chapada, sem perspectiva nem
   volume; os seis hexadecimais da paleta; luz plana e uniforme; proibições: brilho,
   perspectiva 3D, sombras projetadas, cores fora da paleta, letras e logos inventados, mãos
   ou pessoas.
2. **Parâmetros fixos:** Nano Banana Pro (`google/gemini-3-pro-image`) via OpenRouter, geração
   em 1K, recorte e exportação para WebP. Trocar de modelo exige registrar um ADR.
3. **Checklist de aprovação:** paleta conferida com conta-gotas; nenhum texto ou logo; sem
   volume nem perspectiva; os quatro materiais equilibrados no conjunto do site; peso dentro
   do orçamento.
4. **Orçamento de peso:** cerca de 60 KB por amostra; imagens de apoio até cerca de 120 KB.
   Nenhuma tem prioridade de carregamento.
5. **Texto alternativo:** texturas usam `alt=""` (ou entram como fundo CSS). Uma imagem de
   apoio que comunica algo (a 404, por exemplo) ganha uma descrição curta.
6. **Log:** cada geração aprovada é registrada (prompt, modelo, data, custo) em
   `design-systems/marca/ia/log.md`.

**Onde ficam:** as imagens do sistema ficam em `design-systems/labmaes/assets/textura/` depois
da extração. Imagens de páginas específicas criadas depois seguem o mesmo guia e entram pelo
upload do CMS.

## 4. Fluxo de produção

### 4.1 Etapas de cada tela

1. **`/plan-screen` (opcional, invocado pelo usuário):** planeja a tela e propõe wireframes.
2. **Construção com a `design-taste-frontend`:** a tela é feita em HTML, CSS e JS com o kit da
   skill e a camada de marca `design-systems/marca/marca.css` (tokens do manual, fontes, raios
   derivados dos módulos, grão e trama), que vem depois do kit e prevalece sobre ele.
3. **Verificação:** rodam os verificadores da skill (`check.mjs`, `consistency.mjs`,
   `perf.mjs`, `copy-lint.mjs`) e o axe. O resultado fica em `verificacao.md` na pasta da tela:
   avisos que correspondem a uma exceção da seção 4.2 são marcados como aceitos, com a
   exceção citada; todos os outros são corrigidos.
4. **Gate:** o usuário aprova pela captura em PNG (1440 px e 390 px). Sem "aprovado" ou "pode
   seguir", a tela não avança.
5. **Extração:** o `/extract-ds` gera o catálogo `design-systems/labmaes/`. Como ele aceita uma
   única entrada, `design-systems/telas/index.html` liga as telas e serve de entrada.

O site depende só do catálogo extraído, nunca do kit da skill. Se a skill for atualizada ou
trocada, o catálogo e o site não mudam.

### 4.2 Exceções às regras da `design-taste-frontend`

A skill foi feita para sites de empresa. Nestas regras, o LabMAES segue a própria marca:

| Regra da skill | No LabMAES |
|---|---|
| Sem violeta nem lavanda no design | Vale a paleta do manual (azul `#302A66`, gelo `#F0F0FF`) |
| Fundos chapados, sem grão fora de tecnologia | Grão e trama leves como detalhe (seção 2.4) |
| Uma seção por tela | Vale só na home e nas institucionais; repositório, item, leitura longa e programação seguem o conteúdo |
| Nenhuma legenda sob imagem | Acervo e produções têm legenda, crédito e autoria |
| Fotos de banco como substitutas | Proibidas; sem foto real, usa-se composição de módulos ou textura de IA, nunca algo que pareça ser do laboratório |
| Ícones reais coloridos de produtos | Ícones modulares da marca, sempre com rótulo |
| Contatos em `.example`, sem número | Dados reais e públicos do LabMAES |
| Um ou dois "momentos" em toda página | Só na home, no Sobre, na edição de evento e na 404 (seção 2.5) |

As demais regras da skill valem: bordas iguais, sistema único (um par de botões, um estilo de
card, uma escala de raios, um estilo de link), alvos de toque de 44 px, nada além da tela em
320 px, contraste, foco visível, peso das imagens e o `copy-lint` (adaptado ao português onde
couber).

### 4.3 Telas e ordem

| Ciclo | Telas |
|---|---|
| 1 | Home desktop |
| 1 | Home mobile (mesma página da home, responsiva) |
| 1 | Listagem do repositório (Produções, com busca e filtros) |
| — | **Extração 1** → catálogo v1, ponto de revisão e consulta informal à coordenação |
| 2 | Página de item (uma produção) |
| 2 | Página institucional (Sobre) |
| 2 | Edição de evento (Caminhos 2026), com `data-brand="caminhos"` |
| 2 | 404 |
| — | **Extração final** → catálogo completo, fonte da verdade |

O ciclo 1 junta a página mais expressiva (home) e a mais funcional (repositório), para que os
fundamentos não fiquem puxados para um lado só. No ciclo 2, cada tela parte do `styles.css` do
catálogo v1 e só acrescenta o que falta.

### 4.4 Estrutura no repositório

```text
design-systems/
  marca/
    marca.css           # camada de marca sobre o kit da skill
    ia/                 # prompt fixo, checklist e log.md das gerações
  telas/
    index.html          # liga as telas; entrada do /extract-ds
    01-home/            # responsiva: as capturas em 1440 e 390 px cobrem a home desktop e a mobile
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
      textura/
      fonts/
```

### 4.5 Regras

- Cada tela guarda no git só o `index.html`, as capturas, o `verificacao.md` e os waivers do gate.
  A cópia do kit da skill (cerca de 37 MB), a cópia da marca e as saídas dos verificadores ficam
  fora do git e são recriadas por um script. Os arquivos do kit não são editados (regra da
  skill); só a camada de marca muda.
- Por isso as telas não são publicadas no preview: a coordenação vê o catálogo e as capturas.
- Entre a extração 1 e a extração final, o catálogo não é editado à mão, porque a extração
  final o regenera. Ajustes finos só depois dela.
- Alternativas descartadas ficam em `../redesign-fase2-referencias/`, fora do repositório.
- Nenhum token fica em JSON ou outro arquivo paralelo ao `styles.css`.

## 5. Integração com o Eleventy

**Branch da fase.** Todo o trabalho da Fase 2 acontece na branch `redesign/fase-2-design-system`
(PRs menores entram nela, não na `main`). Até a aprovação da coordenação (seção 7), nada da
fase chega à `main`, e o catálogo só existe nos deploys de preview do Cloudflare para essa
branch.

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

**Migração.** A Fase 2 não altera nenhuma página pública, e o próprio catálogo só vai para
produção depois da aprovação da coordenação. As páginas migram para o layout v2
nas Fases 3, 4 e 5, e o `css/` e o `js/` antigos são removidos na Fase 7.

## 6. Acessibilidade e testes

Alvo: WCAG 2.2 AA (ADR 0005).

Durante a construção, cada tela passa pelos verificadores da skill e pelo axe (seção 4.1). Na
CI, um job novo no `.github/workflows/ci.yml` roda Playwright com `@axe-core/playwright`
contra o catálogo gerado pelo build:

1. regras WCAG 2.2 A e AA do axe;
2. a mesma checagem com `prefers-reduced-motion: reduce` emulado;
3. viewport de 320 px de largura, falhando se houver rolagem horizontal.

O catálogo mostra cada componente em todos os estados, então o job cobre o sistema inteiro.
As páginas migradas entram na mesma bateria nas fases seguintes.

## 7. Aprovação da coordenação

A nova versão do site não fica pública sem a aprovação da coordenadora do LabMAES, Profa. Mara
Rúbia Sant'Anna. Essa regra vale para todas as fases do redesign e é registrada no ADR 0010
durante o plan desta fase. Ela não se aplica às atualizações de conteúdo do site atual feitas
pelo CMS, que seguem o ADR 0008.

Na Fase 2, a aprovação é o último passo, depois que os critérios 1 a 7 da seção 9 forem
cumpridos.

**O que é enviado à coordenadora:**

- o link do catálogo no deploy de preview da branch da fase;
- as capturas aprovadas das seis telas e da home mobile (PNG);
- um resumo curto das decisões (site novo com a mesma marca, cor, tipografia, forma, textura,
  movimento), em linguagem não técnica.

**Registro.** A resposta é registrada num documento em `docs/superpowers/reviews/` e num
comentário na issue da aprovação, com data e eventuais ressalvas.

**Se houver pedidos de mudança:** volta-se à etapa correspondente (tela, extração ou
fundamento), refaz-se a extração final se necessário e reenvia-se o pacote.

**Depois da aprovação:** a branch da fase é mesclada na `main`, e o catálogo passa a ser
publicado em `/design-system/` no site de produção.

## 8. Issues

| Issue | Destino |
|---|---|
| #24 | Fecha com esta spec e o plan |
| #26 | Reescrita: header e card saem do catálogo |
| #27 | Absorvida pelas Foundations (seção 2.2) |
| #28 | Regra do DS (seção 2.2); ainda pode ser corrigida no CSS atual |
| #33 | Fechada como substituída pelas telas em HTML construídas com a `design-taste-frontend` |
| #34 | Atendida pelo `design-system.html` |
| #35 | Atendida pelo job da seção 6 |

Issues novas: licença da Thunder, camada de marca e guia de IA, uma por tela, extração 1,
extração final, integração com o Eleventy, ADR 0010 e aprovação da coordenação.

## 9. Critérios de saída

1. As seis telas e a home mobile estão aprovadas pelas capturas, com `verificacao.md` sem
   aviso pendente.
2. O catálogo saiu da extração final e cobre Foundations (com Forma, Textura e Movimento),
   Components e Layouts, e `data-brand="caminhos"`.
3. O guia de IA está no catálogo, com o log das gerações.
4. O catálogo está publicado em `/design-system/` no deploy de preview da branch da fase; as
   macros de `_includes/ds/` e o `layout-v2.njk` existem; nenhuma página pública foi alterada.
5. `test:ds` e o job de acessibilidade estão verdes na CI.
6. A licença da Thunder está resolvida (confirmada, ou a Poppins Black adotada).
7. As issues foram reorganizadas, o ADR 0010 foi registrado, e `docs/roadmap.md` e
   `docs/architecture/README.md` estão atualizados.
8. A coordenadora aprovou o pacote da seção 7, a aprovação está registrada, e só então a branch
   da fase foi mesclada na `main`.

## 10. Riscos

| Risco | Mitigação |
|---|---|
| A skill puxar o visual para fora da marca | Camada de marca obrigatória, tabela de exceções (seção 4.2) e gate do usuário em cada tela |
| Os verificadores da skill acusarem as exceções o tempo todo | Avisos aceitos registrados em `verificacao.md`, citando a exceção |
| O site ficar preso ao kit da skill | O site consome só o catálogo extraído (seção 4.1) |
| O catálogo e as macros divergirem | `test:ds` na CI |
| A extração final sobrescrever ajustes | Nenhuma edição manual entre as extrações |
| A IA se desviar do guia | Prompt fixo e checklist; uso restrito a texturas e apoio |
| Custo das gerações | Geração em 1K e log com custo; conferir o saldo do OpenRouter antes de gerar |
| Thunder sem licença para web | Poppins Black como alternativa definida |
| A coordenação pedir mudanças de fundo só no fim, gerando retrabalho | Mostrar à coordenadora o preview do catálogo v1, depois da extração 1, como consulta informal; a aprovação formal continua sendo o passo final |
