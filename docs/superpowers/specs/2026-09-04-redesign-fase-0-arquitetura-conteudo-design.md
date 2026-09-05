# Spec — Redesign Fase 0: Arquitetura de informação e conteúdo

**Status:** Aprovada  
**Data:** 2026-09-04

## Problema

O site nasceu como solução rápida para divulgação do 7º Caminhos do Contemporâneo e
precisa evoluir para uma plataforma institucional durável, multilíngue, acessível,
otimizada para SEO e capaz de funcionar como repositório das produções do LabMAES.

A manutenção não pode depender de bolsistas editando templates, JSON ou Git diretamente.

## Objetivos da Fase 0

1. definir princípios arquiteturais;
2. definir arquitetura de informação;
3. definir modelo de conteúdo;
4. estabelecer estratégia editorial;
5. estabelecer requisitos de i18n, acessibilidade e SEO;
6. selecionar abordagem inicial de CMS;
7. preparar a fundação da Fase 1 sem alterar o site público.

## Arquitetura aprovada

- Eleventy + Cloudflare Pages permanecem;
- GitHub é fonte da verdade;
- Pages CMS será o primeiro CMS Git-based a ser validado;
- conteúdo será estruturado e relacional;
- PT-BR na raiz, EN/ES/FR em prefixos;
- WCAG 2.2 AA é requisito mínimo;
- produção acadêmica e institucional será catalogada progressivamente.

## Modelo de conteúdo v1

### Person

Mantém integrantes atuais, egressos e colaboradores.

Campos mínimos:
- slug;
- name;
- preferredName;
- status;
- membershipStart / membershipEnd;
- bio;
- institution;
- roles;
- identificadores externos quando disponíveis.

### Project

Uma entidade com `projectType`:
- research;
- teaching;
- extension;
- transversal;
- other.

### Production

Possui macro categoria pública e tipo específico.

Macro categorias:
- bibliographic;
- artistic;
- audiovisual;
- educational;
- documentary;
- other.

`productionType: other` exige `otherTypeLabel`.

Toda produção possui `catalogStatus`.

### Event / EventEdition

O evento é entidade permanente; cada edição é um registro relacionado. O Caminhos do
Contemporâneo deixa de ser uma exceção hardcoded e passa a seguir esse modelo.

### Demais entidades

- page;
- institution;
- document;
- collection;
- news.

## Arquitetura de informação inicial

- Sobre
  - Laboratório
  - História
  - Áreas de atuação
  - Equipe
    - integrantes atuais
    - egressos
  - Redes e parceiros
- Pesquisa e projetos
- Produções
  - bibliográficas
  - artísticas
  - audiovisuais
  - educacionais
  - documentais
  - outros
- Acervo
- Eventos
- Notícias / agenda
- Contato

## Requisitos transversais

### SEO
Metadados, canonical, Open Graph, sitemap, hreflang e Schema.org devem ser gerados por
tipo de conteúdo sempre que aplicável.

### Acessibilidade
Componentes e conteúdo devem observar ADR 0005.

### Internacionalização
Observar ADR 0004. Traduções ausentes não criam páginas mistas.

### Editorial
A edição cotidiana deve ser possível sem conhecimento de Git/YAML.

## Critérios de conclusão da Fase 0

A fase é concluída quando existem e estão aprovados:

- ADRs arquiteturais iniciais;
- esta spec;
- plan correspondente;
- modelo de conteúdo v1;
- arquitetura de informação v1;
- estratégia de CMS;
- política de catalogação progressiva.

Com a inclusão desses documentos, a Fase 0 é considerada concluída.

## Pendências de política editorial (não bloqueiam a Fase 1)

A arquitetura técnica e o modelo de conteúdo estão aprovados. As perguntas abaixo,
levantadas em `insumos-brainstorming/LabMAES-redesign-fase-0-v0.2.md` (seção 17), ainda
não foram respondidas pela equipe do LabMAES e devem ser resolvidas durante a Fase 1,
antes da primeira carga real de conteúdo:

1. **Acervo:** quais materiais já existem e precisam ser preservados/publicados?
2. **Documentos:** quais documentos devem ser públicos e quais nunca devem entrar no
   repositório público?
3. **Eventos:** além do Caminhos do Contemporâneo, existem outros eventos recorrentes
   que precisam do mesmo modelo?
4. **Notícias:** há interesse real em manter publicação periódica de notícias, ou uma
   seção de "Atualizações" mais leve seria sustentável?
5. **Idiomas:** quais conteúdos terão prioridade de tradução completa na primeira versão
   multilíngue?
6. **Equipe editorial:** quantas pessoas editarão e quem fará revisão/aprovação? (Relevante
   para o fluxo `draft → review → published` do ADR 0006, que hoje assume papéis sem
   defini-los.)

Essas respostas não alteram o schema nem os ADRs aceitos; afetam política de conteúdo e
podem ser resolvidas em paralelo à Fase 1.
