# Caderno de Resumos do 7º Caminhos do Contemporâneo — design

Data: 2026-08-10
Status: aprovado (brainstorming)

## Problema

Os 27 resumos aprovados (9 Pôster, 18 Comunicação Oral) foram submetidos antes da
mudança de programação e trazem, no cabeçalho de todas as páginas, a data antiga
"19-22 AGOSTO 2026". A data correta é **18-23**. Além disso, os arquivos vivem
soltos em `Downloads/PO` e `Downloads/CO`, sem versionamento, e não existe ainda
o caderno de resumos que acompanha o evento.

## Entregáveis

1. Os 27 PDFs com o cabeçalho corrigido, versionados no repositório.
2. `caderno-resumos-7-caminhos-2026.pdf` — arquivo único, resumos na ordem de
   apresentação, com capa, expediente, apresentação, sumário clicável, paginação
   e marcadores.
3. Link para download na página de Programação e na página de Submissões.
4. Dois scripts reproduzíveis e um arquivo de dados revisável.

## Fatos apurados no material

- **27 PDFs, 144 páginas, 10,3 MB.** Entre 3 e 9 páginas por resumo.
- O cabeçalho é uma **imagem embutida de 794×113 px** (JPEG na maioria, PNG em
  alguns), colocada no topo de *todas* as páginas, no retângulo
  `≈(1.3, 0.7, 596.3, 85.3)`.
- O rodapé UDESC/CEART/LabMAES/Fapesc é **outra imagem de 794×113**, no retângulo
  `≈(0, 769, 595, 854)`. Mesma dimensão do cabeçalho — a distinção só é segura
  pela posição.
- `Downloads/caminhos_cabecalho.png` é **exatamente 794×113 px, RGB**, mesma arte
  com "18-23". Substituição direta, sem reamostragem.
- Existem hoje **~8 variantes** do mesmo cabeçalho (compressões e origens
  diferentes, de 6 KB a 150 KB). A substituição as unifica.
- As páginas variam de 595,25 a 595,40 pt de largura e 841,8 a 842,0 pt de
  altura. Diferença irrelevante para concatenação.
- A ordem de apresentação já existe, completa e datada, no campo `programa` de
  `_data/programacao.json`: 4 + 9 + 4 + 10 = **27**, casando com a contagem de
  arquivos.
- A pasta `PO` corresponde exatamente à Sessão de Pôster (9) e a pasta `CO` às
  três sessões de Comunicação Oral (4+4+10=18).
- Os nomes de arquivo seguem a lógica `nome do autor/autores - início do título`.

## Decisões

| Questão | Decisão |
|---|---|
| Formato do caderno | PDF único, na ordem das sessões |
| Pré-textual | Capa, expediente/comissões, apresentação, sumário |
| ISBN e ficha catalográfica | **Fora.** O caderno não é os anais |
| Onde os PDFs moram | `labmaes-site`, todos versionados |
| O que é linkado no site | Apenas o caderno completo |
| Onde é publicado | Programação e Submissões. `/anais/` fica intacta |
| Capa | Composta a partir de `banner-caminhos-desktop.webp` |
| Texto de apresentação | Escrito pelo usuário, lido de arquivo externo |

### Por que o caderno não vai em `/anais/`

A página `/anais/` anuncia *"os anais serão disponibilizados após o evento"*, e a
página de Submissões promete anais **com ISBN**, com textos finais entregues até
**22/10/2026**. Publicar o caderno de resumos ali levaria autores a entender que
os anais saíram e que o prazo de outubro caiu. São documentos distintos: o
caderno é o companheiro da programação, sai antes do evento e não tem ISBN.

### Por que substituir o objeto de imagem

As alternativas consideradas e descartadas:

- **Tarja branca + imagem por cima.** O cabeçalho sangra até a borda da página; a
  tarja aparece em impressão e a arte antiga continua no arquivo, extraível.
- **Reexportar dos `.docx` dos autores.** Não temos os fontes e a formatação
  mudaria.

`replace_image(xref)` troca o recurso dentro do PDF: uma chamada resolve todas as
páginas, o texto permanece selecionável e o arquivo encolhe, porque o PNG novo é
mais limpo que as variantes atuais.

## Arquitetura

```
labmaes-site/
  assets/
    graphics/cabecalho-caminhos-2026.png     arquivo-mestre do cabeçalho
    anais/2026/
      caderno-resumos-7-caminhos-2026.pdf    entregável
      resumos/
        01-barblan-criacao-e-avaliacao.pdf   27 arquivos corrigidos
        ...
        27-siqueira-memorias-dissidentes.pdf
  _data/
    caderno.json                             pareamento revisado
    caderno-apresentacao.md                  texto de abertura (do usuário)
    caderno-expediente.md                    comissões (do usuário)
  tools/
    corrigir_cabecalho.py
    gerar_caderno.py
    test_corrigir_cabecalho.py
    test_gerar_caderno.py
```

Fora do repositório: `Caminhos_contemporaneo/_resumos_backup_19-22/`, com os 27
originais intocados — mesmo padrão adotado no backup dos banners.

O prefixo numérico global 01–27 faz a ordem alfabética da pasta coincidir com a
ordem de apresentação. Sessão, horário e autoria completa ficam no `caderno.json`,
não no nome do arquivo.

## Componente 1 — `tools/corrigir_cabecalho.py`

**O que faz:** dado um PDF de entrada e o PNG mestre, grava um PDF de saída com
todos os cabeçalhos substituídos.

**Como identifica o cabeçalho:** para cada imagem da página, obtém os retângulos
de colocação via `page.get_image_rects(xref)`. É cabeçalho a imagem 794×113 cujo
`rect.y0 < 100`; é rodapé a que tem `rect.y0 > 700`. A dimensão sozinha não
distingue as duas.

**Invariantes verificadas antes de escrever.** Falhou qualquer uma, o arquivo é
recusado e entra num relatório de erro, sem gravar saída:

1. Existe exatamente um xref de cabeçalho no documento.
2. Ele aparece em todas as páginas.
3. Existe pelo menos um xref de rodapé, e ele não coincide com o de cabeçalho.

**Escrita:** `replace_image(xref, filename=mestre)` seguido de
`save(saida, garbage=4, deflate=True)`.

**Verificação pós-escrita**, arquivo por arquivo:

1. **Visual:** renderiza a faixa `y ∈ [0, 90]` de **cada página** da saída a
   150 dpi e compara com um render de referência do PNG mestre nas mesmas
   dimensões. Tolerância por diferença média de pixel, para absorver ruído de
   rasterização. Acima do limiar, o arquivo é rejeitado.
2. **Textual:** `page.get_text()` de entrada e saída devem ser **idênticos**,
   página a página.
3. **Estrutural:** a contagem de páginas não mudou.

**Saída:** relatório em stdout com uma linha por arquivo (`OK` / `FALHOU` +
motivo) e um total. Código de saída diferente de zero se algum falhar.

## Componente 2 — o pareamento e `_data/caderno.json`

O casamento entre arquivos e linhas da programação **não é automático**: os nomes
de arquivo são informais e não reproduzem os campos `autores`/`titulo`.

**Heurística de primeira passada:** o nome do arquivo é quebrado em ` - `; a
parte esquerda é pontuada por sobreposição de tokens contra `autores`, a direita
contra `titulo`. Restrição forte que reduz muito o espaço de erro: itens da
Sessão de Pôster só podem casar com arquivos de `PO/`, itens de Comunicação Oral
só com arquivos de `CO/`.

**Revisão humana obrigatória.** O script imprime a tabela dos 27 pareamentos com
a pontuação de cada um, ordenada da menor confiança para a maior, e o usuário
confere antes de qualquer geração. O resultado aprovado é gravado em
`_data/caderno.json`, que passa a ser a fonte de verdade — a heurística não roda
de novo.

Esquema de cada item:

```json
{
  "ordem": 1,
  "sessao": "1ª Sessão de C.O. — Tecendo entre design e artes",
  "modalidade": "Comunicação Oral",
  "data": "2026-08-20",
  "hora": "13h40",
  "local": "Auditório",
  "autores": "Dr. Yves Maurice Jean Barblan",
  "titulo": "Criação e avaliação no ensino obrigatório na área das artes",
  "origem": "CO/Yves Maurice Jean Barblan - criação e avaliação.pdf",
  "arquivo": "assets/anais/2026/resumos/01-barblan-criacao-e-avaliacao.pdf",
  "paginas": 6
}
```

Os campos `sessao`, `data`, `hora`, `local`, `autores` e `titulo` são copiados de
`_data/programacao.json` na geração e **reconferidos a cada execução** do
gerador: divergiu, o gerador avisa em vez de publicar dado velho.

## Componente 3 — `tools/gerar_caderno.py`

Lê `caderno.json`, `caderno-apresentacao.md` e `caderno-expediente.md`; grava o
PDF final.

**Capa.** A4 retrato (595×842 pt), composta a partir de
`assets/banners/banner-caminhos-desktop.webp` — cuja data já foi corrigida para
18-23 — mais o bloco tipográfico "Caderno de Resumos", o tema do seminário, a
data por extenso e o local.

**Expediente e apresentação.** Renderizados a partir dos dois arquivos Markdown,
que ficam sob controle de versão e podem ser editados sem tocar no script. Se o
arquivo de apresentação estiver ausente ou vazio, a seção é omitida — permite
gerar o caderno completo antes de o texto ficar pronto.

**Sumário.** Quatro blocos, um por sessão, com data, hora, local e modalidade no
cabeçalho do bloco. Cada item traz autoria, título e página, com link interno.

**Layout em duas passadas.** O número de páginas do sumário desloca todos os
números de página dos resumos. O gerador monta o sumário uma vez para descobrir
sua extensão, calcula os deslocamentos e só então renderiza a versão final com os
números corretos. Fazer numa passada só produz sumário com páginas erradas — é o
erro clássico deste tipo de script.

**Paginação.** Fólio carimbado sobre a faixa bege de rodapé, alinhado à direita,
em DM Mono, na cor da tinta amostrada da arte. Os logos do rodapé são
centralizados, então a margem direita está livre. Contagem contínua desde a capa,
impressa a partir da primeira página de resumo.

**Marcadores.** Outline em dois níveis, sessão → trabalho: 4 entradas de primeiro
nível e 27 de segundo.

**Metadados.** `title`, `author`, `subject` e `keywords` preenchidos.

**Verificação pós-geração:**

1. Total de páginas = pré-textual + 144.
2. Para cada item, a primeira página do bloco correspondente contém o título
   esperado (comparação normalizada, sem acento e sem caixa). **Esta checagem
   valida o pareamento**: um resumo na sessão errada é detectado aqui.
3. Todo link do sumário resolve para uma página existente.
4. O outline tem 4 entradas de nível 1 e 27 de nível 2.

## Componente 4 — publicação no site

Botão de download do caderno em dois lugares:

- **Programação** (`programacao/index.njk`), no topo, onde o público procura o
  que vai acontecer.
- **Submissões** (`submissoes/index.njk`), junto à seção de resultados, onde os
  autores já estão olhando.

Nenhuma rota nova e nenhum item novo no menu do evento. A página `/anais/` não é
alterada.

Ao editar o menu ou o cabeçalho do evento, lembrar da armadilha conhecida do
repositório: `_includes/event-header.njk` é o arquivo realmente incluído;
`_includes/event-nav.njk` é código morto com a mesma estrutura.

## Testes

`test_corrigir_cabecalho.py` — sobre PDFs sintéticos construídos no próprio teste:

- Documento com cabeçalho e rodapé de mesma dimensão: só o cabeçalho é trocado.
- Documento com dois xrefs de cabeçalho distintos: recusado.
- Documento em que o cabeçalho falta numa página: recusado.
- Cabeçalho JPEG e cabeçalho PNG: ambos aceitos.
- O texto extraído não muda.

`test_gerar_caderno.py`:

- O deslocamento de páginas é recalculado quando o sumário cresce de 2 para 3
  páginas (regressão do bug de passada única).
- Item cujo título não aparece na primeira página do bloco: geração falha.
- Apresentação ausente: caderno gerado sem a seção, com paginação coerente.
- Divergência entre `caderno.json` e `programacao.json`: geração falha.

## Riscos e limitações conhecidas

**Fontes.** `assets/fonts/` traz DM Mono e Poppins apenas em `.woff2`, formato que
o PyMuPDF não embute. `Thunder-BoldHC.otf` está disponível em OTF e serve direto.
Para DM Mono e Poppins será preciso converter `woff2 → ttf` com `fontTools`
(requer `brotli`) ou obter os TTF originais. Resolver antes de codificar a capa.

**Push.** O `credential.helper` do repositório é o Git Credential Manager, que
trava em execução não interativa. Commits podem ser feitos aqui; o `push` que
dispara o deploy no Cloudflare Pages precisa ser feito pelo usuário num terminal
interativo.

**`programacao.json`.** Arquivo em CRLF e **sem newline final**. Ao regravar
programaticamente, remover o `\n` acrescentado pelo `json.dump`, sob pena de
poluir o diff.

**Peso do repositório.** ~10 MB de resumos individuais mais ~8 MB de caderno.
Aceitável, mas cada regeração do caderno acrescenta uma cópia binária ao
histórico. Regerar com parcimônia e commitar o caderno só em versões que valem
ser publicadas.

**Insumos pendentes do usuário.** A lista de comissões e o texto de apresentação
não existem em nenhum lugar do repositório e não podem ser deduzidos. Todo o
resto — correção dos cabeçalhos, pareamento, organização no git, sumário,
paginação — não depende deles e pode ser executado imediatamente.

## Fora de escopo

- ISBN e ficha catalográfica.
- Os anais completos de outubro.
- Correção da data em `cartaz_caminhos.jpg` e no KV em PDF, que seguem com
  "19-22". Continuam como pendência registrada.
- Publicação individual de cada resumo no site.
