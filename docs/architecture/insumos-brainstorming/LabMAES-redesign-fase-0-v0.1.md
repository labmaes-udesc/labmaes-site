# LabMAES — Redesign 2026
## Fase 0 — Arquitetura de informação e modelo de conteúdo v0.1

**Status:** proposta inicial para validação  
**Repositório:** `labmaes-udesc/labmaes-site`  
**Base técnica atual:** Eleventy 3 + Nunjucks + GitHub + Cloudflare Pages

---

## 1. Objetivo

Evoluir o site atual do LabMAES de um site institucional simples, expandido às pressas para hospedar o 7º Seminário Caminhos do Contemporâneo, para uma plataforma institucional durável que também funcione como repositório das produções, projetos, pessoas, eventos, documentos e acervos do laboratório.

Princípio central:

> **Templates definem como o conteúdo aparece; conteúdo estruturado define o que é publicado.**

O GitHub continua como fonte da verdade, o Eleventy continua responsável pela geração estática, o Cloudflare Pages continua responsável pelo deploy e o Pages CMS será a primeira opção de interface editorial para bolsistas e demais editores não técnicos.

---

## 2. Decisões arquiteturais já aceitas

1. Manter Eleventy como gerador estático.
2. Manter GitHub como fonte da verdade e histórico versionado.
3. Manter Cloudflare Pages para build/deploy.
4. Adotar Pages CMS como primeira opção de CMS Git-based.
5. Estruturar o novo site a partir de tipos de conteúdo reutilizáveis, e não de páginas isoladas.
6. Internacionalização nativa em Português, Inglês, Espanhol e Francês.
7. Português em URLs existentes na raiz; idiomas adicionais em `/en/`, `/es/` e `/fr/`.
8. WCAG 2.2 nível AA como requisito formal.
9. SEO, Schema.org, performance e acessibilidade tratados como infraestrutura.
10. Preservar e fortalecer a documentação técnica e editorial do projeto.
11. Tratar o Caminhos do Contemporâneo como um evento com múltiplas edições, e não como uma exceção hardcoded na aplicação.

---

## 3. Inventário inicial do repositório atual

### 3.1 Institucional

- `/` — home institucional do LabMAES;
- `/sobre/` — página atualmente em construção;
- `/contato/` — página de contato completa;
- `/404/` — página de erro;
- header e footer globais em `_includes/`.

### 3.2 Evento

O 7º Caminhos está organizado em:

- `/eventos/caminhos-do-contemporaneo/2026/`;
- programação;
- oficinas;
- submissões;
- mostra audiovisual;
- anais.

Há layouts/header/footer próprios do evento.

### 3.3 Dados estruturados atuais

Em `_data/` já existem alguns precedentes importantes:

- `site.json`;
- `pessoas.json`;
- `programacao.json`;
- `apoiadores.json`.

Esse material demonstra que o projeto já contém conteúdo estruturado, mas atualmente ele está muito associado ao Caminhos 2026 e exige edição manual de JSON.

### 3.4 Infraestrutura

- `eleventy.config.js`;
- `css/tokens.css`;
- `css/components.css`;
- `js/main.js`;
- `_headers`;
- `_redirects`;
- assets de fontes, imagens, logos, editais e gráficos.

### 3.5 Débitos estruturais identificados

- conteúdo institucional relevante ainda embutido diretamente em templates Nunjucks;
- ausência de uma camada editorial amigável;
- ausência de collections institucionais reutilizáveis;
- dados do evento atual misturados à infraestrutura geral;
- navegação com referências hardcoded ao Caminhos 2026;
- ausência de infraestrutura completa de i18n;
- ausência de workflow editorial;
- ausência de busca e filtros por conteúdo;
- ausência de um modelo geral para produções acadêmicas/documentais;
- CSS acumulado com componentes semelhantes ainda não consolidados.

---

## 4. Diretrizes da identidade visual relevantes à arquitetura do design system

O Manual de Marca do LabMAES estabelece quatro conceitos orientadores:

- transdisciplinar;
- impactante;
- convidativo;
- dinâmico.

A identidade é modular: quadrados e formas arredondadas representam a conexão de áreas e podem se desdobrar em módulos gráficos. Essa modularidade é particularmente adequada à construção de um design system digital composto por componentes reutilizáveis.

A paleta institucional registrada no manual inclui:

- Laranja `#F44F21`;
- Vermelho `#B10000`;
- Azul `#302A66`;
- Gelo `#F0F0FF`;
- Verde `#00523C`;
- Rosa `#F4BEBE`.

A fonte principal é Poppins. Thunder é definida como fonte secundária de identidade e deve ser tratada com cautela no produto digital, especialmente quanto a licenciamento, legibilidade, disponibilidade de caracteres e idiomas.

O redesign não deverá simplesmente reproduzir peças gráficas do manual; deverá traduzir esses princípios para um sistema digital acessível, responsivo e consistente.

---

## 5. Modelo de conteúdo v0.1

### 5.1 `page` — Página institucional

Uso: conteúdos editoriais institucionais que não justificam entidade especializada.

Campos-base:

```yaml
id:
slug:
status: draft | review | published
title:
summary:
body:
seoTitle:
seoDescription:
ogImage:
translations:
updatedAt:
```

Exemplos:

- Sobre o LabMAES;
- políticas;
- contato editorial;
- páginas especiais.

---

### 5.2 `person` — Pessoa

Representa membros atuais, egressos, colaboradores e participantes associados a projetos/produções/eventos.

Campos candidatos:

```yaml
id:
slug:
name:
preferredName:
roles: []
status: current | former | collaborator
bio:
photo:
pronouns:
institution:
lattes:
orcid:
website:
socialLinks: []
researchTopics: []
translations:
```

Relações:

- pessoa → projetos;
- pessoa → produções;
- pessoa → eventos;
- pessoa → instituições;
- pessoa → temas.

---

### 5.3 `project` — Projeto

Abrange pesquisa, ensino, extensão e projetos transversais.

```yaml
id:
slug:
title:
acronym:
projectType: research | teaching | extension | other
status: active | completed | planned
startDate:
endDate:
summary:
body:
coordinators: []
participants: []
institutions: []
funders: []
researchTopics: []
productions: []
documents: []
links: []
translations:
```

---

### 5.4 `production` — Produção

Entidade central do repositório acadêmico e cultural.

Tipos candidatos:

- artigo;
- livro;
- capítulo de livro;
- organização de livro;
- trabalho em evento;
- tese/dissertação/TCC;
- produção audiovisual;
- produção artística;
- exposição;
- material didático;
- relatório/documento técnico;
- catálogo;
- podcast/áudio;
- software/recurso digital;
- outro.

Campos-base:

```yaml
id:
slug:
title:
productionType:
year:
date:
authors: []
organizers: []
summary:
abstract:
keywords: []
language:
projects: []
events: []
institutions: []
doi:
isbn:
issn:
citation:
externalUrl:
file:
cover:
license:
featured: false
translations:
```

Observação: campos bibliográficos específicos devem ser condicionais por `productionType`, evitando um formulário enorme para todos os casos.

---

### 5.5 `event` — Evento

Representa a identidade recorrente de um evento.

Exemplo: **Seminário Caminhos do Contemporâneo**.

```yaml
id:
slug:
name:
shortName:
description:
visualIdentity:
websiteSettings:
editions: []
translations:
```

---

### 5.6 `eventEdition` — Edição de evento

Representa uma edição temporal de um evento.

```yaml
id:
event:
year:
title:
theme:
startDate:
endDate:
format:
locations: []
summary:
programItems: []
guests: []
organizers: []
supporters: []
documents: []
productions: []
status: archived | current | planned
translations:
```

O Caminhos 2026 será migrado para esse modelo sem alterar suas URLs públicas existentes durante a transição.

---

### 5.7 `news` — Notícia / atualização

Para atualizações institucionais, chamadas, lançamentos e registros recentes.

```yaml
id:
slug:
title:
date:
summary:
body:
author:
relatedPeople: []
relatedProjects: []
relatedEvents: []
relatedProductions: []
tags: []
cover:
translations:
```

---

### 5.8 `document` — Documento

Representa documentos institucionais e arquivos que precisam ser encontrados e contextualizados.

Tipos candidatos:

- edital;
- regulamento;
- relatório;
- formulário/modelo;
- certificado/modelo;
- programa;
- ata;
- material de apoio;
- outro.

```yaml
id:
slug:
title:
documentType:
date:
summary:
file:
version:
language:
relatedProjects: []
relatedEvents: []
relatedProductions: []
accessibilityNotes:
translations:
```

---

### 5.9 `collection` — Coleção / acervo

Agrupa itens heterogêneos em uma coleção curada.

Exemplos possíveis:

- memória do Caminhos do Contemporâneo;
- acervo audiovisual;
- coleção de publicações;
- coleção documental de um projeto.

```yaml
id:
slug:
title:
summary:
body:
curators: []
items: []
cover:
translations:
```

---

### 5.10 `institution` — Instituição / parceiro

Evita repetir nomes e logos manualmente.

```yaml
id:
slug:
name:
shortName:
kind:
logo:
url:
country:
relationships: []
translations:
```

Pode representar UDESC, CEART, grupos de pesquisa, universidades parceiras, financiadores e instituições apoiadoras.

---

### 5.11 `taxonomy` — Temas e vocabulários controlados

A taxonomia deve ser controlada para impedir variações como `cinema-educação`, `cinema e educação` e `cinema educação` representando conceitos diferentes por acidente.

Inicialmente:

- temas/palavras-chave;
- tipos de produção;
- tipos de projeto;
- papéis de pessoas;
- tipos de documento.

---

## 6. Relações principais

```text
Person ───────┬──── Project
              ├──── Production
              ├──── EventEdition
              └──── Institution

Project ──────┬──── Production
              ├──── Document
              ├──── Person
              └──── Institution

Event ───────────── EventEdition

EventEdition ─┬──── Person
              ├──── Production
              ├──── Document
              └──── Institution

Collection ──────── múltiplos tipos de item
```

O objetivo é que essas relações produzam automaticamente páginas como:

- “Produções de determinada pessoa”;
- “Produções vinculadas a determinado projeto”;
- “Participações no Caminhos”;
- “Documentos de determinada edição”;
- “Projetos relacionados a determinado tema”.

---

## 7. Arquitetura de informação preliminar v0.1

```text
LabMAES
│
├── Sobre
│   ├── O laboratório
│   ├── História
│   ├── Atuação
│   ├── Equipe
│   └── Redes e parceiros
│
├── Projetos
│   ├── Em andamento
│   └── Concluídos
│
├── Produções
│   ├── Todas
│   ├── Bibliográficas
│   ├── Artísticas e audiovisuais
│   ├── Educacionais
│   └── Documentais
│
├── Eventos
│   └── Caminhos do Contemporâneo
│       ├── Edições
│       └── 2026
│
├── Acervo
│   └── Coleções
│
├── Notícias
│
└── Contato
```

### Observação

A separação entre **Produções** e **Acervo** deverá ser validada conceitualmente. A proposta atual é:

- **Produção** = item produzido intelectual, artística, pedagógica ou tecnicamente pelo laboratório e seus membros;
- **Acervo** = coleção curada de objetos, documentos, registros e produções, podendo incluir materiais que não sejam autoria do LabMAES.

---

## 8. Estratégia de URLs e idiomas

Português permanece na raiz para preservar URLs existentes:

```text
/sobre/
/projetos/
/producoes/
/eventos/
```

Idiomas adicionais:

```text
/en/about/
/en/projects/
/en/outputs/

/es/sobre/
/es/proyectos/
/es/producciones/

/fr/a-propos/
/fr/projets/
/fr/productions/
```

Regras:

1. uma tradução ausente não cria uma página artificialmente “traduzida” apenas no menu;
2. páginas equivalentes terão `hreflang` recíproco;
3. idioma e disponibilidade de tradução serão propriedades do conteúdo;
4. títulos de obras e referências bibliográficas não serão automaticamente traduzidos quando isso descaracterizar a publicação original;
5. slugs traduzidos serão explicitamente definidos para evitar geração automática inconsistente.

---

## 9. Estrutura de arquivos candidata

```text
src/
├── _data/
│   ├── site.json
│   ├── navigation.json
│   ├── taxonomies/
│   └── i18n/
│
├── _includes/
│   ├── layouts/
│   ├── components/
│   ├── patterns/
│   └── macros/
│
├── content/
│   ├── pages/
│   ├── people/
│   ├── projects/
│   ├── productions/
│   ├── events/
│   ├── news/
│   ├── documents/
│   ├── collections/
│   └── institutions/
│
├── assets/
├── css/
└── js/
```

Ainda não está decidido se a raiz de input do Eleventy será migrada imediatamente para `src/` ou se essa mudança será feita em etapa posterior para reduzir risco.

---

## 10. Pages CMS — coleções editoriais candidatas

Na primeira configuração do CMS, os editores deverão enxergar conceitos editoriais, e não diretórios técnicos:

- Páginas;
- Pessoas;
- Projetos;
- Produções;
- Eventos e edições;
- Notícias;
- Documentos;
- Coleções;
- Instituições.

Requisitos de UX editorial:

1. campos obrigatórios claramente identificados;
2. ajuda contextual nos campos complexos;
3. selects para vocabulários controlados;
4. referências entre entidades por ID/slug, evitando texto livre;
5. preview de imagem;
6. validação de datas e URLs;
7. metadados SEO com defaults automáticos;
8. status editorial visível;
9. evitar edição direta de YAML sempre que possível;
10. documentação editorial integrada ao fluxo.

---

## 11. Workflow editorial proposto

### Editor / bolsista

- cria e atualiza conteúdo;
- faz upload de mídia;
- associa pessoas, projetos, eventos e produções;
- prepara tradução quando disponível.

### Revisor

- verifica texto, metadados, relações e acessibilidade editorial;
- aprova publicação.

### Administrador / desenvolvedor

- altera schema;
- cria componentes;
- modifica layouts;
- altera build, segurança e infraestrutura.

Fluxo desejado:

```text
Rascunho → Revisão → Publicado
```

A implementação exata dependerá dos recursos disponíveis no Pages CMS e no fluxo GitHub escolhido.

---

## 12. SEO e dados estruturados por tipo

| Entidade | Schema.org candidato |
|---|---|
| LabMAES | `Organization` / relação com `CollegeOrUniversity` |
| Pessoa | `Person` |
| Projeto | `ResearchProject` quando aplicável, ou modelagem complementar |
| Artigo | `ScholarlyArticle` |
| Livro | `Book` |
| Evento | `Event` |
| Produção audiovisual | `VideoObject` quando aplicável |
| Documento | `DigitalDocument` / tipo mais específico quando aplicável |
| Notícia | `Article` / `NewsArticle` apenas quando semanticamente adequado |
| Breadcrumbs | `BreadcrumbList` |

A escolha final será validada entidade por entidade para evitar uso inadequado de tipos apenas por conveniência.

---

## 13. Acessibilidade — critérios transversais iniciais

O redesign terá como baseline WCAG 2.2 AA.

Critérios iniciais:

- navegação completa por teclado;
- foco sempre visível;
- skip links;
- landmarks semânticos;
- headings hierarquicamente corretos;
- contraste validado por token e estado;
- touch targets adequados;
- componentes testados em zoom/reflow;
- `prefers-reduced-motion`;
- alternativas textuais para imagens relevantes;
- imagens decorativas sem ruído para tecnologia assistiva;
- links externos identificáveis de forma acessível quando necessário;
- formulários/CMS orientados a boas práticas de texto alternativo;
- idioma da página e de trechos quando aplicável;
- auditoria automatizada complementada por testes manuais.

---

## 14. Design system — direção inicial

A modularidade da marca será traduzida em arquitetura de componentes:

```text
Design tokens
    ↓
Primitives
    ↓
Components
    ↓
Patterns
    ↓
Templates
    ↓
Pages
```

### Tokens iniciais

- cor;
- tipografia;
- espaçamento;
- dimensões;
- bordas/radius;
- elevação quando necessária;
- motion;
- breakpoints;
- container widths;
- focus states.

### Componentes candidatos

- button;
- link;
- tag;
- card;
- person card;
- production card;
- project card;
- event card;
- document card;
- breadcrumb;
- pagination;
- filter controls;
- language selector;
- search result;
- alert/callout.

---

## 15. ADRs iniciais a registrar

Quando houver acesso de escrita ao repositório:

1. `ADR-001-static-site-eleventy.md` — manutenção do Eleventy;
2. `ADR-002-content-model.md` — conteúdo estruturado e relações;
3. `ADR-003-pages-cms.md` — Pages CMS como camada editorial inicial;
4. `ADR-004-i18n-url-strategy.md` — PT raiz + EN/ES/FR;
5. `ADR-005-accessibility-baseline.md` — WCAG 2.2 AA;
6. `ADR-006-git-content-workflow.md` — GitHub como source of truth.

---

## 16. Fases posteriores propostas

### Fase 0 — Arquitetura e conteúdo

Atual.

### Fase 1 — Fundação técnica

- reorganização segura do projeto;
- collections;
- schema/content validation;
- Pages CMS mínimo;
- i18n foundation;
- CI de qualidade.

### Fase 2 — Design system

- tokens;
- componentes;
- documentação;
- protótipos Figma;
- testes de acessibilidade dos componentes.

### Fase 3 — Institucional

- home;
- sobre;
- equipe;
- projetos;
- contato.

### Fase 4 — Repositório

- produções;
- documentos;
- coleções;
- busca;
- filtros;
- relações automáticas.

### Fase 5 — Eventos

- migrar Caminhos 2026 para o modelo geral;
- preservar URLs;
- preparar novas edições.

### Fase 6 — Internacionalização

- interface;
- workflows de tradução;
- conteúdo prioritário nos quatro idiomas;
- QA linguístico e SEO internacional.

### Fase 7 — Hardening e lançamento

- performance;
- segurança;
- regressão visual;
- acessibilidade manual;
- SEO técnico;
- redirects;
- documentação editorial final.

---

## 17. Pontos a validar com a equipe do LabMAES

1. **Produções:** quais categorias oficiais o laboratório precisa distinguir?
2. **Pessoas:** o site deve manter uma página pública de egressos e colaboradores anteriores?
3. **Projetos:** pesquisa, ensino e extensão devem aparecer como tipos de uma mesma entidade ou como áreas editoriais diferentes?
4. **Acervo:** quais materiais já existem e precisam ser preservados/publicados?
5. **Documentos:** quais documentos devem ser públicos e quais nunca devem entrar no repositório público?
6. **Eventos:** além do Caminhos do Contemporâneo, existem outros eventos recorrentes que precisam do mesmo modelo?
7. **Notícias:** há interesse real em manter publicação periódica de notícias, ou uma seção de “Atualizações” mais leve seria sustentável?
8. **Idiomas:** quais conteúdos terão prioridade de tradução completa na primeira versão multilíngue?
9. **Equipe editorial:** quantas pessoas editarão e quem fará revisão/aprovação?
10. **Produções legadas:** existe uma fonte organizada atual (Lattes, ORCID, planilha, Zotero, currículo institucional etc.) para iniciar a migração?

---

## 18. Critério de conclusão da Fase 0

A Fase 0 estará concluída quando:

- entidades e relações estiverem aprovadas;
- arquitetura de informação estiver aprovada;
- categorias/taxonomias principais estiverem definidas;
- responsabilidades editoriais estiverem definidas;
- estratégia i18n estiver formalizada;
- ADRs estiverem versionados;
- existir uma amostra de conteúdo real suficiente para testar o CMS e os templates na Fase 1.

