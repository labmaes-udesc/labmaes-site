# Auditoria 01 — Fase 1 Content Foundation

**Data:** 2026-09-04  
**Branch auditada:** `redesign/fase-1-content-foundation`  
**Resultado:** foundation coerente com a Fase 0, com correções necessárias antes dos fixtures.

## Conformidades confirmadas

- Fase 1 contém os ADRs 0001–0006, spec e plan da Fase 0.
- A nova camada permanece paralela ao site público.
- `src/**` está ignorado pelo Eleventy durante o piloto.
- O Pages CMS usa coleções relacionais e referências.
- `settings.content.merge: true` preserva chaves ainda não modeladas.
- Operações destrutivas já estavam limitadas nas entidades centrais.
- O validador mínimo existe e está separado do build público.

## Correções aplicadas nesta revisão

### 1. Slug e nome de arquivo

O Pages CMS trata `{slug}` no template de filename como alias do campo primário. Para garantir
que o identificador arquitetural `slug` seja realmente usado, todos os templates passam a usar
`{fields.slug}` explicitamente.

Para entidades com ano próprio:
- produções: `{fields.year}-{fields.slug}.md`;
- edições de evento: `{fields.year}-{fields.slug}.md`.

Notícias passam a usar:
- `{fields.date}-{fields.slug}.md`.

Documentos usam apenas o slug enquanto o schema não tiver um campo `year` explícito.

O editor de filename (`filename.field`) fica oculto; o nome do arquivo é derivado do schema,
evitando divergência entre filename e slug.

### 2. Workflow editorial

`editorialStatus` passa a ser o nome único do campo editorial em todas as coleções:

- `draft`;
- `review`;
- `published`.

Campos `status` continuam reservados para estado de domínio, como:
- vínculo de pessoa;
- situação de projeto;
- situação de edição de evento.

### 3. Operações destrutivas

Durante o piloto, todas as coleções ficam com:

- create: true;
- rename: false;
- delete: false.

A política pode ser relaxada depois do teste editorial.

### 4. Acessibilidade de imagens

Campos auxiliares de texto alternativo foram acrescentados para capa, foto e miniaturas.
Logos institucionais usarão o nome da instituição como alt no template público.

O componente SEO passa a aceitar `ogImageAlt`.

### 5. SVG no CMS

Uploads SVG foram removidos do fluxo editorial inicial. SVG continua permitido como asset
gerenciado por desenvolvimento, mas upload por CMS só deve voltar após definição de sanitização
ou outro controle explícito.

## Pontos ainda abertos (não corrigidos nesta revisão)

1. Tradução de bios de pessoas e conteúdo narrativo de instituições/coleções.
2. Relação efetiva de `collection` com produções/documentos.
3. Política de exclusão/arquivamento após o piloto.
4. Validação completa de frontmatter/schema.
5. Pipeline público de imagens e cópia de `src/assets/uploads`.
6. Teste real do Pages CMS com uma bolsista.

Os itens 1–3 devem ser avaliados com os fixtures e o teste de usabilidade. Os itens 4–6 são
critérios obrigatórios antes de encerrar a Fase 1.
