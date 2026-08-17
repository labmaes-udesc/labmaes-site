# Rodapé de realizadores e apoiadores — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Adicionar uma faixa padronizada de créditos institucionais — 3 realizadores em destaque e 22 apoiadoras em grade reduzida — ao pé das seis páginas do 7º Caminhos do Contemporâneo 2026.

**Architecture:** Um script Python normaliza as logos brutas (recorte, remoção de fundo, escala por área de tinta, caixa uniforme) e grava WebP com alfa em `assets/logos/apoio/`. A lista de instituições vive em `_data/apoiadores.json`. Um include Nunjucks novo, `_includes/event-footer.njk`, itera essa lista e é chamado nas seis páginas do evento. O CSS entra em `css/components.css`, reusando os componentes `.section`, `.container` e `.tag` que já existem.

**Tech Stack:** Eleventy 3 (Nunjucks), CSS puro com tokens, Python 3 + Pillow + numpy (só na etapa de preparação dos assets, fora do build do site).

**Especificação:** [`docs/superpowers/specs/2026-08-05-rodape-realizadores-apoiadores-design.md`](../specs/2026-08-05-rodape-realizadores-apoiadores-design.md)

**Branch:** `rodape-realizadores-apoiadores` (já criada; não trabalhar na `main`)

---

## Contexto que o implementador precisa saber

**O site é Eleventy, não HTML estático na raiz.** As fontes são `.njk`; `npx @11ty/eleventy` gera `_site/`, que é o que a Cloudflare Pages serve. Editar `_site/` não adianta — é sobrescrito a cada build.

**`eleventy.config.js` tem `dir.input: "."`**, ou seja, o Eleventy varre a raiz inteira. A pasta `tools/` que este plano cria precisa entrar em `eleventyConfig.ignores`, senão o Eleventy tenta processá-la.

**Armadilha do nav:** `_includes/event-nav.njk` existe no repositório mas **não é incluído em lugar nenhum** — é código morto. Quem vale é `event-header.njk`. Este plano não toca em nenhum dos dois; cria um arquivo novo, `event-footer.njk`.

**Push não funciona de forma não interativa.** O Git Credential Manager trava esperando janela de login. Faça os commits normalmente; o push fica para o usuário, em terminal interativo.

**Pasta de origem das logos brutas** (fora do repositório):
`C:\Users\Windows 10\Downloads\Logos-20260805T212938Z-1-001\Logos`

---

## Estrutura de arquivos

| Arquivo | Responsabilidade |
|---|---|
| `tools/normalizar_logos.py` | **Criar.** Funções puras de tratamento de imagem + CLI que processa a lista de logos. |
| `tools/test_normalizar_logos.py` | **Criar.** Testes unittest das funções puras, com imagens sintéticas. |
| `tools/logos_apoio.py` | **Criar.** Tabela de dados: slug → (nome por extenso, arquivo de origem). Fonte única da verdade, importada pelo script e usada para gerar o JSON. |
| `assets/logos/apoio/*.webp` | **Criar.** 21 arquivos gerados (a ABEPEM usa o SVG que já existe). |
| `_data/apoiadores.json` | **Criar.** Lista consumida pelo template. |
| `_includes/event-footer.njk` | **Criar.** Markup da faixa. |
| `css/components.css` | **Modificar.** Bloco `.event-support*` no fim do arquivo, antes das media queries; e o utilitário `.visually-hidden`. |
| `eventos/caminhos-do-contemporaneo/2026/**/index.njk` (6 arquivos) | **Modificar.** Uma linha de include antes de `</main>`. |
| `eventos/caminhos-do-contemporaneo/2026/index.njk` | **Modificar.** Remover o bloco lateral antigo de "REALIZAÇÃO" (linhas 26–37). |
| `eleventy.config.js` | **Modificar.** Ignorar `tools/**`. |

A separação entre `logos_apoio.py` (dados) e `normalizar_logos.py` (algoritmo) existe para que os testes exercitem o algoritmo sem depender de arquivos externos, e para que acrescentar uma apoiadora nova seja uma edição de uma linha de tabela.

---

## Task 1: Tabela de dados das instituições

**Files:**
- Create: `tools/logos_apoio.py`

- [ ] **Step 1: Criar o módulo de dados**

Crie `tools/logos_apoio.py`:

```python
"""Tabela das instituições apoiadoras do 7º Caminhos do Contemporâneo.

Fonte única da verdade: o script de normalização lê ORIGEM daqui e o
gerador de JSON lê NOME daqui. Para acrescentar uma apoiadora, adicione
uma linha em APOIO e rode `python tools/normalizar_logos.py`.
"""

# Diretório com os arquivos brutos, fora do repositório.
PASTA_ORIGEM = r"C:\Users\Windows 10\Downloads\Logos-20260805T212938Z-1-001\Logos"

# slug -> (nome por extenso para o alt, arquivo de origem)
# `arquivo` None significa que a marca não passa pelo pipeline raster
# (usa um SVG já versionado em assets/logos/).
APOIO = {
    "abepem":          ("ABEPEM", None),
    "ufsc":            ("Universidade Federal de Santa Catarina", "ufsc.jfif"),
    "ufrj":            ("Universidade Federal do Rio de Janeiro", "ufrj.png"),
    "ifsc":            ("Instituto Federal de Santa Catarina", "ifsc.png"),
    "uem":             ("Universidade Estadual de Maringá", "uem.png"),
    "feevale":         ("Universidade Feevale", "feevale.jfif"),
    "cesusc":          ("Faculdade CESUSC", "cesusc.png"),
    "uniban":          ("Universidade Bandeirante de São Paulo", "uniban.png"),
    "mackenzie":       ("Universidade Presbiteriana Mackenzie", "mkz.webp"),
    "umontreal":       ("Université de Montréal", "umontreal.webp"),
    "uminho":          ("Universidade do Minho", "uminho.jfif"),
    "lusofona":        ("Universidade Lusófona", "uluso.png"),
    "ibero":           ("Universidad Iberoamericana",
                        "universidad-iberoamericana-ibero-logo-vector.png"),
    "moura-lacerda":   ("Instituição Universitária Moura Lacerda",
                        "logo_centro-universitario-moura-lacerda_F5o24S.png"),
    "belas-artes":     ("Centro Universitário Belas Artes de São Paulo", "ba.png"),
    "faeb":            ("Federação de Arte Educadores do Brasil", "faeb.png"),
    "aaesc":           ("Associação dos Arte Educadores de Santa Catarina", "aaesc.jfif"),
    "amae":            ("AMAE", "logo-amae.webp"),
    "came":            ("Casa dos Açores — Museu Etnográfico", "came.jfif"),
    "iema":            ("Instituto de Educação, Ciência e Tecnologia do Maranhão", "iema.png"),
    "seduc-bc":        ("Secretaria de Educação de Balneário Camboriú", "seduc bc.jfif"),
    "cep-edgar-morin": ("Centro de Estudos e Pesquisas Edgar Morin",
                        "Logo-CEP-EDGAR-MORIN.webp"),
}

# Marcas cuja resolução de origem é insuficiente e que precisam de
# ampliação antes da normalização. Valor = fator de ampliação.
UPSCALE = {
    "amae": 4,
}

# Caminho final de cada marca no site, por slug.
# A ABEPEM aponta para o SVG já versionado.
DESTINO_ESPECIAL = {
    "abepem": "/assets/logos/logo-abepem.svg",
}

REALIZACAO = [
    ("labmaes", "LabMAES", "/assets/logos/logo-labmaes-vermelho.svg"),
    ("udesc-ceart", "UDESC CEART", "/assets/logos/logo-ceart.svg"),
    ("fapesc", "Fapesc", "/assets/logos/logo-fapesc.svg"),
]


def caminho_publico(slug: str) -> str:
    """URL pública da logo de uma apoiadora."""
    if slug in DESTINO_ESPECIAL:
        return DESTINO_ESPECIAL[slug]
    return f"/assets/logos/apoio/{slug}.webp"
```

- [ ] **Step 2: Verificar que o módulo importa e que todos os arquivos de origem existem**

Run:

```bash
cd "C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/labmaes-site" && python -c "
import os, sys
sys.path.insert(0, 'tools')
from logos_apoio import APOIO, PASTA_ORIGEM
faltando = [a for _, a in APOIO.values() if a and not os.path.exists(os.path.join(PASTA_ORIGEM, a))]
print('total:', len(APOIO))
print('faltando:', faltando)
assert not faltando, faltando
print('OK')
"
```

Expected: `total: 22`, `faltando: []`, `OK`.

Se algum arquivo aparecer em `faltando`, pare e confira o nome na pasta de origem antes de seguir — o resto do plano depende dessa tabela estar correta.

- [ ] **Step 3: Commit**

```bash
git add tools/logos_apoio.py
```

```bash
git commit -m "feat(logos): tabela de dados das instituicoes apoiadoras"
```

---

## Task 2: Função `caixa_de_tinta`

Localiza a caixa delimitadora do desenho, descartando a moldura de fundo. É a base de tudo: sem ela, um logo pequeno num canvas grande seria escalado como se fosse grande.

**Files:**
- Create: `tools/normalizar_logos.py`
- Create: `tools/test_normalizar_logos.py`

- [ ] **Step 1: Escrever o teste que falha**

Crie `tools/test_normalizar_logos.py`:

```python
"""Testes das funções puras de normalização de logos.

Roda com a biblioteca padrão:
    python -m unittest discover -s tools -p "test_*.py" -v
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image, ImageDraw

from normalizar_logos import caixa_de_tinta


class TestCaixaDeTinta(unittest.TestCase):
    def test_encontra_desenho_dentro_de_moldura_branca(self):
        """Um quadrado vermelho de 40x20 numa tela branca de 200x200."""
        im = Image.new("RGB", (200, 200), (255, 255, 255))
        ImageDraw.Draw(im).rectangle([50, 80, 89, 99], fill=(200, 0, 0))

        self.assertEqual(caixa_de_tinta(im), (50, 80, 90, 100))

    def test_usa_o_canal_alfa_quando_existe(self):
        """Com alfa, o fundo é o transparente — não o branco."""
        im = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
        ImageDraw.Draw(im).rectangle([10, 10, 29, 39], fill=(255, 255, 255, 255))

        self.assertEqual(caixa_de_tinta(im), (10, 10, 30, 40))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Rodar o teste para confirmar que falha**

Run:

```bash
cd "C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/labmaes-site" && python -m unittest discover -s tools -p "test_*.py" -v
```

Expected: FAIL com `ModuleNotFoundError: No module named 'normalizar_logos'`.

- [ ] **Step 3: Implementar o mínimo**

Crie `tools/normalizar_logos.py`:

```python
"""Normalização óptica das logos de apoiadoras.

Recorte, remoção de fundo, escala por área de tinta e caixa uniforme.
Nenhuma etapa distorce marca: só recorte, escala proporcional e margem
transparente. Proporções e cores permanecem intactas.
"""
from PIL import Image, ImageChops

# Limiar de "quase branco" para detectar fundo em imagens sem alfa.
LIMIAR_BRANCO = 18


def caixa_de_tinta(im: Image.Image) -> tuple:
    """Caixa delimitadora do desenho, descartando a moldura de fundo.

    Com canal alfa, o fundo é o transparente. Sem alfa, o fundo é o branco.
    Retorna (esquerda, topo, direita, base) no formato do PIL.
    """
    tem_alfa = im.mode in ("RGBA", "LA") or "transparency" in im.info
    if tem_alfa:
        mascara = im.convert("RGBA").getchannel("A")
        mascara = mascara.point(lambda v: 255 if v > 8 else 0)
    else:
        rgb = im.convert("RGB")
        branco = Image.new("RGB", rgb.size, (255, 255, 255))
        diferenca = ImageChops.difference(rgb, branco).convert("L")
        mascara = diferenca.point(lambda v: 255 if v > LIMIAR_BRANCO else 0)

    caixa = mascara.getbbox()
    return caixa if caixa else (0, 0, im.size[0], im.size[1])
```

- [ ] **Step 4: Rodar o teste para confirmar que passa**

Run:

```bash
cd "C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/labmaes-site" && python -m unittest discover -s tools -p "test_*.py" -v
```

Expected: `Ran 2 tests` … `OK`.

- [ ] **Step 5: Commit**

```bash
git add tools/normalizar_logos.py tools/test_normalizar_logos.py
```

```bash
git commit -m "feat(logos): funcao caixa_de_tinta com testes"
```

---

## Task 3: Função `remover_fundo` — preserva o branco interno

Esta é a função de maior risco do plano. Um recorte por limiar global de cor apagaria o branco *interno* dos brasões (IFSC, UFRJ, UFSC, SEDUC BC, Belas Artes, Moura Lacerda), abrindo buracos no desenho. A solução é preencher a partir das bordas: só o branco conectado à moldura vira transparente.

**Files:**
- Modify: `tools/normalizar_logos.py`
- Modify: `tools/test_normalizar_logos.py`

- [ ] **Step 1: Escrever o teste que falha**

Acrescente a `tools/test_normalizar_logos.py`, logo abaixo do `import` existente, alterando a linha de import:

```python
from normalizar_logos import caixa_de_tinta, remover_fundo
```

E acrescente esta classe antes do bloco `if __name__`:

```python
class TestRemoverFundo(unittest.TestCase):
    def _rosquinha(self):
        """Anel preto com miolo branco sobre fundo branco.

        Reproduz a estrutura de um brasão: há branco DENTRO do desenho que
        precisa sobreviver, e branco FORA que precisa virar transparente.
        """
        im = Image.new("RGB", (100, 100), (255, 255, 255))
        d = ImageDraw.Draw(im)
        d.ellipse([20, 20, 79, 79], fill=(0, 0, 0))
        d.ellipse([35, 35, 64, 64], fill=(255, 255, 255))
        return im

    def test_fundo_externo_fica_transparente(self):
        saida = remover_fundo(self._rosquinha())

        self.assertEqual(saida.mode, "RGBA")
        self.assertEqual(saida.getpixel((2, 2))[3], 0)
        self.assertEqual(saida.getpixel((97, 97))[3], 0)

    def test_branco_interno_do_brasao_sobrevive(self):
        saida = remover_fundo(self._rosquinha())

        centro = saida.getpixel((50, 50))
        self.assertEqual(centro[3], 255, "o miolo branco virou buraco")
        self.assertEqual(centro[:3], (255, 255, 255))

    def test_desenho_permanece_opaco(self):
        saida = remover_fundo(self._rosquinha())

        self.assertEqual(saida.getpixel((25, 50))[3], 255)

    def test_imagem_que_ja_tem_alfa_passa_intacta(self):
        im = Image.new("RGBA", (50, 50), (0, 0, 0, 0))
        ImageDraw.Draw(im).rectangle([10, 10, 39, 39], fill=(10, 20, 30, 255))

        saida = remover_fundo(im)

        self.assertEqual(saida.getpixel((2, 2))[3], 0)
        self.assertEqual(saida.getpixel((25, 25)), (10, 20, 30, 255))
```

- [ ] **Step 2: Rodar o teste para confirmar que falha**

Run:

```bash
cd "C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/labmaes-site" && python -m unittest discover -s tools -p "test_*.py" -v
```

Expected: FAIL com `ImportError: cannot import name 'remover_fundo'`.

- [ ] **Step 3: Implementar**

Acrescente a `tools/normalizar_logos.py`, no topo ajustando os imports:

```python
from PIL import Image, ImageChops, ImageDraw, ImageFilter
```

E acrescente a função:

```python
# Cor sentinela usada no preenchimento por inundação. Improvável em logo.
SENTINELA = (255, 0, 254)
# Tolerância do preenchimento: absorve o degradê de compressão JPEG.
TOLERANCIA_FLOOD = 40


def remover_fundo(im: Image.Image) -> Image.Image:
    """Transforma o fundo em transparência, preservando o branco interno.

    O fundo é definido como a região conectada às bordas da imagem — não
    como "todo pixel branco". É essa distinção que impede que o miolo
    branco de um brasão vire buraco.

    Imagens que já trazem canal alfa são devolvidas como estão: o
    fornecedor já resolveu o recorte.
    """
    if im.mode in ("RGBA", "LA") or "transparency" in im.info:
        return im.convert("RGBA")

    rgb = im.convert("RGB")
    largura, altura = rgb.size

    inundada = rgb.copy()
    for ponto in [(0, 0), (largura - 1, 0), (0, altura - 1), (largura - 1, altura - 1)]:
        ImageDraw.floodfill(inundada, ponto, SENTINELA, thresh=TOLERANCIA_FLOOD)

    # Máscara do primeiro plano: 255 onde NÃO foi inundado.
    canais = inundada.split()
    igual_sentinela = Image.new("L", rgb.size, 0)
    for canal, valor in zip(canais, SENTINELA):
        proximo = canal.point(lambda v, alvo=valor: 255 if abs(v - alvo) < 8 else 0)
        igual_sentinela = ImageChops.lighter(igual_sentinela, ImageChops.invert(proximo))
    frente = igual_sentinela

    # Come 1px do contorno para eliminar o halo de compressão JPEG, e
    # suaviza a borda para o reescalonamento posterior não serrilhar.
    frente = frente.filter(ImageFilter.MinFilter(3))
    frente = frente.filter(ImageFilter.GaussianBlur(0.6))

    saida = rgb.convert("RGBA")
    saida.putalpha(frente)
    return saida
```

**Como a máscara funciona:** para cada canal RGB, `proximo` marca 255 onde aquele canal casa com a sentinela. Invertendo, marca-se onde o canal *diverge*. Basta um canal divergir para o pixel ser primeiro plano — daí o `lighter` (máximo) acumulando as três divergências.

- [ ] **Step 4: Rodar o teste para confirmar que passa**

Run:

```bash
cd "C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/labmaes-site" && python -m unittest discover -s tools -p "test_*.py" -v
```

Expected: `Ran 6 tests` … `OK`.

Se `test_desenho_permanece_opaco` falhar, o `MinFilter(3)` comeu demais numa figura sintética fina — confira que o anel do teste tem pelo menos 15 px de espessura, como especificado.

- [ ] **Step 5: Commit**

```bash
git add tools/normalizar_logos.py tools/test_normalizar_logos.py
```

```bash
git commit -m "feat(logos): remocao de fundo preservando branco interno de brasoes"
```

---

## Task 4: Função `dimensoes_por_area`

Iguala o **peso óptico** das marcas. Igualar altura faria a `came` (2,7:1, deitada) atravessar a célula como uma barra e daria à `ifsc` (0,7:1, em pé) peso de selo.

**Files:**
- Modify: `tools/normalizar_logos.py`
- Modify: `tools/test_normalizar_logos.py`

- [ ] **Step 1: Escrever o teste que falha**

Ajuste o import em `tools/test_normalizar_logos.py`:

```python
from normalizar_logos import (
    caixa_de_tinta,
    remover_fundo,
    dimensoes_por_area,
    AREA_ALVO,
    ALTURA_MAX,
    LARGURA_MAX,
)
```

E acrescente esta classe antes do bloco `if __name__`:

```python
class TestDimensoesPorArea(unittest.TestCase):
    def test_marca_larga_atinge_a_area_alvo(self):
        """Proporção 2,7:1 (como a CAME) não bate em nenhum teto."""
        largura, altura = dimensoes_por_area(2700, 1000)

        self.assertAlmostEqual(largura * altura, AREA_ALVO, delta=AREA_ALVO * 0.02)
        self.assertLessEqual(altura, ALTURA_MAX)
        self.assertLessEqual(largura, LARGURA_MAX)

    def test_proporcao_e_preservada(self):
        largura, altura = dimensoes_por_area(2700, 1000)

        self.assertAlmostEqual(largura / altura, 2.7, delta=0.05)

    def test_marca_quadrada_e_limitada_pela_altura(self):
        """Selos e brasões param no teto de altura — é o comportamento correto."""
        largura, altura = dimensoes_por_area(500, 500)

        self.assertEqual(altura, ALTURA_MAX)
        self.assertEqual(largura, ALTURA_MAX)

    def test_marca_muito_deitada_e_limitada_pela_largura(self):
        largura, altura = dimensoes_por_area(4000, 300)

        self.assertEqual(largura, LARGURA_MAX)
        self.assertLess(altura, ALTURA_MAX)

    def test_nunca_devolve_zero(self):
        largura, altura = dimensoes_por_area(1, 1)

        self.assertGreaterEqual(largura, 1)
        self.assertGreaterEqual(altura, 1)
```

- [ ] **Step 2: Rodar o teste para confirmar que falha**

Run:

```bash
cd "C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/labmaes-site" && python -m unittest discover -s tools -p "test_*.py" -v
```

Expected: FAIL com `ImportError: cannot import name 'dimensoes_por_area'`.

- [ ] **Step 3: Implementar**

Em `tools/normalizar_logos.py`, acrescente `import math` junto aos imports do topo do arquivo, e o restante ao fim:

```python
# Área de tinta alvo, em px² a 1x. Calibrada para que uma marca de
# proporção 2:1 chegue a 44 px de altura.
AREA_ALVO = 3872
ALTURA_MAX = 44
LARGURA_MAX = 150


def dimensoes_por_area(largura_tinta: int, altura_tinta: int) -> tuple:
    """Dimensões de destino que igualam a área de tinta entre marcas.

    Escala pela raiz da razão entre a área atual e a área alvo, e depois
    aplica os tetos de altura e largura. Na prática marcas quadradas e
    verticais batem no teto de altura — correto, porque um selo denso de
    44x44 já pesa mais no olho que um letreiro fino da mesma área.

    A proporção original é sempre preservada.
    """
    proporcao = largura_tinta / altura_tinta

    altura = math.sqrt(AREA_ALVO / proporcao)
    largura = altura * proporcao

    if altura > ALTURA_MAX:
        largura *= ALTURA_MAX / altura
        altura = ALTURA_MAX
    if largura > LARGURA_MAX:
        altura *= LARGURA_MAX / largura
        largura = LARGURA_MAX

    return max(1, round(largura)), max(1, round(altura))
```

- [ ] **Step 4: Rodar o teste para confirmar que passa**

Run:

```bash
cd "C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/labmaes-site" && python -m unittest discover -s tools -p "test_*.py" -v
```

Expected: `Ran 11 tests` … `OK`.

- [ ] **Step 5: Commit**

```bash
git add tools/normalizar_logos.py tools/test_normalizar_logos.py
```

```bash
git commit -m "feat(logos): escala por area de tinta com tetos de altura e largura"
```

---

## Task 5: Função `normalizar` — o pipeline completo

Encadeia as três funções e grava numa **caixa idêntica para todos**. É a caixa uniforme que garante alinhamento óptico na grade: como todos os arquivos saem com o mesmo canvas, o CSS não precisa saber nada sobre a geometria de cada marca.

**Files:**
- Modify: `tools/normalizar_logos.py`
- Modify: `tools/test_normalizar_logos.py`

- [ ] **Step 1: Escrever o teste que falha**

Ajuste o import em `tools/test_normalizar_logos.py`:

```python
from normalizar_logos import (
    caixa_de_tinta,
    remover_fundo,
    dimensoes_por_area,
    normalizar,
    AREA_ALVO,
    ALTURA_MAX,
    LARGURA_MAX,
    CAIXA,
)
```

E acrescente esta classe antes do bloco `if __name__`:

```python
class TestNormalizar(unittest.TestCase):
    def _marca_deitada(self):
        im = Image.new("RGB", (800, 600), (255, 255, 255))
        ImageDraw.Draw(im).rectangle([100, 250, 639, 349], fill=(0, 80, 160))
        return im

    def _marca_quadrada(self):
        im = Image.new("RGB", (400, 400), (255, 255, 255))
        ImageDraw.Draw(im).ellipse([50, 50, 349, 349], fill=(160, 0, 0))
        return im

    def test_saida_tem_sempre_a_mesma_caixa(self):
        """Duas marcas de proporções opostas saem no mesmo canvas."""
        a = normalizar(self._marca_deitada())
        b = normalizar(self._marca_quadrada())

        self.assertEqual(a.size, CAIXA)
        self.assertEqual(b.size, CAIXA)

    def test_saida_e_rgba(self):
        self.assertEqual(normalizar(self._marca_deitada()).mode, "RGBA")

    def test_desenho_fica_centrado_na_caixa(self):
        saida = normalizar(self._marca_quadrada())
        caixa = caixa_de_tinta(saida)

        folga_esquerda = caixa[0]
        folga_direita = CAIXA[0] - caixa[2]
        folga_topo = caixa[1]
        folga_base = CAIXA[1] - caixa[3]

        self.assertLessEqual(abs(folga_esquerda - folga_direita), 2)
        self.assertLessEqual(abs(folga_topo - folga_base), 2)

    def test_cantos_da_caixa_sao_transparentes(self):
        saida = normalizar(self._marca_deitada())

        self.assertEqual(saida.getpixel((0, 0))[3], 0)
        self.assertEqual(saida.getpixel((CAIXA[0] - 1, CAIXA[1] - 1))[3], 0)

    def test_proporcao_da_marca_nao_muda(self):
        """A regra inegociável: nenhuma logo pode distorcer."""
        original = self._marca_deitada()
        caixa_original = caixa_de_tinta(original)
        proporcao_original = (
            (caixa_original[2] - caixa_original[0])
            / (caixa_original[3] - caixa_original[1])
        )

        saida = normalizar(original)
        caixa_saida = caixa_de_tinta(saida)
        proporcao_saida = (
            (caixa_saida[2] - caixa_saida[0]) / (caixa_saida[3] - caixa_saida[1])
        )

        self.assertAlmostEqual(proporcao_saida, proporcao_original, delta=0.08)
```

- [ ] **Step 2: Rodar o teste para confirmar que falha**

Run:

```bash
cd "C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/labmaes-site" && python -m unittest discover -s tools -p "test_*.py" -v
```

Expected: FAIL com `ImportError: cannot import name 'normalizar'`.

- [ ] **Step 3: Implementar**

Acrescente a `tools/normalizar_logos.py`:

```python
# Fator de densidade da saída: 2x para telas retina.
ESCALA = 2
# Caixa uniforme de todos os arquivos gerados, em px reais.
CAIXA = (LARGURA_MAX * ESCALA, ALTURA_MAX * ESCALA)


def normalizar(im: Image.Image, upscale: int = 1) -> Image.Image:
    """Pipeline completo: recorte, alfa, escala por área e caixa uniforme.

    `upscale` amplia a origem antes de tudo, para marcas cuja resolução
    de partida é insuficiente. Use com parcimônia e confira o resultado
    a olho: ampliação não cria detalhe que não existe.
    """
    if upscale > 1:
        im = im.resize(
            (im.size[0] * upscale, im.size[1] * upscale), Image.LANCZOS
        )

    sem_fundo = remover_fundo(im)
    recortada = sem_fundo.crop(caixa_de_tinta(sem_fundo))

    largura, altura = dimensoes_por_area(recortada.size[0], recortada.size[1])
    redimensionada = recortada.resize(
        (largura * ESCALA, altura * ESCALA), Image.LANCZOS
    )

    tela = Image.new("RGBA", CAIXA, (0, 0, 0, 0))
    tela.paste(
        redimensionada,
        (
            (CAIXA[0] - redimensionada.size[0]) // 2,
            (CAIXA[1] - redimensionada.size[1]) // 2,
        ),
    )
    return tela
```

- [ ] **Step 4: Rodar o teste para confirmar que passa**

Run:

```bash
cd "C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/labmaes-site" && python -m unittest discover -s tools -p "test_*.py" -v
```

Expected: `Ran 16 tests` … `OK`.

- [ ] **Step 5: Commit**

```bash
git add tools/normalizar_logos.py tools/test_normalizar_logos.py
```

```bash
git commit -m "feat(logos): pipeline normalizar com caixa uniforme de saida"
```

---

## Task 6: CLI do script e geração dos assets

**Files:**
- Modify: `tools/normalizar_logos.py`
- Create: `assets/logos/apoio/*.webp` (21 arquivos gerados)

- [ ] **Step 1: Acrescentar o CLI**

Acrescente ao fim de `tools/normalizar_logos.py`:

```python
def main():
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from logos_apoio import APOIO, PASTA_ORIGEM, UPSCALE

    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    destino = os.path.join(raiz, "assets", "logos", "apoio")
    os.makedirs(destino, exist_ok=True)

    gerados = 0
    for slug, (nome, arquivo) in APOIO.items():
        if arquivo is None:
            print(f"  pulando {slug:<16} (usa SVG versionado)")
            continue

        origem = os.path.join(PASTA_ORIGEM, arquivo)
        saida = normalizar(Image.open(origem), upscale=UPSCALE.get(slug, 1))
        caminho = os.path.join(destino, f"{slug}.webp")
        saida.save(caminho, "WEBP", quality=92, method=6)

        peso = os.path.getsize(caminho) // 1024
        marca = " [UPSCALE]" if slug in UPSCALE else ""
        print(f"  {slug:<16} {saida.size[0]}x{saida.size[1]}  {peso:>3} KB{marca}")
        gerados += 1

    print(f"\n{gerados} arquivos gravados em assets/logos/apoio/")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Rodar o script**

Run:

```bash
cd "C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/labmaes-site" && python tools/normalizar_logos.py
```

Expected: uma linha `pulando abepem`, 21 linhas `<slug> 300x88 <n> KB` (a da `amae` marcada com `[UPSCALE]`), e `21 arquivos gravados`.

- [ ] **Step 3: Verificar o orçamento de peso e a integridade dos arquivos**

Run:

```bash
cd "C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/labmaes-site" && python -c "
import os, glob
from PIL import Image
arqs = sorted(glob.glob('assets/logos/apoio/*.webp'))
total = sum(os.path.getsize(a) for a in arqs)
for a in arqs:
    im = Image.open(a)
    assert im.size == (300, 88), (a, im.size)
    assert im.mode == 'RGBA', (a, im.mode)
    assert im.getchannel('A').getextrema()[0] == 0, (a, 'sem transparencia')
print(len(arqs), 'arquivos, todos 300x88 RGBA com alfa')
print('total: %.0f KB' % (total/1024))
assert total < 400*1024, 'acima do orcamento'
print('OK')
"
```

Expected: `21 arquivos, todos 300x88 RGBA com alfa`, um total entre 150 e 250 KB, e `OK`.

- [ ] **Step 4: Inspecionar visualmente os casos de risco**

Abra estes seis arquivos e confirme a olho que **o branco interno sobreviveu** e não há halo cinza:

```
assets/logos/apoio/ifsc.webp
assets/logos/apoio/ufrj.webp
assets/logos/apoio/ufsc.webp
assets/logos/apoio/seduc-bc.webp
assets/logos/apoio/belas-artes.webp
assets/logos/apoio/moura-lacerda.webp
```

E confirme separadamente que `assets/logos/apoio/amae.webp` está aceitável apesar da ampliação — é a marca de origem mais fraca do lote, e a decisão de seguir com upscale foi tomada sabendo disso. Se estiver ruim demais, pare e avise: a alternativa é deixar a AMAE fora até chegar um arquivo melhor.

- [ ] **Step 5: Commit**

```bash
git add tools/normalizar_logos.py assets/logos/apoio
```

```bash
git commit -m "feat(logos): CLI de normalizacao e 21 logos de apoiadoras tratadas"
```

---

## Task 7: `_data/apoiadores.json`

**Files:**
- Create: `_data/apoiadores.json`
- Create: `tools/gerar_apoiadores_json.py`

- [ ] **Step 1: Criar o gerador**

O JSON é derivado da tabela — gerá-lo evita que as duas fontes divirjam. Crie `tools/gerar_apoiadores_json.py`:

```python
"""Gera _data/apoiadores.json a partir da tabela em logos_apoio.py."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from logos_apoio import APOIO, REALIZACAO, caminho_publico

raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
destino = os.path.join(raiz, "_data", "apoiadores.json")

dados = {
    "realizacao": [
        {"slug": slug, "nome": nome, "arquivo": arquivo}
        for slug, nome, arquivo in REALIZACAO
    ],
    "apoio": [
        {"slug": slug, "nome": nome, "arquivo": caminho_publico(slug)}
        for slug, (nome, _) in APOIO.items()
    ],
}

with open(destino, "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"{len(dados['realizacao'])} realizadores, {len(dados['apoio'])} apoiadoras")
```

- [ ] **Step 2: Rodar e conferir**

Run:

```bash
cd "C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/labmaes-site" && python tools/gerar_apoiadores_json.py && python -c "
import json, os
d = json.load(open('_data/apoiadores.json', encoding='utf-8'))
assert len(d['realizacao']) == 3, len(d['realizacao'])
assert len(d['apoio']) == 22, len(d['apoio'])
for org in d['realizacao'] + d['apoio']:
    assert org['nome'].strip(), org
    assert os.path.exists(org['arquivo'].lstrip('/')), org['arquivo']
print('OK — todos os 25 arquivos referenciados existem')
"
```

Expected: `3 realizadores, 22 apoiadoras` e `OK — todos os 25 arquivos referenciados existem`.

- [ ] **Step 3: Commit**

```bash
git add tools/gerar_apoiadores_json.py _data/apoiadores.json
```

```bash
git commit -m "feat(evento): dados de realizadores e apoiadores em _data/apoiadores.json"
```

---

## Task 8: O include `event-footer.njk`

**Files:**
- Create: `_includes/event-footer.njk`
- Modify: `eleventy.config.js`

- [ ] **Step 1: Ignorar `tools/` no Eleventy**

Em `eleventy.config.js`, logo abaixo da linha `eleventyConfig.ignores.add("README.md");`, acrescente:

```javascript
  eleventyConfig.ignores.add("tools/**");
```

- [ ] **Step 2: Criar o include**

Crie `_includes/event-footer.njk`:

```njk
<section class="section section--ice event-support" aria-labelledby="creditos-heading">
  <div class="container">
    <h2 id="creditos-heading" class="visually-hidden">Realização e apoio</h2>

    <div class="event-support__group">
      <span class="tag tag--blue">REALIZAÇÃO</span>
      <ul class="event-support__row">
        {% for org in apoiadores.realizacao %}
        <li class="event-support__realizador">
          <img src="{{ org.arquivo }}" alt="{{ org.nome }}" loading="lazy">
        </li>
        {% endfor %}
      </ul>
    </div>

    <hr class="event-support__divisor">

    <div class="event-support__group">
      <span class="tag tag--red">APOIO</span>
      <ul class="event-support__grid">
        {% for org in apoiadores.apoio %}
        <li class="event-support__celula">
          <img src="{{ org.arquivo }}" alt="{{ org.nome }}"
               width="300" height="88" loading="lazy">
        </li>
        {% endfor %}
      </ul>
    </div>
  </div>
</section>
```

A ABEPEM é um SVG sem dimensões intrínsecas garantidas; os atributos `width`/`height` de 300×88 valem para os WebP e são inofensivos para o SVG, porque o CSS impõe as dimensões finais nos dois casos.

- [ ] **Step 3: Verificar que o build passa**

Run:

```bash
cd "C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/labmaes-site" && npx @11ty/eleventy
```

Expected: build sem erro. O include ainda não aparece em nenhuma página — isso é a Task 10.

- [ ] **Step 4: Commit**

```bash
git add _includes/event-footer.njk eleventy.config.js
```

```bash
git commit -m "feat(evento): include event-footer com faixa de creditos"
```

---

## Task 9: CSS da faixa

**Files:**
- Modify: `css/components.css`

- [ ] **Step 1: Acrescentar o utilitário e o bloco da faixa**

Em `css/components.css`, localize o início do primeiro bloco `@media` no fim do arquivo (por volta da linha 2180) e insira **antes dele**:

```css
/* ─── Utilitário: visível só para leitores de tela ───────── */
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
  border: 0;
}

/* ─── Faixa de créditos do evento ────────────────────────── */
.event-support__group {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-24);
}

.event-support__row,
.event-support__grid {
  list-style: none;
  margin: 0;
  padding: 0;
}

.event-support__row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: var(--space-48);
}

.event-support__realizador img {
  display: block;
  height: 56px;
  width: auto;
  max-width: 100%;
}

.event-support__divisor {
  height: 0;
  margin-block: var(--space-48);
  border: 0;
  border-top: 1px solid rgba(48, 42, 102, 0.15);
}

/* Grade das apoiadoras. A célula tem altura fixa e o logo é centrado
   nela — como todos os arquivos saem do pipeline com a mesma caixa de
   300x88, o alinhamento resultante é óptico, não geométrico. */
.event-support__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(156px, 1fr));
  gap: var(--space-24) var(--space-16);
  width: 100%;
}

.event-support__celula {
  display: grid;
  place-items: center;
  height: 72px;
}

.event-support__celula img {
  display: block;
  max-height: 44px;
  max-width: 100%;
  width: auto;
  height: auto;
}
```

- [ ] **Step 2: Acrescentar a variação para telas estreitas**

No fim de `css/components.css`, **dentro** do último bloco `@media (max-width: 767px)` existente, acrescente:

```css
  .event-support__row { gap: var(--space-24); }
  .event-support__realizador img { height: 40px; }
  .event-support__divisor { margin-block: var(--space-32); }
  .event-support__grid {
    grid-template-columns: repeat(auto-fill, minmax(104px, 1fr));
  }
  .event-support__celula { height: 56px; }
  .event-support__celula img { max-height: 34px; }
```

- [ ] **Step 3: Verificar que o build passa**

Run:

```bash
cd "C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/labmaes-site" && npx @11ty/eleventy && grep -c "event-support__celula" _site/css/components.css
```

Expected: build sem erro e `2` (a regra base e a de telas estreitas).

- [ ] **Step 4: Commit**

```bash
git add css/components.css
```

```bash
git commit -m "feat(evento): CSS da faixa de creditos e utilitario visually-hidden"
```

---

## Task 10: Incluir a faixa nas seis páginas

**Files:**
- Modify: `eventos/caminhos-do-contemporaneo/2026/index.njk:276`
- Modify: `eventos/caminhos-do-contemporaneo/2026/programacao/index.njk:124`
- Modify: `eventos/caminhos-do-contemporaneo/2026/submissoes/index.njk:315`
- Modify: `eventos/caminhos-do-contemporaneo/2026/mostra-audiovisual/index.njk:214`
- Modify: `eventos/caminhos-do-contemporaneo/2026/oficinas/index.njk:200`
- Modify: `eventos/caminhos-do-contemporaneo/2026/anais/index.njk:16`

- [ ] **Step 1: Inserir o include nas seis páginas**

Em cada um dos seis arquivos, imediatamente **antes** da linha `</main>`, insira:

```njk
  {% include "event-footer.njk" %}

```

Os números de linha acima são os do `</main>` no estado atual. Se divergirem, localize o `</main>` — há exatamente um por arquivo.

- [ ] **Step 2: Verificar que as seis páginas ganharam a faixa**

Run:

```bash
cd "C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/labmaes-site" && npx @11ty/eleventy && python -c "
import glob
paginas = sorted(glob.glob('_site/eventos/caminhos-do-contemporaneo/2026/**/index.html', recursive=True))
assert len(paginas) == 6, [len(paginas), paginas]
for p in paginas:
    html = open(p, encoding='utf-8').read()
    assert 'event-support__grid' in html, p
    assert html.count('event-support__celula') == 22, (p, html.count('event-support__celula'))
    assert 'alt=\"Universidade Federal de Santa Catarina\"' in html, p
print('OK — 6 paginas, 22 apoiadoras cada, alts presentes')
"
```

Expected: `OK — 6 paginas, 22 apoiadoras cada, alts presentes`.

- [ ] **Step 3: Commit**

```bash
git add eventos/caminhos-do-contemporaneo/2026
```

```bash
git commit -m "feat(evento): faixa de creditos nas seis paginas do evento"
```

---

## Task 11: Remover o bloco antigo da home

Aprovado pelo usuário: com a faixa no pé de todas as páginas, o bloco lateral duplicaria LabMAES, CEART e Fapesc na mesma página.

**Files:**
- Modify: `eventos/caminhos-do-contemporaneo/2026/index.njk:26-37`
- Modify: `css/components.css:540-575`

- [ ] **Step 1: Remover o bloco do template**

Em `eventos/caminhos-do-contemporaneo/2026/index.njk`, apague o bloco inteiro (linhas 26–37 no estado atual):

```njk
          <div class="event-about__realization">
            <span class="tag tag--blue">REALIZAÇÃO</span>
            <div class="event-about__logos">
              <div class="event-about__logos-row">
                <img src="/assets/logos/logo-labmaes-vermelho.svg" alt="LabMAES" height="38">
              </div>
              <div class="event-about__logos-row">
                <img src="/assets/logos/logo-ceart.svg" alt="UDESC CEART" height="32">
                <img src="/assets/logos/logo-fapesc.svg" alt="Fapesc" height="32">
              </div>
            </div>
          </div>
```

O `<aside class="event-about__side">` permanece, agora contendo apenas o bloco `event-about__info` (data e local).

- [ ] **Step 2: Remover o CSS que ficou órfão**

Em `css/components.css`, apague as regras `.event-about__realization`, `.event-about__logos`, `.event-about__logos-row`, `.event-about__logos-row:first-child img` e `.event-about__logos-row:last-child img` (linhas 540–575 no estado atual), incluindo o comentário `/* Divide a largura da linha 1 igualmente entre as duas logos */`.

**Não apague** `.tag--ice` logo abaixo, nem `.event-about__side` ou `.event-about__info` — essas continuam em uso.

- [ ] **Step 3: Verificar que não sobrou referência**

Run:

```bash
cd "C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/labmaes-site" && grep -rn "event-about__realization\|event-about__logos" --include="*.njk" --include="*.css" . | grep -v "_site/" || echo "OK — nenhuma referencia restante"
```

Expected: `OK — nenhuma referencia restante`.

- [ ] **Step 4: Verificar que a home ainda constrói e mantém data e local**

Run:

```bash
cd "C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/labmaes-site" && npx @11ty/eleventy && python -c "
html = open('_site/eventos/caminhos-do-contemporaneo/2026/index.html', encoding='utf-8').read()
assert 'event-about__realization' not in html
assert '18 a 23 de agosto de 2026' in html
assert 'event-about__info' in html
assert html.count('event-support__celula') == 22
print('OK — bloco removido, data e local intactos, faixa presente')
"
```

Expected: `OK — bloco removido, data e local intactos, faixa presente`.

- [ ] **Step 5: Commit**

```bash
git add eventos/caminhos-do-contemporaneo/2026/index.njk css/components.css
```

```bash
git commit -m "refactor(evento): remover bloco lateral de realizacao da home"
```

---

## Task 12: Verificação visual no navegador

Os testes cobrem o pipeline de imagem; a grade só pode ser julgada a olho. Esta task existe porque o critério central do trabalho — "balanço e alinhamento entre todas as logos" — não é verificável por asserção.

**Files:** nenhum (verificação)

- [ ] **Step 1: Criar a configuração de preview, se não existir**

Se `.claude/launch.json` não existir, crie:

```json
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "labmaes-site",
      "runtimeExecutable": "npx",
      "runtimeArgs": ["@11ty/eleventy", "--serve"],
      "port": 8080
    }
  ]
}
```

- [ ] **Step 2: Subir o preview e abrir a página do evento**

Use `preview_start` com `{name: "labmaes-site"}` e navegue para `/eventos/caminhos-do-contemporaneo/2026/`.

- [ ] **Step 3: Conferir a ausência de erros**

Rode `read_console_messages` e `preview_logs`. Expected: nenhum 404 de imagem, nenhum erro de console.

- [ ] **Step 4: Conferir os três pontos de quebra**

Com `resize_window`, verifique em 1280, 768 e 375 px de largura:

- Nenhuma barra de rolagem horizontal na página.
- A grade reflui sem célula órfã ou estourada.
- Os três realizadores permanecem maiores que as apoiadoras.

Tire um `screenshot` em cada largura.

- [ ] **Step 5: Julgar o equilíbrio óptico**

Olhando o screenshot de 1280 px, confirme que nenhuma marca domina a grade nem some ao lado das vizinhas. Os casos-limite a checar de perto são `came` (a mais deitada), `ifsc` e `moura-lacerda` (as mais verticais) e `amae` (a de pior origem).

Se alguma marca destoar, o ajuste é em `AREA_ALVO`, `ALTURA_MAX` ou `LARGURA_MAX` em `tools/normalizar_logos.py`, seguido de nova execução do script — **não** em CSS por marca individual. Regra por marca é o começo de um sistema impossível de manter.

- [ ] **Step 6: Conferir uma segunda página**

Navegue para `/eventos/caminhos-do-contemporaneo/2026/anais/` — a mais curta das seis — e confirme que a faixa aparece corretamente mesmo com pouco conteúdo acima.

- [ ] **Step 7: Commit de eventuais ajustes**

Se a Task 12 gerou mudanças:

```bash
git add -A
```

```bash
git commit -m "fix(evento): ajuste optico da faixa de creditos"
```

---

## Task 13: Fechamento

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Registrar a pendência da AMAE no README**

Na seção de pendências do `README.md`, acrescente:

```markdown
- Substituir a logo da AMAE em `assets/logos/apoio/amae.webp`: a origem
  disponível (98×99 px de tinta) exigiu ampliação. Ao receber um arquivo
  vetorial ou de maior resolução, coloque-o na pasta de origem, ajuste o
  nome em `tools/logos_apoio.py`, remova a entrada de `UPSCALE` e rode
  `python tools/normalizar_logos.py`.
- Confirmar o nome por extenso da AMAE para o atributo `alt` (hoje só "AMAE").
```

- [ ] **Step 2: Rodar a suíte inteira uma última vez**

Run:

```bash
cd "C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/labmaes-site" && python -m unittest discover -s tools -p "test_*.py" && npx @11ty/eleventy
```

Expected: `Ran 16 tests` … `OK`, seguido de build sem erro.

- [ ] **Step 3: Commit**

```bash
git add README.md
```

```bash
git commit -m "docs: registrar pendencia da logo da AMAE"
```

- [ ] **Step 4: Entregar ao usuário**

O push depende de terminal interativo. Informe o usuário de que a branch `rodape-realizadores-apoiadores` está pronta e que ele precisa rodar:

```bash
git push -u origin rodape-realizadores-apoiadores
```

Não tente rodar o push de forma não interativa — o Git Credential Manager trava.

---

## Critérios de aceitação (da especificação)

| # | Critério | Onde é verificado |
|---|---|---|
| 1 | As seis páginas exibem a faixa | Task 10, Step 2 |
| 2 | Apoiadoras com peso visual equivalente | Task 12, Step 5 |
| 3 | Nenhuma logo distorcida, recortada ou com fundo branco | Task 5 (`test_proporcao_da_marca_nao_muda`), Task 6 Steps 3–4 |
| 4 | Nenhum brasão perde o branco interno | Task 3 (`test_branco_interno_do_brasao_sobrevive`), Task 6 Step 4 |
| 5 | Todas as imagens com `alt` por extenso | Task 7 Step 2, Task 10 Step 2 |
| 6 | Grade reflui sem estouro em 375/768/1280 | Task 12, Step 4 |
| 7 | Bloco antigo da home removido | Task 11, Step 4 |
| 8 | Build roda sem erro | Task 13, Step 2 |
