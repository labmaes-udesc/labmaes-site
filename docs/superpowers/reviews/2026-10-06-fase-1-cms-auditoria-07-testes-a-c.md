# Auditoria 07 — testes A, B e C do Pages CMS

**Data:** 2026-10-06
**Status:** testes A, B e C concluídos; ajustes aplicados. Teste D (sessão com bolsista, #15) pendente.

Testes feitos pelo responsável do projeto no Pages CMS, na branch `teste/cms-fase-1`, seguindo o
roteiro da Fase 1. Os resultados detalhados estão nas issues #11, #12 e #14. Esta auditoria
registra o que o CMS gravou de fato (lido nos commits da branch) e os ajustes que vieram dos testes.

## Teste A — situação de publicação e textos de ajuda (#11)

| Verificação | Resultado |
| --- | --- |
| Textos de ajuda de Status editorial, Situação de publicação e Estado de catalogação aparecem | sim |
| Status editorial e Estado de catalogação ficam claros | sim |
| Situação de publicação pode ficar em branco | sim: limpar o campo **remove a chave** do arquivo (commit `ad83206`) |
| Escolher "No prelo" grava `publicationStatus: in-press` | sim (commit `5e26ed8`) |

**Achados:**
- o texto de ajuda de Situação de publicação ficou longo demais;
- "em branco deveria ser o padrão".

**Diagnóstico.** O vazio **já é** o padrão: registro novo sem escolha não grava a chave (ex.: o
registro criado no teste C, `2025-teste-producao.md`). O problema é de comunicação. Segundo o
código do Pages CMS (`fields/core/select/edit-component.tsx`), um `select` vazio mostra o
placeholder padrão em inglês, "Select...", e nada indica que deixar em branco é uma escolha válida.

**Ajustes:**
- todos os 14 campos `select` do `.pages.yml` ganharam `options.placeholder` em português:
  "Selecione…" nos obrigatórios, "Em branco (opcional)" nos opcionais, e
  "Em branco: não se aplica ou ainda não se sabe" em Situação de publicação;
- o texto de ajuda de Situação de publicação foi reduzido a uma frase.

## Teste B — traduções (#12)

Todos os itens aprovados.

- Formato completo (Projetos): título, resumo e corpo em inglês preservados ao reabrir. Espanhol só
  com título; francês vazio **não gera chave** no arquivo. Negrito e lista no corpo são gravados
  como Markdown (bloco YAML `|+`).
- Formato curto (Produções): só o campo de resumo por idioma; resumo em francês preservado.
- Observação: ao salvar, o CMS reformata o arquivo inteiro (aspas, recuo de listas, datas sem
  aspas). O conteúdo é o mesmo, e o validador lê as datas normalmente, mas o diff do Git mostra mais
  linhas do que as editadas.

## Teste C — mensagens de erro e campos obrigatórios (#14)

| Caso | Resultado |
| --- | --- |
| C1 Pessoa sem nome completo | não salva |
| C2 Slug com maiúsculas e espaço | não salva |
| C3 Produção sem nenhuma pessoa autora | não salva |
| C4 Ano com letras | não aceita |
| C5 Documento sem arquivo | não salva |
| C6 Edição de evento sem evento | não salva |
| C7 Tipo "Outro" sem "Se “Outro”, qual?" | o CMS salva (esperado); a CI acusa no PR #89 |

**Achado (C7):** a CI acusou o erro, mas com nomes técnicos (`otherTypeLabel`, `"other"`, caminho
do arquivo). **Ajuste:** issue #90 / PR #91. O validador agora usa os nomes do CMS (coleção, título
do registro, label do campo e das opções) e publica um resumo em português na página da execução.

## Pendências

- Teste D (#15): sessão com uma bolsista, quando houver acesso a uma.
- Os placeholders novos devem ser conferidos no CMS na próxima sessão de uso, que pode ser a do teste D.
- A branch `teste/cms-fase-1` continua existindo para o teste D. O PR #89 foi fechado sem merge,
  depois de cumprir seu papel no C7. Depois do teste D, a branch será apagada, e os registros
  `teste-*` nunca chegam à `main`.
