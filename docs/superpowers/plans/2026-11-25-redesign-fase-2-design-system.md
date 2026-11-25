# Redesign Fase 2: Design system — plano de implementação (v2)

> **Para agentes:** SUB-SKILL OBRIGATÓRIA: use superpowers:subagent-driven-development (recomendado) ou superpowers:executing-plans para executar este plano tarefa por tarefa. Os passos usam checkbox (`- [ ]`) para acompanhamento.
>
> **Atenção:** as Partes B e D são trabalho de design com gates humanos. Elas são executadas **nesta sessão principal**, nunca por subagentes, porque cada tela termina numa aprovação do usuário e a skill `design-taste-frontend` arma um hook de parada (`gate.mjs --hook claude`) que bloqueia o fim do turno enquanto houver um build aberto com falhas. O `/plan-screen` e o `/extract-ds` têm `disable-model-invocation: true`: **quem os invoca é o usuário**, digitando o comando no chat; os textos de invocação estão prontos neste plano. Quem executa nunca avança um gate sem "aprovado" ou "pode seguir" do usuário.

**Objetivo:** produzir o design system do novo site do LabMAES dentro da marca atual (2D, Manual de Marca), como catálogo HTML que é a fonte da verdade, integrá-lo ao Eleventy sem alterar páginas públicas e obter a aprovação da coordenadora antes de qualquer publicação.

**Arquitetura:** cada tela-chave é construída em HTML pela skill `design-taste-frontend`, com o kit dela e uma camada de marca (`design-systems/marca/marca.css`) que redefine tokens, fontes, raios e textura. Os verificadores da skill e o axe checam cada tela; o usuário aprova pela captura. O `/extract-ds` gera `design-systems/labmaes/` (catálogo, `styles.css`, `interactions.js`, `assets/`) a partir das telas, e o site depende só desse catálogo: o Eleventy o copia para `/design-system/`, e o site o consome por um `layout-v2.njk` e por macros Nunjucks em `_includes/ds/`, vigiadas por um teste de sincronia. Todo o trabalho fica na branch `redesign/fase-2-design-system` até a aprovação da coordenação.

**Stack:** Eleventy 3, Nunjucks, CSS e JS puros, Node 22 (`node --test`), skill `design-taste-frontend` 2.5.1 (kit + scripts com Chrome headless), `node-html-parser`, `nunjucks`, `@playwright/test`, `@axe-core/playwright`, OpenRouter (Nano Banana Pro) com `uv`, GitHub Actions, Cloudflare (previews de branch).

**Spec:** [`docs/superpowers/specs/2026-10-07-redesign-fase-2-design-system-design.md`](../specs/2026-10-07-redesign-fase-2-design-system-design.md), **Revisão 1 (2026-11-24)**. Em caso de divergência, a spec prevalece sobre este plano, e um ADR prevalece sobre ambos. Este plano substitui o de 2026-10-12, que seguia a direção visual anterior.

---

## Pré-requisitos do ambiente (máquina Windows do usuário)

**Skill.** A `design-taste-frontend` está em `C:\Users\Windows 10\.claude\skills\design-taste-frontend` (nos comandos, `$SKILL`). Precisa de Node 22+ e de Chrome, Edge ou Chromium. Nos comandos Bash deste plano:

```bash
SKILL="$HOME/.claude/skills/design-taste-frontend"
```

Os scripts dela abrem um Chrome headless cada, **um de cada vez, em primeiro plano**, com timeout de 10 minutos (regra da skill). Nunca rodá-los em segundo plano nem pelo navegador do app.

**Imagens por IA.** O Avast intercepta o HTTPS. Todo comando que chama a API de imagens precisa, no mesmo shell:

```bash
unset SSLKEYLOGFILE
export SSL_CERT_FILE="$NODE_EXTRA_CA_CERTS" REQUESTS_CA_BUNDLE="$NODE_EXTRA_CA_CERTS"
```

e o `uv` precisa de `--system-certs`. O wrapper da Tarefa A4 já faz isso. A chave `OPENROUTER_API_KEY` está em `C:\Users\Windows 10\.env`. O saldo era de cerca de US$ 5,40 em 2026-10-07: **conferir com o usuário antes da primeira geração.**

O `npx playwright install chromium` também passa pelo Avast. Se falhar por certificado, rodar com `NODE_EXTRA_CA_CERTS` já definido (é o padrão nesta máquina) e, se ainda falhar, avisar o usuário em vez de desativar verificações.

## Mapa de arquivos

| Arquivo | Responsabilidade | Tarefa |
|---|---|---|
| `docs/architecture/adr/0010-aprovacao-coordenacao.md` | Regra: o redesign só vai ao ar com aprovação da coordenadora | A2 |
| `docs/architecture/README.md` | Estado do redesign e lista de ADRs | A2, E7 |
| `docs/roadmap.md` | Referência do plan e estado da fase | A1, E7 |
| `eleventy.config.js` | Ignorar `design-systems/**`; copiar o catálogo para `/design-system/` | A3, C2 |
| `.gitignore` | Cópias locais do kit, da marca e saídas dos verificadores fora do git | A4 |
| `design-systems/README.md` | O que é fonte, o que é saída e como regenerar | A4 |
| `design-systems/marca/marca.css` | Camada de marca sobre o kit da skill (tokens, fontes, raios, textura) | A4 |
| `design-systems/marca/excecoes.md` | Exceções às regras da skill (spec, seção 4.2), citadas nas verificações | A4 |
| `design-systems/marca/ia/prompt-fixo.md` | Prompt fixo e checklist das texturas e imagens de apoio | A7 |
| `design-systems/marca/ia/log.md` | Log das gerações | A7 |
| `design-systems/marca/textura/` | Texturas e imagens de apoio aprovadas (WebP) | A7, B, D |
| `tools/ds/preparar-tela.sh` | Cria ou atualiza a pasta de uma tela (kit, marca, fontes, texturas) | A4 |
| `tools/ds/gerar-imagem.sh` | Gera imagem com parâmetros fixos e contorno do Avast | A7 |
| `design-systems/telas/0N-*/` | `index.html`, capturas e `verificacao.md` de cada tela | B, D |
| `design-systems/telas/index.html` | Hub que liga as telas; entrada do `/extract-ds` | C1 |
| `design-systems/labmaes/` | Saída do `/extract-ds` = fonte da verdade | C1, E1, E2 |
| `tools/eleventy/design-system-publicacao.test.mjs` | Teste: catálogo publicado, telas fora do site | C2 |
| `_headers` | `noindex` e `no-cache` para `/design-system/*` | C3 |
| `tools/ds/sincronia.mjs` | Lê componentes do catálogo e compara com as macros | C4 |
| `tools/ds/sincronia.test.mjs` | Testes unitários da sincronia | C4 |
| `tools/ds/renderizar-macro.mjs` | Renderiza `_includes/ds/<nome>.njk` | C4 |
| `tools/ds/catalogo.test.mjs` | Teste de integração: catálogo real × macros reais | C4 |
| `tools/a11y/servidor.mjs` | Servidor estático mínimo para o `_site/` | C5 |
| `tools/a11y/design-system.spec.mjs` | axe WCAG 2.2 AA, movimento reduzido, 320 px | C5 |
| `playwright.config.mjs` | Configuração do Playwright | C5 |
| `.github/workflows/ci.yml` | Jobs de acessibilidade e de sincronia | C5, E4 |
| `_includes/ds/*.njk` | Uma macro por componente do catálogo | E3 |
| `_includes/layout-v2.njk` | Layout que carrega só o DS | E5 |
| `tools/eleventy/layout-v2.test.mjs` | Teste do layout v2 | E5 |
| `docs/superpowers/reviews/2026-MM-DD-fase-2-aprovacao-coordenacao.md` | Registro da aprovação | F3 |

**O que vai e o que não vai para o git nas telas.** Entram: `index.html`, `captura-1440.png`, `captura-390.png`, `verificacao.md` e o `.taste-skill/waivers.json` de cada tela. Ficam fora (`.gitignore`, Tarefa A4): a cópia do kit (`assets/`, 37 MB), a cópia da marca (`marca/`), as saídas dos verificadores (`shots/`) e o estado do gate (`.taste-skill/*` menos `waivers.json`). Quem clona o repositório recria tudo com `tools/ds/preparar-tela.sh`. Por isso as telas **não** são publicadas no preview do Cloudflare: a coordenação vê o catálogo (autocontido) e as capturas.

## Contrato de nomes dos componentes

O `/extract-ds` marca cada componente com `data-ds-section="component"` e `data-component="<nome>"` na seção do catálogo, e as variantes como modificadores BEM (`card--default`). Este plano acrescenta três regras, que vão nos textos de invocação:

1. **O nome do componente é a sua classe-base.** A seção `data-component="card"` contém um preview cuja raiz tem a classe `card`. Variantes usam `card--<variante>`, e elementos internos usam `card__<parte>`.
2. **Nomes canônicos**, usados sempre que a peça existir numa tela (nenhuma peça é criada sem evidência):

| Nome | Peça |
|---|---|
| `skip-link` | Link "Pular para o conteúdo" |
| `site-header` | Cabeçalho com logo e navegação |
| `site-nav` | Navegação principal (desktop e mobile) |
| `site-footer` | Rodapé |
| `hero` | Abertura de página (composição de módulos da marca) |
| `section-header` | Título e subtítulo de seção |
| `button` | Botão e link com aparência de botão |
| `link` | Link de texto |
| `tag` | Etiqueta de tipo, área ou status |
| `type-icon` | Ícone modular por tipo de conteúdo |
| `card` | Card de conteúdo (projeto, produção, evento, pessoa) |
| `breadcrumb` | Trilha de navegação |
| `search-field` | Campo de busca |
| `filter-group` | Grupo de filtros do repositório |
| `pagination` | Paginação |
| `empty-state` | Estado vazio (busca sem resultado, 404) |
| `metadata-list` | Lista de metadados de um item |
| `relation-list` | Pessoas, projetos e produções relacionadas |
| `document-download` | Documento para baixar (PDF, tamanho, idioma) |
| `accordion` | Acordeão (ex.: programação do evento) |
| `prose` | Bloco de leitura longa |

3. **As classes do kit não são nomes de componente.** O kit da skill usa classes próprias (`.btn`, `.wrap`, `.card`…). Na extração, cada peça recebe o nome canônico da tabela acima (por exemplo, `.btn` vira `button`), e o catálogo não carrega classes do kit sem correspondência na tabela.

---

## Parte A — Preparação

### Tarefa A1: Mesclar spec e plan na `main` e abrir a branch da fase

A spec e o plan são documentação (`docs/` é ignorado pelo Eleventy) e podem ir para a `main` sem afetar o site. O código e o design da fase não.

**Arquivos:**
- Modificar: `docs/roadmap.md` (linha da Fase 2)

- [x] **Passo 1: Apontar o roadmap para este plano** (feito em 2026-11-25, junto com a escrita deste plano)

Na linha da Fase 2 de `docs/roadmap.md`, a coluna "Referência" passa a ser:

```markdown
| 2 | Design system | em andamento | [spec](superpowers/specs/2026-10-07-redesign-fase-2-design-system-design.md), [plan](superpowers/plans/2026-11-25-redesign-fase-2-design-system.md) |
```

- [ ] **Passo 2: Commit, push e PR da documentação** (branch `docs/fase-2-spec-design-system`, que já tem a spec revisada e o plano antigo marcado como substituído)

```bash
export PATH="$PATH:/c/Program Files/GitHub CLI"
git add docs/roadmap.md docs/superpowers/plans/
git commit -m "docs: plan v2 da Fase 2 (design system na marca atual)"
git push
gh pr create --base main --title "docs: spec e plan da Fase 2 (design system)" --body "Spec (com a Revisão 1, de 2026-11-24: marca atual 2D, textura como detalhe, telas construídas com a design-taste-frontend) e plan v2 da Fase 2. O plan de 2026-10-12 fica no histórico, marcado como substituído. Só documentação; nenhuma mudança no site.

Closes #24"
```

Esperado: a CI passa (só `docs/` mudou). **Pedir ao usuário para revisar e mesclar o PR.**

- [ ] **Passo 3: Criar a branch da fase a partir da `main` atualizada**

```bash
git switch main && git pull --ff-only
git switch -c redesign/fase-2-design-system
git push -u origin redesign/fase-2-design-system
```

- [ ] **Passo 4: Abrir um PR de rascunho permanente da fase**

O PR de rascunho faz o Cloudflare publicar a URL de preview da branch e concentra a CI. Ele **não** é mesclado antes da Parte F.

```bash
git commit --allow-empty -m "chore: abre a branch da Fase 2"
git push
gh pr create --draft --base main --head redesign/fase-2-design-system \
  --title "Fase 2 — Design system (não mesclar antes da aprovação da coordenação)" \
  --body "Branch da Fase 2. Só é mesclada depois da aprovação da coordenadora (spec, seção 7; ADR 0010)."
```

- [ ] **Passo 5: Confirmar o preview do Cloudflare**

Rodar `gh pr view --comments` e procurar o comentário do Cloudflare com a URL de preview. Se não houver comentário em alguns minutos, **pedir ao usuário** que confira no painel do Cloudflare (Workers & Pages → `labmaes-site` → Settings → Builds) se os builds de branches que não são de produção e as preview URLs estão ativados. Anotar a URL de preview no corpo do PR.

### Tarefa A2: ADR 0010 — aprovação da coordenação

**Arquivos:**
- Criar: `docs/architecture/adr/0010-aprovacao-coordenacao.md`
- Modificar: `docs/architecture/README.md`

- [ ] **Passo 1: Escrever o ADR**

```markdown
# ADR 0010 — O redesign só vai ao ar com a aprovação da coordenadora do LabMAES

- Status: Aceito
- Data: <AAAA-MM-DD do commit>
- Relaciona-se a: ADR 0008

## Contexto

O redesign substitui, fase a fase, a cara pública do LabMAES. A identidade do laboratório e a
forma como ele se apresenta são responsabilidade da coordenação.

## Decisão

- Nenhuma parte da nova versão do site (redesign, Fases 2 a 7) fica pública sem a aprovação da
  coordenadora do LabMAES, Profa. Mara Rúbia Sant'Anna.
- O trabalho de cada fase acontece numa branch própria (`redesign/fase-N-...`). Até a
  aprovação, só existem deploys de preview, e nada da fase chega à `main`, que publica em
  produção.
- O último passo de cada fase é enviar à coordenadora um pacote com o link do preview, as
  imagens das telas e um resumo das decisões em linguagem não técnica.
- A resposta é registrada em `docs/superpowers/reviews/` e na issue da aprovação. Pedidos de
  mudança levam de volta à etapa correspondente, e o pacote é reenviado.

## Fora do alcance desta regra

As atualizações de conteúdo do site atual feitas pelo Pages CMS seguem o ADR 0008 e não
dependem desta aprovação.

## Consequências

- A data de publicação de cada fase depende da agenda da coordenação.
- As URLs de preview não são indexadas nem aparecem no site, mas qualquer pessoa com o endereço
  consegue abri-las. Se for preciso restringir o acesso, a alternativa é o Cloudflare Access.
- Para reduzir retrabalho, previews intermediários podem ser mostrados à coordenação como
  consulta informal; a aprovação formal continua sendo o último passo.
```

- [ ] **Passo 2: Atualizar o README da arquitetura**

Em `docs/architecture/README.md`, trocar a linha "- Fases 2–7: planejadas; ..." por:

```markdown
- Fase 2 — Design system: **em andamento** (spec e plan em `docs/superpowers/`; ADR 0010).
- Fases 3–7: planejadas; ver [roadmap](../roadmap.md) e as milestones no GitHub.

Desde o ADR 0010, nenhuma fase do redesign é publicada sem a aprovação da coordenadora do LabMAES.
```

- [ ] **Passo 3: Commit**

```bash
git add docs/architecture/adr/0010-aprovacao-coordenacao.md docs/architecture/README.md
git commit -m "docs: ADR 0010, aprovação da coordenação antes de publicar o redesign"
git push
```

### Tarefa A3: Isolar `design-systems/` do build

O Eleventy usa `input: "."`; sem isto, os `index.html` das telas virariam páginas do site.

**Arquivos:**
- Modificar: `eleventy.config.js` (bloco de `ignores`)

- [ ] **Passo 1: Acrescentar o ignore**

Logo depois de `eleventyConfig.ignores.add("src/**");`:

```js
  // Design system (Fase 2): telas e catálogo não são templates. O catálogo é copiado por passthrough.
  eleventyConfig.ignores.add("design-systems/**");
```

- [ ] **Passo 2: Verificar o build**

Run: `npm run build`
Esperado: termina sem erro, com o mesmo número de páginas de antes (`Wrote N files`).

- [ ] **Passo 3: Commit**

```bash
git add eleventy.config.js
git commit -m "build: Eleventy ignora design-systems/"
git push
```


### Tarefa A4: Camada de marca e preparação das telas

**Arquivos:**
- Modificar: `.gitignore`
- Criar: `design-systems/README.md`
- Criar: `design-systems/marca/marca.css`
- Criar: `design-systems/marca/excecoes.md`
- Criar: `tools/ds/preparar-tela.sh`

- [ ] **Passo 1: Ignorar as cópias locais**

Acrescentar ao fim de `.gitignore`:

```gitignore
# Design system (Fase 2): cópias locais recriadas por tools/ds/preparar-tela.sh
design-systems/telas/*/assets/
design-systems/telas/*/marca/
design-systems/telas/*/shots/
design-systems/telas/*/.taste-skill/*
!design-systems/telas/*/.taste-skill/waivers.json
/.taste-skill/
```

- [ ] **Passo 2: Escrever a camada de marca**

`design-systems/marca/marca.css` (carregado **depois** do `assets/system.css` do kit; redefine só tokens e fontes, nunca classes do kit):

```css
/* Camada de marca do LabMAES sobre o kit da design-taste-frontend (spec da Fase 2, seções 2 e 4.1).
   Fonte: Manual de Marca e css/tokens.css do site atual. Carregar depois de assets/system.css. */

@font-face { font-family: "Poppins"; src: url("fonts/Poppins-Regular.woff2") format("woff2"); font-weight: 400; font-style: normal; font-display: swap; }
@font-face { font-family: "Poppins"; src: url("fonts/Poppins-SemiBold.woff2") format("woff2"); font-weight: 600; font-style: normal; font-display: swap; }
@font-face { font-family: "Poppins"; src: url("fonts/Poppins-Bold.woff2") format("woff2"); font-weight: 700; font-style: normal; font-display: swap; }
/* Thunder: só depois da Tarefa A5 (licença para web). Sem licença, Poppins Black (fonts/Poppins-Black.woff2). */
@font-face { font-family: "Thunder"; src: url("fonts/Thunder-BoldHC.woff2") format("woff2"); font-weight: 700; font-style: normal; font-display: swap; }

:root {
  /* paleta do manual (spec 2.1) */
  --marca-azul: #302A66;
  --marca-vermelho: #B10000;
  --marca-verde: #00523C;
  --marca-laranja: #F44F21;
  --marca-rosa: #F4BEBE;
  --marca-gelo: #F0F0FF;

  /* tokens do kit (system.css) apontados para a marca */
  --p-bg: var(--marca-gelo);
  --p-surface: #FFFFFF;
  --p-ink: var(--marca-azul);
  --p-muted: rgba(48, 42, 102, 0.78);
  --p-accent: var(--marca-vermelho);
  --p-accent-ink: #FFFFFF;
  --p-action: var(--marca-vermelho);
  --p-action-ink: #FFFFFF;
  --p-inv-bg: var(--marca-azul);
  --p-inv-surface: #3B3477;
  --p-inv-ink: var(--marca-gelo);
  --p-inv-muted: rgba(240, 240, 255, 0.82);
  --p-inv-accent: var(--marca-gelo);
  --p-inv-accent-ink: var(--marca-azul);
  --p-inv-action: var(--marca-gelo);
  --p-inv-action-ink: var(--marca-azul);

  --font-display: "Thunder", "Poppins", system-ui, sans-serif;
  --font-text: "Poppins", system-ui, sans-serif;
  --display-weight: 700;
  --display-tracking: 0;

  /* raios derivados dos módulos do manual (quadrado de canto arredondado) */
  --r-sm: 8px;
  --r-md: 16px;
  --r-lg: 24px;
  --r-btn: 999px;

  /* textura como detalhe (spec 2.4): grão de papel em SVG, aplicado só onde a tela pedir */
  --textura-grao: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 .19 0 0 0 0 .16 0 0 0 0 .4 0 0 0 .06 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23g)'/%3E%3C/svg%3E");
}

/* Utilitário de textura: um elemento com data-textura="grao" ganha o grão por cima do próprio fundo */
[data-textura="grao"] { background-image: var(--textura-grao); background-repeat: repeat; }
```

Os raios e o `--display-tracking` são o ponto de partida; a Tarefa B1 calibra com o usuário. A Thunder só entra no catálogo depois da Tarefa A5.

- [ ] **Passo 3: Escrever as exceções**

`design-systems/marca/excecoes.md`:

```markdown
# Exceções às regras da design-taste-frontend (spec da Fase 2, seção 4.2)

Cada tela cita estes códigos no `verificacao.md` quando um aviso dos verificadores cai numa
exceção. Um aviso que não cai em nenhuma exceção é corrigido.

| Código | Regra da skill | No LabMAES |
|---|---|---|
| EX-1 | Sem violeta nem lavanda | Vale a paleta do manual (azul #302A66, gelo #F0F0FF) |
| EX-2 | Fundos chapados, sem grão fora de tecnologia | Grão e trama leves como detalhe (spec 2.4) |
| EX-3 | Uma seção por tela | Só na home e nas institucionais; repositório, item, leitura longa e programação seguem o conteúdo |
| EX-4 | Nenhuma legenda sob imagem | Acervo e produções têm legenda, crédito e autoria |
| EX-5 | Fotos de banco como substitutas | Proibidas; sem foto real, composição de módulos ou textura de IA |
| EX-6 | Ícones reais coloridos de produtos | Ícones modulares da marca, sempre com rótulo |
| EX-7 | Contatos em .example, sem número | Dados reais e públicos do LabMAES |
| EX-8 | Um ou dois "momentos" em toda página | Só na home, no Sobre, na edição de evento e na 404 |
| EX-9 | copy-lint em inglês | Textos em português; avisos de vocabulário inglês não se aplicam |

O gate da skill aceita no máximo 5 waivers por tela. Avisos cobertos por exceção além disso
ficam só no `verificacao.md`, e a tela é encerrada com `gate.mjs --done` depois da aprovação do
usuário (Tarefa B0, Passo 7).
```

- [ ] **Passo 4: Escrever o preparador de telas**

`tools/ds/preparar-tela.sh`:

```bash
#!/usr/bin/env bash
# Cria ou atualiza a pasta de uma tela-chave (plan v2 da Fase 2, Tarefa A4).
# Uso: tools/ds/preparar-tela.sh <slug>     ex.: tools/ds/preparar-tela.sh 01-home
# Copia o kit da design-taste-frontend (assets/), a camada de marca, as fontes e as texturas
# aprovadas. Nunca sobrescreve o index.html de uma tela que já existe.
set -euo pipefail

slug="${1:?uso: tools/ds/preparar-tela.sh <slug>}"
skill="${SKILL:-$HOME/.claude/skills/design-taste-frontend}"
tela="design-systems/telas/$slug"

[ -f "$skill/assets/starter.html" ] || { echo "kit da skill não encontrado em $skill" >&2; exit 1; }
mkdir -p "$tela/marca/fonts" "$tela/marca/textura"

rm -rf "$tela/assets"
cp -r "$skill/assets" "$tela/assets"

cp design-systems/marca/marca.css "$tela/marca/marca.css"
cp assets/fonts/Poppins-*.woff2 assets/fonts/Thunder-BoldHC.woff2 "$tela/marca/fonts/"
if compgen -G "design-systems/marca/textura/*" > /dev/null; then
  cp design-systems/marca/textura/* "$tela/marca/textura/"
fi

if [ ! -f "$tela/index.html" ]; then
  cp "$skill/assets/starter.html" "$tela/index.html"
  echo "index.html criado a partir do starter da skill"
fi
grep -q 'marca/marca.css' "$tela/index.html" \
  || echo "LEMBRETE: ligar <link rel=\"stylesheet\" href=\"marca/marca.css\"> depois de assets/system.css em $tela/index.html"
echo "tela $slug pronta em $tela"
```

Run: `chmod +x tools/ds/preparar-tela.sh`

- [ ] **Passo 5: Testar o preparador numa pasta descartável**

```bash
tools/ds/preparar-tela.sh 00-teste
ls design-systems/telas/00-teste design-systems/telas/00-teste/marca
git status --short design-systems/
rm -rf design-systems/telas/00-teste
```

Esperado: `assets/`, `index.html` e `marca/` (com `marca.css` e `fonts/`) existem; o lembrete do `marca.css` aparece; o `git status` lista só `design-systems/telas/00-teste/index.html` (as cópias são ignoradas). Depois a pasta é removida.

- [ ] **Passo 6: Escrever o README da pasta**

`design-systems/README.md`:

```markdown
# design-systems/

Design system do novo site do LabMAES (Fase 2 do redesign). Spec:
`docs/superpowers/specs/2026-10-07-redesign-fase-2-design-system-design.md`.

| Pasta | O que é | Fonte ou saída |
|---|---|---|
| `marca/` | Camada de marca (`marca.css`), exceções à skill, guia e log da IA, texturas aprovadas | Fonte |
| `telas/0N-*/` | Telas-chave construídas com a skill design-taste-frontend 2.5.1 | Fonte (só `index.html`, capturas, `verificacao.md` e `waivers.json` vão para o git) |
| `telas/index.html` | Hub que liga as telas; entrada do `/extract-ds` | Fonte |
| `labmaes/` | Catálogo extraído: `design-system.html`, `styles.css`, `interactions.js`, `assets/` | Saída do `/extract-ds`; fonte da verdade do site |

## Como regenerar

- Recriar a pasta local de uma tela (kit, marca, fontes, texturas): `tools/ds/preparar-tela.sh 01-home`.
- Verificar uma tela: os comandos da Tarefa B0 do plan da Fase 2.
- Regerar o catálogo: o usuário invoca o `/extract-ds` com o texto da Tarefa E1 do plan.

O site publica só `labmaes/`, em `/design-system/`. As telas nunca vão para o site.
```

- [ ] **Passo 7: Commit**

```bash
git add .gitignore design-systems/README.md design-systems/marca/marca.css design-systems/marca/excecoes.md tools/ds/preparar-tela.sh
git commit -m "feat(ds): camada de marca, exceções à skill e preparador de telas" -m "Refs #<issue da camada de marca>"
git push
```

### Tarefa A5: Licença da Thunder (ação do usuário)

- [ ] **Passo 1: Pedir ao usuário** que verifique com a coordenação ou com o designer do Manual de Marca se o LabMAES tem licença da Thunder (Thunder-BoldHC) **para uso web** (`@font-face`), e com quais idiomas e caracteres.
- [ ] **Passo 2: Registrar o resultado** num comentário da issue "Licença da Thunder" (Tarefa A6).
  - Se houver licença: salvar o arquivo da licença em `assets/fonts/Thunder-LICENSE.txt` (ou `.pdf`) e fazer o commit.
  - Se não houver: registrar que a Poppins Black substitui a Thunder. Nas invocações das Partes B e D, trocar "Thunder" por "Poppins Black".

- [ ] **Passo 3: Se a Poppins Black for adotada,** baixar `Poppins-Black.woff2` do repositório oficial da Poppins (licença OFL, já em `assets/fonts/Poppins-OFL.txt`), salvar em `assets/fonts/`, acrescentá-la ao `tools/ds/preparar-tela.sh` (linha do `cp assets/fonts/...`) e trocar, em `design-systems/marca/marca.css`, o `@font-face` da Thunder pela Poppins 900 e `--font-display` por `"Poppins", system-ui, sans-serif` com `--display-weight: 900`. Pedir ao usuário a aprovação do download antes (nome do arquivo, origem e tamanho).

Essa tarefa pode correr em paralelo com o resto. Ela só bloqueia a extração final (E1).

### Tarefa A6: Reorganizar as issues da milestone

- [ ] **Passo 1: Comentar e fechar as issues absorvidas**

```bash
gh issue comment 33 --body "Substituída pela spec da Fase 2: os protótipos passam a ser telas em HTML construídas com a skill design-taste-frontend sobre a marca atual (Revisão 1 da spec). Ver docs/superpowers/specs/2026-10-07-redesign-fase-2-design-system-design.md."
gh issue close 33 --reason "not planned"
gh issue comment 26 --body "Na Fase 2, o header e o card saem do catálogo extraído (componentes site-header e card). Esta issue fecha com a extração final (Tarefa E1 do plan)."
gh issue comment 27 --body "Absorvida pelas Foundations do DS (spec da Fase 2, seção 2.2): tamanhos com clamp() e breakpoint de tablet."
gh issue comment 28 --body "Vira regra do DS (spec da Fase 2, seção 2.2): nada de white-space: nowrap em texto traduzível. Continua valendo como good first issue no CSS atual."
gh issue comment 34 --body "Atendida pelo catálogo design-systems/labmaes/design-system.html, publicado em /design-system/ depois da aprovação da coordenação."
gh issue comment 35 --body "Atendida pelo job de acessibilidade da Tarefa C5 do plan da Fase 2 (Playwright + axe sobre o catálogo)."
```

- [ ] **Passo 2: Criar as issues novas**

```bash
M="Fase 2 — Design system"
gh issue create --milestone "$M" --label "tipo:decisão,área:design-system" --title "Licença da Thunder para uso web" --body "Confirmar se o LabMAES tem licença da Thunder-BoldHC para @font-face. Sem licença, a Poppins Black substitui a Thunder (spec da Fase 2, seção 2.2)."
gh issue create --milestone "$M" --label "tipo:tarefa,área:design-system" --title "Camada de marca e guia da IA" --body "marca.css, exceções à skill, prompt fixo, checklist e log das texturas (spec, seções 2.4, 3 e 4.2; plan, Tarefas A4, A7 e E2)."
for t in "Tela 01 — Home (desktop e mobile)" "Tela 03 — Listagem do repositório" "Tela 04 — Página de item" "Tela 05 — Sobre" "Tela 06 — Edição de evento (Caminhos)" "Tela 07 — 404"; do
  gh issue create --milestone "$M" --label "tipo:tarefa,área:design-system" --title "$t" --body "Tela construída com a design-taste-frontend, verificada (verificacao.md) e aprovada pelas capturas em 1440 e 390 px. Ver plan da Fase 2 (Tarefa B0)."
done
gh issue create --milestone "$M" --label "tipo:tarefa,área:design-system" --title "Extração 1 do catálogo (ciclo 1)" --body "/extract-ds sobre as telas 01–03 (plan, Tarefa C1) e consulta informal à coordenação."
gh issue create --milestone "$M" --label "tipo:tarefa,área:design-system" --title "Extração final do catálogo" --body "/extract-ds sobre as seis telas (plan, Tarefa E1)."
gh issue create --milestone "$M" --label "tipo:tarefa,área:design-system,área:infra" --title "Integração do DS com o Eleventy" --body "Publicação em /design-system/, macros em _includes/ds/, layout-v2.njk, test:ds (plan, Tarefas C2–C4, E3–E5)."
gh issue create --milestone "$M" --label "tipo:decisão,área:design-system" --title "Aprovação da coordenação (Fase 2)" --body "Pacote para a Profa. Mara Rúbia Sant'Anna e registro da resposta (spec, seção 7; ADR 0010; plan, Parte F)."
```

- [ ] **Passo 3: Anotar os números das issues** criadas no corpo do PR de rascunho da fase, para referenciá-las nos commits (`Refs #N`).

### Tarefa A7: Ferramenta de imagens e guia da IA

Só texturas chapadas e imagens de apoio 2D (spec, seções 2.4 e 3).

**Arquivos:**
- Criar: `tools/ds/gerar-imagem.sh`
- Criar: `design-systems/marca/ia/prompt-fixo.md`
- Criar: `design-systems/marca/ia/log.md`
- Criar: `design-systems/marca/textura/.gitkeep`

- [ ] **Passo 1: Escrever o wrapper**

`tools/ds/gerar-imagem.sh`:

```bash
#!/usr/bin/env bash
# Gera uma textura ou imagem de apoio com os parâmetros fixos (spec da Fase 2, seção 3).
# Uso: tools/ds/gerar-imagem.sh <saida.png> <arquivo-de-prompt> [proporcao]
set -euo pipefail

saida="$1"; arquivo_prompt="$2"; proporcao="${3:-1:1}"
script="$HOME/.agents/skills/openrouter-img/scripts/generate_image.py"
fixo="design-systems/marca/ia/prompt-fixo.md"
log="design-systems/marca/ia/log.md"

# Contorno do Avast (intercepta HTTPS) e do bug OPENSSL_Uplink do Python no Windows
unset SSLKEYLOGFILE
if [ -n "${NODE_EXTRA_CA_CERTS:-}" ]; then
  export SSL_CERT_FILE="$NODE_EXTRA_CA_CERTS" REQUESTS_CA_BUNDLE="$NODE_EXTRA_CA_CERTS"
fi

# O prompt final é o bloco "prompt" do arquivo fixo + o prompt específico
prompt="$(tr -d '\r' < "$fixo" | sed -n '/^```prompt$/,/^```$/p' | sed '1d;$d') $(tr -d '\r' < "$arquivo_prompt")"

mkdir -p "$(dirname "$saida")"
resultado="$(uv run --system-certs "$script" --model pro --resolution 1K --aspect-ratio "$proporcao" \
  --filename "$saida" --prompt "$prompt" 2>&1 | tail -3)"
echo "$resultado"

custo="$(printf '%s\n' "$resultado" | sed -n 's/.*usage.cost): \(.*\)$/\1/p')"
printf '| %s | `%s` | `%s` | %s | %s |\n' \
  "$(date +%Y-%m-%d)" "$saida" "$arquivo_prompt" "$proporcao" "${custo:-?}" >> "$log"
```

Run: `chmod +x tools/ds/gerar-imagem.sh`

- [ ] **Passo 2: Escrever o prompt fixo e o checklist**

`design-systems/marca/ia/prompt-fixo.md`:

````markdown
# Prompt fixo das imagens geradas (spec da Fase 2, seção 3)

Todo prompt começa por este bloco. O prompt específico só diz o material e o enquadramento.

```prompt
Flat top-down material swatch for the website of LabMAES, a university research lab in Fashion, Arts, Education and Society. Seen straight from above, completely flat, no perspective, no depth, no volume, no cast shadows, even flat lighting. The swatch fills the whole frame edge to edge. Strict palette, no other hues: orange #F44F21, deep red #B10000, navy blue #302A66, ice white #F0F0FF, dark green #00523C, soft pink #F4BEBE. Forbidden: glossy or plastic sheen, 3D objects, perspective, colors outside the palette, letters, words, logos, hands, people.
```

## Checklist de aprovação (cada imagem)

- [ ] Paleta conferida com conta-gotas (nenhuma cor fora dos seis hexadecimais).
- [ ] Nenhum texto, letra ou logo.
- [ ] Chapada: sem volume, perspectiva nem sombra projetada.
- [ ] Os quatro materiais (papel, tecido, massinha, blocos) equilibrados no conjunto do site.
- [ ] WebP dentro do orçamento: cerca de 60 KB por textura, até cerca de 120 KB por imagem de apoio.
- [ ] Aprovada pelo usuário; linha marcada com ✅ no `log.md`.
````

- [ ] **Passo 3: Criar o log e a pasta das texturas**

`design-systems/marca/ia/log.md`:

```markdown
# Log das gerações

Uma linha por geração feita com `tools/ds/gerar-imagem.sh`. Gerações aprovadas recebem ✅ ao
fim da linha, à mão, depois da aprovação do usuário.

| Data | Saída | Prompt | Proporção | Custo (US$) |
|---|---|---|---|---|
```

Run: `mkdir -p design-systems/marca/textura && touch design-systems/marca/textura/.gitkeep`

- [ ] **Passo 4: Testar o wrapper com uma geração barata** (só depois de o usuário confirmar o saldo do OpenRouter)

```bash
printf 'Swatch of ice-white cotton paper with a faint fibrous texture.' > ../redesign-fase2-referencias/teste.txt
tools/ds/gerar-imagem.sh ../redesign-fase2-referencias/teste-wrapper.png ../redesign-fase2-referencias/teste.txt 1:1
tail -1 design-systems/marca/ia/log.md
```

Esperado: `Image saved to: ...teste-wrapper.png`, custo em torno de US$ 0,13 e uma linha nova no log. Apagar essa linha de teste do log e o arquivo `../redesign-fase2-referencias/teste.txt`.

- [ ] **Passo 5: Commit**

```bash
git add tools/ds/gerar-imagem.sh design-systems/marca/ia design-systems/marca/textura/.gitkeep
git commit -m "feat(ds): wrapper de imagens e guia da IA (texturas chapadas)" -m "Refs #<issue da camada de marca>"
git push
```

```

## Parte B — Ciclo 1: os extremos

### Tarefa B0: Roteiro comum de cada tela

Toda tela das Partes B e D segue estes passos. As tarefas de cada tela só trazem o que muda.

- [ ] **Passo 1 (opcional): Planejamento.** Se o usuário quiser alternativas de estrutura antes de construir, ele invoca o `/plan-screen` com o texto da tarefa da tela. O gate do `/plan-screen` vale integralmente.
- [ ] **Passo 2: Preparar a pasta**

```bash
tools/ds/preparar-tela.sh <slug>
cd design-systems/telas/<slug>
```

- [ ] **Passo 3: Armar o gate e ler a skill.** Invocar a skill `design-taste-frontend` (Skill tool) e seguir o "run" dela (seção 4), com estas regras fixas:
  - `kind`: `service`; `<html lang="pt-BR" data-type="service">`; `<meta name="site-kind" content="other">`.
  - Ler antes, inteiros: `copy.md`, `copy-voice.md`, `system.md`, `layout-v4.md`, `sections.md` (exigência da skill) e `design-systems/marca/excecoes.md`.
  - **Não** rodar `start.mjs css` nem `start.mjs brand`: a paleta e as fontes vêm só do `marca.css`. Os sorteios de hero, navegação, rodapé, ritmo e botões (`deal.mjs` e a linha de listas de `service`) valem, e o resultado vai para o comentário no topo do `<body>`.
  - No `<head>`, depois de `assets/system.css`: `<link rel="stylesheet" href="marca/marca.css">`.
  - Textos em português, a partir do conteúdo real do site atual e da política editorial (`docs/politica-editorial.md`); nada inventado (números, citações, parceiros). Onde faltar texto, uma frase curta marcada com `data-assumed`.
  - Fotos: só fotos reais do LabMAES que já estão em `assets/` do site (eventos, pessoas). Sem foto real, composição de módulos ou textura (EX-5). Nunca `photos.mjs search`.

```bash
node "$SKILL/scripts/gate.mjs" --start index.html --kind service --category "<categoria da tela>" --primary "<ação principal da tela>"
```

- [ ] **Passo 4: Textura, se a tela pedir.** Para cada textura ou imagem de apoio nova: escrever o prompt específico em `../redesign-fase2-referencias/prompts/<nome>.txt`, gerar com `tools/ds/gerar-imagem.sh`, mostrar ao usuário (SendUserFile) e, aprovada, converter para WebP em `design-systems/marca/textura/<nome>.webp`, marcar ✅ no log e rodar de novo `tools/ds/preparar-tela.sh <slug>`. A conversão:

```bash
python -c "from PIL import Image; import sys; Image.open(sys.argv[1]).save(sys.argv[2], 'WEBP', quality=72, method=6)" <entrada.png> design-systems/marca/textura/<nome>.webp
ls -l design-systems/marca/textura/<nome>.webp
```

Esperado: até cerca de 60 KB (textura) ou 120 KB (apoio); acima disso, reduzir `quality` ou as dimensões. Antes de cada geração, somar a coluna de custo do log; se o saldo estimado ficar abaixo de US$ 2, avisar o usuário.

- [ ] **Passo 5: Construir** a tela conforme a seção 4, passo 5, da skill e o texto da tarefa da tela.
- [ ] **Passo 6: Verificar**, da pasta da tela, um script de cada vez, em primeiro plano:

```bash
P=".taste-skill/chrome-check"
node "$SKILL/scripts/copy-lint.mjs" index.html --kind service
node "$SKILL/scripts/consistency.mjs" index.html --widths 1440,1024,820,768,390 --rhythm-widths 1440,820,768,390 --profile $P --page service --category "<categoria>" --primary "<ação>"
node "$SKILL/assets/layout/check.mjs" --url index.html --profile $P --sizes 1440x900,1024x768,820x1180,768x1024,390x844 --shots shots/layout
node "$SKILL/scripts/perf.mjs" index.html --profile $P
npx --yes @axe-core/cli@4 "file://$(pwd -W 2>/dev/null || pwd)/index.html" --tags wcag2a,wcag2aa,wcag21aa,wcag22aa
node "$SKILL/scripts/gate.mjs" index.html
```

Se o `@axe-core/cli` não rodar nesta máquina (chromedriver ou certificado), registrar isso no `verificacao.md` e seguir: o job de acessibilidade da Tarefa C5 roda o axe sobre o catálogo na CI.

Corrigir todo FAIL que não caia numa exceção de `design-systems/marca/excecoes.md`. Para os que caem, até 5 waivers em `.taste-skill/waivers.json`, no formato da skill:

```json
[{ "check": "<id do aviso>", "target": "<parte do local, 3+ caracteres>", "reason": "EX-1: paleta do manual do LabMAES" }]
```

Repetir até `GATE: PASS` ou `GATE: OPEN` (três rodadas no máximo, regra da skill). Nunca editar arquivos do kit nem esconder nada do verificador.

- [ ] **Passo 7: Registrar e capturar**

```bash
node "$SKILL/scripts/shoot.mjs" --url index.html --w 1440 --out captura-1440.png --profile .taste-skill/chrome-check
node "$SKILL/scripts/shoot.mjs" --url index.html --w 390 --out captura-390.png --profile .taste-skill/chrome-check
```

`verificacao.md` na pasta da tela:

```markdown
# Verificação — <slug>

- **Data:** <AAAA-MM-DD>
- **Gate:** <última linha do gate.mjs>
- **Sorteios da skill:** <hero, navegação, rodapé, ritmo, botões, momento>
- **axe:** <0 violações | lista>
- **perf:** <sem FAIL | lista>

## Avisos aceitos por exceção

| Verificador | Aviso | Local | Exceção |
|---|---|---|---|

## Fatos assumidos (data-assumed)

- <texto> → a confirmar com a equipe
```

- [ ] **Passo 8: Gate do usuário.** Enviar `captura-1440.png` e `captura-390.png` (SendUserFile) e o resumo do `verificacao.md`. Ajustes pedidos voltam ao Passo 5. Com "aprovado", se o gate ainda estiver aberto, encerrá-lo com as palavras do usuário:

```bash
node "$SKILL/scripts/gate.mjs" --done "<o que o usuário disse>"
```

- [ ] **Passo 9: Commit** (da raiz do repositório)

```bash
git add design-systems/telas/<slug>/index.html design-systems/telas/<slug>/captura-*.png design-systems/telas/<slug>/verificacao.md design-systems/marca
git add -f design-systems/telas/<slug>/.taste-skill/waivers.json 2>/dev/null || true
git status --short design-systems/
git commit -m "feat(ds): tela <slug> aprovada" -m "Refs #<issue da tela>"
git push
```

Esperado no `git status`: nenhum arquivo de `assets/`, `marca/` ou `shots/` da tela.

### Tarefa B1: Tela 01 — Home (desktop e mobile)

A home é uma tela só, responsiva: as capturas em 1440 e 390 cobrem as telas "home desktop" e "home mobile" da spec (as duas issues fecham juntas).

- **slug:** `01-home` · **categoria:** "laboratório de pesquisa, ensino e extensão em Moda, Artes, Ensino e Sociedade" · **ação principal:** "Conhecer as produções"
- **Texto do `/plan-screen` (opcional):**

```text
/plan-screen Home do novo site do LabMAES (Laboratório de Moda, Artes, Ensino e Sociedade, UDESC CEART), desktop e mobile. Siga a spec docs/superpowers/specs/2026-10-07-redesign-fase-2-design-system-design.md (Revisão 1): site novo com a marca atual, 2D e chapada; a expressão vem dos módulos do Manual de Marca (quadrado de canto arredondado, quarto de círculo, arco) na paleta azul #302A66, vermelho #B10000, verde #00523C, laranja #F44F21, rosa #F4BEBE e gelo #F0F0FF; textura só como detalhe. Moda, Artes, Ensino e Sociedade com peso igual (saberes sensíveis). Seções: hero com composição de módulos; o que é o LabMAES; produções em destaque (repositório); projetos; próximo evento (Caminhos do Contemporâneo); equipe; rodapé com realizadores e apoiadores. Critério de impacto: clareza e reconhecimento da marca, não conteúdo para redes sociais.
```

- **Regras da construção:**
  - Hero: composição de módulos chapados na paleta, com entrada única (`data-enter`); os módulos "se encaixam" (spec 2.5). Pode ter um módulo preenchido com textura (Passo 4 do B0).
  - Um "momento" tipográfico ou de módulos (EX-8 permite na home); "uma seção por tela" vale aqui.
  - Calibrar com o usuário os raios e o `--display-tracking` do `marca.css` nesta tela; os valores aprovados ficam no `marca.css` (rodar `tools/ds/preparar-tela.sh 01-home` depois de editar).
  - Ícones modulares por tipo de conteúdo, com rótulo (EX-6).

### Tarefa B2: Tela 03 — Listagem do repositório

- **slug:** `03-repositorio` · **categoria:** "repositório de produções acadêmicas e artísticas do LabMAES" · **ação principal:** "Buscar produções"
- **Texto do `/plan-screen` (opcional):**

```text
/plan-screen Listagem do repositório de Produções do LabMAES, desktop e mobile. Parte da home aprovada em labmaes-site/design-systems/telas/01-home/ (mesma marca, mesmo marca.css). Página funcional: a estrutura domina, textura no máximo num detalhe do cabeçalho. Campo de busca, filtros (tipo de produção, ano, pessoa, projeto, idioma), contagem de resultados, cards de produção com ícone de tipo e rótulo, paginação e estado vazio (busca sem resultado). Os tipos e categorias vêm de tools/content-model/categorias-producao.mjs.
```

- **Regras da construção:**
  - EX-3: a listagem segue o conteúdo, sem "uma seção por tela"; sem momento (EX-8); sem animação em filtros, busca e paginação (spec 2.5).
  - Cards com 12 produções de exemplo realistas a partir dos tipos de `tools/content-model/categorias-producao.mjs`, marcadas com `data-assumed` (títulos de exemplo, nunca atribuídos a pessoas reais).
  - Mostrar o estado vazio numa segunda seção da mesma página (`id="estado-vazio"`), para a extração encontrar o componente `empty-state`.
  - Filtros com `<fieldset>`/`<legend>`, busca com `<label>` visível, paginação com `aria-current`.

---

## Parte C — Extração 1 e infraestrutura

### Tarefa C1: Hub das telas e extração 1

**Arquivos:**
- Criar: `design-systems/telas/index.html`
- Criar (pela skill): `design-systems/labmaes/`

- [ ] **Passo 1: Escrever o hub**

`design-systems/telas/index.html`:

```html
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex">
  <title>Telas-chave do design system — LabMAES</title>
</head>
<body>
  <main>
    <h1>Telas-chave do design system</h1>
    <p>Entrada do /extract-ds. Cada tela foi construída com a design-taste-frontend sobre a camada de marca e aprovada pelo usuário.</p>
    <ol>
      <li><a href="01-home/index.html">Home (responsiva: desktop e mobile)</a></li>
      <li><a href="03-repositorio/index.html">Listagem do repositório</a></li>
    </ol>
  </main>
</body>
</html>
```

- [ ] **Passo 2: Garantir as cópias locais** (o `/extract-ds` precisa abrir as telas com kit e marca)

```bash
tools/ds/preparar-tela.sh 01-home && tools/ds/preparar-tela.sh 03-repositorio
```

- [ ] **Passo 3: O usuário invoca o `/extract-ds`:**

```text
/extract-ds html=labmaes-site/design-systems/telas/index.html slug=labmaes — Saída em labmaes-site/design-systems/labmaes/. O index.html é um hub: inspecione TODAS as telas ligadas a ele (01-home, responsiva, e 03-repositorio) como um único projeto. As telas usam o kit da design-taste-frontend (assets/system.css, system.js, assets/motion) com a camada de marca marca/marca.css por cima: extraia só o que as telas de fato usam, com os valores finais da marca. Regras extras: (1) contrato de nomes do plan (docs/superpowers/plans/2026-11-25-redesign-fase-2-design-system.md): o nome em data-component é a classe-base da raiz do preview, sempre um nome da tabela (as classes do kit, como .btn e .wrap, são renomeadas para o nome canônico); variantes em BEM; (2) Foundations com Cor, Tipografia, Forma (módulos do manual e raios), Textura (grão em CSS e as texturas de marca/textura/) e Movimento (tokens da spec, seção 2.5); (3) o catálogo precisa de <meta name="robots" content="noindex">; (4) nenhum style="" e nenhum <style>/<script> inline (a CSP do site só permite 'self'); fontes auto-hospedadas em assets/fonts/; (5) nenhum arquivo do kit é copiado inteiro: só o CSS e o JS que os componentes usam, reescritos em styles.css e interactions.js.
```

- [ ] **Passo 4: Revisão com o usuário.** Abrir o catálogo no navegador do app, percorrer Overview, Foundations, Components e Layouts, e mostrar screenshots. Ajustes neste momento são feitos **nas telas** (`design-systems/telas/`) seguidos de nova execução do `/extract-ds`, nunca no catálogo.
- [ ] **Passo 5: Verificar o contrato de nomes e a ausência do kit**

```bash
grep -o 'data-component="[^"]*"' design-systems/labmaes/design-system.html | sort -u
grep -rlE 'system\.css|assets/motion|taste-skill' design-systems/labmaes/ || echo "sem referências ao kit"
du -sh design-systems/labmaes
```

Esperado: só nomes da tabela "Contrato de nomes" (ou nomes novos que o usuário aprovar e que então são acrescentados à tabela deste plano); "sem referências ao kit"; o catálogo com poucos MB (fontes e texturas), nunca dezenas.

- [ ] **Passo 6: Commit**

```bash
git add design-systems/telas/index.html design-systems/labmaes
git commit -m "feat(ds): extração 1 do catálogo (ciclo 1)" -m "Refs #<issue da extração 1>"
git push
```

```

### Tarefa C2: Publicar o catálogo em `/design-system/`

**Arquivos:**
- Criar: `tools/eleventy/design-system-publicacao.test.mjs`
- Modificar: `eleventy.config.js` (bloco de passthrough)

- [ ] **Passo 1: Escrever o teste que falha**

`tools/eleventy/design-system-publicacao.test.mjs`:

```js
import test from "node:test";
import assert from "node:assert/strict";
import { access, mkdtemp, readFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import Eleventy from "@11ty/eleventy";

const CATALOGO = "design-systems/labmaes/design-system.html";
const existe = (p) => access(p).then(() => true, () => false);

test(
  "catálogo publicado em /design-system/ e telas fora do site",
  { skip: !(await existe(CATALOGO)) && "catálogo ainda não extraído" },
  async () => {
    const saida = await mkdtemp(path.join(tmpdir(), "labmaes-build-"));
    try {
      const eleventy = new Eleventy(".", saida, { configPath: "eleventy.config.js", quietMode: true });
      await eleventy.write();

      const original = await readFile(CATALOGO, "utf8");
      assert.equal(await readFile(path.join(saida, "design-system/index.html"), "utf8"), original);
      assert.equal(await readFile(path.join(saida, "design-system/design-system.html"), "utf8"), original);
      assert.ok(await existe(path.join(saida, "design-system/styles.css")));
      assert.equal(await existe(path.join(saida, "design-systems")), false, "as telas não podem ir para o site");
    } finally {
      await rm(saida, { recursive: true, force: true });
    }
  },
);
```

- [ ] **Passo 2: Rodar e ver falhar**

Run: `npm run test:site`
Esperado: FAIL em `design-system/index.html` (ENOENT).

- [ ] **Passo 3: Implementar o passthrough**

Em `eleventy.config.js`, depois de `eleventyConfig.addPassthroughCopy("_redirects");`:

```js
  // Design system (Fase 2): o catálogo extraído é publicado sem transformação em /design-system/
  eleventyConfig.addPassthroughCopy({ "design-systems/labmaes": "design-system" });
  eleventyConfig.addPassthroughCopy({ "design-systems/labmaes/design-system.html": "design-system/index.html" });
```

- [ ] **Passo 4: Rodar e ver passar**

Run: `npm run test:site`
Esperado: PASS em todos os testes.

- [ ] **Passo 5: Commit**

```bash
git add eleventy.config.js tools/eleventy/design-system-publicacao.test.mjs
git commit -m "build: publica o catálogo do DS em /design-system/" -m "Refs #<issue da integração>"
git push
```

### Tarefa C3: `noindex` e cache do catálogo por cabeçalho

O `noindex` por cabeçalho sobrevive a qualquer nova extração do catálogo.

**Arquivos:**
- Modificar: `_headers`
- Modificar: `tools/eleventy/design-system-publicacao.test.mjs`

- [ ] **Passo 1: Acrescentar o teste**

No fim de `tools/eleventy/design-system-publicacao.test.mjs`:

```js
test("catálogo tem noindex e no-cache por cabeçalho", async () => {
  const headers = await readFile("_headers", "utf8");
  assert.match(headers, /^\/design-system\/\*\r?\n  X-Robots-Tag: noindex\r?\n  Cache-Control: no-cache$/m);
});
```

- [ ] **Passo 2: Rodar e ver falhar**

Run: `npm run test:site`
Esperado: FAIL no teste "catálogo tem noindex e no-cache por cabeçalho".

- [ ] **Passo 3: Acrescentar o bloco ao `_headers`**

No fim de `_headers`:

```text

# Catálogo do design system: fora dos buscadores e sempre revalidado
/design-system/*
  X-Robots-Tag: noindex
  Cache-Control: no-cache
```

- [ ] **Passo 4: Rodar e ver passar**

Run: `npm run test:site`
Esperado: PASS.

- [ ] **Passo 5: Commit**

```bash
git add _headers tools/eleventy/design-system-publicacao.test.mjs
git commit -m "build: noindex e no-cache para /design-system/"
git push
```

### Tarefa C4: Ferramenta de sincronia catálogo × macros

**Arquivos:**
- Modificar: `package.json` (devDependencies e script `test:ds`)
- Criar: `tools/ds/sincronia.mjs`
- Criar: `tools/ds/sincronia.test.mjs`
- Criar: `tools/ds/renderizar-macro.mjs`
- Criar: `tools/ds/catalogo.test.mjs`

- [ ] **Passo 1: Instalar as dependências**

Run: `npm install --save-dev node-html-parser nunjucks`

Em `package.json`, acrescentar aos `scripts`:

```json
    "test:ds": "node --test tools/ds/*.test.mjs"
```

- [ ] **Passo 2: Escrever os testes unitários que falham**

`tools/ds/sincronia.test.mjs`:

```js
import test from "node:test";
import assert from "node:assert/strict";
import { componentesDoCatalogo, verificarSincronia } from "./sincronia.mjs";

const CATALOGO = `
<section data-ds-section="component" data-component="button" class="ds-doc">
  <h3>Button</h3>
  <button class="button button--primary">Ação</button>
  <button class="button button--secondary">Ação</button>
</section>
<section data-ds-section="component" data-component="card" class="ds-doc">
  <article class="card"><h4 class="card__title">Título</h4></article>
</section>`;

test("lê os componentes e as classes de cada preview", () => {
  const mapa = componentesDoCatalogo(CATALOGO);
  assert.deepEqual([...mapa.keys()], ["button", "card"]);
  assert.deepEqual([...mapa.get("button")].sort(), ["button", "button--primary", "button--secondary"]);
  assert.deepEqual([...mapa.get("card")], ["card"]);
});

test("seção sem preview com a classe-base é erro de contrato", () => {
  const html = '<section data-ds-section="component" data-component="tag"><span class="etiqueta">x</span></section>';
  assert.throws(() => componentesDoCatalogo(html), /tag: nenhum preview com a classe-base "tag"/);
});

test("macros sincronizadas não geram erros", () => {
  const macros = {
    button: '<button class="button button--primary">Ação</button>',
    card: '<article class="card"><h4 class="card__title">T</h4></article>',
  };
  assert.deepEqual(verificarSincronia(componentesDoCatalogo(CATALOGO), (n) => macros[n]), []);
});

test("macro ausente, sem classe-base ou com classe desconhecida gera erro", () => {
  const macros = {
    button: '<button class="button button--fantasma">Ação</button>',
    card: '<div class="cartao">T</div>',
  };
  const erros = verificarSincronia(componentesDoCatalogo(CATALOGO), (n) => {
    if (!(n in macros)) throw new Error("template not found");
    return macros[n];
  });
  assert.deepEqual(erros, [
    'button: classe "button--fantasma" não existe no catálogo',
    'card: a raiz da macro não tem a classe-base "card"',
  ]);
  const semMacro = verificarSincronia(new Map([["tag", new Set(["tag"])]]), () => {
    throw new Error("template not found");
  });
  assert.deepEqual(semMacro, ["tag: sem macro em _includes/ds/tag.njk (template not found)"]);
});
```

- [ ] **Passo 3: Rodar e ver falhar**

Run: `npm run test:ds`
Esperado: FAIL com `Cannot find module './sincronia.mjs'`.

- [ ] **Passo 4: Implementar**

`tools/ds/sincronia.mjs`:

```js
// Sincronia entre o catálogo do design system e as macros Nunjucks (spec da Fase 2, seção 5).
// Contrato: o nome em data-component é a classe-base da raiz do preview; variantes em BEM.
import { parse } from "node-html-parser";

const classesDe = (el) => (el.getAttribute("class") || "").split(/\s+/).filter(Boolean);

// Map<nome, Set<classe>>: todas as classes usadas nas raízes de preview de cada componente
export function componentesDoCatalogo(html) {
  const mapa = new Map();
  for (const secao of parse(html).querySelectorAll('[data-ds-section="component"][data-component]')) {
    const nome = secao.getAttribute("data-component");
    const raizes = secao.querySelectorAll(`.${nome}`);
    if (raizes.length === 0) throw new Error(`${nome}: nenhum preview com a classe-base "${nome}"`);
    const classes = mapa.get(nome) ?? new Set();
    for (const raiz of raizes) for (const c of classesDe(raiz)) classes.add(c);
    mapa.set(nome, classes);
  }
  return mapa;
}

// Lista de erros; vazia quando toda macro bate com o catálogo
export function verificarSincronia(catalogo, renderizar) {
  const erros = [];
  for (const [nome, permitidas] of catalogo) {
    let html;
    try {
      html = renderizar(nome);
    } catch (erro) {
      erros.push(`${nome}: sem macro em _includes/ds/${nome}.njk (${erro.message})`);
      continue;
    }
    const raiz = parse(html.trim()).childNodes.find((n) => n.nodeType === 1);
    const classes = raiz ? classesDe(raiz) : [];
    if (!classes.includes(nome)) {
      erros.push(`${nome}: a raiz da macro não tem a classe-base "${nome}"`);
      continue;
    }
    for (const c of classes) {
      if (!permitidas.has(c)) erros.push(`${nome}: classe "${c}" não existe no catálogo`);
    }
  }
  return erros;
}
```

- [ ] **Passo 5: Rodar e ver passar**

Run: `npm run test:ds`
Esperado: PASS nos quatro testes.

- [ ] **Passo 6: Escrever o renderizador e o teste de integração**

`tools/ds/renderizar-macro.mjs`:

```js
// Renderiza a macro `render` de _includes/ds/<nome>.njk com os parâmetros padrão
import nunjucks from "nunjucks";

const env = new nunjucks.Environment(new nunjucks.FileSystemLoader("_includes"), { autoescape: true });

export function renderizarMacro(nome) {
  return env.renderString(`{% from "ds/${nome}.njk" import render %}{{ render() }}`);
}
```

`tools/ds/catalogo.test.mjs`:

```js
import test from "node:test";
import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import { componentesDoCatalogo, verificarSincronia } from "./sincronia.mjs";
import { renderizarMacro } from "./renderizar-macro.mjs";

const CATALOGO = "design-systems/labmaes/design-system.html";
const temCatalogo = await access(CATALOGO).then(() => true, () => false);

test(
  "toda peça do catálogo tem macro sincronizada em _includes/ds/",
  { skip: !temCatalogo && "catálogo ainda não extraído" },
  async () => {
    const catalogo = componentesDoCatalogo(await readFile(CATALOGO, "utf8"));
    assert.ok(catalogo.size > 0, "nenhum data-component no catálogo");
    assert.deepEqual(verificarSincronia(catalogo, renderizarMacro), []);
  },
);
```

- [ ] **Passo 7: Rodar contra o catálogo v1**

Run: `npm run test:ds`
Esperado: os unitários passam, e `catalogo.test.mjs` **falha** listando `sem macro em _includes/ds/...` para cada componente. Isso é o esperado até a Tarefa E3. Se aparecer `nenhum preview com a classe-base`, o catálogo violou o contrato: corrigir a tela correspondente e reextrair (Tarefa C1, Passo 3).

O `test:ds` **não** entra na CI agora (entra na Tarefa E4), para não deixar a branch vermelha durante o ciclo 2.

- [ ] **Passo 8: Commit**

```bash
git add package.json package-lock.json tools/ds/sincronia.mjs tools/ds/sincronia.test.mjs tools/ds/renderizar-macro.mjs tools/ds/catalogo.test.mjs
git commit -m "test(ds): sincronia entre o catálogo e as macros Nunjucks" -m "Refs #<issue da integração>"
git push
```

### Tarefa C5: Testes de acessibilidade na CI

**Arquivos:**
- Modificar: `package.json`
- Modificar: `.gitignore`
- Criar: `playwright.config.mjs`
- Criar: `tools/a11y/servidor.mjs`
- Criar: `tools/a11y/design-system.spec.mjs`
- Modificar: `.github/workflows/ci.yml`

- [ ] **Passo 1: Instalar as dependências**

```bash
npm install --save-dev @playwright/test @axe-core/playwright
npx playwright install chromium
```

Em `package.json`, acrescentar aos `scripts`:

```json
    "test:a11y": "playwright test"
```

Em `.gitignore`, acrescentar:

```text

# Playwright
test-results/
playwright-report/
```

- [ ] **Passo 2: Servidor estático mínimo**

`tools/a11y/servidor.mjs`:

```js
// Servidor estático mínimo para os testes de acessibilidade (sem dependências).
// Uso: node tools/a11y/servidor.mjs [raiz=_site] [porta=8085]
import { createServer } from "node:http";
import { readFile, stat } from "node:fs/promises";
import path from "node:path";

const [raizArg = "_site", porta = "8085"] = process.argv.slice(2);
const raiz = path.resolve(raizArg);
const tipos = {
  ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript",
  ".svg": "image/svg+xml", ".webp": "image/webp", ".png": "image/png", ".jpg": "image/jpeg",
  ".woff2": "font/woff2", ".json": "application/json",
};

createServer(async (req, res) => {
  let arquivo = path.join(raiz, decodeURIComponent(new URL(req.url, "http://localhost").pathname));
  if (!arquivo.startsWith(raiz)) {
    res.writeHead(403).end();
    return;
  }
  try {
    if ((await stat(arquivo)).isDirectory()) arquivo = path.join(arquivo, "index.html");
    const corpo = await readFile(arquivo);
    res.writeHead(200, { "Content-Type": tipos[path.extname(arquivo)] ?? "application/octet-stream" });
    res.end(corpo);
  } catch {
    res.writeHead(404).end("404");
  }
}).listen(Number(porta), "127.0.0.1");
```

- [ ] **Passo 3: Configuração do Playwright**

`playwright.config.mjs`:

```js
import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "tools/a11y",
  testMatch: "*.spec.mjs",
  use: { baseURL: "http://127.0.0.1:8085" },
  webServer: {
    command: "node tools/a11y/servidor.mjs _site 8085",
    url: "http://127.0.0.1:8085/design-system/",
    reuseExistingServer: !process.env.CI,
  },
  projects: [{ name: "chromium", use: { browserName: "chromium" } }],
});
```

- [ ] **Passo 4: Escrever os testes**

`tools/a11y/design-system.spec.mjs`:

```js
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

const TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"];

async function violacoes(page) {
  const { violations } = await new AxeBuilder({ page }).withTags(TAGS).analyze();
  return violations.map((v) => `${v.id} (${v.nodes.length}): ${v.help} — ${v.nodes[0]?.target.join(" ")}`);
}

test("catálogo sem violações WCAG 2.2 AA", async ({ page }) => {
  await page.goto("/design-system/");
  expect(await violacoes(page)).toEqual([]);
});

test("catálogo sem violações com movimento reduzido", async ({ page }) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/design-system/");
  expect(await violacoes(page)).toEqual([]);
});

test("catálogo sem rolagem horizontal em 320 px", async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 800 });
  await page.goto("/design-system/");
  const excesso = await page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  );
  expect(excesso).toBeLessThanOrEqual(0);
});
```

- [ ] **Passo 5: Conferir se o catálogo esconde seções**

Abrir `/design-system/` no navegador do app. Se a barra superior do catálogo **esconder** as outras seções (abas) em vez de rolar até elas, o axe só verá a seção visível. Nesse caso, nos dois primeiros testes, trocar a análise única por um laço que clica em cada item da barra superior (`page.getByRole("navigation").getByRole("link")`) e acumula as violações de cada seção.

- [ ] **Passo 6: Rodar localmente**

```bash
npm run build
npm run test:a11y
```

Esperado: os três testes rodam. As violações encontradas são corrigidas **nas telas** (`design-systems/telas/`) e reextraídas, nunca no catálogo. Se forem muitas para resolver agora, registrar a lista numa issue e seguir: o job deve estar verde antes da Tarefa F1.

- [ ] **Passo 7: Acrescentar o job à CI**

No fim de `.github/workflows/ci.yml`:

```yaml

  acessibilidade:
    name: Acessibilidade do design system
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7

      - uses: actions/setup-node@v7
        with:
          node-version-file: .nvmrc
          cache: npm

      - run: npm ci

      - name: Build do Eleventy
        run: npm run build

      - name: Navegador do Playwright
        run: npx playwright install --with-deps chromium

      - name: axe (WCAG 2.2 AA), movimento reduzido e 320 px
        run: npm run test:a11y
```

- [ ] **Passo 8: Commit e conferir a CI**

```bash
git add package.json package-lock.json .gitignore playwright.config.mjs tools/a11y .github/workflows/ci.yml
git commit -m "ci: testes de acessibilidade do design system (axe + Playwright)" -m "Refs #35"
git push
gh pr checks
```

Esperado: os jobs "Build e validação de conteúdo" e "Acessibilidade do design system" aparecem no PR de rascunho.

### Tarefa C6: Consulta informal à coordenação

- [ ] **Passo 1: Conferir o preview.** Abrir `<URL de preview>/design-system/` (Tarefa A1, Passo 5) e confirmar que o catálogo v1 carrega com fontes e imagens.
- [ ] **Passo 2: Pedir ao usuário** que mostre o preview à Profa. Mara Rúbia como **consulta informal**, deixando claro que não é a aprovação final.
- [ ] **Passo 3: Registrar** as observações dela num comentário da issue "Extração 1 do catálogo" e fechar a issue. Observações de fundo voltam como ajustes nas telas 01 a 03 antes do ciclo 2.


---

## Parte D — Ciclo 2: o meio

Cada tela segue a Tarefa B0, com uma regra a mais na construção:

> Ligar também `../../labmaes/styles.css` (catálogo v1), antes do `marca/marca.css`, e reutilizar as classes e os componentes do catálogo; não criar variantes paralelas de peças que já existem. O que for novo usa o kit e a camada de marca, como no ciclo 1.

Como o `/extract-ds` só lê as telas, `preparar-tela.sh` não copia o catálogo: o caminho relativo `../../labmaes/` funciona porque o verificador da skill serve a página pela pasta. Se o verificador não encontrar o CSS do catálogo (FAIL de fonte ou de estilo ausente nas capturas), rodar os comandos do B0, Passo 6, com `--root ../..` apontando para `design-systems/` e a URL `telas/<slug>/index.html`.

### Tarefa D1: Tela 04 — Página de item

- **slug:** `04-item` · **categoria:** "produção do repositório do LabMAES" · **ação principal:** "Baixar o documento"
- **Texto do `/plan-screen` (opcional):**

```text
/plan-screen Página de uma produção do repositório do LabMAES, desktop e mobile. Parte do catálogo v1 em labmaes-site/design-systems/labmaes/ (reutilizar componentes). Página de leitura: estrutura domina, sem momento. Breadcrumb, tipo com ícone e rótulo, título, autoria (pessoas relacionadas), metadados (ano, tipo, idioma, projeto, evento), resumo em leitura longa, documento para baixar (PDF, tamanho, idioma), imagem com legenda e crédito, produções relacionadas.
```

- **Regras:** EX-3 (segue o conteúdo), EX-4 (legenda, crédito e autoria sob a imagem), EX-8 (sem momento). Componentes esperados: `breadcrumb`, `metadata-list`, `relation-list`, `document-download`, `prose`. Conteúdo de exemplo com `data-assumed`.

### Tarefa D2: Tela 05 — Sobre

- **slug:** `05-sobre` · **categoria:** "laboratório de pesquisa, ensino e extensão em Moda, Artes, Ensino e Sociedade" · **ação principal:** "Conhecer a equipe"
- **Texto do `/plan-screen` (opcional):**

```text
/plan-screen Página institucional "Sobre" do LabMAES, desktop e mobile. Parte do catálogo v1 em labmaes-site/design-systems/labmaes/. Hero com composição de módulos da marca; o que é o laboratório e a estratégia dos saberes sensíveis (Moda, Artes, Ensino e Sociedade com peso igual); linhas de atuação; coordenação; instituições parceiras; documentos institucionais. Textos a partir da página /sobre/ do site atual.
```

- **Regras:** um momento permitido (EX-8); "uma seção por tela" vale (institucional). Textos de `sobre/index.njk` do site atual.

### Tarefa D3: Tela 06 — Edição de evento (Caminhos 2026)

- **slug:** `06-evento` · **categoria:** "seminário acadêmico Caminhos do Contemporâneo, 7ª edição" · **ação principal:** "Ver a programação"
- **Texto do `/plan-screen` (opcional):**

```text
/plan-screen Página da 7ª edição (2026) do seminário Caminhos do Contemporâneo, desktop e mobile, com a submarca do evento: data-brand="caminhos" troca a tipografia para Cormorant Garamond + DM Mono e os acentos para tijolo #8B3A2A, azul-acinzentado #506A80 e azul-petróleo #042A34 sobre bege #ECE7DF, mantendo os componentes do catálogo v1. Hero com a arte do evento, datas (18 a 23 de agosto de 2026), programação em acordeão por dia, oficinas, mostra audiovisual, anais, realizadores e apoiadores. Conteúdo real de _data/programacao.json.
```

- **Regras:**
  - A submarca entra como um bloco `[data-brand="caminhos"] { … }` no `marca.css` (só tokens de fonte e acento); acrescentar `@font-face` da Cormorant Garamond e da DM Mono com arquivos em `assets/fonts/` (a DM Mono já existe; a Cormorant Garamond é OFL: pedir ao usuário a aprovação do download, com nome, origem e tamanho) e incluí-los no `preparar-tela.sh`.
  - A arte do evento vem de `assets/banners/` do site (é do evento, não é foto de banco).
  - Um momento permitido (EX-8); programação sem animação além do acordeão (200–250 ms).

### Tarefa D4: Tela 07 — 404

- **slug:** `07-404` · **categoria:** "página não encontrada do site do LabMAES" · **ação principal:** "Voltar para o início"
- **Texto do `/plan-screen` (opcional):**

```text
/plan-screen Página 404 do site do LabMAES, desktop e mobile. Parte do catálogo v1 em labmaes-site/design-systems/labmaes/. Uma composição de módulos da marca com humor leve (um módulo fora do encaixe), mensagem curta, busca e links para Início, Produções e Contato.
```

- **Regras:** um momento permitido (EX-8), com elasticidade leve só nos módulos decorativos (spec 2.5); a composição que comunica algo ganha `alt` curto; pode usar uma imagem de apoio gerada (B0, Passo 4).

---

## Parte E — Extração final, integração e documentação

### Tarefa E1: Extração final

Bloqueada pela Tarefa A5 (licença da Thunder resolvida).

- [ ] **Passo 1: Completar o hub**

Em `design-systems/telas/index.html`, a lista passa a ser:

```html
    <ol>
      <li><a href="01-home/index.html">Home (responsiva: desktop e mobile)</a></li>
      <li><a href="03-repositorio/index.html">Listagem do repositório</a></li>
      <li><a href="04-item/index.html">Página de item</a></li>
      <li><a href="05-sobre/index.html">Sobre</a></li>
      <li><a href="06-evento/index.html">Edição de evento, submarca Caminhos</a></li>
      <li><a href="07-404/index.html">404</a></li>
    </ol>
```

- [ ] **Passo 2: Garantir as cópias locais**

```bash
for s in 01-home 03-repositorio 04-item 05-sobre 06-evento 07-404; do tools/ds/preparar-tela.sh $s; done
```

- [ ] **Passo 3: O usuário invoca o `/extract-ds`** com o mesmo texto da Tarefa C1, Passo 3, trocando a lista de telas pelas seis acima e acrescentando: "(6) documente `data-brand="caminhos"` em Foundations; (7) esta é a extração final e substitui a extração 1 por inteiro."
- [ ] **Passo 4: Revisão com o usuário**, como na Tarefa C1, Passo 4. Ajustes de fundo voltam às telas e a uma nova extração.
- [ ] **Passo 5: Verificar** como na Tarefa C1, Passo 5.
- [ ] **Passo 6: Commit**

```bash
git add design-systems/telas/index.html design-systems/labmaes
git commit -m "feat(ds): extração final do catálogo" -m "Refs #<issue da extração final>, #26"
git push
```

A partir daqui, ajustes finos podem ser feitos direto no catálogo.

### Tarefa E2: Guia da IA no catálogo

**Arquivos:**
- Copiar: `design-systems/marca/ia/{prompt-fixo.md,log.md}` → `design-systems/labmaes/assets/textura/`
- Copiar: `design-systems/marca/textura/*.webp` → `design-systems/labmaes/assets/textura/` (se a extração ainda não copiou)
- Modificar: `design-systems/labmaes/design-system.html` (Foundations → Textura)

- [ ] **Passo 1: Copiar o material**

```bash
mkdir -p design-systems/labmaes/assets/textura
cp design-systems/marca/ia/prompt-fixo.md design-systems/marca/ia/log.md design-systems/labmaes/assets/textura/
cp -n design-systems/marca/textura/*.webp design-systems/labmaes/assets/textura/ 2>/dev/null || true
```

- [ ] **Passo 2: Acrescentar ao catálogo** uma subseção "Imagens geradas por IA" dentro de Foundations → Textura, no padrão de marcação das outras subseções do catálogo (sem `style=""` nem `<style>` inline), com:
  - quando usar (só texturas chapadas dentro de módulos e imagens de apoio; fotos de pessoas, eventos e acervo são sempre reais);
  - as texturas aprovadas (`assets/textura/*.webp`, `alt=""` porque são decorativas, e legenda com o material);
  - o checklist de aprovação (copiado de `prompt-fixo.md`);
  - os parâmetros fixos (Nano Banana Pro, 1K, WebP, orçamento de peso);
  - links para `assets/textura/prompt-fixo.md` e `assets/textura/log.md`.
- [ ] **Passo 3: Conferir** que o `test:ds` continua verde (`npm run test:ds`) e que o catálogo não ganhou `style=""`:

```bash
grep -c 'style="' design-systems/labmaes/design-system.html
```

Esperado: `0`.

- [ ] **Passo 4: Commit**

```bash
git add design-systems/labmaes
git commit -m "docs(ds): guia das imagens geradas no catálogo" -m "Refs #<issue da camada de marca>"
git push
```

```

### Tarefa E3: Macros dos componentes

**Arquivos:**
- Criar: `_includes/ds/<nome>.njk` para cada `data-component` do catálogo

- [ ] **Passo 1: Listar os componentes**

Run: `npm run test:ds`
Esperado: FAIL em `catalogo.test.mjs`, com uma linha `sem macro` por componente. Essa é a lista de trabalho.

- [ ] **Passo 2: Escrever uma macro por componente**, sempre copiando o markup do preview **padrão** do catálogo e trocando só o texto e os atributos variáveis por parâmetros com valor padrão. Exemplo, supondo que o catálogo tenha `<a class="button button--primary" href="#">Conheça o laboratório</a>`:

`_includes/ds/button.njk`:

```njk
{#- Botão do DS. Variantes: primary (padrão), secondary. Fonte: catálogo, seção "button". -#}
{% macro render(p = {}) -%}
{%- set variante = p.variante or "primary" -%}
{%- if p.href -%}
<a class="button button--{{ variante }}" href="{{ p.href }}">{{ p.texto or "Ação" }}</a>
{%- else -%}
<button class="button button--{{ variante }}" type="{{ p.tipo or 'button' }}">{{ p.texto or "Ação" }}</button>
{%- endif -%}
{%- endmacro %}
```

Regras:
- a macro sempre se chama `render` e aceita um único objeto `p`;
- sem `p`, ela renderiza o preview padrão (é isso que o teste usa);
- classes só do catálogo; nenhuma classe ou estilo novo;
- componentes compostos chamam as macros dos componentes internos (`{% from "ds/button.njk" import render as button %}`).
- [ ] **Passo 3: Rodar até passar**

Run: `npm run test:ds`
Esperado: PASS em todos os testes, incluindo `catalogo.test.mjs`.

- [ ] **Passo 4: Commit** (um commit por grupo coerente de macros, por exemplo navegação, conteúdo, repositório, evento)

```bash
git add _includes/ds/
git commit -m "feat(ds): macros Nunjucks dos componentes do catálogo" -m "Refs #<issue da integração>"
git push
```

### Tarefa E4: Sincronia na CI

**Arquivos:**
- Modificar: `.github/workflows/ci.yml` (job `build`)

- [ ] **Passo 1: Acrescentar o passo** ao job `build`, logo depois de "Testes do build do site":

```yaml
      - name: Sincronia do design system (catálogo × macros)
        run: npm run test:ds --if-present
```

- [ ] **Passo 2: Commit e conferir a CI**

```bash
git add .github/workflows/ci.yml
git commit -m "ci: sincronia do design system"
git push
gh pr checks
```

Esperado: todos os jobs verdes.

### Tarefa E5: Layout v2

**Arquivos:**
- Criar: `tools/eleventy/layout-v2.test.mjs`
- Criar: `_includes/layout-v2.njk`

- [ ] **Passo 1: Escrever o teste que falha**

`tools/eleventy/layout-v2.test.mjs`:

```js
import test from "node:test";
import assert from "node:assert/strict";
import nunjucks from "nunjucks";

const env = new nunjucks.Environment(new nunjucks.FileSystemLoader("_includes"), { autoescape: true });
const contexto = (extra = {}) => ({
  content: '<main id="conteudo"><p>Teste</p></main>',
  site: { url: "https://exemplo.org", description: "Descrição" },
  page: { url: "/teste/" },
  buildId: "t1",
  title: "Teste",
  ...extra,
});

test("layout v2 carrega só o design system", () => {
  const html = env.render("layout-v2.njk", contexto());
  assert.match(html, /<link rel="stylesheet" href="\/design-system\/styles\.css\?v=t1">/);
  assert.match(html, /<script src="\/design-system\/interactions\.js\?v=t1" defer><\/script>/);
  assert.doesNotMatch(html, /\/css\/(tokens|components)\.css|\/js\/main\.js/);
});

test("submarca opcional", () => {
  assert.match(env.render("layout-v2.njk", contexto()), /<body>/);
  assert.match(env.render("layout-v2.njk", contexto({ brand: "caminhos" })), /<body data-brand="caminhos">/);
});

test("layout v2 tem skip-link, cabeçalho e rodapé do DS", () => {
  const html = env.render("layout-v2.njk", contexto());
  assert.match(html, /class="skip-link[ "]/);
  assert.match(html, /class="site-header[ "]/);
  assert.match(html, /class="site-footer[ "]/);
});
```

- [ ] **Passo 2: Rodar e ver falhar**

Run: `npm run test:site`
Esperado: FAIL com `template not found: layout-v2.njk`.

- [ ] **Passo 3: Implementar**

`_includes/layout-v2.njk`:

```njk
{%- from "ds/skip-link.njk" import render as skipLink -%}
{%- from "ds/site-header.njk" import render as siteHeader -%}
{%- from "ds/site-footer.njk" import render as siteFooter -%}
<!doctype html>
<html lang="{{ lang or 'pt-BR' }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% if title and title != 'LabMAES' %}{{ title }} | LabMAES{% else %}LabMAES{% endif %}</title>
  <meta name="description" content="{{ description or site.description }}">
  <link rel="canonical" href="{{ site.url }}{{ page.url }}">
  {%- if noindex %}
  <meta name="robots" content="noindex">
  {%- endif %}
  <meta property="og:title" content="{% if title and title != 'LabMAES' %}{{ title }} | LabMAES{% else %}LabMAES{% endif %}">
  <meta property="og:description" content="{{ description or site.description }}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{{ site.url }}{{ page.url }}">
  <meta property="og:locale" content="pt_BR">
  <link rel="stylesheet" href="/design-system/styles.css?v={{ buildId }}">
  <link rel="icon" href="/assets/logos/logo-labmaes-vermelho.svg" type="image/svg+xml">
</head>
<body{% if brand %} data-brand="{{ brand }}"{% endif %}>
  {{ skipLink({ href: "#conteudo" }) }}
  {{ siteHeader() }}
  {{ content | safe }}
  {{ siteFooter() }}
  <script src="/design-system/interactions.js?v={{ buildId }}" defer></script>
</body>
</html>
```

Se o catálogo não tiver `interactions.js` (nenhum comportamento extraído), remover a linha do `<script>` e a asserção correspondente no teste. Se o preload de fontes estiver documentado no catálogo, copiar as linhas `<link rel="preload">` de lá.

- [ ] **Passo 4: Rodar e ver passar**

Run: `npm run test:site && npm run build`
Esperado: PASS, e o build não muda nenhuma página pública. Conferir que nenhum arquivo em `*.njk` de página usa `layout-v2`:

```bash
grep -rl "layout-v2" --include="*.njk" --include="*.md" --include="*.json" . | grep -v "^./_includes/\|^./docs/\|node_modules"
```

Esperado: nenhuma saída.

- [ ] **Passo 5: Commit**

```bash
git add _includes/layout-v2.njk tools/eleventy/layout-v2.test.mjs
git commit -m "feat(ds): layout v2, que carrega só o design system" -m "Refs #<issue da integração>"
git push
```

### Tarefa E6: Revisão do movimento

- [ ] **Passo 1: Câmera lenta.** No navegador do app, abrir `/design-system/` (build local) e rodar, no console, `document.getAnimations().forEach(a => a.playbackRate = 0.25)` antes de disparar cada animação documentada. Conferir origem do `transform`, sincronia entre opacidade e transformação, e se nenhuma animação de interface passa de 300 ms.
- [ ] **Passo 2: Movimento reduzido.** Pedir ao usuário que abra o catálogo no Chrome com o DevTools (Rendering → "Emulate CSS media feature prefers-reduced-motion: reduce") e confira se só sobram transições de opacidade e cor. O teste da Tarefa C5 cobre só a acessibilidade, não a ausência de movimento.
- [ ] **Passo 3: Olhos descansados.** Pedir ao usuário que reveja as animações no dia seguinte. Ajustes vão para o catálogo (permitido depois da extração final) e são reconferidos pelo `test:ds` e pelo job de acessibilidade.
- [ ] **Passo 4: Commit** dos ajustes, se houver:

```bash
git add design-systems/labmaes _includes/ds
git commit -m "fix(ds): ajustes de movimento após revisão"
git push
```

### Tarefa E7: Documentação e issues

**Arquivos:**
- Modificar: `docs/roadmap.md`
- Modificar: `docs/architecture/README.md`
- Modificar: `README.md` (seção de estrutura do repositório, se existir)

- [ ] **Passo 1: Roadmap.** A linha da Fase 2 passa a "aguardando aprovação da coordenação".
- [ ] **Passo 2: README da arquitetura.** Trocar o estado da Fase 2 por "**implementada, aguardando aprovação da coordenação** (ADR 0010)".
- [ ] **Passo 3: README do repositório.** Se houver uma seção sobre a estrutura de pastas, acrescentar `design-systems/` (telas e catálogo) e os comandos `npm run test:ds` e `npm run test:a11y`.
- [ ] **Passo 4: Fechar as issues cumpridas**: as das seis telas, a da extração final, a da camada de marca e guia da IA, a da integração, a da licença da Thunder, a #26, a #27 e a #35 (a #34 fecha com o merge, porque o catálogo só fica público então).
- [ ] **Passo 5: Commit**

```bash
git add docs/roadmap.md docs/architecture/README.md README.md
git commit -m "docs: Fase 2 implementada, aguardando aprovação da coordenação"
git push
```

---

## Parte F — Aprovação da coordenação

### Tarefa F1: Pacote para a coordenadora

Pré-condição: critérios 1 a 7 da seção 9 da spec cumpridos e CI verde no PR da fase.

- [ ] **Passo 1: Conferir o preview.** Abrir `<URL de preview>/design-system/` Conferir fontes, texturas e console sem erros. As telas não são publicadas (o kit fica fora do git); a coordenação vê o catálogo e as capturas.
- [ ] **Passo 2: Escrever o resumo** em linguagem não técnica, como um Claude Doc (skill `anthropic-skills:docs`), com: o conceito (site novo com a mesma marca), cor, tipografia, forma, textura como detalhe e movimento, as capturas das seis telas (desktop e mobile) e o link do catálogo. Mostrar ao usuário antes de qualquer envio.
- [ ] **Passo 3: O usuário envia** o pacote à Profa. Mara Rúbia. Quem executa o plano não envia mensagens em nome do usuário.

### Tarefa F2: Pedidos de mudança (se houver)

- [ ] **Passo 1:** Classificar cada pedido: fundamento (Foundations), componente, tela ou direção de arte.
- [ ] **Passo 2:** Ajustes de fundamento ou de tela voltam às telas e a uma nova extração (Tarefa E1, Passos 2–5), seguidos de E2–E5 se o catálogo mudar. Ajustes finos vão direto ao catálogo.
- [ ] **Passo 3:** Rodar `npm run test:site && npm run test:ds && npm run build && npm run test:a11y` e reenviar o pacote (Tarefa F1).

### Tarefa F3: Registrar a aprovação e mesclar

**Arquivos:**
- Criar: `docs/superpowers/reviews/<AAAA-MM-DD>-fase-2-aprovacao-coordenacao.md` (data da resposta)

- [ ] **Passo 1: Registrar**

```markdown
# Fase 2 — Aprovação da coordenação

- **Data da resposta:** <AAAA-MM-DD>
- **Coordenadora:** Profa. Mara Rúbia Sant'Anna
- **Pacote enviado em:** <AAAA-MM-DD>, com o preview <URL> e o resumo <link do Claude Doc>
- **Resultado:** aprovado | aprovado com ressalvas

## Ressalvas e encaminhamentos

- <ressalva> → <issue ou "atendida no commit abc1234">
```

(Os campos entre `< >` são preenchidos com a resposta real; o arquivo só é criado quando ela chega.)

- [ ] **Passo 2: Comentar na issue "Aprovação da coordenação (Fase 2)"** com o resultado e o link do registro, e fechá-la.
- [ ] **Passo 3: Commit**

```bash
git add docs/superpowers/reviews/
git commit -m "docs: aprovação da coordenação da Fase 2"
git push
```

- [ ] **Passo 4: Tirar o PR de rascunho e pedir ao usuário que mescle**

```bash
gh pr ready
gh pr edit --title "Fase 2 — Design system" --body "Design system da Fase 2, aprovado pela coordenação em <data> (registro em docs/superpowers/reviews/). Publica o catálogo em /design-system/ (noindex); nenhuma página pública muda.

Closes #34"
```
