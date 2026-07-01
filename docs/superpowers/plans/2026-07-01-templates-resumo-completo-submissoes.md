# Templates Resumo/Completo na página de Submissões — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Atualizar `eventos/caminhos-do-contemporaneo/2026/submissoes/index.njk` para usar os dois novos templates (`Caminhos-template-resumo.docx` e `Caminhos-template-completo.docx`) no lugar do template único antigo, e remover o arquivo antigo do repositório.

**Architecture:** Site estático Eleventy (`.njk` templates → build em `_site/`). Mudança é puramente de conteúdo/markup em um único arquivo `.njk`, mais a remoção de um asset. Nenhum componente novo de CSS ou JS.

**Tech Stack:** Eleventy 3, Nunjucks, CSS puro (`css/components.css`).

Spec de referência: `docs/superpowers/specs/2026-07-01-templates-resumo-completo-submissoes-design.md`

---

### Task 1: Atualizar botão de template no card "Comunicação Oral"

**Files:**
- Modify: `eventos/caminhos-do-contemporaneo/2026/submissoes/index.njk:84-89`

- [ ] **Step 1: Editar o botão de template do card CO**

Trocar:

```html
            <a class="button button--outline"
               href="/assets/editais/Caminhos-template.docx"
               download
               aria-label="Baixar template de submissão">
              Template ↓
            </a>
```

Por:

```html
            <a class="button button--outline"
               href="/assets/editais/Caminhos-template-resumo.docx"
               download
               aria-label="Baixar template do resumo expandido">
              Template do resumo ↓
            </a>
```

- [ ] **Step 2: Conferir visualmente**

Run: `grep -n "Caminhos-template-resumo" "eventos/caminhos-do-contemporaneo/2026/submissoes/index.njk"`
Expected: pelo menos 1 ocorrência (a que acabou de ser adicionada).

---

### Task 2: Atualizar botão de template no card "Pôster Digital"

**Files:**
- Modify: `eventos/caminhos-do-contemporaneo/2026/submissoes/index.njk:121-126`

- [ ] **Step 1: Editar o botão de template do card Pôster**

Trocar:

```html
            <a class="button button--outline"
               href="/assets/editais/Caminhos-template.docx"
               download
               aria-label="Baixar template de submissão">
              Template ↓
            </a>
```

Por:

```html
            <a class="button button--outline"
               href="/assets/editais/Caminhos-template-resumo.docx"
               download
               aria-label="Baixar template do resumo expandido">
              Template do resumo ↓
            </a>
```

Nota: o trecho é textualmente idêntico ao do Task 1 — usar o contexto ao redor
(`card-poster-title` / "Edital 2") para editar a ocorrência correta, já que a
substituição literal do Task 1 é ambígua se repetida sem contexto.

- [ ] **Step 2: Conferir que agora há 2 ocorrências**

Run: `grep -n "Caminhos-template-resumo" "eventos/caminhos-do-contemporaneo/2026/submissoes/index.njk"`
Expected: 2 ocorrências (cards CO e Pôster).

- [ ] **Step 3: Conferir que o template antigo não é mais referenciado**

Run: `grep -n "Caminhos-template\.docx" "eventos/caminhos-do-contemporaneo/2026/submissoes/index.njk"`
Expected: nenhuma ocorrência (comando não retorna nada).

---

### Task 3: Reescrever o card "Template (Editais 1 e 2)" em Normas gerais

**Files:**
- Modify: `eventos/caminhos-do-contemporaneo/2026/submissoes/index.njk:184-187`

- [ ] **Step 1: Substituir o card inteiro**

Trocar:

```html
        <article class="event-card normas-card">
          <h3>Template (Editais 1 e 2)</h3>
          <p>Comunicação oral e pôster utilizam o mesmo template Word disponível para download. O template contém as orientações de formatação e as normas de apresentação do texto.</p>
        </article>
```

Por:

```html
        <article class="event-card normas-card">
          <h3>Templates de submissão (Editais 1 e 2)</h3>
          <p>Comunicação oral e pôster usam os mesmos dois templates. Envie o resumo expandido no momento da submissão; o artigo completo só é necessário depois, caso o trabalho seja aprovado e vá compor os anais do evento.</p>
          <div class="normas-card__actions">
            <a class="button button--secondary"
               href="/assets/editais/Caminhos-template-resumo.docx"
               download
               aria-label="Baixar template do resumo expandido">
              Template do resumo ↓
            </a>
            <a class="button button--outline"
               href="/assets/editais/Caminhos-template-completo.docx"
               download
               aria-label="Baixar template do artigo completo">
              Template do artigo completo ↓
            </a>
          </div>
        </article>
```

- [ ] **Step 2: Conferir o resultado**

Run: `grep -n "Templates de submissão\|Caminhos-template-completo" "eventos/caminhos-do-contemporaneo/2026/submissoes/index.njk"`
Expected: 2 ocorrências — o `<h3>` novo e o `href` do template completo.

---

### Task 4: Remover o template antigo do repositório

**Files:**
- Delete: `assets/editais/Caminhos-template.docx`

- [ ] **Step 1: Confirmar que nada mais referencia o arquivo antigo**

Run: `grep -rn "Caminhos-template\.docx" --include=*.njk --include=*.md .`
Expected: nenhuma ocorrência (já confirmado no Task 2, reconfirmar após Task 3 por segurança).

- [ ] **Step 2: Remover o arquivo**

```bash
git rm "assets/editais/Caminhos-template.docx"
```

---

### Task 5: Build local e verificação visual

**Files:** nenhum (só verificação)

- [ ] **Step 1: Rodar o build do Eleventy**

Run: `npx @11ty/eleventy`
Expected: build conclui sem erro; gera `_site/eventos/caminhos-do-contemporaneo/2026/submissoes/index.html`.

- [ ] **Step 2: Conferir os links gerados no HTML de saída**

Run: `grep -n "Caminhos-template" "_site/eventos/caminhos-do-contemporaneo/2026/submissoes/index.html"`
Expected: 3 ocorrências de `Caminhos-template-resumo.docx` (2 cards de modalidade + 1 no card de normas) e 1 ocorrência de `Caminhos-template-completo.docx` (card de normas); nenhuma ocorrência de `Caminhos-template.docx` sozinho (sem sufixo).

- [ ] **Step 3: Conferir visualmente no preview (dev server)**

Usar `preview_start` (conforme configuração em `.claude/launch.json`, script `start` = `npx @11ty/eleventy --serve`) e abrir
`/eventos/caminhos-do-contemporaneo/2026/submissoes/`. Confirmar:
- Os 2 cards de modalidade mostram "Template do resumo ↓".
- O card "Templates de submissão (Editais 1 e 2)" em Normas gerais mostra 2 botões lado a lado, sem quebrar o grid de 3 colunas.
- Os downloads (clique nos botões) apontam para os arquivos corretos (checar via `preview_network` ou inspecionar o `href`).

---

### Task 6: Commit

**Files:**
- `eventos/caminhos-do-contemporaneo/2026/submissoes/index.njk`
- `assets/editais/Caminhos-template.docx` (removido)
- `assets/editais/Caminhos-template-resumo.docx` (novo, já criado em sessão anterior)
- `assets/editais/Caminhos-template-completo.docx` (novo, já criado em sessão anterior)

- [ ] **Step 1: Conferir o que será commitado**

Run: `git status`
Expected: exatamente os 4 caminhos acima como staged/modified/untracked (mais possivelmente `.claude/` e `assets/fonts/Poppins/` untracked, que **não** devem ser incluídos — ver spec, seção "Fora de escopo").

- [ ] **Step 2: Adicionar os arquivos explicitamente (sem `git add -A`)**

```bash
git add "eventos/caminhos-do-contemporaneo/2026/submissoes/index.njk" \
        "assets/editais/Caminhos-template-resumo.docx" \
        "assets/editais/Caminhos-template-completo.docx"
```

(A remoção de `Caminhos-template.docx` já foi staged no Task 4 via `git rm`.)

- [ ] **Step 3: Commit**

```bash
git commit -m "$(cat <<'EOF'
feat(submissoes): troca template único pelos templates de resumo e artigo completo

Os cards de Comunicação Oral e Pôster agora apontam para o template de
resumo expandido (exigido na submissão); o card de Normas gerais passa a
oferecer os dois templates (resumo e artigo completo, este último exigido
só após aprovação, para os anais). Remove o template antigo, que não é
mais referenciado em nenhum lugar do site.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 4: Confirmar o commit**

Run: `git log --oneline -1` e `git status`
Expected: commit criado; working tree limpo em relação aos 4 caminhos acima (pode restar `.claude/` e `assets/fonts/Poppins/` untracked — esperado, fora de escopo).

**Nota sobre push:** o spec deixa o push como decisão a tomar junto com o usuário no
momento da implementação. Não incluir `git push` automaticamente — perguntar antes.
