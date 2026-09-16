# Auditoria 03b — fallback para labels explícitos

**Data:** 2026-09-16  
**Status:** correção pendente de reteste no CMS

## Achado

Após a Correção 03, as referências continuaram presentes, mas seus chips apareceram sem texto.

Configuração testada:

```yaml
value: '{fields.slug}'
label: '{primary}'
```

O conteúdo relacional já salvo permaneceu estruturado por slug; o problema observado é de
apresentação no editor.

## Decisão

Não depender de `{primary}` no piloto hospedado.

Usar labels explícitos:

- pessoa: `{fields.name}`;
- instituição: `{fields.name}`;
- projeto: `{fields.title}`;
- evento: `{fields.name}`.

O valor permanece:

`{fields.slug}`

## Critério de aprovação

O teste será aprovado quando:
1. os chips e opções do seletor exibirem nomes/títulos legíveis;
2. o frontmatter continuar armazenando slugs;
3. referências múltiplas mantiverem a ordem.
