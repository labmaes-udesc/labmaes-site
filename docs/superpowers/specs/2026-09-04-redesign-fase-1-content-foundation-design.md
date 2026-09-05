# Spec — Redesign Fase 1: Content foundation

**Status:** Em implementação  
**Data:** 2026-09-04  
**Dependência:** Fase 0 concluída e ADRs 0001–0006 aceitos.

## Objetivo

Introduzir uma camada editorial estruturada e paralela ao site atual, validando o
Pages CMS e o schema v1 sem alterar URLs nem comportamento público.

## Escopo

- `.pages.yml`;
- `src/content/`;
- coleções do schema v1;
- diretórios de mídia;
- mecanismo inicial de validação;
- fixtures editoriais não publicadas;
- teste da experiência de edição.

## Fora de escopo

- redesign visual;
- migração integral do conteúdo atual;
- busca pública;
- integração completa do novo conteúdo com templates do Eleventy;
- importação automática Lattes/ORCID;
- mudança de domínio/deploy.

## Requisitos

### Compatibilidade

O build atual deve continuar produzindo o mesmo site público enquanto a nova camada não
for ativada.

### CMS

Uma bolsista deve conseguir, sem editar YAML:
- criar pessoa;
- marcar egresso;
- criar projeto;
- relacionar pessoas e instituições;
- cadastrar produção;
- anexar mídia;
- editar traduções;
- localizar e corrigir registros.

### Segurança editorial

Durante o piloto, operações destrutivas que possam quebrar referências devem ser
limitadas. Slugs devem ser tratados como identificadores estáveis.

### Validação

Antes da integração pública, validar:
- slugs/IDs únicos;
- referências existentes;
- `other` + `otherTypeLabel`;
- datas coerentes;
- campos mínimos;
- frontmatter/schema;
- build do Eleventy.

## Critérios de saída

A Fase 1 termina quando:
1. o CMS carrega a configuração sem erros;
2. fixtures relacionais funcionam;
3. schema é validado automaticamente;
4. o site atual continua inalterado;
5. o fluxo editorial é aprovado para uso por bolsistas;
6. decisões emergentes são registradas em ADR quando arquiteturais.
