# Plan — Redesign Fase 1: Content foundation

**Status:** Em andamento  
**Data:** 2026-09-16

## Etapas

### 1. Reconciliar histórico — CONCLUÍDA

A branch da Fase 1 contém a Fase 0 e está sincronizada com `main`.

### 2. Formalizar documentação — CONCLUÍDA

Presentes:
- ADRs 0001–0006;
- spec e plan da Fase 0;
- spec e plan da Fase 1;
- índice `docs/architecture/README.md`.

### 3. Validar foundation existente — CONCLUÍDA

Auditoria 01 aplicada:
- filenames com tokens explícitos de campos;
- `editorialStatus` padronizado;
- operações destrutivas bloqueadas durante piloto;
- campos de texto alternativo;
- SVG removido do upload editorial inicial.

Auditoria 02 aplicada:
- datas opcionais usam `default: ''`;
- valores artificiais em datas vazias deixaram de ser aceitos como comportamento esperado.

### 4. Criar fixtures — CONCLUÍDA

Conjunto criado em `src/content/**`, marcado como fixture e mantido fora do build público.

### 5. Validar CMS — EM ANDAMENTO

#### Criação de registros — APROVADA

O Pages CMS cria registros na branch corretamente e preserva o frontmatter.

#### Datas opcionais — APROVADAS

A Correção 02 eliminou o valor artificial em campos de data opcionais.

#### Referências relacionais — APROVADAS

O teste real confirmou:
- múltiplas referências;
- armazenamento por slug;
- preservação da ordem;
- labels legíveis no CMS.

A tentativa com `{primary}` produziu labels vazios no CMS hospedado. A Correção 03b passou a usar
labels explícitos (`{fields.name}` / `{fields.title}`), e o reteste foi aprovado.

#### Modelo de autoria / créditos — APROVADO

Produções passam de `authors` para `contributors`, lista ordenada com dois formatos:
- `internal`: referência a `people`;
- `external`: nome e metadados mínimos.

O ADR 0003 foi refinado para registrar a decisão.

`list: {min: 1}` não é sintaxe reconhecida pelo Pages CMS para `type: block` (só `list: true`);
corrigido, e o reteste real confirmou criação, reordenação, persistência da ordem após reabrir e
o bloqueio de salvar produção sem nenhum contributor.

Ver:
`docs/superpowers/reviews/2026-09-16-fase-1-cms-auditoria-04-contributors.md`.

#### Situação de publicação da obra — IMPLEMENTADO; RETESTE PENDENTE

O teste do bloqueio "sem contributor" levantou duas dúvidas de clareza editorial:
- `catalogStatus` ("Estado de catalogação") não deixava claro que é sobre a confiança do NOSSO
  cadastro, não sobre a obra — ganhou `description` explicando os três níveis;
- não havia como registrar se a obra está no prelo (aceita, ainda não publicada) ou já publicada,
  distinto de `editorialStatus` (que é só o nosso fluxo de edição do site).

Produções ganham `publicationStatus` (opcional): `in-press` / `published`. `editorial_status`
(componente usado em todas as coleções) ganhou `description` reforçando que não é sobre a obra.

Próximo teste: confirmar no Pages CMS que os dois novos textos de ajuda aparecem nos campos e que
`publicationStatus` pode ficar em branco sem impedir salvar.

#### Mídia — APROVADA, COM LIMITE DE TAMANHO DE ARQUIVO CONHECIDO

Upload de foto em `people` funcionou (`outra-pessoa-teste.md` ganhou `photo`/`photoAlt` reais).
`people.photo` ganhou `description` com formatos aceitos e recomendação de tamanho.

Upload de documento (`documents.file`) testado com arquivos de vários tamanhos: aceito até
~2,89 MB, falhou com `Failed to upload file: 413` a partir de ~3,8 MB. Limite não é configurável
em `.pages.yml` (sem opção de tamanho máximo em `type: image`/`type: file`); é do lado do serviço
hospedado do Pages CMS, provavelmente limite de corpo de requisição serverless (~4,5 MB
codificados em base64 ≈ 3,3–3,4 MB de arquivo original). Recomendação prática: manter uploads pelo
CMS até ~2,5 MB; arquivos maiores continuam indo por commit direto, como já é o caso de
`assets/editais/`.

Ver:
`docs/superpowers/reviews/2026-09-16-fase-1-cms-auditoria-06-limite-upload-e-purga.md`.

**Incidente:** um PDF com dado de saúde pessoal foi commitado por engano durante esse teste de
limites e ficou pushado publicamente por um curto intervalo. Histórico da branch foi reescrito e
forçado no `origin` para removê-lo; ver o mesmo documento acima para detalhes e o alerta a
qualquer clone local desatualizado.

Ainda testar depois disso:
- traduções;
- workflow editorial;
- mensagens de erro e campos obrigatórios;
- ergonomia com uma pessoa não técnica.

### 6. Evoluir validação

Substituir o validador estrutural mínimo por validação real de frontmatter/schema e referências,
incluindo regras específicas de `contributors`.

### 7. Gate de saída

Não conectar `src/content` ao Eleventy público até os critérios da spec da Fase 1 serem atendidos.
