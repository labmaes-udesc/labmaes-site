# Fase 1 — Content foundation

## Objetivo

Introduzir a nova camada editorial sem alterar o comportamento do site publicado.

## Incluído neste pacote

- `.pages.yml` na raiz;
- estrutura `src/content/*`;
- estrutura de uploads separada para imagens e documentos;
- validador mínimo sem dependências;
- instrução de script para `package.json`.

## Decisões de segurança editorial nesta versão

No Pages CMS, as coleções centrais de pessoas, instituições, projetos, produções e eventos
permitem criação, mas desabilitam rename/delete inicialmente. Isso evita quebra de referências
durante o piloto editorial.

`settings.content.merge: true` preserva metadados ainda não modelados enquanto o schema está em
transição.

## O que não muda nesta etapa

- Eleventy continua lendo a estrutura atual;
- nenhuma URL pública muda;
- Cloudflare continua com o build atual;
- `_data/`, `_includes/`, páginas `.njk`, CSS e JS existentes permanecem intocados.

## Critério para avançar

A camada só será ligada ao Eleventy depois que:
1. o Pages CMS carregar sem erro;
2. os registros de fixture puderem ser relacionados;
3. o workflow de edição estiver entendido;
4. o schema completo tiver validação automatizada;
5. não houver risco de publicar fixtures por engano.
