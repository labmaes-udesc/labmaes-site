# Rodapé de realizadores e apoiadores — 7º Caminhos do Contemporâneo

**Data:** 2026-08-05
**Branch:** `rodape-realizadores-apoiadores`
**Escopo:** as seis páginas de `/eventos/caminhos-do-contemporaneo/2026/`

## Problema

Os créditos institucionais do evento aparecem hoje em um único lugar: um bloco pequeno
na coluna lateral da home do evento (`2026/index.njk`, linhas 26–37), com LabMAES,
UDESC CEART e Fapesc. As outras cinco páginas do evento — Programação, Submissões,
Mostra Audiovisual, Oficinas e Anais — não creditam ninguém, embora sejam páginas de
entrada frequentes para quem chega pelo Instagram ou por link direto.

Faltam também as 22 instituições apoiadoras, que nunca estiveram no site.

## Solução

Uma faixa de créditos padronizada ao pé das seis páginas do evento, com dois níveis de
hierarquia: realizadores em destaque, apoiadoras em tamanho reduzido numa grade regular.

### Hierarquia

**Realização:** LabMAES, UDESC CEART, Fapesc.
**Apoio:** as 22 demais instituições.

### Onde vive

Include novo `_includes/event-footer.njk`, chamado nas seis páginas do evento
imediatamente antes de fechar o `<main>`. Fica acima do rodapé geral do LabMAES
(`_includes/footer.njk`), que permanece intacto.

A lista de instituições **não** fica no template. Vai para `_data/apoiadores.json`,
no mesmo padrão de `_data/pessoas.json` e `_data/programacao.json`. Formato:

```json
{
  "realizacao": [
    { "slug": "labmaes", "nome": "LabMAES", "arquivo": "/assets/logos/logo-labmaes-vermelho.svg" }
  ],
  "apoio": [
    { "slug": "ufsc", "nome": "Universidade Federal de Santa Catarina", "arquivo": "/assets/logos/apoio/ufsc.webp" }
  ]
}
```

Acrescentar ou remover uma instituição passa a ser uma edição de JSON, sem tocar em HTML.

**Atenção à armadilha conhecida do repositório:** `_includes/event-nav.njk` é código morto;
quem é realmente incluído é `event-header.njk`. Nada disso muda aqui — o `event-footer.njk`
é um arquivo novo, incluído explicitamente em cada uma das seis páginas. A repetição da
linha de include é deliberada: mantém explícito qual página tem a faixa.

### Estrutura visual

Fundo `--color-brand-ice` (#F0F0FF), um dos fundos de seção que o site já alterna. Logos
com canal alfa assentam sobre ele sem caixa branca.

**Realização** — rótulo com o componente existente `.tag.tag--blue`; as três marcas em
linha centralizada, altura óptica ~56 px, espaçamento `--space-48`.

**Divisória** — regra fina, azul da marca a 15% de opacidade.

**Apoio** — rótulo `.tag.tag--red`; grade CSS:

```css
grid-template-columns: repeat(auto-fill, minmax(156px, 1fr));
```

O mínimo de 156 px vem da caixa uniforme de saída do pipeline: 150 px de largura a 1×,
mais folga. Uma coluna mais estreita que a caixa faria o `max-width: 100%` encolher a
logo, quebrando o alinhamento óptico que a caixa uniforme existe para garantir.

Cada célula tem **altura fixa de 72 px** com `place-items: center`; cada logo é limitado a
`max-height: 44px` e `max-width: 100%`. As colunas refluem sozinhas: ~7 no desktop, 4 no
tablet, 3 no celular, onde célula e logo caem para 56 px e 34 px.

### Normalização óptica

Script `tools/normalizar-logos.py`, versionado no repositório para que o processo seja
repetível quando chegar uma apoiadora nova. Para cada arquivo, nesta ordem:

1. **Recorte** da moldura pela caixa de tinta real.
2. **Fundo → alfa** por preenchimento a partir das bordas, **não** por limiar global de cor.
   Essa escolha é o que preserva o branco *interno* dos brasões — IFSC, UFRJ, UFSC,
   SEDUC BC, Belas Artes, Moura Lacerda —, que um recorte por limiar transformaria em buraco.
3. **Limpeza do halo** de compressão JPEG nos arquivos `.jfif`.
4. **Escala por área de tinta, não por altura.** Cada logo é escalado pela raiz da razão
   entre sua área de tinta e a área-alvo. Igualar altura faria a `came` (2,7:1, deitada)
   atravessar a célula como uma barra e daria à `ifsc` (0,7:1, em pé) peso visual de selo.
   Igualando área, as marcas ocupam a mesma mancha na página — que é como o olho compara peso.
   Dois tetos protegem os casos extremos: 44 px de altura e 150 px de largura.
5. **Preenchimento transparente** até uma caixa idêntica para todos, de modo que o
   alinhamento vertical na grade seja óptico e não dependa da geometria de cada arquivo.

Nenhuma etapa distorce marca: só recorte, escala proporcional e margem transparente.
Nenhuma proporção e nenhuma cor mudam.

**Saída:** WebP com alfa a 2× (88 px de altura de caixa), em `assets/logos/apoio/<slug>.webp`.

### Acessibilidade e performance

- `alt` com o nome por extenso de cada instituição. Sem isso a faixa não significa nada
  em leitor de tela — é a razão de as identificações terem sido levantadas antes.
- `width` e `height` explícitos em todas as imagens, para não haver salto de layout.
- `loading="lazy"`: a faixa está sempre abaixo da primeira dobra.
- Orçamento estimado: 150–250 KB no total das 22 imagens, carregadas de forma preguiçosa.

### Decisão registrada: as logos não são links

Com 22 apoiadoras em seis páginas, transformá-las em links acrescentaria 22 paradas de
tabulação antes do rodapé em cada página e espalharia links externos por todo o site sem
benefício claro para o visitante. Se os links vierem a ser desejados, o caminho menos ruim
é linkar apenas os três realizadores.

## Inventário das instituições

### Realização (3) — arquivos já no repositório

| Slug | Nome (alt) | Arquivo |
|---|---|---|
| `labmaes` | LabMAES | `assets/logos/logo-labmaes-vermelho.svg` |
| `udesc-ceart` | UDESC CEART | `assets/logos/logo-ceart.svg` |
| `fapesc` | Fapesc | `assets/logos/logo-fapesc.svg` |

### Apoio (22)

| Slug | Nome (alt) | Origem |
|---|---|---|
| `abepem` | ABEPEM | `assets/logos/logo-abepem.svg` (SVG já no repo — usar este, não o PNG) |
| `ufsc` | Universidade Federal de Santa Catarina | `ufsc.jfif` |
| `ufrj` | Universidade Federal do Rio de Janeiro | `ufrj.png` |
| `ifsc` | Instituto Federal de Santa Catarina | `ifsc.png` |
| `uem` | Universidade Estadual de Maringá | `uem.png` (reposto) |
| `feevale` | Universidade Feevale | `feevale.jfif` |
| `cesusc` | Faculdade CESUSC | `cesusc.png` (reposto) |
| `uniban` | Universidade Bandeirante de São Paulo | `uniban.png` (reposto) |
| `mackenzie` | Universidade Presbiteriana Mackenzie | `mkz.webp` (reposto) |
| `umontreal` | Université de Montréal | `umontreal.webp` (reposto) |
| `uminho` | Universidade do Minho | `uminho.jfif` |
| `lusofona` | Universidade Lusófona | `uluso.png` |
| `ibero` | Universidad Iberoamericana | `universidad-iberoamericana-ibero-logo-vector.png` |
| `moura-lacerda` | Instituição Universitária Moura Lacerda | `logo_centro-universitario-moura-lacerda_F5o24S.png` (reposto) |
| `belas-artes` | Centro Universitário Belas Artes de São Paulo | `ba.png` |
| `faeb` | Federação de Arte Educadores do Brasil | `faeb.png` (reposto) |
| `aaesc` | Associação dos Arte Educadores de Santa Catarina | `aaesc.jfif` |
| `came` | Casa dos Açores — Museu Etnográfico | `came.jfif` |
| `iema` | Instituto de Educação, Ciência e Tecnologia do Maranhão | `iema.png` |
| `seduc-bc` | Secretaria de Educação de Balneário Camboriú | `seduc bc.jfif` |
| `cep-edgar-morin` | Centro de Estudos e Pesquisas Edgar Morin | `Logo-CEP-EDGAR-MORIN.webp` |
| `amae` | AMAE | `logo-amae.webp` — **pendência, ver abaixo** |

Pasta de origem dos arquivos:
`C:\Users\Windows 10\Downloads\Logos-20260805T212938Z-1-001\Logos`

### Pendência: AMAE

O melhor arquivo disponível (`logo-amae.webp`) tem 98×99 px de tinta — 1,1× do mínimo
necessário, sem folga alguma. O outro arquivo do lote (`amae.jpg`, 123×33 px) é um lockup
diferente e pior, a 0,4× do mínimo.

Decisão do usuário: seguir mesmo assim, com **upscale**. O upscale entra como etapa
específica só desta marca, aplicado antes da normalização, e o resultado precisa ser
inspecionado visualmente antes de ir para o site. O nome por extenso da AMAE ainda não foi
confirmado; até lá o `alt` fica como "AMAE".

## Critérios de aceitação

1. As seis páginas do evento exibem a faixa, com o mesmo conteúdo e o mesmo espaçamento.
2. As 22 apoiadoras aparecem com peso visual equivalente, alinhadas na grade, sem que
   nenhuma marca domine ou desapareça.
3. Nenhuma logo aparece distorcida, recortada ou com fundo branco residual.
4. Nenhum brasão perde seu branco interno.
5. Todas as imagens têm `alt` com o nome por extenso.
6. A grade reflui sem estouro horizontal em 375 px, 768 px e 1280 px.
7. O bloco antigo de "REALIZAÇÃO" na coluna lateral da home é removido, para não duplicar
   a informação na mesma página.
8. O build (`npx @11ty/eleventy`) roda sem erro e o site continua servindo de `_site/`.

## Fora de escopo

- Tradução FR/EN da faixa (faz parte da pendência maior de i18n do site).
- Links externos para os sites das instituições.
- Qualquer alteração no rodapé geral do LabMAES.
- Reposição das logos que passam "no limite" (`uluso`, `iema`, `feevale`, `aaesc`, `cuml`):
  ficam com a resolução atual, que é suficiente para 44 px.

## Notas de trabalho

Todo o trabalho ocorre na branch `rodape-realizadores-apoiadores`, não na `main`.
O push para publicar depende de terminal interativo do usuário — o Git Credential Manager
trava em execução não interativa.
