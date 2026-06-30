# Botão do template de apresentação na página de Submissões + publicação do Edital 03

**Data:** 2026-06-23
**Página afetada:** `/eventos/caminhos-do-contemporaneo/2026/submissoes/`

## Objetivo

Disponibilizar o **template de apresentação de slides** do seminário na página de
submissões, em dois formatos (Canva online e PowerPoint `.pptx`), e publicar o
**Edital 03 (Mostra Audiovisual)** já atualizado.

São duas frentes:
1. **Conteúdo/UI** — novo card "Template de apresentação" na seção "Normas gerais".
2. **Deploy** — push mínimo para `origin/main` (Cloudflare Pages publica automaticamente).

## 1. Card "Template de apresentação"

**Localização:** seção S4 "Normas gerais" de
`eventos/caminhos-do-contemporaneo/2026/submissoes/index.njk`, dentro de
`.normas-grid`. Inserido **logo após** o card "Template (Editais 1 e 2)", para os
dois assuntos de template ficarem adjacentes. O grid passa de 6 para 7 cards
(layout de 3 colunas já existente acomoda; última linha fica com 1 card — aceitável
e consistente com o comportamento responsivo atual).

**Markup (segue o padrão `event-card normas-card`):**

```html
<article class="event-card normas-card">
  <h3>Template de apresentação</h3>
  <p>Modelo de slides para quem for apresentar comunicação oral ou pôster no
  seminário. Edite online no Canva ou baixe em PowerPoint (.pptx).</p>
  <div class="normas-card__actions">
    <a class="button button--secondary"
       href="https://canva.link/lmy5s44w830m1pv"
       target="_blank"
       rel="noopener noreferrer"
       aria-label="Abrir template de apresentação no Canva">
      Abrir no Canva ↗
    </a>
    <a class="button button--outline"
       href="/assets/editais/Caminhos_template_apresentacao.pptx"
       download
       aria-label="Baixar template de apresentação em PowerPoint">
      Baixar .pptx ↓
    </a>
  </div>
</article>
```

**Decisões:**
- Classes de botão reutilizadas: `button--secondary` (Canva, ação primária) e
  `button--outline` (.pptx), iguais às usadas nos cards de modalidade.
- Canva abre em nova aba; `.pptx` usa atributo `download`.
- `aria-label` descritivo em cada botão.

## 2. Arquivo .pptx

Copiar de
`C:\Users\Windows 10\Downloads\Templates para Apresentação - Seminário Caminhos do Contemporâneo.pptx`
(9,1 MB) para:

`labmaes-site/assets/editais/Caminhos_template_apresentacao.pptx`

Mesma pasta do template Word (`Caminhos-template.docx`), mantendo os materiais de
submissão/apresentação num só lugar. Nome sem espaços/acentos para URL limpa.

## 3. CSS

Adicionar uma regra mínima em `css/components.css`, junto ao bloco
`.normas-card`, para alinhar os dois botões dentro do card:

```css
.normas-card__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: var(--space-16);
}
.normas-card__actions .button {
  flex: 1;
  min-width: 0;
  font-size: 14px;
  white-space: nowrap;
}
```

Sem componente novo; apenas um wrapper de ações reaproveitando `.button`.

## 4. Publicação (deploy)

**Realidade das branches (verificada em 2026-06-23):**
- Workspace está em `feat/programacao-rica`; o commit do spec foi feito aqui.
- `main` == `origin/main` == `11ccbc7` (já publicada), **5 commits à frente** desta
  branch. Cloudflare Pages serve a partir de `main` (build Eleventy → `_site/`,
  conforme `wrangler.jsonc`).
- As mudanças pendentes (edital, `submissoes/index.njk`, `2026/index.njk`, Poppins)
  estão no **working tree**, soltas.

**Estratégia (decisão do usuário): commitar direto na `main` + push.**

Como o edital `.pdf` já está modificado no working tree e o estado de
`submissoes/index.njk` em `main` pode diferir do estado nesta branch, o plano de
implementação deve:
1. Preservar a versão modificada do Edital 03 (copiar para fora antes de trocar de branch).
2. `git checkout main` (sincronizado com origin).
3. Aplicar **na `main`**, do zero: copiar o Edital 03 atualizado, copiar o `.pptx`,
   adicionar o card em `submissoes/index.njk` e a regra em `css/components.css`.
4. Verificar com `git status` que **apenas** estes caminhos estão modificados/staged:
   - `assets/editais/Caminhos_edital_03_MA.pdf`
   - `assets/editais/Caminhos_template_apresentacao.pptx`
   - `eventos/caminhos-do-contemporaneo/2026/submissoes/index.njk`
   - `css/components.css`
5. Commit + `git push origin main`. Cloudflare publica automaticamente.

**Verificar durante a implementação:** se `submissoes/index.njk` na `main` ainda
contém o card "Edital 3 — Mostra Audiovisual" (3 modalidades). Se sim, o card de
template é adicionado de forma independente — **não** mexer na remoção da Mostra
neste push (essa reestruturação fica para outra entrega).

**Sem `git add -A`.** Usar `git add` explícito apenas nos 4 caminhos acima.

**Deixados de fora deste push** (permanecem como trabalho separado):
- Reestruturação da Mostra (`2026/index.njk` e remoção do card em `submissoes`).
- `assets/fonts/Poppins/` (novas).
- `.claude/` (não versionar).

## Verificação

- Build local Eleventy (se disponível) ou inspeção do `_site` gerado, confirmando
  que o card aparece e os dois links resolvem.
- Conferir que o `.pptx` foi copiado e que o href `/assets/editais/...` bate com o
  nome do arquivo.
- `git status` antes do push: confirmar que só os 4 caminhos estão staged.

## Fora de escopo

- Mexer no card de modalidades ou no callout Even3.
- Publicar a reestruturação da Mostra na home do evento (`2026/index.njk`).
- Versionar fontes Poppins ou `.claude/`.
