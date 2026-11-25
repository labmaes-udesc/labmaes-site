# ADR 0010 — O redesign só vai ao ar com a aprovação da coordenadora do LabMAES

- Status: Aceito
- Data: 2026-11-25
- Relaciona-se a: ADR 0008

## Contexto

O redesign substitui, fase a fase, a cara pública do LabMAES. A identidade do laboratório e a
forma como ele se apresenta são responsabilidade da coordenação.

## Decisão

- Nenhuma parte da nova versão do site (redesign, Fases 2 a 7) fica pública sem a aprovação da
  coordenadora do LabMAES, Profa. Mara Rúbia Sant'Anna.
- O trabalho de cada fase acontece numa branch própria (`redesign/fase-N-...`). Até a
  aprovação, só existem deploys de preview, e nada da fase chega à `main`, que publica em
  produção.
- O último passo de cada fase é enviar à coordenadora um pacote com o link do preview, as
  imagens das telas e um resumo das decisões em linguagem não técnica.
- A resposta é registrada em `docs/superpowers/reviews/` e na issue da aprovação. Pedidos de
  mudança levam de volta à etapa correspondente, e o pacote é reenviado.

## Fora do alcance desta regra

As atualizações de conteúdo do site atual feitas pelo Pages CMS seguem o ADR 0008 e não
dependem desta aprovação.

## Consequências

- A data de publicação de cada fase depende da agenda da coordenação.
- As URLs de preview não são indexadas nem aparecem no site, mas qualquer pessoa com o endereço
  consegue abri-las. Se for preciso restringir o acesso, a alternativa é o Cloudflare Access.
- Para reduzir retrabalho, previews intermediários podem ser mostrados à coordenação como
  consulta informal; a aprovação formal continua sendo o último passo.
