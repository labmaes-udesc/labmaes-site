# LabMAES — Schema editorial v1 e Pages CMS
## Fase 0 — Especificação técnica preliminar

**Status:** protótipo para implementação em branch  
**Derivado de:** `LabMAES-redesign-fase-0-v0.2.md`

## 1. Objetivo

Converter o modelo de conteúdo aprovado em uma primeira configuração concreta do Pages CMS, sem acoplar ainda o site público à nova estrutura.

A configuração proposta usa `.pages.yml` na raiz, collections para entidades repetíveis, referências entre collections, grupos apenas para organização da interface editorial e duas fontes de mídia separadas: imagens e documentos.

A documentação atual do Pages CMS confirma que `.pages.yml` é a fonte de configuração do CMS; `content` aceita `collection`, `file` e `group`; campos podem ser reutilizados por `components`; referências entre collections são suportadas por `reference`; e mídia pode ser configurada em múltiplas fontes com caminhos de entrada e saída distintos.

## 2. Decisões do schema v1

### Pessoas

`person.status`:
- `current`;
- `alumnus`;
- `collaborator`.

Egressos não são excluídos. Permanecem pesquisáveis e relacionados às produções, projetos e eventos de seu período de vínculo.

### Projetos

Uma única entidade `project`, com:

- `research`;
- `teaching`;
- `extension`;
- `transversal`;
- `other`.

Isso permite filtros públicos sem duplicação de schema.

### Produções

Há dois níveis de classificação:

**Macro categoria pública**
- bibliográfica;
- artística;
- audiovisual;
- educacional;
- documental;
- outros.

**Tipo específico**
- artigo;
- livro;
- capítulo;
- organização de livro;
- trabalho em evento;
- tese/dissertação/TCC;
- audiovisual;
- artística;
- exposição;
- material didático;
- documento técnico;
- catálogo;
- podcast/áudio;
- software/recurso digital;
- outro.

Quando `productionType = other`, `otherTypeLabel` deverá ser exigido pelo validador de conteúdo no CI. O Pages CMS mostra o campo permanentemente no protótipo porque a validação condicional ficará fora do CMS na primeira implementação.

### Catalogação

Como não existe uma base consolidada de produções, todo item recebe:

- `identified`;
- `verified`;
- `complete`.

Também pode conter `sourceNotes` e `lastVerifiedAt`, campos internos para rastreabilidade.

## 3. Estratégia de implantação

### Etapa A — branch técnica

Criar branch:

`redesign/fase-1-content-foundation`

Sem alterar as rotas públicas.

### Etapa B — estrutura paralela

Criar:

```text
src/
├── content/
│   ├── pages/
│   ├── people/
│   ├── institutions/
│   ├── projects/
│   ├── productions/
│   ├── documents/
│   ├── collections/
│   ├── events/
│   ├── event-editions/
│   └── news/
└── assets/
    └── uploads/
        ├── images/
        └── documents/
```

A estrutura nova deve coexistir temporariamente com o site atual. O Eleventy só passa a renderizá-la depois que os schemas e testes estiverem estáveis.

### Etapa C — Pages CMS

Adicionar `.pages.yml` e testar em branch.

O Pages CMS permite configuração por repositório e branch, então a primeira validação deve ocorrer fora de `main`.

### Etapa D — fixtures

Cadastrar registros fictícios/temporários representativos:

- 1 integrante atual;
- 1 egresso;
- 1 instituição;
- 1 projeto de pesquisa;
- 1 projeto de extensão;
- 1 produção bibliográfica;
- 1 produção audiovisual;
- 1 produção “outros”;
- 1 evento;
- 1 edição de evento;
- 1 documento.

Os fixtures não devem ser publicados no site real; servem para validar a experiência editorial e as relações.

### Etapa E — validação automática

Antes de integrar conteúdo novo ao build público:

- validação de frontmatter/schema;
- IDs/slugs únicos;
- referências existentes;
- regra `other -> otherTypeLabel`;
- datas coerentes;
- campos mínimos por tipo de produção;
- links;
- acessibilidade automatizável do HTML renderizado.

## 4. Internacionalização

O protótipo adota português como conteúdo primário e um objeto `translations` para EN/ES/FR.

Isso é uma decisão provisória de armazenamento, não apenas visual. Precisaremos testar a ergonomia de editar textos longos traduzidos no Pages CMS antes de congelar o ADR de i18n.

Regras já firmes:

- PT-BR permanece na raiz;
- EN em `/en/`;
- ES em `/es/`;
- FR em `/fr/`;
- tradução incompleta não cria página híbrida;
- título oficial de obra não é automaticamente traduzido;
- `hreflang` e canonical serão gerados no build.

## 5. Mídia

O protótipo separa:

- `src/assets/uploads/images`;
- `src/assets/uploads/documents`.

O Pages CMS grava os caminhos públicos como:

- `/assets/uploads/images/...`;
- `/assets/uploads/documents/...`.

Uploads recebem nomes seguros/slugificados.

Na implementação, imagens raster deverão passar por pipeline de otimização antes de considerarmos o fluxo finalizado.

## 6. Git e governança

O protótipo define commits semânticos do CMS:

- `content(create): ...`
- `content(update): ...`
- `content(delete): ...`
- `content(rename): ...`

A identidade do usuário é preservada quando disponível.

A existência de `draft | review | published` no conteúdo não substitui, por si só, revisão por PR. Precisaremos decidir na Fase 1 se o workflow editorial será:

1. edição diretamente em branch editorial + PR; ou
2. edição em `main`, mantendo itens não publicados ignorados pelo build.

A primeira opção é arquiteturalmente mais segura para o LabMAES.

## 7. Primeiro recorte de catálogo

Como não há inventário prévio, não devemos tentar “completar o LabMAES” antes do lançamento.

Primeiro lote real recomendado:

1. integrantes atuais e egressos cuja informação já esteja disponível;
2. projetos ativos;
3. produções recentes facilmente verificáveis;
4. materiais diretamente produzidos pelo laboratório;
5. registros do Caminhos 2026 já existentes no repositório.

Depois disso, a catalogação histórica passa a ser uma rotina editorial.

## 8. Pontos que o protótipo deliberadamente não resolve

- schema bibliográfico completo por subtipo;
- importação Lattes/ORCID;
- busca pública;
- paginação;
- geração automática de citação ABNT;
- otimização automática de imagens;
- tradução automática;
- workflow de aprovação definitivo;
- migração do Caminhos 2026 para `eventEdition`;
- design visual do painel (o Pages CMS fornece a interface);
- design system público.

Esses itens não bloqueiam a fundação de conteúdo.

## 9. Critério de aprovação do Pages CMS

O protótipo será considerado adequado se uma bolsista sem conhecimento de Git conseguir:

1. cadastrar uma pessoa;
2. marcar uma pessoa como egressa;
3. cadastrar um projeto e relacionar pessoas;
4. cadastrar uma produção e relacionar autoria/projeto;
5. anexar imagem/documento;
6. reconhecer claramente rascunho, revisão e publicação;
7. preencher tradução sem editar YAML;
8. localizar e corrigir um registro já existente.

Se esse teste revelar fricção importante, ajustaremos o schema antes de desenvolver templates públicos.
