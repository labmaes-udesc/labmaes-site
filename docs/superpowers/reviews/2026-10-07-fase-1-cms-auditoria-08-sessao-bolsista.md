# Auditoria 08 — sessão de uso do CMS com bolsista e fluxo de revisão

**Data da sessão:** 2026-10-06; resultados registrados em 2026-10-07
**Status:** aprovado; um ajuste de clareza aplicado; um risco operacional registrado

Teste D do roteiro da Fase 1 (#15), com uma bolsista que nunca tinha usado o Pages CMS, e o teste do
fluxo de revisão (#13), feito na mesma sessão. Branch `teste/cms-fase-1`, recriada a partir da `main`
(`dce007d`) antes da sessão. Os resultados detalhados estão nas issues; esta auditoria registra o que
o CMS gravou de fato e os achados.

## Resultado

| Tarefa | Sozinha? |
| --- | --- |
| D1 Cadastrar pessoa fictícia com foto e texto alternativo | sim |
| D2 Marcar pessoa como egressa, com fim do vínculo | sim |
| D3 Criar projeto de extensão com coordenação | sim |
| D4 Ligar o projeto a uma instituição | sim |
| D5 Cadastrar artigo com autora interna e autor externo, em ordem | sim |
| D6 Anexar PDF e capa com texto alternativo | sim |
| D7 Escrever o resumo do projeto em inglês | sim |
| D8 Achar um registro e corrigir a biografia | sim |
| #13 Rascunho → Em revisão → Publicado; entendeu os três estados sem explicação | sim |

Nos commits da sessão (`d02ec0c` … `51d0a76`), os registros foram gravados com as relações
corretas: coordenação e instituição no projeto; `contributors` na ordem, com bloco interno e
externo; foto e capa com texto alternativo; egressa com `status: alumnus`.

## Achados

**1. Os dois resumos de Produções não eram distinguíveis.** A própria bolsista registrou a dúvida
dentro do campo de tradução: não sabia a diferença entre "Resumo de apresentação" e
"Resumo/abstract da obra", nem qual dos dois o campo "Summary" traduzia. **Ajuste:** os dois campos
e o grupo "Traduções" ganharam texto de ajuda. O de apresentação é escrito pelo LabMAES e é o que se
traduz; o abstract é copiado da obra, no original.

**2. O CMS usou a configuração antiga do `.pages.yml`.** A produção criada na sessão traz
`productionCategory`, campo removido da `main` pelo ADR 0009 antes da sessão. A branch tinha sido
recriada por *force-update* da referência, sem commits novos alterando o `.pages.yml`. Isso indica que
o Pages CMS mantém a configuração em cache e só a relê quando um push traz mudança nesse arquivo. O
validador acusou o campo desconhecido. **Consequências:**
- uma mudança no `.pages.yml` deve entrar por commit normal (merge de PR), nunca por reset de branch;
- depois de mudar o `.pages.yml`, conferir no CMS que o formulário reflete a mudança;
- os placeholders em português (#92) e a remoção de "Macro categoria" (#95) foram vistos pela
  bolsista na versão antiga, então a conferência deles fica para o primeiro uso real na `main`.

**3. Arquivo real usado como "PDF de teste".** O PDF anexado na tarefa D6 é um capítulo de livro
publicado, protegido por direito autoral. Não contém dado pessoal, mas ficou numa branch pública até
a branch ser apagada. A política editorial já proíbe "qualquer arquivo usado só para testar". Nos próximos
testes, usar o PDF fictício que já está no repositório (`src/assets/uploads/documents/fixture-documento.pdf`,
baixável pelo GitHub) e uma imagem sem pessoas criada para isso.

## Limpeza

A branch `teste/cms-fase-1` foi apagada depois desta auditoria; os registros `teste-*` nunca chegaram
à `main`. Os commits dela deixam de aparecer no repositório, embora o GitHub possa mantê-los
acessíveis pelo SHA por algum tempo.
