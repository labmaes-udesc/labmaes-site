# Programação rica — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Substituir a página de programação por uma agenda expansível orientada a dados, onde cada atividade mostra tipo/título/horário/local/modalidade e nomes na capa e revela ementa + participantes (foto/iniciais + mini-bio) ao expandir.

**Architecture:** Duas fontes de dados normalizadas em `_data/` (`pessoas.json` por slug; `programacao.json` com os 4 dias e atividades que referenciam pessoas por slug). O template Nunjucks percorre os dados e renderiza cada atividade como `<details open>` nativo (acessível e tudo-aberto sem JS); um JS leve colapsa quando disponível. Reaproveita tokens e componentes CSS existentes.

**Tech Stack:** Eleventy 3 (ESM), Nunjucks, HTML/CSS estáticos, JS vanilla. Sem framework de testes — cada tarefa é verificada por validação de JSON, build do Eleventy e inspeção do HTML gerado / preview.

**Spec:** `docs/superpowers/specs/2026-06-18-programacao-rica-design.md`
**Fonte do conteúdo:** `C:\Users\Windows 10\Downloads\ementas_programacao_7o_caminhos (1).docx` (31 atividades, dias 19–22/08/2026). Dump de texto já extraído em `C:\Users\Windows 10\Downloads\_dump.txt`.

---

## Convenções de dados

### Slugs canônicos (usar exatamente estes nos dois arquivos)

Pessoas que se repetem — fixar o slug para que `pessoas.json` e `programacao.json` batam:

- `mara-rubia` — Profa. Dra. Mara Rúbia Sant'Anna (UDESC)
- `valdecir-babinski` — Prof. Me. Valdecir Babinski Júnior (UEM)
- `andrei-galkowski` — Prof. Me. Andrei Galkowski (UDESC)
- `camila-franca` — Profa. Ma. Camila Geremias França (IFSC-JS)
- `janaina-nascimento` — Profa. Ma. Janaina Nascimento (UDESC)
- `mario-barro` — Prof. Dr. Mario Barro Hérnandez (UNAM)
- `monica-rodrigues` — Profa. Dra. Monica Rodrigues (IEMA)
- `karine-joulie` — Karine Joulie Martins
- `leticia-francez` — Profa. Dra. Letícia Francez (SED/SC)
- `monica-faria` — Profa. Dra. Mónica Faria (UMinho)
- `ivis-aguiar` — Me. Ivis de Aguiar (UMinho)
- `monica-fantin` — Profa. Dra. Mônica Fantin (UFSC)
- `myriam-lemonchois` — Prof. Dra. Myriam Lemonchois (Montréal)
- `maria-de-fatima` — Profa. Dra. Maria de Fátima Mattos (Abepem/CUML)
- `monica-stein` — Profa. Dra. Mônica Stein (UFSC)

Regra de slug para os demais: minúsculas, sem titulação (Prof./Dra./Me. etc.), sem acentos, espaços → hífens (ex.: "José Douglas Alves dos Santos" → `jose-douglas`).

### Regras de mapeamento do documento → dados

- **"Responsável"** do documento é dado interno → **nunca** entra nos dados públicos.
- **"A definir"** / célula vazia em ementa, bio, foto, título, papel ou local → **omitir a chave** (não gravar string vazia nem "a definir").
- **Papel** (`papel`) vem dos sufixos do documento: "– mediação/mediador(a)" → `"mediador"`; "– curadoria" → `"curadoria"`; "– Coordenação" → `"coordenação"`; "– fala" → omitir (é o padrão). Normalizar para minúsculas.
- **Título de fala individual** (coluna "Título" nas mesas, quando preenchida) → `titulo_fala` no participante.
- **Modalidade:** "Presencial" → `presencial`; "Online" → `online`; "Presencial + Online" → `hibrido`.
- **Tag de cor** por tipo (reaproveitar classes existentes): Abertura/Conferência/Cultural/Encerramento → `tag--red`; Exposição/Mediação/Mostra/Mesa Temática/Oficina/Comunicações Orais/Pôster/Roda de Conversa/Coffee Break → `tag--blue`.
- **Coffee Break (atividade 08):** renderizar **apenas** o rótulo "Coffee Break" — sem título, ementa, participantes nem expansão (`expansivel: false`). A "Apresentação da Coletânea" fica fora por ora.
- **Atividades simultâneas** no mesmo horário (mesas/oficinas/exposições paralelas) → agrupar num item com `paralelas: [...]`.
- **Oficinas e Mostra** → incluir `link` para a página dedicada.

---

## File Structure

- `_data/pessoas.json` — **criar.** Dicionário de pessoas por slug (nome, instituição, bio?, foto?).
- `_data/programacao.json` — **criar.** Lista de 4 dias; cada um com lista de atividades (single ou paralela).
- `eleventy.config.js` — **modificar.** Adicionar filtros `iniciais` e `corAvatar`.
- `eventos/caminhos-do-contemporaneo/2026/programacao/index.njk` — **reescrever.** Template orientado a dados.
- `css/components.css` — **modificar.** Estilos do card expansível, lista de participantes (avatar/iniciais), link de inscrição.
- `js/main.js` — **modificar.** Enhancement: colapsar os `<details>` quando há JS.
- `assets/img/convidados/` — **criar pasta.** As 6 fotos `.webp` por slug.

---

## Task 1: Filtros do Eleventy (`iniciais`, `corAvatar`)

São necessários antes do template, que os usa para o fallback de avatar.

**Files:**
- Modify: `eleventy.config.js`

- [ ] **Step 1: Adicionar os filtros dentro da função de config**

Em `eleventy.config.js`, logo após a linha `eleventyConfig.addPassthroughCopy("_redirects");`, inserir:

```javascript
  // Iniciais para o fallback de avatar (remove titulação, pega 1ª+última palavra)
  eleventyConfig.addFilter("iniciais", (nome) => {
    if (!nome) return "?";
    const limpo = nome.replace(
      /\b(prof\.?a?|prof|dra?\.?|dr|me\.?|ma\.?|phd\.?|candidate)\b/gi,
      ""
    );
    const palavras = limpo
      .replace(/[.’']/g, "")
      .split(/\s+/)
      .filter(Boolean);
    if (palavras.length === 0) return "?";
    const primeira = palavras[0][0] || "";
    const ultima = palavras.length > 1 ? palavras[palavras.length - 1][0] : "";
    return (primeira + ultima).toUpperCase();
  });

  // Índice de cor 1..6 derivado de forma estável do slug
  eleventyConfig.addFilter("corAvatar", (slug) => {
    if (!slug) return 1;
    let h = 0;
    for (let i = 0; i < slug.length; i++) h = (h * 31 + slug.charCodeAt(i)) % 997;
    return (h % 6) + 1;
  });
```

- [ ] **Step 2: Verificar que o build ainda passa**

Run: `cd labmaes-site && npx @11ty/eleventy`
Expected: build conclui sem erro (`Wrote N files`).

- [ ] **Step 3: Commit**

```bash
git add eleventy.config.js
git commit -m "feat: filtros iniciais e corAvatar para fallback de avatar"
```

---

## Task 2: `_data/pessoas.json`

Dicionário de todas as pessoas públicas do documento, indexadas por slug. Transcrever **todas** as pessoas das colunas "Participantes / equipe indicada" + "Mini currículo" das 31 tabelas do documento-fonte, aplicando as regras de mapeamento.

**Files:**
- Create: `_data/pessoas.json`

- [ ] **Step 1: Criar o arquivo com a estrutura e os exemplos já resolvidos**

Schema: objeto cujas chaves são slugs. Cada valor: `nome` (obrigatório, com titulação como deve aparecer), `instituicao` (opcional), `bio` (opcional — omitir se "a definir"/vazio), `foto` (opcional — nome do arquivo em `assets/img/convidados/`).

Começar com estes registros já resolvidos (exemplos do padrão) e **continuar transcrevendo os demais**:

```json
{
  "mara-rubia": {
    "nome": "Profa. Dra. Mara Rúbia Sant'Anna",
    "instituicao": "UDESC",
    "bio": "Coordenadora Geral do evento e coordenadora do Laboratório Moda, Artes, Ensino e Sociedade (LabMAES). Professora no bacharelado em Moda e no Programa de Pós-Graduação em Artes Visuais da Udesc. Doutora em História (UFRGS, 2005), com pós-doutorado em História (Université de Strasbourg, 2011) e em Artes Visuais (UFRJ, 2017)."
  },
  "myriam-lemonchois": {
    "nome": "Prof. Dra. Myriam Lemonchois",
    "instituicao": "Université de Montréal",
    "bio": "Professora aposentada da Universidade de Montréal. Realiza pesquisas na linha do Ensino das Artes Visuais. Seus trabalhos discutem as finalidades atribuídas à educação artística no âmbito da pedagogia e da didática, em especial tendo desenvolvido a abordagem SIR: sensibilidade, imaginação e compreensão. Coordenou com Alain Kerlan o livro \"Infâncias de hoje: da criança cidadão à criança artística, as políticas para a infância\" (2014), entre diversos outros artigos, capítulos de livros e livros."
  },
  "mario-barro": {
    "nome": "Prof. Dr. Mario Barro Hérnandez",
    "instituicao": "UNAM",
    "bio": "Pesquisador do Instituto de Pesquisa Estética e professor do curso de graduação em Design e Comunicação Visual da Faculdade de Artes e Design (FAD) e do curso de pós-graduação em História da Arte da Universidade Nacional Autônoma do México (UNAM). Seu trabalho situa-se na interseção entre estudos cinematográficos, cultura visual e novas tecnologias. Desenvolveu projetos sobre cinema mexicano e latino-americano, alfabetização cinematográfica e, mais recentemente, sobre o uso da inteligência artificial aplicada à pós-produção fotográfica."
  },
  "valdecir-babinski": {
    "nome": "Prof. Me. Valdecir Babinski Júnior",
    "instituicao": "UEM",
    "bio": "Professor efetivo da Universidade Estadual de Maringá (UEM). Conselheiro da Associação Nacional dos Docentes de Moda da Rede Federal de Ensino (ADMODA). Vice-presidente da Associação para o Design do Paraná (prodesign>pr). Coordenador do Projeto de Extensão Laboratório de Figurino (nº 116/2026/UEM)."
  },
  "estudantes-unam": {
    "nome": "Estudantes da UNAM"
  }
}
```

Notas de transcrição:
- A bio do Valdecir é idêntica em 4 atividades — gravar **uma vez** aqui.
- Pessoas sem bio no documento (ex.: "Estudantes da UNAM", "Joana Sequeira", "Ana Hoffmann") → só `nome` (+ `instituicao` quando houver).
- Mesmos slugs canônicos da tabela no topo do plano.

- [ ] **Step 2: Validar JSON**

Run: `cd labmaes-site && node -e "JSON.parse(require('fs').readFileSync('_data/pessoas.json','utf8')); console.log('JSON ok')"`
Expected: `JSON ok`

- [ ] **Step 3: Build**

Run: `cd labmaes-site && npx @11ty/eleventy`
Expected: build sem erro.

- [ ] **Step 4: Commit**

```bash
git add _data/pessoas.json
git commit -m "feat: dados das pessoas (convidados) por slug"
```

---

## Task 3: `_data/programacao.json`

Os 4 dias e suas atividades em ordem cronológica, referenciando pessoas por slug. Transcrever **todas as 31 atividades** do documento-fonte aplicando as regras de mapeamento.

**Files:**
- Create: `_data/programacao.json`

- [ ] **Step 1: Criar o arquivo com a estrutura e exemplos resolvidos**

Schema:

```
[
  {
    "data": "2026-08-19",
    "rotulo": "19 AGO",
    "diaSemana": "quarta-feira",
    "secao": "section--pink",          // alternar pink/ice por dia
    "atividades": [ <atividade> | <paralelo>, ... ]
  }, ...
]
```

`<atividade>` (item simples):
```
{
  "hora": "9h30",
  "tipo": "Conferência",
  "tag": "tag--red",
  "destaque": true,                    // opcional: conferências/abertura/desfile
  "titulo": "…",                       // opcional
  "modalidade": "presencial",          // presencial | online | hibrido
  "local": "Auditório",                // opcional
  "ementa": "…",                       // opcional
  "expansivel": true,                  // default true; false só no Coffee Break
  "link": { "texto": "Ver inscrição e materiais →", "href": "/eventos/caminhos-do-contemporaneo/2026/oficinas/" }, // opcional
  "participantes": [
    { "slug": "myriam-lemonchois" },
    { "slug": "leticia-francez", "papel": "mediadora" }
  ]
}
```

`<paralelo>` (sessões simultâneas):
```
{
  "hora": "15h–17h",
  "paralelas": [ <atividade>, <atividade> ]
}
```

Exemplos resolvidos para fixar o padrão (transcrever o restante igual):

```json
[
  {
    "data": "2026-08-19",
    "rotulo": "19 AGO",
    "diaSemana": "quarta-feira",
    "secao": "section--pink",
    "atividades": [
      {
        "hora": "9h",
        "tipo": "Abertura",
        "tag": "tag--red",
        "titulo": "Cerimônia de Abertura",
        "modalidade": "presencial",
        "local": "Auditório do Bloco Amarelo",
        "ementa": "Cerimônia de abertura com as autoridades convidadas.",
        "participantes": [
          { "slug": "mara-rubia" },
          { "slug": "vicente-concilio" },
          { "slug": "maria-de-fatima" }
        ]
      },
      {
        "hora": "9h30",
        "tipo": "Conferência",
        "tag": "tag--red",
        "destaque": true,
        "titulo": "A formação da sensibilidade para a preparação de uma vida artística. Tecer com quatro fios condutores",
        "modalidade": "presencial",
        "local": "Auditório",
        "ementa": "A partir da crítica sobre a formação da sensibilidade, em diálogo com Rousseau e as possibilidades de uma educação emancipatória segundo John Dewey, a professora Lemonchois propõe discussões sobre a formação da sensibilidade na preparação de uma vida artística a partir das quatro formas de educação de Rousseau, descrevendo exemplos de situações diversas e métodos de emancipação para aprender uma lógica de ação que permita experimentar, em muitas dimensões, a criação, interpretação e apreciação de uma obra de arte.",
        "participantes": [
          { "slug": "myriam-lemonchois" },
          { "slug": "leticia-francez", "papel": "mediadora" }
        ]
      },
      {
        "hora": "17h",
        "tipo": "Coffee Break",
        "tag": "tag--blue",
        "modalidade": "presencial",
        "expansivel": false
      },
      {
        "hora": "17h30–19h",
        "paralelas": [
          {
            "tipo": "Oficina 1",
            "tag": "tag--blue",
            "titulo": "Composição visual para figurinos cênicos: exercícios de representação",
            "modalidade": "presencial",
            "local": "BC 102",
            "link": { "texto": "Ver inscrição e materiais →", "href": "/eventos/caminhos-do-contemporaneo/2026/oficinas/" },
            "ementa": "Com base nos elementos compositivos utilizados para a elaboração de figurinos cênicos (cor, estilo, forma, movimento, origem, textura e volume), os participantes irão desenhar personagens para representar trajes de cena, descrevendo e justificando escolhas técnicas, criativas, plásticas e estéticas.",
            "participantes": [
              { "slug": "valdecir-babinski" },
              { "slug": "pietra-eurich" },
              { "slug": "poliana-cardoso" },
              { "slug": "maria-gabriela-zoldan" }
            ]
          },
          {
            "tipo": "Oficina 2",
            "tag": "tag--blue",
            "titulo": "Do texto ao têxtil",
            "modalidade": "presencial",
            "local": "BC 101",
            "link": { "texto": "Ver inscrição e materiais →", "href": "/eventos/caminhos-do-contemporaneo/2026/oficinas/" },
            "ementa": "A oficina propõe experimentações para investigar as relações entre a palavra escrita e a materialidade têxtil. Tendo como partida a raiz etimológica que une texto e têxtil, a proposição convida os participantes a ativar a sensibilidade visual e tátil a partir da leitura e despedaçamento das palavras poéticas.",
            "participantes": [ { "slug": "janaina-nascimento" } ]
          }
        ]
      }
    ]
  }
]
```

Notas de transcrição:
- Dias e cores: 19 → `section--pink`; 20 → `section--ice`; 21 → `section--pink`; 22 → `section--ice` (segue a página atual).
- A Mostra Audiovisual usa `"link": { "texto": "Ver programação completa →", "href": "/eventos/caminhos-do-contemporaneo/2026/mostra-audiovisual/" }`.
- Mesas com coluna "Título" preenchida → `titulo_fala` no participante (ex.: Mara Rúbia na Mesa "Educação e Complexidade": `"titulo_fala": "Incertezas e possibilidades de uma estratégia nominada Saberes Sensíveis"`).
- Atividades sem título no documento → omitir `titulo`.
- Conferências, Abertura e Desfile recebem `"destaque": true`.

- [ ] **Step 2: Validar JSON**

Run: `cd labmaes-site && node -e "const d=JSON.parse(require('fs').readFileSync('_data/programacao.json','utf8')); console.log('dias:', d.length, '| atividades:', d.reduce((n,dia)=>n+dia.atividades.reduce((m,a)=>m+(a.paralelas?a.paralelas.length:1),0),0))"`
Expected: `dias: 4 | atividades: 31`

- [ ] **Step 3: Verificar integridade dos slugs (todo slug referenciado existe em pessoas.json)**

Run:
```bash
cd labmaes-site && node -e "
const prog=JSON.parse(require('fs').readFileSync('_data/programacao.json','utf8'));
const pess=JSON.parse(require('fs').readFileSync('_data/pessoas.json','utf8'));
const faltam=new Set();
for(const dia of prog) for(const it of dia.atividades){
  const ats=it.paralelas||[it];
  for(const a of ats) for(const p of (a.participantes||[])) if(!pess[p.slug]) faltam.add(p.slug);
}
console.log(faltam.size? 'SLUGS AUSENTES: '+[...faltam].join(', ') : 'todos os slugs ok');
"
```
Expected: `todos os slugs ok` (se aparecerem slugs ausentes, adicioná-los ao `pessoas.json`).

- [ ] **Step 4: Build + commit**

```bash
cd labmaes-site && npx @11ty/eleventy
git add _data/programacao.json
git commit -m "feat: dados da programação (4 dias, 31 atividades)"
```

---

## Task 4: Template da página de programação

Reescrever `index.njk` para gerar a agenda a partir dos dados, com cada atividade em `<details open>` nativo. Definir macros para card e participante.

**Files:**
- Modify: `eventos/caminhos-do-contemporaneo/2026/programacao/index.njk`

- [ ] **Step 1: Substituir o corpo da página pelo template orientado a dados**

Manter o front-matter (`layout`, `title`, `description`) e o `event-header.njk`. Substituir as seções P2–P5 escritas à mão por:

```njk
{% macro participante(p) %}
  {% set pessoa = pessoas[p.slug] %}
  {% if pessoa %}
  <li class="participante">
    {% if pessoa.foto %}
      <img class="participante__avatar" src="/assets/img/convidados/{{ pessoa.foto }}" alt="{{ pessoa.nome }}" loading="lazy" width="48" height="48">
    {% else %}
      <span class="participante__avatar participante__avatar--iniciais avatar--c{{ p.slug | corAvatar }}" aria-hidden="true">{{ pessoa.nome | iniciais }}</span>
    {% endif %}
    <div class="participante__texto">
      <p class="participante__nome">{{ pessoa.nome }}{% if pessoa.instituicao %} <span class="participante__inst">· {{ pessoa.instituicao }}</span>{% endif %}{% if p.papel %} <span class="participante__papel">{{ p.papel }}</span>{% endif %}</p>
      {% if p.titulo_fala %}<p class="participante__fala">{{ p.titulo_fala }}</p>{% endif %}
      {% if pessoa.bio %}<p class="participante__bio">{{ pessoa.bio }}</p>{% endif %}
    </div>
  </li>
  {% endif %}
{% endmacro %}

{% macro card(a) %}
  {% if a.expansivel == false %}
  <article class="prog-card prog-card--simples">
    <div class="prog-card__slot">{% if a.hora %}<p class="prog-card__time">{{ a.hora }}</p>{% endif %}</div>
    <div class="prog-card__head">
      <span class="tag {{ a.tag }}">{{ a.tipo }}</span>
    </div>
  </article>
  {% else %}
  <details class="prog-card{% if a.destaque %} prog-card--destaque{% endif %}" open>
    <summary class="prog-card__summary">
      <div class="prog-card__slot">{% if a.hora %}<p class="prog-card__time">{{ a.hora }}</p>{% endif %}</div>
      <div class="prog-card__head">
        <span class="tag {{ a.tag }}">{{ a.tipo }}</span>
        {% if a.titulo %}<h3 class="prog-card__title">{{ a.titulo }}</h3>{% endif %}
        {% if a.participantes %}<p class="prog-card__nomes">{% for p in a.participantes %}{% if pessoas[p.slug] %}{{ pessoas[p.slug].nome }}{% if not loop.last %} · {% endif %}{% endif %}{% endfor %}</p>{% endif %}
        <div class="prog-card__meta">
          <span class="modality-tag modality-tag--{{ a.modalidade }}">{{ a.modalidade | capitalize }}</span>
          {% if a.local %}<span class="prog-card__location">{{ a.local }}</span>{% endif %}
        </div>
      </div>
      <span class="prog-card__chevron" aria-hidden="true"></span>
    </summary>
    <div class="prog-card__detail">
      {% if a.ementa %}<p class="prog-card__ementa">{{ a.ementa }}</p>{% endif %}
      {% if a.link %}<a class="prog-card__link" href="{{ a.link.href }}">{{ a.link.texto }}</a>{% endif %}
      {% if a.participantes %}
      <ul class="participantes" role="list">
        {% for p in a.participantes %}{{ participante(p) }}{% endfor %}
      </ul>
      {% endif %}
    </div>
  </details>
  {% endif %}
{% endmacro %}

{% for dia in programacao %}
<section class="section {{ dia.secao }}" aria-labelledby="dia{{ dia.rotulo | replace(' ', '') }}-heading">
  <div class="container">
    <div class="schedule-day">
      <div class="schedule-day__text">
        <h2 id="dia{{ dia.rotulo | replace(' ', '') }}-heading" class="schedule-day__date">{{ dia.rotulo }}</h2>
        <p class="schedule-day__weekday">{{ dia.diaSemana }}</p>
      </div>
    </div>
    <div class="prog-list section-content">
      {% for a in dia.atividades %}
        {% if a.paralelas %}
        <div class="prog-parallel">
          {% if a.hora %}<div class="prog-parallel__slot"><p class="prog-card__time">{{ a.hora }}</p></div>{% endif %}
          <div class="prog-parallel__sessions">
            {% for sub in a.paralelas %}{{ card(sub) }}{% endfor %}
          </div>
        </div>
        {% else %}
          {{ card(a) }}
        {% endif %}
      {% endfor %}
    </div>
  </div>
</section>
{% endfor %}
```

Manter a seção P1 (cabeçalho "PROGRAMAÇÃO") como está, acima do loop.

- [ ] **Step 2: Build**

Run: `cd labmaes-site && npx @11ty/eleventy`
Expected: build sem erro.

- [ ] **Step 3: Conferir o HTML gerado**

Run: `cd labmaes-site && grep -c "prog-card" _site/eventos/caminhos-do-contemporaneo/2026/programacao/index.html`
Expected: número alto (≥ 31). Conferir também que **não** aparece a palavra "Responsável" nem "a definir":
Run: `cd labmaes-site && grep -ci "responsável\|a definir" _site/eventos/caminhos-do-contemporaneo/2026/programacao/index.html`
Expected: `0`

- [ ] **Step 4: Commit**

```bash
git add eventos/caminhos-do-contemporaneo/2026/programacao/index.njk
git commit -m "feat: template orientado a dados da programação"
```

---

## Task 5: Estilos do card expansível e participantes

**Files:**
- Modify: `css/components.css` (acrescentar ao final)

- [ ] **Step 1: Acrescentar os estilos**

```css
/* ─── Programação rica ──────────────────────────────────── */
.prog-list { display: grid; gap: var(--space-16); }

.prog-card {
  background: var(--color-white);
  border: 1px solid rgba(48, 42, 102, 0.10);
  border-radius: var(--radius-lg);
  overflow: hidden;
}
.prog-card--destaque { border-left: 3px solid var(--color-brand-red); }

.prog-card__summary {
  display: grid;
  grid-template-columns: 116px 1fr auto;
  gap: var(--space-24);
  padding: 24px 28px;
  cursor: pointer;
  list-style: none;
  align-items: start;
}
.prog-card__summary::-webkit-details-marker { display: none; }
.prog-card--simples {
  display: grid;
  grid-template-columns: 116px 1fr;
  gap: var(--space-24);
  padding: 24px 28px;
  align-items: center;
}

.prog-card__time {
  margin: 0;
  font-family: var(--font-event);
  font-size: 15px;
  font-weight: 700;
  color: var(--color-brand-red);
  line-height: 1.3;
}
.prog-card__head { display: flex; flex-direction: column; gap: var(--space-8); min-width: 0; }
.prog-card__title { margin: 4px 0 0; font-size: 17px; font-weight: 600; line-height: 1.4; color: var(--color-brand-blue); }
.prog-card--destaque .prog-card__title { font-size: 20px; }
.prog-card__nomes { margin: 0; font-family: var(--font-event); font-size: 13px; color: rgba(48, 42, 102, 0.70); line-height: 1.4; }
.prog-card__meta { display: flex; flex-wrap: wrap; align-items: center; gap: var(--space-8); margin-top: 2px; }
.prog-card__location { font-family: var(--font-event); font-size: 12px; color: rgba(48, 42, 102, 0.44); }

.prog-card__chevron {
  width: 12px; height: 12px; align-self: center;
  border-right: 2px solid rgba(48, 42, 102, 0.40);
  border-bottom: 2px solid rgba(48, 42, 102, 0.40);
  transform: rotate(45deg);
  transition: transform 0.2s ease;
}
.prog-card[open] .prog-card__chevron { transform: rotate(-135deg); }

.prog-card__detail { padding: 0 28px 28px 28px; }
.prog-card__summary + .prog-card__detail { margin-top: -8px; }
.prog-card__ementa { margin: 0 0 var(--space-16); font-size: var(--text-body-size); line-height: var(--text-body-line); }
.prog-card__link {
  display: inline-block; margin-bottom: var(--space-16);
  font-family: var(--font-event); font-size: 13px; font-weight: 700;
  color: var(--color-brand-red); text-decoration: none;
}
.prog-card__link:hover { text-decoration: underline; }

.participantes { list-style: none; margin: 0; padding: 0; display: grid; gap: var(--space-16); }
.participante { display: flex; gap: var(--space-12); }
.participante__avatar {
  width: 48px; height: 48px; border-radius: var(--radius-pill);
  flex-shrink: 0; object-fit: cover;
}
.participante__avatar--iniciais {
  display: flex; align-items: center; justify-content: center;
  font-family: var(--font-event); font-size: 15px; font-weight: 700;
}
.avatar--c1 { background: rgba(177,0,0,0.12); color: var(--color-brand-red); }
.avatar--c2 { background: rgba(48,42,102,0.10); color: var(--color-brand-blue); }
.avatar--c3 { background: rgba(0,82,60,0.12); color: var(--color-support-green); }
.avatar--c4 { background: rgba(244,79,33,0.14); color: var(--color-support-orange); }
.avatar--c5 { background: rgba(48,42,102,0.16); color: var(--color-brand-blue); }
.avatar--c6 { background: rgba(177,0,0,0.18); color: var(--color-brand-red); }

.participante__texto { min-width: 0; }
.participante__nome { margin: 0; font-size: 15px; font-weight: 600; color: var(--color-brand-blue); }
.participante__inst { font-weight: 400; color: rgba(48,42,102,0.60); }
.participante__papel {
  display: inline-block; margin-left: 6px; padding: 1px 8px;
  border-radius: var(--radius-pill); background: rgba(48,42,102,0.07);
  font-family: var(--font-event); font-size: 11px; font-weight: 700;
  text-transform: lowercase; color: rgba(48,42,102,0.70);
}
.participante__fala { margin: 2px 0 0; font-size: 14px; font-style: italic; color: rgba(48,42,102,0.75); }
.participante__bio { margin: 4px 0 0; font-size: 15px; line-height: 1.55; color: rgba(48,42,102,0.78); }

.prog-parallel { display: grid; grid-template-columns: 116px 1fr; gap: var(--space-24); align-items: start; }
.prog-parallel__sessions { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-12); }
.prog-parallel__sessions .prog-card__summary { grid-template-columns: 1fr auto; padding: 20px 24px; }
.prog-parallel__sessions .prog-card__detail { padding: 0 24px 24px; }

@media (max-width: 767px) {
  .prog-card__summary,
  .prog-card--simples,
  .prog-parallel { grid-template-columns: 1fr; gap: var(--space-12); }
  .prog-parallel__sessions { grid-template-columns: 1fr; }
  .prog-card__chevron { display: none; }
}
```

- [ ] **Step 2: Build + preview**

Run: `cd labmaes-site && npx @11ty/eleventy --serve`
Abrir `http://localhost:8080/eventos/caminhos-do-contemporaneo/2026/programacao/` e confirmar: cards renderizam, avatares com iniciais coloridas, sessões paralelas lado a lado, Coffee Break sem chevron.

- [ ] **Step 3: Commit**

```bash
git add css/components.css
git commit -m "feat: estilos do card expansível e lista de participantes"
```

---

## Task 6: JS — colapsar quando há JavaScript (progressive enhancement)

Sem JS, os `<details open>` ficam abertos (tudo visível). Com JS, colapsar para a agenda escaneável.

**Files:**
- Modify: `js/main.js`

- [ ] **Step 1: Adicionar o bloco antes do fechamento do callback `DOMContentLoaded`**

Inserir logo após a linha `document.documentElement.classList.add("js");` (fora do listener, executa cedo, evita flash de conteúdo aberto):

```javascript
// Programação: com JS, inicia colapsada (sem JS, <details open> mostra tudo)
window.addEventListener("DOMContentLoaded", () => {
  document
    .querySelectorAll(".prog-card[open]")
    .forEach((d) => d.removeAttribute("open"));
});
```

- [ ] **Step 2: Preview da interação**

Run: `cd labmaes-site && npx @11ty/eleventy --serve`
Confirmar: ao carregar com JS, os cards iniciam **fechados**; clicar no summary expande/colapsa; foco por teclado (Tab + Enter) funciona (comportamento nativo do `<details>`).

- [ ] **Step 3: Confirmar degradação sem JS**

No DevTools, desabilitar JavaScript e recarregar. Expected: todos os cards aparecem **abertos** com ementa e participantes visíveis.

- [ ] **Step 4: Commit**

```bash
git add js/main.js
git commit -m "feat: colapsar programação quando há JS (progressive enhancement)"
```

---

## Task 7: Encaixe das 6 fotos disponíveis

**Files:**
- Create: `assets/img/convidados/` (pasta + 6 arquivos `.webp`)
- Modify: `_data/pessoas.json` (campo `foto` das 6 pessoas)

- [ ] **Step 1: Obter e otimizar as imagens**

O autor baixa as 6 fotos do Drive para uma pasta temporária. Para cada uma, converter para WebP (largura máx. 400px, qualidade ~82) e salvar em `assets/img/convidados/<slug>.webp`. Se houver `cwebp` instalado:

```bash
cwebp -q 82 -resize 400 0 origem.jpg -o "labmaes-site/assets/img/convidados/<slug>.webp"
```

(Sem `cwebp`, usar qualquer conversor; o importante é o arquivo final `.webp` nomeado pelo slug.)

- [ ] **Step 2: Referenciar as fotos no `pessoas.json`**

Para cada uma das 6 pessoas, adicionar a chave `"foto": "<slug>.webp"`. Exemplo:

```json
"mario-barro": {
  "nome": "Prof. Dr. Mario Barro Hérnandez",
  "instituicao": "UNAM",
  "foto": "mario-barro.webp",
  "bio": "…"
}
```

- [ ] **Step 3: Build + preview**

Run: `cd labmaes-site && npx @11ty/eleventy --serve`
Confirmar: as 6 pessoas mostram foto; as demais seguem com iniciais.

- [ ] **Step 4: Commit**

```bash
git add assets/img/convidados _data/pessoas.json
git commit -m "feat: fotos dos convidados disponíveis"
```

---

## Task 8: Validação final e revisão da página inteira

**Files:** nenhum (verificação).

- [ ] **Step 1: Build limpo**

Run: `cd labmaes-site && rm -rf _site && npx @11ty/eleventy`
Expected: build sem avisos/erros.

- [ ] **Step 2: Checagem de conteúdo no HTML gerado**

Run:
```bash
cd labmaes-site
grep -ci "responsável\|a definir\|undefined\|null" _site/eventos/caminhos-do-contemporaneo/2026/programacao/index.html
```
Expected: `0`.

- [ ] **Step 3: Revisão visual no preview**

Abrir a página e percorrer os 4 dias confirmando: nomes na capa de cada card; expansão revela ementa + participantes; oficinas/mostra com link para a página dedicada; Coffee Break só rótulo; responsivo (mobile) empilha corretamente; sem fotos quebradas.

- [ ] **Step 4: Commit final (se houver ajustes) e parar antes do merge**

Não fazer merge para `main`. Reportar ao autor para validação final na branch `feat/programacao-rica`.

---

## Self-Review

- **Spec coverage:** experiência integrada/agenda backbone (Task 4) ✓; expansão inline (Task 4, `<details>`) ✓; nomes na capa (Task 4, `prog-card__nomes`) ✓; sem vitrine no topo (não há tarefa que a crie) ✓; responsável interno omitido (regra de mapeamento + grep na Task 4/8) ✓; oficinas/mostra com link (campo `link`, Tasks 3–4) ✓; coffee break só rótulo (Tasks 3–4, `expansivel:false`) ✓; fallback de iniciais (Tasks 1, 4, 5) ✓; fotos incrementais (Task 7) ✓; dados normalizados pessoas+programação (Tasks 2–3) ✓; campos vazios não renderizam (regras + `{% if %}` no template) ✓; degradação sem JS (Task 6) ✓; branch nova / sem merge (Task 8) ✓.
- **Placeholders:** as instruções "transcrever os demais" apontam para o documento-fonte como conteúdo autoritativo (não dá para re-digitar o .docx inteiro no plano); o schema e as regras de mapeamento tornam a transcrição mecânica. Sem TODO/TBD de código.
- **Consistência de tipos:** slugs canônicos fixados no topo; campos do schema (`tipo/tag/titulo/modalidade/local/ementa/participantes[slug,papel,titulo_fala]/expansivel/link/destaque/paralelas`) usados de forma idêntica em Tasks 3 e 4; filtros `iniciais`/`corAvatar` definidos na Task 1 e usados na Task 4; classes `avatar--c1..c6` definidas na Task 5 batem com `corAvatar` (1..6) da Task 1.
