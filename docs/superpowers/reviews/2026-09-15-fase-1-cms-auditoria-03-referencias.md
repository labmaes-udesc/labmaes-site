# Auditoria 03 — referências relacionais no Pages CMS

**Data:** 2026-09-15  
**Status:** teste funcional aprovado com correção de UX pendente

## Teste realizado

Foi criado pelo Pages CMS o projeto:

`src/content/projects/teste-referencias-projeto.md`

O teste incluiu:

- coordenação;
- múltiplos participantes;
- instituição relacionada;
- armazenamento em lista ordenada.

## Resultado

### Aprovado

- busca e seleção de referências funcionam;
- múltiplas referências funcionam;
- os valores persistidos são slugs, não nomes duplicados;
- a ordem das listas é preservada;
- coordenação, participantes e instituições permanecem campos independentes.

Exemplo persistido:

```yaml
coordinators:
  - outra-pessoa-teste

participants:
  - fixture-pessoa-atual
  - fixture-pessoa-egressa
  - outra-pessoa-teste

institutions:
  - fixture-instituicao-parceira
```

### Problema encontrado

No seletor do Pages CMS, as referências foram exibidas como nomes de arquivo, por exemplo:

`fixture-pessoa-atual.md`

A configuração utilizava `label: '{name}'`. No Pages CMS, `{name}` representa o nome da entrada,
enquanto `{primary}` representa o campo definido em `view.primary`.

## Correção 03

Padronizar todas as referências para:

```yaml
value: '{fields.slug}'
label: '{primary}'
```

## Decisão adicional de modelagem

Para produções, o campo simples `authors` será substituído por um modelo ordenado `contributors`
capaz de representar tanto pessoas internas referenciadas quanto pessoas externas informadas
nominalmente.

Essa decisão refina o modelo relacional já estabelecido no ADR 0003 e não exige um novo ADR neste
momento.

## Critério de aprovação

A Correção 03 será considerada aprovada quando o Pages CMS:

1. exibir pessoas/instituições/projetos/eventos por nome ou título legível;
2. continuar salvando os slugs no frontmatter;
3. preservar a ordem de referências múltiplas.
