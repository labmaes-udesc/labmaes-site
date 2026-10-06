# Auditoria 06 — limite de upload de mídia e purga de histórico

**Data:** 2026-09-16
**Status:** limite estimado; nenhuma ação de schema pendente

## Limite de tamanho de upload

Testes reais no Pages CMS hospedado, subindo documentos de tamanhos variados via
`documents.file`:

| Resultado | Tamanho |
|---|---|
| Aceito | ~0,49 MB |
| Aceito | ~0,99 MB |
| Aceito | ~2,25 MB |
| Aceito | ~2,89 MB (3.032.957 bytes) |
| **Falhou** (`Failed to upload file: 413`) | ~3,8 MB |
| **Falhou** (`Failed to upload file: 413`) | ~18 MB |

O limite está entre **2,89 MB e 3,8 MB**. Não existe opção de tamanho máximo documentada em
`type: file`/`type: image` no `.pages.yml` — isso não é ajustável pelo nosso schema.

**Hipótese mais provável:** o Pages CMS hospedado roda sobre Next.js, tipicamente em
infraestrutura serverless (Vercel), cujo limite clássico de corpo de requisição em funções
serverless é ~4,5 MB. Uploads via API Git costumam ir em base64 (~33% maior que o arquivo
original). 4,5 MB de payload codificado ÷ 1,33 ≈ **3,3–3,4 MB de arquivo original** — bem no meio
da faixa observada (aceita a 2,89 MB, falha a 3,8 MB). Não confirmado oficialmente, mas consistente
com todos os dados coletados.

**Recomendação prática:** orientar quem for subir documentos pelo CMS a manter arquivos **até ~2,5
MB** por segurança (comprimir PDFs maiores antes do upload). Documentos maiores que isso podem
continuar sendo commitados diretamente via Git, como já acontece hoje com `assets/editais/`.

## Purga de histórico — incidente com arquivo sensível

Durante o teste de limites de upload, um PDF chamado `20260720-ultrassom-abdominal.pdf` (exame de
imagem, dado de saúde pessoal) foi commitado por engano só para testar tamanho de arquivo, e
pushado para o `origin` (repositório público) por um curto intervalo.

**Ação tomada:**
- histórico da branch `redesign/fase-1-content-foundation` reescrito (`git filter-branch`,
  escopo restrito aos commits exclusivos da branch — `main` nunca teve o arquivo);
- push forçado (`--force-with-lease`) sobrescrevendo o histórico antigo no `origin`;
- verificado que nenhum commit alcançável pela branch, local ou remota, contém mais o arquivo.

**Consequência para qualquer outro clone local:** precisa de `git fetch` + `git reset --hard
origin/redesign/fase-1-content-foundation` para se realinhar; um `git pull` comum vai conflitar.

**Lição para o piloto editorial:** ao testar limites de upload, usar sempre arquivos claramente
fictícios/sem dado pessoal (como os fixtures `fixture-*`), nunca documentos reais do computador de
quem está testando.
