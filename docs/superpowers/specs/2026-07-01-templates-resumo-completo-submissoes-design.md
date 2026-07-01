# Atualizar página de Submissões para os novos templates (resumo/completo)

**Data:** 2026-07-01
**Página afetada:** `/eventos/caminhos-do-contemporaneo/2026/submissoes/`

## Objetivo

O template único de submissão (`Caminhos-template.docx`) foi substituído por dois
templates específicos, já revisados contra os editais 01 (Comunicação Oral) e 02
(Pôster) — ver `docs/superpowers/specs/` anterior sobre o alinhamento de conteúdo:
- `Caminhos-template-resumo.docx` — resumo expandido, exigido **na submissão**.
- `Caminhos-template-completo.docx` — artigo completo, exigido **só depois da
  aprovação**, para compor os anais.

A página de Submissões ainda referencia apenas o template antigo. Este spec cobre a
atualização da página para os dois novos arquivos e a remoção do template antigo.

## 1. Cards de modalidade (Comunicação Oral e Pôster)

**Localização:** seção S2 "Modalidades de submissão", cards `submissao-card` com
`id="card-co-title"` e `id="card-poster-title"`.

Cada card mantém os mesmos 2 botões (`submissao-card__actions`), só troca o alvo e o
rótulo do botão de template — o resumo é o que se exige nesta etapa (submissão via
Even3), então é o único visível nos cards de modalidade:

```html
<a class="button button--outline"
   href="/assets/editais/Caminhos-template-resumo.docx"
   download
   aria-label="Baixar template do resumo expandido">
  Template do resumo ↓
</a>
```

Aplicar essa troca nos dois cards (CO e Pôster) — botão de edital (`button--secondary`)
não muda.

## 2. Card "Templates de submissão (Editais 1 e 2)" em Normas gerais

**Localização:** seção S4 "Normas gerais", `.normas-grid`, card atualmente chamado
"Template (Editais 1 e 2)".

Renomear e reescrever para explicar as duas etapas, seguindo o mesmo padrão do card
vizinho "Template de apresentação" (texto + `.normas-card__actions` com 2 botões):

```html
<article class="event-card normas-card">
  <h3>Templates de submissão (Editais 1 e 2)</h3>
  <p>Comunicação oral e pôster usam os mesmos dois templates. Envie o resumo expandido
  no momento da submissão; o artigo completo só é necessário depois, caso o trabalho
  seja aprovado e vá compor os anais do evento.</p>
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

Nenhuma classe nova — `.normas-card__actions` e `.button` já existem e já estão
estilizados (usados no card "Template de apresentação"); ver
`css/components.css:983-996`.

## 3. Remoção do template antigo

Apagar `assets/editais/Caminhos-template.docx`. Confirmado via grep que nenhum outro
arquivo do site (`.njk`, `.md`) referencia esse caminho fora da própria página de
Submissões, que deixa de referenciá-lo após a mudança acima.

## Fora de escopo

- Mudar o texto/links do card de "Template de apresentação" (`.pptx`/Canva) — não é
  afetado por esta mudança.
- Mexer no callout Even3 ou nos prazos (S1/S3).
- CSS novo — reaproveita `.normas-card__actions` existente.
- Deploy/push para `main` — a decidir junto com o usuário na hora da implementação,
  seguindo a mesma lógica do spec anterior (branch `main` está sincronizada com
  `origin/main`; commit direto nela quando aplicável).

## Verificação

- Build local Eleventy (ou inspeção do `_site` gerado): confirmar que os 3 links
  (`Template do resumo` nos 2 cards de modalidade + os 2 botões do card de Normas
  gerais) resolvem para os arquivos corretos e que os arquivos existem em
  `assets/editais/`.
- Conferir visualmente a página renderizada (screenshot do preview) para garantir que
  o card de Normas gerais com 2 botões não quebra o grid de 3 colunas.
- `git status` antes do commit: confirmar que apenas
  `eventos/caminhos-do-contemporaneo/2026/submissoes/index.njk` foi modificado e que
  `assets/editais/Caminhos-template.docx` aparece como removido, junto com os dois
  novos arquivos `assets/editais/Caminhos-template-resumo.docx` e
  `Caminhos-template-completo.docx` (já untracked) sendo adicionados.
