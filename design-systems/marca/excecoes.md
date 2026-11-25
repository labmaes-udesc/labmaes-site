# Exceções às regras da design-taste-frontend (spec da Fase 2, seção 4.2)

Cada tela cita estes códigos no `verificacao.md` quando um aviso dos verificadores cai numa
exceção. Um aviso que não cai em nenhuma exceção é corrigido.

| Código | Regra da skill | No LabMAES |
|---|---|---|
| EX-1 | Sem violeta nem lavanda | Vale a paleta do manual (azul #302A66, gelo #F0F0FF) |
| EX-2 | Fundos chapados, sem grão fora de tecnologia | Grão e trama leves como detalhe (spec 2.4) |
| EX-3 | Uma seção por tela | Só na home e nas institucionais; repositório, item, leitura longa e programação seguem o conteúdo |
| EX-4 | Nenhuma legenda sob imagem | Acervo e produções têm legenda, crédito e autoria |
| EX-5 | Fotos de banco como substitutas | Proibidas; sem foto real, composição de módulos ou textura de IA |
| EX-6 | Ícones reais coloridos de produtos | Ícones modulares da marca, sempre com rótulo |
| EX-7 | Contatos em .example, sem número | Dados reais e públicos do LabMAES |
| EX-8 | Um ou dois "momentos" em toda página | Só na home, no Sobre, na edição de evento e na 404 |
| EX-9 | copy-lint em inglês | Textos em português; avisos de vocabulário inglês não se aplicam |

O gate da skill aceita no máximo 5 waivers por tela. Avisos cobertos por exceção além disso
ficam só no `verificacao.md`, e a tela é encerrada com `gate.mjs --done` depois da aprovação do
usuário (Tarefa B0, Passo 7).
