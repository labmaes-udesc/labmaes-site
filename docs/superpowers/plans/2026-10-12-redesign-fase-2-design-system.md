# Redesign Fase 2: Design system — plano de implementação

> **Para agentes:** SUB-SKILL OBRIGATÓRIA: use superpowers:subagent-driven-development (recomendado) ou superpowers:executing-plans para executar este plano tarefa por tarefa. Os passos usam checkbox (`- [ ]`) para acompanhamento.
>
> **Atenção:** as Partes B, D e parte da C e da E são trabalho de design com gates humanos. As skills `/plan-screen`, `/to-img`, `/img-to-html`, `/to-wireframe` e `/extract-ds` têm `disable-model-invocation: true`, então **quem as invoca é o usuário**, digitando o comando no chat. Os textos de invocação estão prontos neste plano. Essas tarefas não podem ser delegadas a subagentes, e quem executa nunca avança um gate sem aprovação explícita do usuário.

**Objetivo:** produzir o design system do LabMAES como catálogo HTML (fonte da verdade), integrá-lo ao Eleventy sem alterar páginas públicas e obter a aprovação da coordenadora antes de qualquer publicação.

**Arquitetura:** as telas-chave nascem como mocks PNG (`/plan-screen` + `/to-img`), viram HTML puro (`/img-to-html`) e alimentam o `/extract-ds`, que gera `design-systems/labmaes/` (catálogo, `styles.css`, `interactions.js`, `assets/`). O Eleventy copia essa pasta sem transformação para `/design-system/`; o site a consome por um `layout-v2.njk` e por macros Nunjucks em `_includes/ds/`, vigiadas por um teste de sincronia. A acessibilidade do catálogo é verificada na CI com Playwright e axe. Todo o trabalho fica na branch `redesign/fase-2-design-system` até a aprovação da coordenação.

**Stack:** Eleventy 3, Nunjucks, CSS e JS puros, Node 22 (`node --test`), `node-html-parser`, `nunjucks`, `@playwright/test`, `@axe-core/playwright`, OpenRouter (Nano Banana Pro) com `uv`, GitHub Actions, Cloudflare (previews de branch).

**Spec:** [`docs/superpowers/specs/2026-10-07-redesign-fase-2-design-system-design.md`](../specs/2026-10-07-redesign-fase-2-design-system-design.md). Em caso de divergência, a spec prevalece sobre este plano, e um ADR prevalece sobre ambos.

---

## Pré-requisitos do ambiente (máquina Windows do usuário)

O Avast intercepta o HTTPS. Todo comando que chama a API de imagens precisa, no mesmo shell:

```bash
unset SSLKEYLOGFILE
export SSL_CERT_FILE="$NODE_EXTRA_CA_CERTS" REQUESTS_CA_BUNDLE="$NODE_EXTRA_CA_CERTS"
```

e o `uv` precisa de `--system-certs`. O wrapper da Tarefa A4 já faz isso. A chave `OPENROUTER_API_KEY` está em `C:\Users\Windows 10\.env`. Saldo em 2026-10-07: cerca de US$ 5,40.

O `npx playwright install chromium` também passa pelo Avast. Se falhar por certificado, rodar com `NODE_EXTRA_CA_CERTS` já definido (é o padrão nesta máquina) e, se ainda falhar, avisar o usuário em vez de desativar verificações.

## Mapa de arquivos

| Arquivo | Responsabilidade | Tarefa |
|---|---|---|
| `docs/architecture/adr/0010-aprovacao-coordenacao.md` | Regra: o redesign só vai ao ar com aprovação da coordenadora | A2 |
| `docs/architecture/README.md` | Estado do redesign e lista de ADRs | A2, E7 |
| `docs/roadmap.md` | Referência do plan e estado da fase | A1, E7 |
| `eleventy.config.js` | Ignorar `design-systems/**`; copiar o catálogo para `/design-system/`; telas só no preview da fase | A3, C2 |
| `design-systems/materia/prompt-mestre.md` | Prompt-mestre da direção de arte (rascunho de trabalho) | A4 |
| `design-systems/materia/log.md` | Log das gerações aprovadas | A4 |
| `tools/ds/gerar-imagem.sh` | Gera imagem com parâmetros fixos e contorno do Avast | A4 |
| `tools/ds/montar-prancha.py` | Junta as imagens-âncora numa prancha única (o script de imagem aceita uma só entrada) | B2 |
| `design-systems/telas/0N-*/` | Saída do `/img-to-html` por tela | B, D |
| `design-systems/telas/index.html` | Hub que liga as telas; entrada do `/extract-ds` | C1 |
| `design-systems/labmaes/` | Saída do `/extract-ds` = fonte da verdade | C1, E1 |
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

---

## Contrato de nomes dos componentes

O `/extract-ds` marca cada componente com `data-ds-section="component"` e `data-component="<nome>"` na seção do catálogo, e as variantes como modificadores BEM (`card--default`). Este plano acrescenta duas regras, que vão nos textos de invocação:

1. **O nome do componente é a sua classe-base.** A seção `data-component="card"` contém um preview cuja raiz tem a classe `card`. Variantes usam `card--<variante>`, e elementos internos usam `card__<parte>`.
2. **Nomes canônicos**, usados sempre que a peça existir numa tela (nenhuma peça é criada sem evidência):

| Nome | Peça |
|---|---|
| `skip-link` | Link "Pular para o conteúdo" |
| `site-header` | Cabeçalho com logo e navegação |
| `site-nav` | Navegação principal (desktop e mobile) |
| `site-footer` | Rodapé |
| `hero` | Abertura de página (com `data-intensity`) |
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

---

## Parte A — Preparação

### Tarefa A1: Mesclar spec e plan na `main` e abrir a branch da fase

A spec e o plan são documentação (`docs/` é ignorado pelo Eleventy) e podem ir para a `main` sem afetar o site. O código e o design da fase não.

**Arquivos:**
- Modificar: `docs/roadmap.md` (linha da Fase 2)

- [ ] **Passo 1: Acrescentar o plan na referência do roadmap**

Na linha da Fase 2 de `docs/roadmap.md`, a coluna "Referência" passa a ser:

```markdown
| 2 | Design system | em andamento | [spec](superpowers/specs/2026-10-07-redesign-fase-2-design-system-design.md), [plan](superpowers/plans/2026-10-12-redesign-fase-2-design-system.md) |
```

- [ ] **Passo 2: Commit, push e PR da documentação**

```bash
git add docs/roadmap.md docs/superpowers/plans/2026-10-12-redesign-fase-2-design-system.md
git commit -m "docs: plan da Fase 2 (design system)"
git push -u origin docs/fase-2-spec-design-system
gh pr create --base main --title "docs: spec e plan da Fase 2 (design system)" --body "Spec e plan da Fase 2. Só documentação; nenhuma mudança no site.

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
- Data: 2026-10-12
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

### Tarefa A4: Ferramenta de geração e direção de arte inicial

**Arquivos:**
- Criar: `tools/ds/gerar-imagem.sh`
- Criar: `design-systems/materia/prompt-mestre.md`
- Criar: `design-systems/materia/log.md`

A pasta `design-systems/materia/` é a área de trabalho da direção de arte até a extração final. Na Tarefa E2, o conteúdo aprovado é copiado para `design-systems/labmaes/assets/materia/`, como a spec pede, sem editar o catálogo entre as extrações.

- [ ] **Passo 1: Escrever o wrapper**

`tools/ds/gerar-imagem.sh`:

```bash
#!/usr/bin/env bash
# Gera uma imagem com os parâmetros fixos da direção de arte (spec da Fase 2, seção 3).
# Uso: tools/ds/gerar-imagem.sh <saida.png> <arquivo-de-prompt> [imagem-de-entrada] [resolucao] [proporcao]
set -euo pipefail

saida="$1"; arquivo_prompt="$2"; entrada="${3:-}"; resolucao="${4:-1K}"; proporcao="${5:-16:9}"
script="$HOME/.agents/skills/openrouter-img/scripts/generate_image.py"
mestre="design-systems/materia/prompt-mestre.md"

# Contorno do Avast (intercepta HTTPS) e do bug OPENSSL_Uplink do Python no Windows
unset SSLKEYLOGFILE
if [ -n "${NODE_EXTRA_CA_CERTS:-}" ]; then
  export SSL_CERT_FILE="$NODE_EXTRA_CA_CERTS" REQUESTS_CA_BUNDLE="$NODE_EXTRA_CA_CERTS"
fi

# O prompt final é o bloco "PROMPT" do mestre + o prompt específico
prompt="$(tr -d '' < "$mestre" | sed -n '/^```prompt$/,/^```$/p' | sed '1d;$d') $(tr -d '' < "$arquivo_prompt")"

args=(--model pro --resolution "$resolucao" --aspect-ratio "$proporcao" --filename "$saida" --prompt "$prompt")
[ -n "$entrada" ] && args+=(--input-image "$entrada")

mkdir -p "$(dirname "$saida")"
resultado="$(uv run --system-certs "$script" "${args[@]}" 2>&1 | tail -3)"
echo "$resultado"

custo="$(printf '%s\n' "$resultado" | sed -n 's/.*usage.cost): \(.*\)$/\1/p')"
printf '\n| %s | `%s` | `%s` | `%s` | %s | %s |\n' \
  "$(date +%Y-%m-%d)" "$saida" "$arquivo_prompt" "${entrada:--}" "$resolucao" "${custo:-?}" \
  >> design-systems/materia/log.md
```

Run: `chmod +x tools/ds/gerar-imagem.sh`

- [ ] **Passo 2: Escrever o prompt-mestre**

`design-systems/materia/prompt-mestre.md`:

````markdown
# Prompt-mestre da matéria (direção de arte, spec da Fase 2, seção 3)

Todo prompt de imagem começa por este bloco. O prompt específico só descreve a composição.

```prompt
Tactile handmade still life photographed straight-on, for the website of LabMAES, a university research lab in Fashion, Arts, Education and Society. Materials, always balanced with equal weight: matte modeling clay (plasticine) with visible fingerprints and soft tool marks; slightly crumpled cotton paper; matte toy building blocks; woven fabric with visible weave. Shapes come from a modular vocabulary only: rounded squares, quarter circles and arches. Strict palette, no other hues: orange #F44F21, deep red #B10000, navy blue #302A66, ice white #F0F0FF, dark green #00523C, soft pink #F4BEBE. Soft diffuse light from the top left, short soft shadows, camera frontal or at 30 degrees, background of ice-white paper. Calm negative space reserved for interface text. Forbidden: glossy or plastic sheen, colors outside the palette, invented letters, words or logos, hands, people.
```

## Checklist de aprovação (cada imagem)

- [ ] Paleta conferida com conta-gotas (nenhuma cor fora dos seis hexadecimais, além das sombras).
- [ ] Nenhum texto, letra ou logo inventado.
- [ ] Os quatro materiais equilibrados no conjunto das imagens.
- [ ] Luz e ângulo iguais aos das âncoras.
- [ ] Área lisa reservada onde o texto da interface vai ficar.
- [ ] Peso final em WebP dentro do orçamento (hero da home < ~200 KB no mobile; demais < ~120 KB).
````

- [ ] **Passo 3: Criar o log**

`design-systems/materia/log.md`:

```markdown
# Log das gerações

Uma linha por geração feita com `tools/ds/gerar-imagem.sh`. Gerações aprovadas recebem ✅ na
última coluna, à mão, depois da aprovação.

| Data | Saída | Prompt | Entrada | Resolução | Custo (US$) |
|---|---|---|---|---|---|
```

- [ ] **Passo 4: Testar o wrapper com uma geração barata**

```bash
printf 'A single rounded square of orange modeling clay resting on ice-white paper.' > design-systems/materia/teste.txt
tools/ds/gerar-imagem.sh ../redesign-fase2-referencias/teste-wrapper.png design-systems/materia/teste.txt "" 1K 1:1
tail -2 design-systems/materia/log.md
rm design-systems/materia/teste.txt
```

Esperado: `Image saved to: ...teste-wrapper.png`, custo em torno de US$ 0,13 e uma linha nova no log. Apagar essa linha de teste do log.

- [ ] **Passo 5: Commit**

```bash
git add tools/ds/gerar-imagem.sh design-systems/materia/
git commit -m "feat(ds): wrapper de geração e prompt-mestre da direção de arte"
git push
```

### Tarefa A5: Licença da Thunder (ação do usuário)

- [ ] **Passo 1: Pedir ao usuário** que verifique com a coordenação ou com o designer do Manual de Marca se o LabMAES tem licença da Thunder (Thunder-BoldHC) **para uso web** (`@font-face`), e com quais idiomas e caracteres.
- [ ] **Passo 2: Registrar o resultado** num comentário da issue "Licença da Thunder" (Tarefa A6).
  - Se houver licença: salvar o arquivo da licença em `assets/fonts/Thunder-LICENSE.txt` (ou `.pdf`) e fazer o commit.
  - Se não houver: registrar que a Poppins Black substitui a Thunder. Nas invocações das Partes B e D, trocar "Thunder" por "Poppins Black".

Essa tarefa pode correr em paralelo com o resto. Ela só bloqueia a extração final (E1).

### Tarefa A6: Reorganizar as issues da milestone

- [ ] **Passo 1: Comentar e fechar as issues absorvidas**

```bash
gh issue comment 33 --body "Substituída pela spec da Fase 2: os protótipos passam a ser mocks PNG (/plan-screen + /to-img) e telas em HTML (/img-to-html). Ver docs/superpowers/specs/2026-10-07-redesign-fase-2-design-system-design.md."
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
gh issue create --milestone "$M" --label "tipo:tarefa,área:design-system" --title "Direção de arte das imagens geradas (âncoras e guia)" --body "Prompt-mestre, prancha de âncoras, checklist e log (spec, seção 3; plan, Tarefas A4, B2 e E2)."
for t in "Tela 01 — Home desktop" "Tela 02 — Home mobile" "Tela 03 — Listagem do repositório" "Tela 04 — Página de item" "Tela 05 — Sobre" "Tela 06 — Edição de evento (Caminhos)" "Tela 07 — 404"; do
  gh issue create --milestone "$M" --label "tipo:tarefa,área:design-system" --title "$t" --body "Mock aprovado (/plan-screen + /to-img) e HTML aprovado (/img-to-html). Ver plan da Fase 2."
done
gh issue create --milestone "$M" --label "tipo:tarefa,área:design-system" --title "Extração 1 do catálogo (ciclo 1)" --body "/extract-ds sobre as telas 01–03 (plan, Tarefa C1) e consulta informal à coordenação."
gh issue create --milestone "$M" --label "tipo:tarefa,área:design-system" --title "Extração final do catálogo" --body "/extract-ds sobre as sete telas (plan, Tarefa E1)."
gh issue create --milestone "$M" --label "tipo:tarefa,área:design-system,área:infra" --title "Integração do DS com o Eleventy" --body "Publicação em /design-system/, macros em _includes/ds/, layout-v2.njk, test:ds (plan, Tarefas C2–C4, E3–E5)."
gh issue create --milestone "$M" --label "tipo:decisão,área:design-system" --title "Aprovação da coordenação (Fase 2)" --body "Pacote para a Profa. Mara Rúbia Sant'Anna e registro da resposta (spec, seção 7; ADR 0010; plan, Parte F)."
```

- [ ] **Passo 3: Anotar os números das issues** criadas no corpo do PR de rascunho da fase, para referenciá-las nos commits (`Refs #N`).

---

## Parte B — Ciclo 1: os extremos

Regras para todas as telas das Partes B e D:

- Os gates das skills valem integralmente; nunca avançar sem "aprovado" ou "pode seguir" do usuário.
- Os mocks são gerados em 1K, com 2 variantes por tela, para caber no orçamento. Só as imagens de matéria finais saem em 2K.
- As alternativas descartadas ficam em `../redesign-fase2-referencias/mocks/`. Só o mock aprovado vai para `design-systems/telas/0N-*/reference.png`.
- Sempre que o `/to-img` ou o `/img-to-html` gerarem imagens, usar `tools/ds/gerar-imagem.sh` em vez de chamar o script do OpenRouter direto (contorno do Avast e log).
- **Orçamento:** antes de começar cada tela, somar a coluna de custo de `design-systems/materia/log.md`. Se o saldo estimado do OpenRouter ficar abaixo de US$ 2, avisar o usuário antes de gerar.

### Tarefa B1: Tela 01 — Home desktop

- [ ] **Passo 1: O usuário invoca o `/plan-screen`** com este texto (quem executa o prepara e entrega ao usuário):

```text
/plan-screen Home do site do LabMAES (Laboratório de Moda, Artes, Ensino e Sociedade, UDESC). Desktop. Siga a spec docs/superpowers/specs/2026-10-07-redesign-fase-2-design-system-design.md (seções 1 a 3), que substitui o "background" de redes sociais da skill: o critério de impacto é o conceito estrutura (bloco de montar) + matéria (massinha, papel, blocos, tecido, com peso igual), intensidade nível 3 só em toques sobre a base do nível 2, saberes sensíveis, Moda/Artes/Ensino/Sociedade sem hierarquia. Paleta e fontes do Manual de Marca (Poppins; Thunder só em título de impacto). Conteúdo: cabeçalho com navegação (Sobre, Equipe, Projetos, Produções, Eventos, Contato), hero de matéria com título e uma ação, destaques de projetos, produções recentes, próximo evento, rodapé. Referências: ../redesign-fase2-referencias/ref-0*.webp e 2026-10-07-14-16-nivel-2-medio.png. Wireframes em ASCII. Salvar em ../redesign-fase2-referencias/mocks/.
```

- [ ] **Passo 2: Gate.** O usuário escolhe uma das três propostas.
- [ ] **Passo 3: Mocks.** No passo de imagens, o usuário pede 2 versões. As gerações usam o wrapper, sem imagem de entrada nesta tela (as âncoras ainda não existem):

```bash
tools/ds/gerar-imagem.sh ../redesign-fase2-referencias/mocks/1-home-a.png ../redesign-fase2-referencias/mocks/1-home-a.prompt.txt "" 1K 16:9
```

(Um arquivo `.prompt.txt` por variante, com o prompt montado pelo `/plan-screen`.)

- [ ] **Passo 4: Gate.** O usuário aprova um mock.
- [ ] **Passo 5: O usuário invoca o `/img-to-html`:**

```text
/img-to-html ../redesign-fase2-referencias/mocks/<mock-aprovado>.png slug=telas/01-home — Saída em labmaes-site/design-systems/telas/01-home/. Regras extras: <body data-intensity="3">; inclua o skip-link; use os nomes canônicos de componente do plan (docs/superpowers/plans/2026-10-12-redesign-fase-2-design-system.md, "Contrato de nomes"), com o nome como classe-base e variantes em BEM; fontes auto-hospedadas (Poppins em /assets/fonts/; nada de CDN), porque a CSP do site só permite 'self'; nenhum style="" nem <style>/<script> inline; movimento conforme a spec, seção 2.5 (tokens --ease-out/--ease-in-out, durações, prefers-reduced-motion, hover só com (hover: hover) and (pointer: fine)). As imagens de matéria do fundo são geradas com tools/ds/gerar-imagem.sh em 2K.
```

- [ ] **Passo 6: Gates do `/img-to-html`** (wireframe e plano → fundo → componentes → assets → revisão). Cada um com aprovação explícita.
- [ ] **Passo 7: Commit**

```bash
git add design-systems/telas/01-home design-systems/materia/log.md
git commit -m "feat(ds): tela 01, home desktop (mock e HTML aprovados)" -m "Refs #<issue da tela 01>"
git push
```

### Tarefa B2: Imagens-âncora

- [ ] **Passo 1: Escolher as âncoras com o usuário.** Entre as imagens de matéria aprovadas na Tela 01, selecionar de 3 a 5 que melhor representem a direção de arte (os quatro materiais presentes no conjunto). Copiá-las para `design-systems/materia/ancoras/ancora-1.png` … `ancora-N.png`.
- [ ] **Passo 2: Escrever o montador de prancha**

`tools/ds/montar-prancha.py`:

```python
# /// script
# requires-python = ">=3.10"
# dependencies = ["pillow"]
# ///
"""Junta as imagens-âncora numa prancha única, porque o gerador aceita uma só --input-image."""
import sys
from pathlib import Path
from PIL import Image

pasta = Path(sys.argv[1] if len(sys.argv) > 1 else "design-systems/materia/ancoras")
saida = pasta / "prancha.png"
imagens = [Image.open(p).convert("RGB") for p in sorted(pasta.glob("ancora-*.png"))]
if not imagens:
    sys.exit(f"Nenhuma ancora-*.png em {pasta}")

lado = 768
colunas = min(3, len(imagens))
linhas = -(-len(imagens) // colunas)
prancha = Image.new("RGB", (colunas * lado, linhas * lado), "#F0F0FF")
for i, img in enumerate(imagens):
    img.thumbnail((lado, lado))
    x = (i % colunas) * lado + (lado - img.width) // 2
    y = (i // colunas) * lado + (lado - img.height) // 2
    prancha.paste(img, (x, y))
prancha.save(saida)
print(saida)
```

- [ ] **Passo 3: Gerar a prancha**

Run: `uv run --system-certs tools/ds/montar-prancha.py`
Esperado: `design-systems/materia/ancoras/prancha.png`.

- [ ] **Passo 4: Registrar no prompt-mestre.** Acrescentar ao fim de `design-systems/materia/prompt-mestre.md`:

```markdown
## Âncoras

A partir da Tela 02, toda geração passa `design-systems/materia/ancoras/prancha.png` como imagem
de entrada (3º argumento do `tools/ds/gerar-imagem.sh`) e acrescenta ao prompt específico:
"Match exactly the materials, light, camera angle and finish of the reference board."
```

- [ ] **Passo 5: Commit**

```bash
git add tools/ds/montar-prancha.py design-systems/materia/
git commit -m "feat(ds): imagens-âncora da direção de arte" -m "Refs #<issue da direção de arte>"
git push
```

### Tarefa B3: Tela 02 — Home mobile

- [ ] **Passo 1: O usuário invoca o `/plan-screen`:**

```text
/plan-screen Versão mobile (390 px) da Home aprovada em labmaes-site/design-systems/telas/01-home/ (reference.png e index.html). Uma tela só, sem três propostas de direção nova: as três propostas exploram só como a composição de matéria do hero se reorganiza no mobile, mantendo conteúdo e componentes. Spec da Fase 2, seções 1 a 3. Wireframes ASCII em ../redesign-fase2-referencias/mocks/.
```

- [ ] **Passo 2: Gate** da proposta.
- [ ] **Passo 3: Mocks** com âncoras, em retrato:

```bash
tools/ds/gerar-imagem.sh ../redesign-fase2-referencias/mocks/2-home-mobile-a.png ../redesign-fase2-referencias/mocks/2-home-mobile-a.prompt.txt design-systems/materia/ancoras/prancha.png 1K 9:16
```

- [ ] **Passo 4: Gate** do mock.
- [ ] **Passo 5: O usuário invoca o `/img-to-html`** com o mesmo texto da Tarefa B1, Passo 5, trocando a referência, o `slug=telas/02-home-mobile` e a pasta. Acrescentar: "Parta de design-systems/telas/01-home/assets/styles.css; esta tela é a mesma home em 390 px, então o resultado deve ser a home responsiva, não uma página nova: atualize 01-home para ser responsiva e use 02-home-mobile só para registrar o reference.png e o wireframe."
- [ ] **Passo 6: Gates** do `/img-to-html`.
- [ ] **Passo 7: Conferir a responsividade** abrindo `design-systems/telas/01-home/index.html` em 390 px e em 1280 px no navegador do app (`mcp__Claude_Browser__resize_window`), com screenshot para o usuário.
- [ ] **Passo 8: Commit**

```bash
git add design-systems/telas/01-home design-systems/telas/02-home-mobile design-systems/materia/log.md
git commit -m "feat(ds): tela 02, home mobile (home responsiva)" -m "Refs #<issue da tela 02>"
git push
```

### Tarefa B4: Tela 03 — Listagem do repositório

- [ ] **Passo 1: O usuário invoca o `/plan-screen`:**

```text
/plan-screen Listagem do repositório de Produções do LabMAES, desktop. Intensidade nível 1 (spec da Fase 2, seção 1.3): estrutura domina, matéria só como eco (grão de papel, módulos chapados, no máximo um acento). Deve dialogar com a Home aprovada (labmaes-site/design-systems/telas/01-home/). Conteúdo: cabeçalho, título da página, campo de busca, filtros (tipo de produção, ano, área — áreas sem hierarquia e sem cor própria), contagem de resultados, lista de cards com ícone modular por tipo + rótulo, paginação, estado vazio, rodapé. Interações frequentes (filtros, busca, paginação) sem animação (spec 2.5). Wireframes ASCII em ../redesign-fase2-referencias/mocks/.
```

- [ ] **Passo 2: Gate** da proposta.
- [ ] **Passo 3: Mocks** (com âncoras, 16:9, 2 variantes):

```bash
tools/ds/gerar-imagem.sh ../redesign-fase2-referencias/mocks/3-repositorio-a.png ../redesign-fase2-referencias/mocks/3-repositorio-a.prompt.txt design-systems/materia/ancoras/prancha.png 1K 16:9
```

- [ ] **Passo 4: Gate** do mock. Pedir ao usuário que avalie também o **estado vazio** (pode exigir um segundo mock, só da área de resultados).
- [ ] **Passo 5: O usuário invoca o `/img-to-html`** com o texto da Tarefa B1, Passo 5, trocando referência, `slug=telas/03-repositorio`, pasta e `data-intensity="1"`. Acrescentar: "Parta das Foundations de design-systems/telas/01-home/assets/styles.css (cores, tipografia, espaçamento, tokens de movimento); não redefina o que já existe."
- [ ] **Passo 6: Gates** do `/img-to-html`.
- [ ] **Passo 7: Commit**

```bash
git add design-systems/telas/03-repositorio design-systems/materia/log.md
git commit -m "feat(ds): tela 03, listagem do repositório" -m "Refs #<issue da tela 03>"
git push
```

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
    <p>Entrada do /extract-ds. Cada tela é a recriação HTML aprovada de um mock.</p>
    <ol>
      <li><a href="01-home/index.html">Home (desktop e mobile, intensidade 3)</a></li>
      <li><a href="03-repositorio/index.html">Listagem do repositório (intensidade 1)</a></li>
    </ol>
  </main>
</body>
</html>
```

- [ ] **Passo 2: O usuário invoca o `/extract-ds`:**

```text
/extract-ds html=labmaes-site/design-systems/telas/index.html slug=labmaes — Saída em labmaes-site/design-systems/labmaes/. O index.html é um hub: inspecione TODAS as telas ligadas a ele (01-home, que é responsiva, e 03-repositorio) como um único projeto. Regras extras: (1) contrato de nomes do plan (docs/superpowers/plans/2026-10-12-redesign-fase-2-design-system.md): o nome em data-component é a classe-base da raiz do preview; variantes em BEM; (2) documente data-intensity (1 e 3, observados) em Foundations, numa seção "Matéria", e os tokens de movimento numa seção "Movimento"; (3) o catálogo precisa de <meta name="robots" content="noindex">; (4) nenhum style="" e nenhum <style>/<script> inline (a CSP do site só permite 'self'); fontes auto-hospedadas.
```

- [ ] **Passo 3: Revisão com o usuário.** Abrir o catálogo no navegador do app, percorrer Overview, Foundations, Components e Layouts, e mostrar screenshots. Ajustes neste momento são feitos **nas telas** (`design-systems/telas/`) seguidos de nova execução do `/extract-ds`, nunca no catálogo.
- [ ] **Passo 4: Verificar o contrato de nomes**

Run:

```bash
grep -o 'data-component="[^"]*"' design-systems/labmaes/design-system.html | sort -u
```

Esperado: só nomes da tabela "Contrato de nomes" (ou nomes novos que o usuário aprovar e que então são acrescentados à tabela deste plano).

- [ ] **Passo 5: Commit**

```bash
git add design-systems/telas/index.html design-systems/labmaes
git commit -m "feat(ds): extração 1 do catálogo (ciclo 1)" -m "Refs #<issue da extração 1>"
git push
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

- [ ] **Passo 5: Telas visíveis só no preview da branch da fase**

A spec (seção 7) pede os links das telas em HTML no preview enviado à coordenação, e a seção 4.3 manda não publicá-las em produção. O Workers Builds do Cloudflare expõe a branch em `WORKERS_CI_BRANCH`. Em `eleventy.config.js`, logo depois das duas linhas do Passo 3:

```js
  // Só no preview da branch da Fase 2: telas-chave em /design-systems/ (com o catálogo ao lado, para os links relativos)
  if (process.env.WORKERS_CI_BRANCH === "redesign/fase-2-design-system") {
    eleventyConfig.addPassthroughCopy("design-systems/telas");
    eleventyConfig.addPassthroughCopy("design-systems/labmaes");
  }
```

Localmente e na `main` a variável não existe, então o teste do Passo 1 continua valendo. Depois do próximo push, conferir `<URL de preview>/design-systems/telas/` (Tarefa A1, Passo 5). Se a variável não existir no ambiente de build do Cloudflare, pedir ao usuário que crie, nas variáveis de build do projeto, `DS_PREVIEW_TELAS=1` só para builds de branch, e trocar a condição por `process.env.DS_PREVIEW_TELAS === "1"`.

- [ ] **Passo 6: Commit**

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

Cada tela segue o roteiro da Tarefa B4 (plan-screen → gate → mocks com âncoras → gate → img-to-html → gates → commit), com duas regras a mais nas invocações do `/img-to-html`:

> "Ligue primeiro `../../labmaes/styles.css` (catálogo v1) e use `assets/styles.css` só para o que ainda não existe no catálogo. Reutilize as classes e componentes do catálogo; não crie variantes paralelas de peças que já existem."

### Tarefa D1: Tela 04 — Página de item

- [ ] **Passo 1: O usuário invoca o `/plan-screen`:**

```text
/plan-screen Página de uma produção do repositório do LabMAES, desktop, intensidade nível 1 (spec da Fase 2). Parte do catálogo v1 em labmaes-site/design-systems/labmaes/design-system.html. Conteúdo: breadcrumb, tipo (ícone modular + rótulo), título, autoria (pessoas relacionadas), resumo em leitura longa (prose, Poppins em corpo maior e entrelinha generosa), lista de metadados (ano, tipo, projeto, áreas sem hierarquia, idioma, DOI/link), documentos para baixar (PDF com tamanho e idioma), produções relacionadas, rodapé. Wireframes ASCII em ../redesign-fase2-referencias/mocks/.
```

- [ ] **Passos 2–6:** gates, mocks (`4-item-a.png`, `4-item-b.png`, com âncoras, 16:9), `/img-to-html` com `slug=telas/04-item` e `data-intensity="1"`, gates.
- [ ] **Passo 7: Commit**

```bash
git add design-systems/telas/04-item design-systems/materia/log.md
git commit -m "feat(ds): tela 04, página de item" -m "Refs #<issue da tela 04>"
git push
```

### Tarefa D2: Tela 05 — Sobre

- [ ] **Passo 1: O usuário invoca o `/plan-screen`:**

```text
/plan-screen Página institucional "Sobre" do LabMAES, desktop, intensidade nível 1–2 (spec da Fase 2): hero com uma composição de matéria contida (menor que a da home), depois leitura longa. Parte do catálogo v1 em labmaes-site/design-systems/labmaes/design-system.html. Conteúdo: hero com título, apresentação em leitura longa (prose), as quatro áreas (Moda, Artes, Ensino, Sociedade) com peso igual e sem cor própria, a estratégia dos saberes sensíveis, coordenação, chamada para Equipe e Projetos, rodapé. Textos provisórios (o conteúdo real vem na Fase 3). Wireframes ASCII em ../redesign-fase2-referencias/mocks/.
```

- [ ] **Passos 2–6:** gates, mocks (`5-sobre-a.png`, `5-sobre-b.png`), `/img-to-html` com `slug=telas/05-sobre` e `data-intensity="2"`, gates.
- [ ] **Passo 7: Commit**

```bash
git add design-systems/telas/05-sobre design-systems/materia/log.md
git commit -m "feat(ds): tela 05, Sobre" -m "Refs #<issue da tela 05>"
git push
```

### Tarefa D3: Tela 06 — Edição de evento (Caminhos 2026)

- [ ] **Passo 1: O usuário invoca o `/plan-screen`:**

```text
/plan-screen Página da edição 2026 do evento Caminhos do Contemporâneo, desktop, intensidade nível 1–2, com a submarca do evento (spec da Fase 2, seção 2.6): data-brand="caminhos" troca só a tipografia (Cormorant Garamond + DM Mono) e os acentos de cor do evento; os componentes são os do catálogo v1 (labmaes-site/design-systems/labmaes/design-system.html), sem fork. Referência da identidade atual do evento: páginas em /eventos/caminhos-do-contemporaneo/2026/ do site atual. Conteúdo: hero do evento (datas, local, chamada), programação em acordeão, oficinas, submissões/anais (documentos para baixar), realizadores e apoiadores, rodapé. Wireframes ASCII em ../redesign-fase2-referencias/mocks/.
```

- [ ] **Passos 2–6:** gates, mocks (`6-evento-a.png`, `6-evento-b.png`), `/img-to-html` com `slug=telas/06-evento`, `data-intensity="2"` e `data-brand="caminhos"` no `<body>`. Acrescentar à invocação: "A troca de submarca é feita só por regras `[data-brand="caminhos"]` que redefinem tokens de tipografia e de acento; nenhuma classe nova de componente."
- [ ] **Passo 7: Commit**

```bash
git add design-systems/telas/06-evento design-systems/materia/log.md
git commit -m "feat(ds): tela 06, edição de evento (submarca Caminhos)" -m "Refs #<issue da tela 06>"
git push
```

### Tarefa D4: Tela 07 — 404

- [ ] **Passo 1: O usuário invoca o `/plan-screen`:**

```text
/plan-screen Página 404 do site do LabMAES, desktop e mobile, intensidade nível 2 (spec da Fase 2): uma composição de matéria com humor (peças de massinha "fora do encaixe", um bloco que não se encaixa), com elasticidade leve permitida só nas peças decorativas (bounce 0,1–0,2) e desligada com prefers-reduced-motion. Parte do catálogo v1 em labmaes-site/design-systems/labmaes/design-system.html. Conteúdo: mensagem curta, busca, links para Início, Produções e Contato, rodapé. A imagem comunica algo, então precisa de texto alternativo curto. Wireframes ASCII em ../redesign-fase2-referencias/mocks/.
```

- [ ] **Passos 2–6:** gates, mocks (`7-404-a.png`, `7-404-b.png`), `/img-to-html` com `slug=telas/07-404` e `data-intensity="2"`, gates.
- [ ] **Passo 7: Commit**

```bash
git add design-systems/telas/07-404 design-systems/materia/log.md
git commit -m "feat(ds): tela 07, 404" -m "Refs #<issue da tela 07>"
git push
```

---

## Parte E — Extração final, integração e documentação

### Tarefa E1: Extração final

Bloqueada pela Tarefa A5 (licença da Thunder resolvida).

- [ ] **Passo 1: Completar o hub**

Em `design-systems/telas/index.html`, a lista passa a ser:

```html
    <ol>
      <li><a href="01-home/index.html">Home (desktop e mobile, intensidade 3)</a></li>
      <li><a href="03-repositorio/index.html">Listagem do repositório (intensidade 1)</a></li>
      <li><a href="04-item/index.html">Página de item (intensidade 1)</a></li>
      <li><a href="05-sobre/index.html">Sobre (intensidade 2)</a></li>
      <li><a href="06-evento/index.html">Edição de evento, submarca Caminhos (intensidade 2)</a></li>
      <li><a href="07-404/index.html">404 (intensidade 2)</a></li>
    </ol>
```

- [ ] **Passo 2: O usuário invoca o `/extract-ds`** com o mesmo texto da Tarefa C1, Passo 2, trocando a lista de telas pelas seis acima e acrescentando: "(5) documente `data-intensity` 1, 2 e 3 e `data-brand="caminhos"` em Foundations; (6) esta é a extração final e substitui a extração 1 por inteiro."
- [ ] **Passo 3: Revisão com o usuário**, como na Tarefa C1, Passo 3. Ajustes de fundo voltam às telas e a uma nova extração.
- [ ] **Passo 4: Verificar o contrato de nomes** como na Tarefa C1, Passo 4.
- [ ] **Passo 5: Commit**

```bash
git add design-systems/telas/index.html design-systems/labmaes
git commit -m "feat(ds): extração final do catálogo" -m "Refs #<issue da extração final>, #26"
git push
```

A partir daqui, ajustes finos podem ser feitos direto no catálogo.

### Tarefa E2: Guia de direção de arte no catálogo

**Arquivos:**
- Copiar: `design-systems/materia/{prompt-mestre.md,log.md,ancoras/}` → `design-systems/labmaes/assets/materia/`
- Modificar: `design-systems/labmaes/design-system.html` (seção Foundations → Matéria)

- [ ] **Passo 1: Copiar o material**

```bash
mkdir -p design-systems/labmaes/assets/materia
cp design-systems/materia/prompt-mestre.md design-systems/materia/log.md design-systems/labmaes/assets/materia/
cp -r design-systems/materia/ancoras design-systems/labmaes/assets/materia/
```

- [ ] **Passo 2: Acrescentar ao catálogo** uma subseção "Direção de arte" dentro de Foundations → Matéria, no padrão de marcação das outras subseções do catálogo (`data-ds-section="foundation"`), com:
  - as imagens-âncora (`assets/materia/ancoras/ancora-*.png`, `alt=""` porque são exemplos decorativos, e uma legenda);
  - o prompt-mestre em `<pre><code>`;
  - o checklist de aprovação como lista;
  - o orçamento de peso;
  - a regra de texto alternativo (spec, seção 3, item 6);
  - um link para `assets/materia/log.md`.
- [ ] **Passo 3: Conferir no navegador do app** e mostrar um screenshot ao usuário.
- [ ] **Passo 4: Commit**

```bash
git add design-systems/labmaes
git commit -m "docs(ds): guia de direção de arte no catálogo" -m "Refs #<issue da direção de arte>"
git push
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

test("intensidade padrão 1 e submarca opcional", () => {
  assert.match(env.render("layout-v2.njk", contexto()), /<body data-intensity="1">/);
  assert.match(
    env.render("layout-v2.njk", contexto({ intensity: 2, brand: "caminhos" })),
    /<body data-intensity="2" data-brand="caminhos">/,
  );
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
<body data-intensity="{{ intensity or 1 }}"{% if brand %} data-brand="{{ brand }}"{% endif %}>
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
- [ ] **Passo 4: Fechar as issues cumpridas**: as das sete telas, a da extração final, a da direção de arte, a da integração, a da licença da Thunder, a #26, a #27 e a #35 (a #34 fecha com o merge, porque o catálogo só fica público então).
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

- [ ] **Passo 1: Conferir o preview.** Abrir `<URL de preview>/design-system/` e cada tela em `<URL de preview>/design-systems/telas/` (publicadas só no preview, Tarefa C2, Passo 5). Conferir fontes, imagens e console sem erros.
- [ ] **Passo 2: Escrever o resumo** em linguagem não técnica, como um Claude Doc (skill `anthropic-skills:docs`), com: o conceito (estrutura e matéria), a intensidade por contexto, cor, tipografia, matéria e movimento, as sete telas (imagens) e o link do catálogo. Mostrar ao usuário antes de qualquer envio.
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

- [ ] **Passo 5: Depois do merge**, conferir `https://<domínio de produção>/design-system/` e o cabeçalho `X-Robots-Tag: noindex` (`curl -sI .../design-system/ | grep -i robots`), atualizar `docs/roadmap.md` e `docs/architecture/README.md` para "concluída" (num PR de docs) e fechar a milestone "Fase 2 — Design system".
