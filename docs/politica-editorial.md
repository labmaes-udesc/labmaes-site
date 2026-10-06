# Política editorial do site do LabMAES

**Decidida em:** 2026-10-06, pela coordenação do projeto (issues #17 a #22)
**Vale para:** todo conteúdo editado pelo Pages CMS (`src/content/`)

Este documento responde às pendências de política editorial da spec da Fase 0. Ele não altera o
schema nem os ADRs; diz como a equipe usa o CMS. A ordem de precedência continua a de
[architecture/README.md](architecture/README.md).

## Quem publica (#22)

**Bolsistas criam e publicam.** A coordenação revisa por amostragem, depois de publicado.

- "Rascunho": trabalho em andamento; não aparece no site.
- "Em revisão": a bolsista tem dúvida e pede que a coordenação olhe antes. Não é etapa obrigatória.
- "Publicado": aparece no site.

O CMS não tem permissão por campo: a regra é combinada, não travada. As edições vão direto para a
`main` ([ADR 0008](architecture/adr/0008-publicacao-direta-cms.md)), e a CI avisa quem editou se
algum registro quebrar uma regra.

## Que documentos podem entrar no CMS (#18)

O repositório é público e **o histórico do Git é permanente**: um arquivo enviado pelo CMS continua
recuperável mesmo depois de apagado. Por isso, só entram arquivos **que já são públicos por
natureza**.

| Pode | Nunca |
| --- | --- |
| editais, chamadas e regulamentos já divulgados | avaliações, pareceres e notas |
| programações e cadernos de resumos | listas de inscritos ou de participantes com dados de contato |
| anais e trabalhos já publicados | documentos pessoais (RG, CPF, comprovantes, laudos, exames) |
| relatórios publicados | contratos, termos de outorga, prestação de contas |
| templates e materiais de apoio | qualquer arquivo usado "só para testar" |

Na dúvida, não envie: guarde o documento fora do site e publique só o link.

Fotos de pessoas só com autorização de uso de imagem. Fontes primárias digitalizadas do acervo
físico (ver abaixo) só depois de conferir direitos e se há dados pessoais de terceiros.

Limite prático de upload pelo CMS: cerca de 2,5 MB por arquivo. Arquivos maiores vão por commit
direto, feito por quem administra o repositório.

## Atualizações em vez de notícias (#20)

A seção de notícias vira **"Atualizações"**, sem compromisso de periodicidade: título, data, duas ou
três frases e um link. A home mostra as três mais recentes. Assim o site não parece abandonado
quando passa meses sem uma nova publicação. A divulgação do dia a dia continua no Instagram.

Implementação: Fase 3 (#44). A coleção `news` do CMS é a base.

## O que é traduzido (#21)

Na primeira versão multilíngue (EN, ES, FR), são traduzidos por completo:

- as páginas institucionais (Sobre, áreas de atuação, contato) e a interface do site;
- os resumos de projetos e de produções.

**Ficam só em português:** atualizações e páginas de eventos. **Títulos oficiais de obras** ficam
no idioma original. Uma página sem tradução não ganha versão parcial no outro idioma
([ADR 0004](architecture/adr/0004-i18n.md)).

## Eventos (#19)

O único evento recorrente é o **Caminhos do Contemporâneo**. O modelo `event` / `eventEdition`
existe para ele; eventos pontuais entram como atualizações.

## Acervo (#17)

Materiais que o LabMAES tem e quer preservar ou publicar, em ordem de entrada prevista no
repositório de produções (Fase 4):

1. anais do Caminhos (2017–2026) e cadernos de resumos;
2. trabalhos acadêmicos;
3. materiais didáticos (apostilas, oficinas, extensão);
4. registros de eventos (fotos, vídeos, gravações de mesas e da Mostra Audiovisual);
5. peças e coleções do acervo físico de moda e indumentária, com fotos e fichas de catalogação;
6. fontes primárias de pesquisa guardadas no acervo físico.

Os itens 4 a 6 exigem mais cuidado com direitos de imagem, autorização de uso e dados pessoais (ver
"Que documentos podem entrar no CMS"). O formato de catalogação deles é definido na spec da Fase 4.
