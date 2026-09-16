# Auditoria 04 — modelo `contributors`

**Data:** 2026-09-16  
**Status:** implementação preparada; reteste no Pages CMS pendente

## Motivação

O campo anterior `authors` aceitava apenas referências para a coleção `people`. Isso exigiria
criar perfis artificiais para coautores externos e não representaria adequadamente créditos de
produções artísticas ou audiovisuais.

## Decisão

Substituir `authors` por `contributors`, uma lista ordenada de blocos.

Tipos:

### `internal`

```yaml
kind: internal
person: <slug de people>
role: <opcional>
```

### `external`

```yaml
kind: external
name: <obrigatório>
role: <opcional>
affiliation: <opcional>
orcid: <opcional>
```

## Por que `block`

O Pages CMS usa `type: block` para listas em que cada item pode ter um schema diferente.
`blockKey: kind` persiste explicitamente qual formato foi selecionado.

## Fixture de teste principal

`2025-fixture-producao-bibliografica.md` passa a conter:

1. integrante interna;
2. pessoa externa fictícia;
3. integrante interna.

Isso testa simultaneamente:
- referência aninhada;
- pessoa externa;
- ordem autoral;
- mistura de tipos na mesma lista.

## Critérios de aprovação

O modelo será aprovado quando o Pages CMS:

1. carregar os três contributors existentes;
2. permitir reordená-los;
3. preservar a ordem após salvar e reabrir;
4. exibir a pessoa interna por nome legível;
5. salvar o slug no campo `person`;
6. salvar o nome diretamente no bloco externo;
7. impedir produção sem nenhum contributor;
8. não reintroduzir `authors`.

## Ponto deliberadamente adiado

A busca da lista de Produções não indexará `contributors` nesta correção. Primeiro será validado
o comportamento de campos aninhados em listas `block`.
