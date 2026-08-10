# Caderno de Resumos do 7º Caminhos — plano de implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Corrigir a data no cabeçalho dos 27 resumos aprovados (19-22 → 18-23), versioná-los no repositório e gerar o caderno de resumos em PDF único, na ordem de apresentação, com capa, sumário clicável, paginação e marcadores.

**Architecture:** Três etapas encadeadas, cada uma com script próprio e verificação automática. (1) `corrigir_cabecalho.py` substitui o objeto de imagem do cabeçalho dentro de cada PDF, sem tocar no texto. (2) `parear_resumos.py` casa cada arquivo com sua linha da programação, grava `_data/caderno.json` para revisão humana e copia os PDFs para o repositório com nome numerado. (3) `gerar_caderno.py` monta o volume final a partir do `caderno.json`. Nenhuma etapa reescreve a anterior: o `caderno.json` aprovado vira fonte de verdade e a heurística de pareamento não roda de novo.

**Tech Stack:** Python 3.14, PyMuPDF 1.27, Pillow 12, fontTools (+brotli), `unittest` da biblioteca padrão. Site em Eleventy 3 (`.njk`), hospedado no Cloudflare Pages.

---

## Contexto para quem nunca abriu este repositório

**Onde ficam as coisas.** O repositório é `labmaes-site/`, dentro de `C:\Users\Windows 10\Documents\Claude\Projects\Caminhos_contemporaneo\`. A branch de trabalho é `caderno-resumos`, já criada a partir de `main`.

**Os PDFs de origem** estão fora do repositório, em `C:\Users\Windows 10\Downloads\PO` (9 arquivos) e `C:\Users\Windows 10\Downloads\CO` (18 arquivos). Não os edite no lugar: eles são o backup.

**Como rodar os testes.** O repositório não usa pytest. Use a biblioteca padrão, a partir da raiz do repositório:

```bash
python -m unittest discover -s tools -p "test_*.py" -v
```

**Anatomia dos PDFs de resumo** (apurado, não suposto): cada página tem uma imagem de cabeçalho 794×113 px no topo (retângulo `≈(1.3, 0.7, 596.3, 85.3)`) e uma imagem de rodapé **também 794×113** embaixo (`≈(0, 769, 595, 854)`). As duas têm a mesma dimensão — a única forma segura de distinguir é a **posição de colocação**. Um script que filtre só por tamanho troca o rodapé por engano.

**Armadilha do `git add`.** `tools/` contém scripts que pertencem à branch `rodape-realizadores-apoiadores`, ainda não mesclada. Nesta branch a pasta traz apenas `__pycache__`. **Nunca use `git add tools/`** — adicione arquivo por arquivo, sempre.

**Armadilha do push.** O `credential.helper` deste repositório é o Git Credential Manager, que trava em execução não interativa. Faça commits à vontade; o `push` fica para o usuário, num terminal interativo.

**Armadilha do `programacao.json`.** O arquivo é CRLF e **sem newline final**. Este plano só o lê — se algum dia for regravar, remova o `\n` que o `json.dump` acrescenta.

## Estrutura de arquivos

| Arquivo | Responsabilidade |
|---|---|
| `assets/graphics/cabecalho-caminhos-2026.png` | Arquivo-mestre do cabeçalho, 794×113 |
| `assets/fonts/DMMono-Regular.ttf` | DM Mono em TTF (PyMuPDF não lê woff2) |
| `assets/fonts/Poppins-Regular.ttf` | Poppins regular em TTF |
| `assets/fonts/Poppins-SemiBold.ttf` | Poppins semibold em TTF |
| `tools/converter_fontes.py` | woff2 → ttf, uma vez |
| `tools/corrigir_cabecalho.py` | Classificação, validação, substituição e verificação do cabeçalho |
| `tools/test_corrigir_cabecalho.py` | Testes sobre PDFs sintéticos |
| `tools/parear_resumos.py` | Pareamento arquivo ↔ programação, nomes de destino, `caderno.json` |
| `tools/test_parear_resumos.py` | Testes de normalização, pontuação e atribuição |
| `tools/caderno_dados.py` | Carga e validação cruzada dos dados do caderno |
| `tools/caderno_texto.py` | Markdown mínimo → blocos de texto, medição tipográfica |
| `tools/caderno_paginas.py` | Capa, páginas de texto e sumário |
| `tools/gerar_caderno.py` | Orquestra, carimba fólios, escreve outline/metadados, verifica |
| `tools/test_caderno.py` | Testes dos três módulos acima |
| `_data/caderno.json` | Pareamento aprovado — fonte de verdade |
| `_data/caderno-expediente.md` | Comissões (texto do usuário) |
| `_data/caderno-apresentacao.md` | Abertura (texto do usuário) |
| `assets/anais/2026/resumos/NN-*.pdf` | 27 resumos corrigidos |
| `assets/anais/2026/caderno-resumos-7-caminhos-2026.pdf` | Entregável |

Fora do repositório, em `Caminhos_contemporaneo/`:
`_resumos_backup_19-22/{PO,CO}/` (originais) e `_resumos_corrigidos/{PO,CO}/` (saída da etapa 1).

## Dois refinamentos em relação à spec

1. **Verificação do cabeçalho.** A spec previa comparação visual de faixas renderizadas. É frágil (ruído de rasterização, margens variáveis) e foi trocada por algo mais forte e mais simples: comparar os **samples decodificados** do xref de cabeçalho do PDF de saída com os do PNG mestre. Igualdade exata, independente de página. A cobertura de "todas as páginas" já vem da invariante de que o xref ocorre em todas elas.
2. **Componente 3 dividido.** `gerar_caderno.py` viraria um arquivo de ~400 linhas fazendo carga de dados, tipografia, layout e verificação. Foi dividido em `caderno_dados` / `caderno_texto` / `caderno_paginas` / `gerar_caderno`, cada um com uma responsabilidade.

Uma descoberta que muda uma checagem: os títulos em `programacao.json` **não são idênticos** aos títulos dentro dos PDFs. Exemplo real — a programação traz "Narrativas compartilhadas: costuras, escola e memórias" e o PDF traz "Costuras, escola e memória." (singular, caixa diferente). Por isso a verificação de pareamento usa **sobreposição de tokens ≥ 0,6**, nunca igualdade de string.

---

## Task 1: Fontes em TTF

**Files:**
- Create: `tools/converter_fontes.py`
- Create: `assets/fonts/DMMono-Regular.ttf`, `assets/fonts/Poppins-Regular.ttf`, `assets/fonts/Poppins-SemiBold.ttf`

`assets/fonts/` só tem `.woff2`, que o PyMuPDF não embute. `Thunder-BoldHC.otf` já existe em OTF e será usado direto, sem conversão.

- [ ] **Step 1: Escrever o conversor**

Crie `tools/converter_fontes.py`:

```python
"""Converte as fontes .woff2 do site para .ttf, formato que o PyMuPDF embute.

Uso (a partir da raiz do repositório):
    python tools/converter_fontes.py
"""
import os
import sys

from fontTools.ttLib import TTFont

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTES = os.path.join(RAIZ, "assets", "fonts")

CONVERTER = [
    "DMMono-Regular",
    "Poppins-Regular",
    "Poppins-SemiBold",
]


def converter(nome):
    origem = os.path.join(FONTES, nome + ".woff2")
    destino = os.path.join(FONTES, nome + ".ttf")
    fonte = TTFont(origem)
    fonte.flavor = None
    fonte.save(destino)
    return destino


def main():
    for nome in CONVERTER:
        destino = converter(nome)
        print("gravado:", os.path.relpath(destino, RAIZ), os.path.getsize(destino), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Rodar**

```bash
python tools/converter_fontes.py
```

Esperado: três linhas `gravado: assets\fonts\<nome>.ttf <n> bytes`, com `n` acima de 20000.

- [ ] **Step 3: Verificar que o PyMuPDF carrega os três**

```bash
python -c "import fitz; [print(n, round(fitz.Font(fontfile='assets/fonts/'+n+'.ttf').text_length('18-23 AGOSTO 2026', 10), 1)) for n in ('DMMono-Regular','Poppins-Regular','Poppins-SemiBold')]"
```

Esperado: três linhas com um comprimento em pontos, sem exceção. Se `fitz.Font` levantar erro, a conversão falhou e não adianta seguir.

- [ ] **Step 4: Commit**

```bash
git add tools/converter_fontes.py assets/fonts/DMMono-Regular.ttf assets/fonts/Poppins-Regular.ttf assets/fonts/Poppins-SemiBold.ttf
git commit -m "Converte fontes do site para TTF para uso no PyMuPDF"
```

---

## Task 2: Cabeçalho — classificação e validação

**Files:**
- Create: `tools/corrigir_cabecalho.py`
- Test: `tools/test_corrigir_cabecalho.py`

- [ ] **Step 1: Escrever os testes que falham**

Crie `tools/test_corrigir_cabecalho.py`:

```python
"""Testes da correção de cabeçalho dos PDFs de resumo.

Roda com a biblioteca padrão:
    python -m unittest discover -s tools -p "test_*.py" -v
"""
import io
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import fitz
from PIL import Image

from corrigir_cabecalho import (
    CabecalhoInvalido,
    classificar_imagens,
    validar,
)

LARGURA_PAGINA = 595.0
ALTURA_PAGINA = 842.0


def png_solido(cor):
    """PNG 794x113 de cor sólida, no tamanho real do cabeçalho dos resumos."""
    buffer = io.BytesIO()
    Image.new("RGB", (794, 113), cor).save(buffer, format="PNG")
    return buffer.getvalue()


def pdf_sintetico(paginas=2, cores_cabecalho=None, rodape=True, pular_cabecalho_em=()):
    """Monta um PDF com cabeçalho no topo e rodapé embaixo, ambos 794x113.

    cores_cabecalho: uma cor por página; cores diferentes geram xrefs diferentes.
    """
    if cores_cabecalho is None:
        cores_cabecalho = [(10, 20, 30)] * paginas
    doc = fitz.open()
    caixa_topo = fitz.Rect(1.3, 0.7, 596.3, 85.3)
    caixa_rodape = fitz.Rect(0, 769, 595, 842)
    for numero in range(paginas):
        pagina = doc.new_page(width=LARGURA_PAGINA, height=ALTURA_PAGINA)
        pagina.insert_text((72, 300), "Resumo de teste, pagina %d" % numero, fontsize=11)
        if numero not in pular_cabecalho_em:
            pagina.insert_image(caixa_topo, stream=png_solido(cores_cabecalho[numero]))
        if rodape:
            pagina.insert_image(caixa_rodape, stream=png_solido((200, 200, 200)))
    return doc


class TestClassificarImagens(unittest.TestCase):
    def test_separa_cabecalho_de_rodape_de_mesma_dimensao(self):
        doc = pdf_sintetico(paginas=2)

        cabecalho, rodape, ocorrencias = classificar_imagens(doc)

        self.assertEqual(len(cabecalho), 1)
        self.assertEqual(len(rodape), 1)
        self.assertNotEqual(cabecalho, rodape)
        xref = next(iter(cabecalho))
        self.assertEqual(ocorrencias[xref], {0, 1})

    def test_aceita_cabecalho_gravado_em_jpeg(self):
        """Nos 27 resumos reais o cabeçalho vem ora em JPEG, ora em PNG."""
        doc = fitz.open()
        pagina = doc.new_page(width=LARGURA_PAGINA, height=ALTURA_PAGINA)
        buffer = io.BytesIO()
        Image.new("RGB", (794, 113), (10, 20, 30)).save(buffer, format="JPEG")
        pagina.insert_image(fitz.Rect(1.3, 0.7, 596.3, 85.3), stream=buffer.getvalue())
        pagina.insert_image(fitz.Rect(0, 769, 595, 842), stream=png_solido((200, 200, 200)))

        cabecalho, rodape, _ = classificar_imagens(doc)

        self.assertEqual(len(cabecalho), 1)
        self.assertEqual(len(rodape), 1)

    def test_ignora_imagens_de_outra_dimensao(self):
        doc = pdf_sintetico(paginas=1)
        buffer = io.BytesIO()
        Image.new("RGB", (400, 300), (5, 5, 5)).save(buffer, format="PNG")
        doc[0].insert_image(fitz.Rect(100, 200, 300, 350), stream=buffer.getvalue())

        cabecalho, rodape, _ = classificar_imagens(doc)

        self.assertEqual(len(cabecalho), 1)
        self.assertEqual(len(rodape), 1)


class TestValidar(unittest.TestCase):
    def test_aceita_documento_regular_e_devolve_o_xref(self):
        doc = pdf_sintetico(paginas=3)

        xref = validar(doc, *classificar_imagens(doc))

        self.assertIn(xref, classificar_imagens(doc)[0])

    def test_recusa_dois_cabecalhos_distintos(self):
        doc = pdf_sintetico(paginas=2, cores_cabecalho=[(10, 20, 30), (40, 50, 60)])

        with self.assertRaises(CabecalhoInvalido) as erro:
            validar(doc, *classificar_imagens(doc))

        self.assertIn("distintas", str(erro.exception))

    def test_recusa_cabecalho_ausente_numa_pagina(self):
        doc = pdf_sintetico(paginas=3, pular_cabecalho_em=(1,))

        with self.assertRaises(CabecalhoInvalido) as erro:
            validar(doc, *classificar_imagens(doc))

        self.assertIn("[1]", str(erro.exception))

    def test_recusa_documento_sem_rodape(self):
        doc = pdf_sintetico(paginas=2, rodape=False)

        with self.assertRaises(CabecalhoInvalido) as erro:
            validar(doc, *classificar_imagens(doc))

        self.assertIn("rodapé", str(erro.exception))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Rodar os testes e confirmar que falham**

```bash
python -m unittest discover -s tools -p "test_corrigir_cabecalho.py" -v
```

Esperado: `ModuleNotFoundError: No module named 'corrigir_cabecalho'`.

- [ ] **Step 3: Escrever a implementação mínima**

Crie `tools/corrigir_cabecalho.py`:

```python
"""Troca a imagem de cabeçalho dos PDFs de resumo pelo mestre com a data correta.

O cabeçalho e o rodapé dos resumos têm a MESMA dimensão (794x113). A distinção
é feita pela posição de colocação na página, nunca pelo tamanho.

Uso (a partir da raiz do repositório):
    python tools/corrigir_cabecalho.py ORIGEM DESTINO

Testes:
    python -m unittest discover -s tools -p "test_*.py" -v
"""
import os
import sys

import fitz

LARGURA_CABECALHO = 794
ALTURA_CABECALHO = 113
Y_MAXIMO_CABECALHO = 100.0
Y_MINIMO_RODAPE = 700.0


class CabecalhoInvalido(Exception):
    """O documento não tem a estrutura de cabeçalho esperada."""


def classificar_imagens(doc):
    """Devolve (xrefs de cabeçalho, xrefs de rodapé, {xref: páginas em que ocorre})."""
    cabecalho = set()
    rodape = set()
    ocorrencias = {}
    for numero, pagina in enumerate(doc):
        for informacao in pagina.get_images(full=True):
            xref, largura, altura = informacao[0], informacao[2], informacao[3]
            if (largura, altura) != (LARGURA_CABECALHO, ALTURA_CABECALHO):
                continue
            for retangulo in pagina.get_image_rects(xref):
                if retangulo.y0 < Y_MAXIMO_CABECALHO:
                    cabecalho.add(xref)
                    ocorrencias.setdefault(xref, set()).add(numero)
                elif retangulo.y0 > Y_MINIMO_RODAPE:
                    rodape.add(xref)
    return cabecalho, rodape, ocorrencias


def validar(doc, cabecalho, rodape, ocorrencias):
    """Confere as invariantes e devolve o único xref de cabeçalho."""
    if not cabecalho:
        raise CabecalhoInvalido("nenhuma imagem 794x113 no topo das páginas")
    if len(cabecalho) > 1:
        raise CabecalhoInvalido(
            "%d imagens distintas de cabeçalho: %s" % (len(cabecalho), sorted(cabecalho))
        )
    xref = next(iter(cabecalho))
    faltando = sorted(set(range(len(doc))) - ocorrencias[xref])
    if faltando:
        raise CabecalhoInvalido("cabeçalho ausente nas páginas %s" % faltando)
    if not rodape:
        raise CabecalhoInvalido("nenhuma imagem de rodapé encontrada")
    if xref in rodape:
        raise CabecalhoInvalido("o xref %d aparece como cabeçalho e como rodapé" % xref)
    return xref
```

- [ ] **Step 4: Rodar os testes e confirmar que passam**

```bash
python -m unittest discover -s tools -p "test_corrigir_cabecalho.py" -v
```

Esperado: `Ran 7 tests` e `OK`.

- [ ] **Step 5: Commit**

```bash
git add tools/corrigir_cabecalho.py tools/test_corrigir_cabecalho.py
git commit -m "Classifica e valida o cabeçalho dos PDFs de resumo"
```

---

## Task 3: Cabeçalho — substituição e verificação

**Files:**
- Modify: `tools/corrigir_cabecalho.py`
- Modify: `tools/test_corrigir_cabecalho.py`

- [ ] **Step 1: Escrever os testes que falham**

Acrescente ao final de `tools/test_corrigir_cabecalho.py`, **antes** do bloco `if __name__`:

```python
class TestCorrigir(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.mkdtemp()
        self.mestre = os.path.join(self.pasta, "mestre.png")
        Image.new("RGB", (794, 113), (250, 240, 230)).save(self.mestre)

    def _gravar(self, doc):
        caminho = os.path.join(self.pasta, "entrada.pdf")
        doc.save(caminho)
        return caminho

    def test_troca_o_cabecalho_e_preserva_o_rodape(self):
        entrada = self._gravar(pdf_sintetico(paginas=3))
        saida = os.path.join(self.pasta, "saida.pdf")

        corrigir(entrada, saida, self.mestre)

        doc = fitz.open(saida)
        cabecalho, rodape, ocorrencias = classificar_imagens(doc)
        xref_cabecalho = validar(doc, cabecalho, rodape, ocorrencias)
        self.assertEqual(amostras(doc, xref_cabecalho), amostras_do_arquivo(self.mestre))
        xref_rodape = next(iter(rodape))
        self.assertEqual(fitz.Pixmap(doc, xref_rodape).pixel(10, 10), (200, 200, 200))

    def test_texto_extraido_nao_muda(self):
        entrada = self._gravar(pdf_sintetico(paginas=3))
        saida = os.path.join(self.pasta, "saida.pdf")
        antes = [p.get_text() for p in fitz.open(entrada)]

        corrigir(entrada, saida, self.mestre)

        self.assertEqual([p.get_text() for p in fitz.open(saida)], antes)

    def test_contagem_de_paginas_nao_muda(self):
        entrada = self._gravar(pdf_sintetico(paginas=4))
        saida = os.path.join(self.pasta, "saida.pdf")

        corrigir(entrada, saida, self.mestre)

        self.assertEqual(len(fitz.open(saida)), 4)

    def test_nao_grava_saida_quando_o_documento_e_invalido(self):
        entrada = self._gravar(pdf_sintetico(paginas=2, rodape=False))
        saida = os.path.join(self.pasta, "saida.pdf")

        with self.assertRaises(CabecalhoInvalido):
            corrigir(entrada, saida, self.mestre)

        self.assertFalse(os.path.exists(saida))

    def test_conferir_recusa_arquivo_nao_corrigido(self):
        entrada = self._gravar(pdf_sintetico(paginas=2))

        with self.assertRaises(CabecalhoInvalido):
            conferir(entrada, self.mestre)

    def test_conferir_aceita_arquivo_corrigido(self):
        entrada = self._gravar(pdf_sintetico(paginas=2))
        saida = os.path.join(self.pasta, "saida.pdf")
        corrigir(entrada, saida, self.mestre)

        conferir(saida, self.mestre)
```

E troque a linha de import do módulo, no topo do arquivo, por:

```python
from corrigir_cabecalho import (
    CabecalhoInvalido,
    amostras,
    amostras_do_arquivo,
    classificar_imagens,
    conferir,
    corrigir,
    validar,
)
```

- [ ] **Step 2: Rodar e confirmar que falha**

```bash
python -m unittest discover -s tools -p "test_corrigir_cabecalho.py" -v
```

Esperado: `ImportError: cannot import name 'amostras'`.

- [ ] **Step 3: Implementar**

Acrescente ao final de `tools/corrigir_cabecalho.py`:

```python
def amostras(doc, xref):
    """Bytes decodificados da imagem, sem canal alfa."""
    pixmap = fitz.Pixmap(doc, xref)
    if pixmap.alpha:
        pixmap = fitz.Pixmap(pixmap, 0)
    return pixmap.samples


def amostras_do_arquivo(caminho):
    pixmap = fitz.Pixmap(caminho)
    if pixmap.alpha:
        pixmap = fitz.Pixmap(pixmap, 0)
    return pixmap.samples


def corrigir(entrada, saida, mestre):
    """Grava em `saida` uma cópia de `entrada` com o cabeçalho substituído."""
    doc = fitz.open(entrada)
    try:
        xref = validar(doc, *classificar_imagens(doc))
        doc[0].replace_image(xref, filename=str(mestre))
        doc.save(str(saida), garbage=4, deflate=True)
    finally:
        doc.close()
    return xref


def conferir(caminho, mestre):
    """Levanta CabecalhoInvalido se o PDF não estiver com o cabeçalho mestre."""
    doc = fitz.open(caminho)
    try:
        xref = validar(doc, *classificar_imagens(doc))
        obtido = amostras(doc, xref)
    finally:
        doc.close()
    esperado = amostras_do_arquivo(mestre)
    if obtido != esperado:
        raise CabecalhoInvalido("o cabeçalho de %s não é o mestre" % os.path.basename(caminho))
```

`replace_image` é método de página, mas afeta **todas** as páginas que exibem aquele xref — por isso basta chamá-lo em `doc[0]`.

- [ ] **Step 4: Rodar e confirmar que passa**

```bash
python -m unittest discover -s tools -p "test_corrigir_cabecalho.py" -v
```

Esperado: `Ran 13 tests` e `OK`.

- [ ] **Step 5: Commit**

```bash
git add tools/corrigir_cabecalho.py tools/test_corrigir_cabecalho.py
git commit -m "Substitui e confere o cabeçalho dos PDFs de resumo"
```

---

## Task 4: CLI e execução sobre os 27 resumos

**Files:**
- Modify: `tools/corrigir_cabecalho.py`
- Create: `assets/graphics/cabecalho-caminhos-2026.png`

- [ ] **Step 1: Levar o cabeçalho mestre para o repositório**

```bash
cp "C:/Users/Windows 10/Downloads/caminhos_cabecalho.png" assets/graphics/cabecalho-caminhos-2026.png
python -c "from PIL import Image; im=Image.open('assets/graphics/cabecalho-caminhos-2026.png'); print(im.size, im.mode)"
```

Esperado: `(794, 113) RGB`. Qualquer outra dimensão invalida o resto do plano — pare e investigue.

- [ ] **Step 2: Guardar os originais fora do repositório**

```bash
mkdir -p "C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/_resumos_backup_19-22"
cp -r "C:/Users/Windows 10/Downloads/PO" "C:/Users/Windows 10/Downloads/CO" "C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/_resumos_backup_19-22/"
ls "C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/_resumos_backup_19-22/PO" | wc -l
ls "C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/_resumos_backup_19-22/CO" | wc -l
```

Esperado: `9` e `18`.

- [ ] **Step 3: Acrescentar a interface de linha de comando**

Acrescente ao final de `tools/corrigir_cabecalho.py`:

```python
def corrigir_pasta(origem, destino, mestre):
    """Corrige todos os PDFs de `origem`, preservando os nomes. Devolve (ok, falhas)."""
    os.makedirs(destino, exist_ok=True)
    ok = []
    falhas = []
    for nome in sorted(os.listdir(origem)):
        if not nome.lower().endswith(".pdf"):
            continue
        entrada = os.path.join(origem, nome)
        saida = os.path.join(destino, nome)
        try:
            texto_antes = [pagina.get_text() for pagina in fitz.open(entrada)]
            paginas_antes = len(texto_antes)
            corrigir(entrada, saida, mestre)
            conferir(saida, mestre)
            doc = fitz.open(saida)
            texto_depois = [pagina.get_text() for pagina in doc]
            doc.close()
            if texto_depois != texto_antes:
                raise CabecalhoInvalido("o texto extraído mudou")
            if len(texto_depois) != paginas_antes:
                raise CabecalhoInvalido("a contagem de páginas mudou")
            ok.append(nome)
            print("OK      %s" % nome)
        except CabecalhoInvalido as erro:
            if os.path.exists(saida):
                os.remove(saida)
            falhas.append((nome, str(erro)))
            print("FALHOU  %s — %s" % (nome, erro))
    return ok, falhas


def main(argumentos):
    if len(argumentos) != 2:
        print(__doc__)
        return 2
    origem, destino = argumentos
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mestre = os.path.join(raiz, "assets", "graphics", "cabecalho-caminhos-2026.png")
    ok, falhas = corrigir_pasta(origem, destino, mestre)
    print("\n%d corrigidos, %d falhas" % (len(ok), len(falhas)))
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

- [ ] **Step 4: Rodar sobre as duas pastas**

```bash
python tools/corrigir_cabecalho.py "C:/Users/Windows 10/Downloads/PO" "C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/_resumos_corrigidos/PO"
```

Esperado: 9 linhas `OK` e `9 corrigidos, 0 falhas`.

```bash
python tools/corrigir_cabecalho.py "C:/Users/Windows 10/Downloads/CO" "C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/_resumos_corrigidos/CO"
```

Esperado: 18 linhas `OK` e `18 corrigidos, 0 falhas`.

Se algum arquivo falhar, **não contorne**: leia a mensagem, entenda por que aquele PDF foge do padrão e ajuste a classificação. Um resumo com cabeçalho diferente é informação, não obstáculo.

- [ ] **Step 5: Conferência visual, uma vez, com olho humano**

```bash
python -c "import fitz; d=fitz.open('C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/_resumos_corrigidos/CO/felipe fonseca - tecendo caminhos.pdf'); d[0].get_pixmap(clip=fitz.Rect(0,0,595,120), dpi=150).save('amostra-cabecalho.png')"
```

Abra `amostra-cabecalho.png` e confirme que se lê **18-23 AGOSTO 2026**. Apague o arquivo depois.

- [ ] **Step 6: Commit**

```bash
git add assets/graphics/cabecalho-caminhos-2026.png tools/corrigir_cabecalho.py
git commit -m "Adiciona cabeçalho mestre 18-23 e a CLI de correção em lote"
```

---

## Task 5: Pareamento — normalização e pontuação

**Files:**
- Create: `tools/parear_resumos.py`
- Test: `tools/test_parear_resumos.py`

- [ ] **Step 1: Escrever os testes que falham**

Crie `tools/test_parear_resumos.py`:

```python
"""Testes do pareamento entre arquivos de resumo e linhas da programação.

    python -m unittest discover -s tools -p "test_*.py" -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parear_resumos import (
    itens_da_programacao,
    nome_destino,
    parear,
    pontuar,
    sem_acento,
    tokens,
)


class TestNormalizacao(unittest.TestCase):
    def test_remove_acentos(self):
        self.assertEqual(sem_acento("Criação e avaliação"), "Criacao e avaliacao")

    def test_tokens_descartam_palavras_vazias_e_curtas(self):
        self.assertEqual(
            tokens("O design têxtil na indústria de malharia"),
            {"design", "textil", "industria", "malharia"},
        )


class TestPontuar(unittest.TestCase):
    def test_par_correto_pontua_alto(self):
        nota = pontuar(
            "felipe fonseca - tecendo caminhos.pdf",
            "Felipe Fonseca",
            "Tecendo caminhos: a construção recursiva do método em uma pesquisa sobre criação em Moda",
        )

        self.assertGreater(nota, 0.9)

    def test_par_errado_pontua_baixo(self):
        nota = pontuar(
            "felipe fonseca - tecendo caminhos.pdf",
            "Angelica Neumaier",
            "Caminhar, coletar, imprimir",
        )

        self.assertLess(nota, 0.3)

    def test_nome_sem_separador_ainda_pontua_pelo_conjunto(self):
        nota = pontuar("Mare Tranquillitatis.pdf", "Sergio Augusto Medeiros", "Mare Tranquillitatis")

        self.assertGreater(nota, 0.4)


class TestParear(unittest.TestCase):
    def setUp(self):
        self.itens = [
            {"ordem": 1, "modalidade": "CO", "autores": "Felipe Fonseca", "titulo": "Tecendo caminhos"},
            {"ordem": 2, "modalidade": "CO", "autores": "Angelica Neumaier", "titulo": "Caminhar, coletar, imprimir"},
            {"ordem": 3, "modalidade": "PO", "autores": "Renata Leahy", "titulo": "Corpo, ancestralidade e envolvimento"},
        ]
        self.arquivos = {
            "CO": [
                "CO/felipe fonseca - tecendo caminhos.pdf",
                "CO/Angelica Neumaier - caminhar coletar imprimir.pdf",
            ],
            "PO": ["PO/renata leahy - corpo ancestralidade.pdf"],
        }

    def test_cada_item_recebe_o_arquivo_certo(self):
        escolhido = parear(self.itens, self.arquivos)

        self.assertEqual(escolhido[0][0], "CO/felipe fonseca - tecendo caminhos.pdf")
        self.assertEqual(escolhido[1][0], "CO/Angelica Neumaier - caminhar coletar imprimir.pdf")
        self.assertEqual(escolhido[2][0], "PO/renata leahy - corpo ancestralidade.pdf")

    def test_nenhum_arquivo_e_usado_duas_vezes(self):
        escolhido = parear(self.itens, self.arquivos)

        usados = [arquivo for arquivo, _ in escolhido.values()]
        self.assertEqual(len(usados), len(set(usados)))

    def test_poster_nunca_casa_com_arquivo_de_comunicacao_oral(self):
        itens = [{"ordem": 1, "modalidade": "PO", "autores": "Felipe Fonseca", "titulo": "Tecendo caminhos"}]

        escolhido = parear(itens, self.arquivos)

        self.assertTrue(escolhido[0][0].startswith("PO/"))


class TestNomeDestino(unittest.TestCase):
    def test_usa_sobrenome_do_primeiro_autor_e_quatro_palavras_do_titulo(self):
        nome = nome_destino(
            1,
            "Dr. Yves Maurice Jean Barblan",
            "Criação e avaliação no ensino obrigatório na área das artes",
        )

        self.assertEqual(nome, "01-barblan-criacao-avaliacao-ensino-obrigatorio.pdf")

    def test_ignora_tratamento_e_usa_o_primeiro_autor_de_uma_lista(self):
        nome = nome_destino(12, "Mara Rúbia Sant'Anna; Pam Ignowski", "Cartografias Sensíveis e as Trajetórias")

        self.assertEqual(nome, "12-santanna-cartografias-sensiveis-trajetorias.pdf")


class TestItensDaProgramacao(unittest.TestCase):
    def test_extrai_itens_em_ordem_cronologica_com_a_modalidade(self):
        programacao = [
            {
                "rotulo": "20 AGO",
                "data": "2026-08-20",
                "atividades": [
                    {
                        "hora": "13h30–15h",
                        "tipo": "Comunicações Orais",
                        "titulo": "1ª Sessão de C.O.",
                        "modalidade": "presencial",
                        "local": "Auditório",
                        "programa": [{"hora": "13h40", "autores": "A B", "titulo": "T1"}],
                    },
                    {
                        "hora": "17h30–19h",
                        "tipo": "Pôster",
                        "titulo": "Sessão de Pôster",
                        "modalidade": "online",
                        "local": "Zoom",
                        "programa": [{"hora": "17h35", "autores": "C D", "titulo": "T2"}],
                    },
                ],
            }
        ]

        itens = itens_da_programacao(programacao)

        self.assertEqual([i["ordem"] for i in itens], [1, 2])
        self.assertEqual([i["modalidade"] for i in itens], ["CO", "PO"])
        self.assertEqual(itens[0]["sessao"], "1ª Sessão de C.O.")
        self.assertEqual(itens[1]["local"], "Zoom")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Rodar e confirmar que falha**

```bash
python -m unittest discover -s tools -p "test_parear_resumos.py" -v
```

Esperado: `ModuleNotFoundError: No module named 'parear_resumos'`.

- [ ] **Step 3: Implementar**

Crie `tools/parear_resumos.py`:

```python
"""Casa cada PDF de resumo com sua linha da programação e grava _data/caderno.json.

A heurística roda UMA vez, é revisada por gente e o resultado aprovado vira fonte
de verdade. Depois disso o gerador do caderno lê o JSON, nunca a heurística.

Uso (a partir da raiz do repositório):
    python tools/parear_resumos.py CORRIGIDOS         # só mostra a tabela
    python tools/parear_resumos.py CORRIGIDOS --gravar  # grava JSON e copia PDFs

Testes:
    python -m unittest discover -s tools -p "test_*.py" -v
"""
import json
import os
import re
import shutil
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROGRAMACAO = os.path.join(RAIZ, "_data", "programacao.json")
CADERNO = os.path.join(RAIZ, "_data", "caderno.json")
DESTINO_RESUMOS = os.path.join(RAIZ, "assets", "anais", "2026", "resumos")

PALAVRAS_VAZIAS = {
    "de", "da", "do", "das", "dos", "para", "com", "sem", "por", "em", "na", "no",
    "nas", "nos", "que", "uma", "uns", "umas", "ao", "aos", "sobre", "entre",
}
TRATAMENTOS = {"dr", "dra", "prof", "profa", "me", "ms", "msc", "phd"}


def sem_acento(texto):
    decomposto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in decomposto if not unicodedata.combining(c))


def tokens(texto):
    palavras = re.findall(r"[a-z0-9]+", sem_acento(texto).lower())
    return {p for p in palavras if len(p) >= 3 and p not in PALAVRAS_VAZIAS}


def pontuar(nome_arquivo, autores, titulo):
    """0 a 1. Metade do peso para a autoria, metade para o título."""
    base = os.path.splitext(os.path.basename(nome_arquivo))[0]
    esquerda, separador, direita = base.partition(" - ")
    if not separador:
        esquerda, direita = base, base
    tokens_esquerda, tokens_direita = tokens(esquerda), tokens(direita)
    nota_autores = (
        len(tokens_esquerda & tokens(autores)) / len(tokens_esquerda) if tokens_esquerda else 0.0
    )
    nota_titulo = (
        len(tokens_direita & tokens(titulo)) / len(tokens_direita) if tokens_direita else 0.0
    )
    return 0.5 * nota_autores + 0.5 * nota_titulo


def parear(itens, arquivos_por_modalidade):
    """Atribuição gulosa global. Devolve {índice do item: (arquivo, nota)}."""
    candidatos = []
    for indice, item in enumerate(itens):
        for arquivo in arquivos_por_modalidade.get(item["modalidade"], []):
            candidatos.append((pontuar(arquivo, item["autores"], item["titulo"]), indice, arquivo))
    candidatos.sort(key=lambda t: (-t[0], t[1], t[2]))
    escolhido = {}
    usados = set()
    for nota, indice, arquivo in candidatos:
        if indice in escolhido or arquivo in usados:
            continue
        escolhido[indice] = (arquivo, nota)
        usados.add(arquivo)
    return escolhido


def _slug(texto, limite):
    palavras = [
        p for p in re.findall(r"[a-z0-9]+", sem_acento(texto).lower())
        if len(p) >= 3 and p not in PALAVRAS_VAZIAS
    ]
    return "-".join(palavras[:limite])


def nome_destino(ordem, autores, titulo):
    primeiro = autores.split(";")[0]
    partes = [
        p for p in re.findall(r"[A-Za-zÀ-ÿ']+", primeiro)
        if sem_acento(p).lower().strip(".") not in TRATAMENTOS
    ]
    # Sant'Anna vira "santanna", não "sant": o apóstrofo não parte o sobrenome.
    sobrenome = _slug(partes[-1].replace("'", ""), 1) if partes else "autoria"
    return "%02d-%s-%s.pdf" % (ordem, sobrenome, _slug(titulo, 4))


def itens_da_programacao(programacao):
    """Achata o campo `programa` das atividades, em ordem cronológica."""
    itens = []
    ordem = 0
    for dia in programacao:
        for atividade in dia["atividades"]:
            blocos = atividade.get("paralelas") or [atividade]
            for bloco in blocos:
                for trabalho in bloco.get("programa") or []:
                    ordem += 1
                    itens.append({
                        "ordem": ordem,
                        "sessao": bloco.get("titulo", ""),
                        "modalidade": "PO" if "Pôster" in bloco.get("tipo", "") else "CO",
                        "data": dia.get("data", ""),
                        "hora": trabalho.get("hora", ""),
                        "local": bloco.get("local", ""),
                        "autores": trabalho["autores"],
                        "titulo": trabalho["titulo"],
                    })
    return itens
```

- [ ] **Step 4: Rodar e confirmar que passa**

```bash
python -m unittest discover -s tools -p "test_parear_resumos.py" -v
```

Esperado: `Ran 11 tests` e `OK`.

Se `test_usa_sobrenome_do_primeiro_autor_e_quatro_palavras_do_titulo` falhar por uma palavra a mais ou a menos, ajuste `PALAVRAS_VAZIAS` — não o teste. O nome de arquivo precisa ser previsível.

- [ ] **Step 5: Commit**

```bash
git add tools/parear_resumos.py tools/test_parear_resumos.py
git commit -m "Pareia arquivos de resumo com as linhas da programação"
```

---

## Task 6: Pareamento — tabela de revisão, JSON e cópia

**Files:**
- Modify: `tools/parear_resumos.py`
- Create: `_data/caderno.json`
- Create: `assets/anais/2026/resumos/*.pdf`

- [ ] **Step 1: Acrescentar a CLI**

Acrescente ao final de `tools/parear_resumos.py`:

```python
def arquivos_por_modalidade(pasta_corrigidos):
    mapa = {}
    for modalidade in ("PO", "CO"):
        pasta = os.path.join(pasta_corrigidos, modalidade)
        mapa[modalidade] = sorted(
            os.path.join(pasta, nome)
            for nome in os.listdir(pasta)
            if nome.lower().endswith(".pdf")
        )
    return mapa


def montar(pasta_corrigidos):
    import fitz

    programacao = json.load(open(PROGRAMACAO, encoding="utf-8"))
    itens = itens_da_programacao(programacao)
    mapa = arquivos_por_modalidade(pasta_corrigidos)
    escolhido = parear(itens, mapa)

    registros = []
    for indice, item in enumerate(itens):
        arquivo, nota = escolhido[indice]
        doc = fitz.open(arquivo)
        paginas = len(doc)
        doc.close()
        registro = dict(item)
        registro["origem"] = os.path.basename(arquivo)
        registro["arquivo"] = "assets/anais/2026/resumos/" + nome_destino(
            item["ordem"], item["autores"], item["titulo"]
        )
        registro["paginas"] = paginas
        registro["_nota"] = round(nota, 3)
        registro["_caminho_origem"] = arquivo
        registros.append(registro)
    return registros


def imprimir_tabela(registros):
    """Menor confiança primeiro — é onde a revisão humana precisa olhar."""
    print("%-5s %-6s %-4s %-42s %s" % ("NOTA", "MODAL", "ORD", "PROGRAMAÇÃO (autores)", "ARQUIVO"))
    for registro in sorted(registros, key=lambda r: r["_nota"]):
        print("%-5.2f %-6s %-4d %-42s %s" % (
            registro["_nota"],
            registro["modalidade"],
            registro["ordem"],
            registro["autores"][:42],
            registro["origem"],
        ))


def gravar(registros):
    os.makedirs(DESTINO_RESUMOS, exist_ok=True)
    limpos = []
    for registro in registros:
        shutil.copyfile(registro["_caminho_origem"], os.path.join(RAIZ, registro["arquivo"]))
        limpo = {c: registro[c] for c in registro if not c.startswith("_")}
        limpos.append(limpo)
    with open(CADERNO, "w", encoding="utf-8", newline="\n") as saida:
        json.dump({"itens": limpos}, saida, ensure_ascii=False, indent=2)
        saida.write("\n")
    print("gravados %d PDFs em %s" % (len(limpos), os.path.relpath(DESTINO_RESUMOS, RAIZ)))
    print("gravado %s" % os.path.relpath(CADERNO, RAIZ))


def main(argumentos):
    if not argumentos:
        print(__doc__)
        return 2
    registros = montar(argumentos[0])
    imprimir_tabela(registros)
    if "--gravar" in argumentos:
        gravar(registros)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

- [ ] **Step 2: Rodar em modo de conferência**

```bash
python tools/parear_resumos.py "C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/_resumos_corrigidos"
```

Esperado: 27 linhas, ordenadas da menor nota para a maior.

- [ ] **Step 3: Revisão humana — parada obrigatória**

Leve a tabela ao usuário e peça confirmação, item a item, das **linhas com nota abaixo de 0,6**. Não siga sem o aval dele. Um resumo na sessão errada não é detectável depois pelo leitor do caderno.

Se algum par estiver errado, corrija editando o `_data/caderno.json` depois de gravado (Step 4) — o JSON é a fonte de verdade e a heurística não roda de novo.

- [ ] **Step 4: Gravar**

```bash
python tools/parear_resumos.py "C:/Users/Windows 10/Documents/Claude/Projects/Caminhos_contemporaneo/_resumos_corrigidos" --gravar
```

Esperado: `gravados 27 PDFs` e `gravado _data\caderno.json`.

- [ ] **Step 5: Conferir contagens**

```bash
ls assets/anais/2026/resumos/*.pdf | wc -l
python -c "import json; d=json.load(open('_data/caderno.json',encoding='utf-8')); print(len(d['itens']), sum(i['paginas'] for i in d['itens']))"
```

Esperado: `27`, e `27 144`.

- [ ] **Step 6: Commit**

```bash
git add tools/parear_resumos.py _data/caderno.json assets/anais/2026/resumos
git commit -m "Adiciona os 27 resumos corrigidos e o pareamento aprovado"
```

---

## Task 7: Carga e validação cruzada dos dados

**Files:**
- Create: `tools/caderno_dados.py`
- Test: `tools/test_caderno.py`

- [ ] **Step 1: Escrever os testes que falham**

Crie `tools/test_caderno.py`:

```python
"""Testes dos módulos que montam o caderno de resumos.

    python -m unittest discover -s tools -p "test_*.py" -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from caderno_dados import DadosInvalidos, agrupar_por_sessao, conferir_contra_programacao


def item(ordem, sessao="1ª Sessão", titulo="T", autores="A", paginas=4):
    return {
        "ordem": ordem,
        "sessao": sessao,
        "modalidade": "CO",
        "data": "2026-08-20",
        "hora": "13h40",
        "local": "Auditório",
        "autores": autores,
        "titulo": titulo,
        "arquivo": "assets/anais/2026/resumos/%02d-x-y.pdf" % ordem,
        "paginas": paginas,
    }


class TestAgrupar(unittest.TestCase):
    def test_preserva_a_ordem_das_sessoes_e_dos_itens(self):
        itens = [item(1, "S1"), item(2, "S1"), item(3, "S2")]

        grupos = agrupar_por_sessao(itens)

        self.assertEqual([nome for nome, _ in grupos], ["S1", "S2"])
        self.assertEqual([i["ordem"] for i in grupos[0][1]], [1, 2])


class TestConferirContraProgramacao(unittest.TestCase):
    def test_aceita_quando_bate(self):
        itens = [item(1, titulo="Tecendo caminhos", autores="Felipe Fonseca")]
        programacao = [dict(itens[0])]

        conferir_contra_programacao(itens, programacao)

    def test_recusa_titulo_divergente(self):
        itens = [item(1, titulo="Tecendo caminhos")]
        programacao = [dict(itens[0], titulo="Outro título")]

        with self.assertRaises(DadosInvalidos) as erro:
            conferir_contra_programacao(itens, programacao)

        self.assertIn("titulo", str(erro.exception))

    def test_recusa_contagem_diferente(self):
        with self.assertRaises(DadosInvalidos):
            conferir_contra_programacao([item(1)], [item(1), item(2)])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Rodar e confirmar que falha**

```bash
python -m unittest discover -s tools -p "test_caderno.py" -v
```

Esperado: `ModuleNotFoundError: No module named 'caderno_dados'`.

- [ ] **Step 3: Implementar**

Crie `tools/caderno_dados.py`:

```python
"""Carga dos dados do caderno e conferência contra a programação do site."""
import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CADERNO = os.path.join(RAIZ, "_data", "caderno.json")
PROGRAMACAO = os.path.join(RAIZ, "_data", "programacao.json")

CAMPOS_CONFERIDOS = ("sessao", "data", "hora", "local", "autores", "titulo")


class DadosInvalidos(Exception):
    """Os dados do caderno divergem da programação publicada."""


def carregar_itens():
    with open(CADERNO, encoding="utf-8") as arquivo:
        return json.load(arquivo)["itens"]


def carregar_programacao():
    from parear_resumos import itens_da_programacao

    with open(PROGRAMACAO, encoding="utf-8") as arquivo:
        return itens_da_programacao(json.load(arquivo))


def conferir_contra_programacao(itens, programacao):
    """O caderno.json não pode publicar dado mais velho que a programação."""
    if len(itens) != len(programacao):
        raise DadosInvalidos(
            "caderno.json tem %d itens e a programação tem %d" % (len(itens), len(programacao))
        )
    for item, referencia in zip(itens, programacao):
        for campo in CAMPOS_CONFERIDOS:
            if item.get(campo, "") != referencia.get(campo, ""):
                raise DadosInvalidos(
                    "item %s: %s difere da programação — %r vs %r"
                    % (item["ordem"], campo, item.get(campo), referencia.get(campo))
                )


def agrupar_por_sessao(itens):
    """[(nome da sessão, [itens])], preservando a ordem de apresentação."""
    grupos = []
    for item in itens:
        if not grupos or grupos[-1][0] != item["sessao"]:
            grupos.append((item["sessao"], []))
        grupos[-1][1].append(item)
    return grupos
```

- [ ] **Step 4: Rodar e confirmar que passa**

```bash
python -m unittest discover -s tools -p "test_caderno.py" -v
```

Esperado: `Ran 4 tests` e `OK`.

- [ ] **Step 5: Conferir contra os dados reais**

```bash
python -c "from tools.caderno_dados import *" 2>/dev/null; python -c "
import sys; sys.path.insert(0,'tools')
from caderno_dados import carregar_itens, carregar_programacao, conferir_contra_programacao, agrupar_por_sessao
itens = carregar_itens()
conferir_contra_programacao(itens, carregar_programacao())
print('itens:', len(itens))
print('sessões:', [nome for nome, _ in agrupar_por_sessao(itens)])
"
```

Esperado: `itens: 27` e quatro nomes de sessão. Se levantar `DadosInvalidos`, o `caderno.json` ficou fora de sincronia com a programação — resolva antes de seguir.

- [ ] **Step 6: Commit**

```bash
git add tools/caderno_dados.py tools/test_caderno.py
git commit -m "Carrega e valida os dados do caderno contra a programação"
```

---

## Task 8: Markdown mínimo e medição de texto

**Files:**
- Create: `tools/caderno_texto.py`
- Modify: `tools/test_caderno.py`

O expediente e a apresentação vêm de arquivos Markdown escritos pelo usuário. Não precisamos de um parser completo — só de títulos, parágrafos e listas.

- [ ] **Step 1: Escrever os testes que falham**

Acrescente a `tools/test_caderno.py`, antes do bloco `if __name__`:

```python
from caderno_texto import blocos_de_markdown, quebrar_linhas


class TestBlocosDeMarkdown(unittest.TestCase):
    def test_reconhece_titulos_paragrafos_e_itens(self):
        texto = "# Expediente\n\nRealização do evento.\n\n## Comissão\n\n- Ana\n- Bruno\n"

        blocos = blocos_de_markdown(texto)

        self.assertEqual(blocos, [
            ("h1", "Expediente"),
            ("p", "Realização do evento."),
            ("h2", "Comissão"),
            ("li", "Ana"),
            ("li", "Bruno"),
        ])

    def test_junta_linhas_de_um_mesmo_paragrafo(self):
        texto = "Primeira linha\nsegunda linha\n\nOutro parágrafo\n"

        blocos = blocos_de_markdown(texto)

        self.assertEqual(blocos, [("p", "Primeira linha segunda linha"), ("p", "Outro parágrafo")])

    def test_remove_marcacao_de_negrito_e_italico(self):
        blocos = blocos_de_markdown("Texto **forte** e *suave*.\n")

        self.assertEqual(blocos, [("p", "Texto forte e suave.")])

    def test_texto_vazio_nao_gera_blocos(self):
        self.assertEqual(blocos_de_markdown("   \n\n"), [])


class TestQuebrarLinhas(unittest.TestCase):
    def test_quebra_respeitando_a_largura(self):
        import fitz

        fonte = fitz.Font(fontfile=os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "assets", "fonts", "Poppins-Regular.ttf",
        ))

        linhas = quebrar_linhas("palavra " * 40, fonte, 10, 200)

        self.assertGreater(len(linhas), 1)
        for linha in linhas:
            self.assertLessEqual(fonte.text_length(linha, 10), 200)
```

- [ ] **Step 2: Rodar e confirmar que falha**

```bash
python -m unittest discover -s tools -p "test_caderno.py" -v
```

Esperado: `ImportError: cannot import name 'blocos_de_markdown'`.

- [ ] **Step 3: Implementar**

Crie `tools/caderno_texto.py`:

```python
"""Markdown mínimo e medição tipográfica para as páginas de texto do caderno.

Suporta apenas o que o expediente e a apresentação precisam: `#`, `##`,
parágrafos separados por linha em branco e itens de lista com `-`.
"""
import re

NEGRITO_ITALICO = re.compile(r"\*{1,2}([^*]+)\*{1,2}")


def _limpar(linha):
    return NEGRITO_ITALICO.sub(r"\1", linha).strip()


def blocos_de_markdown(texto):
    """Devolve [(tipo, conteúdo)] com tipo em {h1, h2, p, li}."""
    blocos = []
    paragrafo = []

    def fechar():
        if paragrafo:
            blocos.append(("p", " ".join(paragrafo)))
            del paragrafo[:]

    for linha_bruta in texto.splitlines():
        linha = _limpar(linha_bruta)
        if not linha:
            fechar()
        elif linha.startswith("## "):
            fechar()
            blocos.append(("h2", linha[3:].strip()))
        elif linha.startswith("# "):
            fechar()
            blocos.append(("h1", linha[2:].strip()))
        elif linha.startswith("- "):
            fechar()
            blocos.append(("li", linha[2:].strip()))
        else:
            paragrafo.append(linha)
    fechar()
    return blocos


def quebrar_linhas(texto, fonte, corpo, largura):
    """Quebra `texto` em linhas que cabem em `largura` pontos."""
    linhas = []
    atual = ""
    for palavra in texto.split():
        proposta = palavra if not atual else atual + " " + palavra
        if fonte.text_length(proposta, corpo) <= largura or not atual:
            atual = proposta
        else:
            linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas
```

- [ ] **Step 4: Rodar e confirmar que passa**

```bash
python -m unittest discover -s tools -p "test_caderno.py" -v
```

Esperado: `Ran 9 tests` e `OK`.

- [ ] **Step 5: Commit**

```bash
git add tools/caderno_texto.py tools/test_caderno.py
git commit -m "Adiciona markdown mínimo e quebra de linhas do caderno"
```

---

## Task 9: Sumário — paginação em duas passadas

**Files:**
- Create: `tools/caderno_paginas.py`
- Modify: `tools/test_caderno.py`

O número de páginas do sumário desloca a numeração de tudo que vem depois. A saída para não entrar em laço: o fólio ocupa uma **coluna de largura fixa** à direita, então a quebra de linhas do sumário não depende dos números. Paginar primeiro, calcular deslocamentos depois, renderizar por último.

- [ ] **Step 1: Escrever os testes que falham**

Acrescente a `tools/test_caderno.py`, antes do bloco `if __name__`:

```python
from caderno_paginas import linhas_do_sumario, paginar_sumario, primeiras_paginas


class TestSumario(unittest.TestCase):
    def test_gera_uma_linha_de_sessao_e_uma_por_item(self):
        itens = [item(1, "S1"), item(2, "S1"), item(3, "S2")]

        linhas = linhas_do_sumario(itens)

        self.assertEqual([l[0] for l in linhas], ["sessao", "item", "item", "sessao", "item"])

    def test_paginar_respeita_a_capacidade(self):
        linhas = linhas_do_sumario([item(n, "S1") for n in range(1, 21)])

        paginas = paginar_sumario(linhas, capacidade=8)

        self.assertEqual(len(paginas), 3)
        self.assertEqual(sum(len(p) for p in paginas), len(linhas))


class TestPrimeirasPaginas(unittest.TestCase):
    def test_soma_as_paginas_de_cada_resumo(self):
        itens = [item(1, paginas=4), item(2, paginas=3), item(3, paginas=6)]

        paginas = primeiras_paginas(itens, paginas_antes=7)

        self.assertEqual(paginas, [8, 12, 15])

    def test_sumario_maior_empurra_todos_os_resumos(self):
        itens = [item(1, paginas=4), item(2, paginas=3)]

        curto = primeiras_paginas(itens, paginas_antes=5)
        longo = primeiras_paginas(itens, paginas_antes=6)

        self.assertEqual([p + 1 for p in curto], longo)
```

- [ ] **Step 2: Rodar e confirmar que falha**

```bash
python -m unittest discover -s tools -p "test_caderno.py" -v
```

Esperado: `ImportError: cannot import name 'linhas_do_sumario'`.

- [ ] **Step 3: Implementar a parte pura**

Crie `tools/caderno_paginas.py`:

```python
"""Montagem das páginas do caderno: capa, páginas de texto e sumário.

O fólio do sumário ocupa uma coluna de largura fixa à direita. Por isso a quebra
de linhas não depende dos números de página, e duas passadas bastam: paginar,
calcular os deslocamentos, renderizar.
"""
import os

import fitz

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTES = os.path.join(RAIZ, "assets", "fonts")

LARGURA = 595.0
ALTURA = 842.0
MARGEM = 64.0
LARGURA_UTIL = LARGURA - 2 * MARGEM
COLUNA_FOLIO = 34.0

BEGE = (223 / 255, 215 / 255, 204 / 255)
TINTA = (0.18, 0.20, 0.23)

CAPACIDADE_SUMARIO = 22


def linhas_do_sumario(itens):
    """[(tipo, dados)] com tipo em {sessao, item}, na ordem de apresentação."""
    linhas = []
    sessao_corrente = None
    for item in itens:
        if item["sessao"] != sessao_corrente:
            sessao_corrente = item["sessao"]
            linhas.append(("sessao", item))
        linhas.append(("item", item))
    return linhas


def paginar_sumario(linhas, capacidade=CAPACIDADE_SUMARIO):
    """Fatia as linhas em páginas, sem deixar uma sessão órfã no fim da página."""
    paginas = []
    atual = []
    for indice, linha in enumerate(linhas):
        sozinha = linha[0] == "sessao" and len(atual) == capacidade - 1
        if len(atual) == capacidade or sozinha:
            paginas.append(atual)
            atual = []
        atual.append(linha)
    if atual:
        paginas.append(atual)
    return paginas


def primeiras_paginas(itens, paginas_antes):
    """Número da primeira página de cada resumo, contando a capa como página 1."""
    numeros = []
    proxima = paginas_antes + 1
    for item in itens:
        numeros.append(proxima)
        proxima += item["paginas"]
    return numeros
```

- [ ] **Step 4: Rodar e confirmar que passa**

```bash
python -m unittest discover -s tools -p "test_caderno.py" -v
```

Esperado: `Ran 13 tests` e `OK`.

- [ ] **Step 5: Commit**

```bash
git add tools/caderno_paginas.py tools/test_caderno.py
git commit -m "Calcula a paginação do sumário em duas passadas"
```

---

## Task 10: Capa, páginas de texto e desenho do sumário

**Files:**
- Modify: `tools/caderno_paginas.py`
- Modify: `tools/test_caderno.py`

- [ ] **Step 1: Escrever os testes que falham**

Acrescente a `tools/test_caderno.py`, antes do bloco `if __name__`:

```python
from caderno_paginas import desenhar_capa, desenhar_sumario, desenhar_texto, registrar_fontes


class TestDesenho(unittest.TestCase):
    def test_capa_traz_titulo_e_data_correta(self):
        import fitz

        doc = fitz.open()
        desenhar_capa(doc)

        texto = doc[0].get_text()
        self.assertEqual(len(doc), 1)
        self.assertIn("Caderno de Resumos", texto)
        self.assertIn("18 a 23 de agosto de 2026", texto)
        self.assertNotIn("19", texto)

    def test_texto_gera_pelo_menos_uma_pagina_com_o_conteudo(self):
        import fitz

        doc = fitz.open()
        desenhar_texto(doc, [("h1", "Expediente"), ("p", "Realização: LabMAES.")])

        self.assertGreaterEqual(len(doc), 1)
        self.assertIn("Expediente", doc[0].get_text())
        self.assertIn("LabMAES", doc[0].get_text())

    def test_sumario_mostra_titulo_e_numero_de_pagina(self):
        import fitz

        doc = fitz.open()
        itens = [item(1, "1ª Sessão", titulo="Tecendo caminhos", paginas=4)]
        linhas = linhas_do_sumario(itens)

        desenhar_sumario(doc, paginar_sumario(linhas), {1: 9})

        texto = doc[0].get_text()
        self.assertIn("Tecendo caminhos", texto)
        self.assertIn("1ª Sessão", texto)
        self.assertIn("9", texto)
```

- [ ] **Step 2: Rodar e confirmar que falha**

```bash
python -m unittest discover -s tools -p "test_caderno.py" -v
```

Esperado: `ImportError: cannot import name 'desenhar_capa'`.

- [ ] **Step 3: Implementar**

Acrescente ao final de `tools/caderno_paginas.py`:

```python
import io

from PIL import Image

TIPOS = {
    "thunder": os.path.join(FONTES, "Thunder-BoldHC.otf"),
    "poppins": os.path.join(FONTES, "Poppins-Regular.ttf"),
    "poppins-semi": os.path.join(FONTES, "Poppins-SemiBold.ttf"),
    "dmmono": os.path.join(FONTES, "DMMono-Regular.ttf"),
}

TEMA = "Criação, tessituras sensíveis e narrativas em movimento"
DATA_POR_EXTENSO = "18 a 23 de agosto de 2026"
LOCAL = "UDESC CEART — Florianópolis, Santa Catarina"

BANNER = os.path.join(RAIZ, "assets", "banners", "banner-caminhos-desktop.webp")


def registrar_fontes(pagina):
    for nome, caminho in TIPOS.items():
        pagina.insert_font(fontname=nome, fontfile=caminho)


def _fonte(nome):
    return fitz.Font(fontfile=TIPOS[nome])


def _banner_como_png():
    """O PyMuPDF não lê webp de forma confiável; convertemos com o Pillow."""
    imagem = Image.open(BANNER).convert("RGB")
    largura, altura = imagem.size
    recorte = imagem.crop((0, 0, largura, int(altura * 0.62)))
    buffer = io.BytesIO()
    recorte.save(buffer, format="PNG")
    return buffer.getvalue()


def desenhar_capa(doc):
    pagina = doc.new_page(width=LARGURA, height=ALTURA)
    registrar_fontes(pagina)
    pagina.draw_rect(fitz.Rect(0, 0, LARGURA, ALTURA), color=None, fill=BEGE)
    pagina.insert_image(fitz.Rect(0, 0, LARGURA, 300), stream=_banner_como_png())

    pagina.insert_textbox(
        fitz.Rect(MARGEM, 360, LARGURA - MARGEM, 440),
        "Caderno de Resumos",
        fontname="thunder", fontsize=44, color=TINTA,
    )
    pagina.insert_textbox(
        fitz.Rect(MARGEM, 450, LARGURA - MARGEM, 540),
        TEMA,
        fontname="poppins", fontsize=14, color=TINTA,
    )
    pagina.insert_textbox(
        fitz.Rect(MARGEM, 700, LARGURA - MARGEM, 760),
        DATA_POR_EXTENSO + "\n" + LOCAL,
        fontname="dmmono", fontsize=11, color=TINTA,
    )
    return pagina


def desenhar_texto(doc, blocos):
    """Renderiza blocos de markdown, abrindo páginas conforme necessário."""
    corpos = {"h1": 26, "h2": 15, "p": 10.5, "li": 10.5}
    espacos = {"h1": 20, "h2": 14, "p": 8, "li": 3}
    fontes = {"h1": "thunder", "h2": "poppins-semi", "p": "poppins", "li": "poppins"}

    pagina = doc.new_page(width=LARGURA, height=ALTURA)
    registrar_fontes(pagina)
    y = MARGEM + 20

    for tipo, conteudo in blocos:
        corpo = corpos[tipo]
        recuo = 14 if tipo == "li" else 0
        texto = ("•  " + conteudo) if tipo == "li" else conteudo
        linhas = quebrar_linhas_local(texto, fontes[tipo], corpo, LARGURA_UTIL - recuo)
        altura_bloco = len(linhas) * corpo * 1.45 + espacos[tipo]
        if y + altura_bloco > ALTURA - MARGEM - 40:
            pagina = doc.new_page(width=LARGURA, height=ALTURA)
            registrar_fontes(pagina)
            y = MARGEM + 20
        for linha in linhas:
            pagina.insert_text(
                (MARGEM + recuo, y), linha,
                fontname=fontes[tipo], fontsize=corpo, color=TINTA,
            )
            y += corpo * 1.45
        y += espacos[tipo]
    return doc


def quebrar_linhas_local(texto, nome_fonte, corpo, largura):
    from caderno_texto import quebrar_linhas

    return quebrar_linhas(texto, _fonte(nome_fonte), corpo, largura)


def desenhar_sumario(doc, paginas_de_linhas, numero_por_ordem):
    """`numero_por_ordem` mapeia item['ordem'] → página no caderno."""
    fonte_item = _fonte("poppins")
    for linhas in paginas_de_linhas:
        pagina = doc.new_page(width=LARGURA, height=ALTURA)
        registrar_fontes(pagina)
        y = MARGEM + 20
        pagina.insert_text((MARGEM, y), "Sumário", fontname="thunder", fontsize=26, color=TINTA)
        y += 40
        for tipo, item in linhas:
            if tipo == "sessao":
                y += 10
                pagina.insert_text(
                    (MARGEM, y), item["sessao"],
                    fontname="poppins-semi", fontsize=11, color=TINTA,
                )
                y += 13
                pagina.insert_text(
                    (MARGEM, y),
                    "%s · %s · %s" % (item["data"], item["hora"], item["local"]),
                    fontname="dmmono", fontsize=8, color=TINTA,
                )
                y += 16
                continue

            largura_texto = LARGURA_UTIL - COLUNA_FOLIO
            linhas_item = quebrar_linhas_local(
                "%s. %s" % (item["autores"], item["titulo"]), "poppins", 9.5, largura_texto
            )
            topo = y
            for linha in linhas_item:
                pagina.insert_text((MARGEM, y), linha, fontname="poppins", fontsize=9.5, color=TINTA)
                y += 13
            numero = str(numero_por_ordem[item["ordem"]])
            pagina.insert_text(
                (LARGURA - MARGEM - fonte_item.text_length(numero, 9.5), topo),
                numero, fontname="dmmono", fontsize=9.5, color=TINTA,
            )
            pagina.insert_link({
                "kind": fitz.LINK_GOTO,
                "from": fitz.Rect(MARGEM, topo - 10, LARGURA - MARGEM, y - 4),
                "page": numero_por_ordem[item["ordem"]] - 1,
            })
            y += 6
    return doc
```

- [ ] **Step 4: Rodar e confirmar que passa**

```bash
python -m unittest discover -s tools -p "test_caderno.py" -v
```

Esperado: `Ran 16 tests` e `OK`.

- [ ] **Step 5: Commit**

```bash
git add tools/caderno_paginas.py tools/test_caderno.py
git commit -m "Desenha capa, páginas de texto e sumário do caderno"
```

---

## Task 11: Montagem, fólios, marcadores e metadados

**Files:**
- Create: `tools/gerar_caderno.py`
- Modify: `tools/test_caderno.py`

- [ ] **Step 1: Escrever os testes que falham**

Acrescente a `tools/test_caderno.py`, antes do bloco `if __name__`:

```python
from gerar_caderno import CAIXA_FOLIO, carimbar_folio, montar_outline


class TestFolio(unittest.TestCase):
    def test_a_caixa_do_folio_fica_dentro_da_faixa_de_rodape_e_a_direita_dos_logos(self):
        self.assertGreaterEqual(CAIXA_FOLIO.y0, 769)
        self.assertLessEqual(CAIXA_FOLIO.y1, 842)
        self.assertGreaterEqual(CAIXA_FOLIO.x0, 495)

    def test_carimba_o_numero_na_pagina(self):
        import fitz

        doc = fitz.open()
        pagina = doc.new_page(width=595, height=842)

        carimbar_folio(pagina, 42)

        self.assertIn("42", pagina.get_text())


class TestOutline(unittest.TestCase):
    def test_dois_niveis_sessao_e_trabalho(self):
        itens = [item(1, "S1"), item(2, "S1"), item(3, "S2")]

        outline = montar_outline(itens, {1: 10, 2: 14, 3: 17})

        self.assertEqual([linha[0] for linha in outline], [1, 2, 2, 1, 2])
        self.assertEqual(outline[0][1], "S1")
        self.assertEqual(outline[1][2], 10)
```

- [ ] **Step 2: Rodar e confirmar que falha**

```bash
python -m unittest discover -s tools -p "test_caderno.py" -v
```

Esperado: `ModuleNotFoundError: No module named 'gerar_caderno'`.

- [ ] **Step 3: Implementar**

Crie `tools/gerar_caderno.py`:

```python
"""Monta o caderno de resumos do 7º Caminhos do Contemporâneo.

Uso (a partir da raiz do repositório):
    python tools/gerar_caderno.py

Testes:
    python -m unittest discover -s tools -p "test_*.py" -v
"""
import os
import sys

import fitz

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from caderno_dados import (
    RAIZ,
    carregar_itens,
    carregar_programacao,
    conferir_contra_programacao,
)
from caderno_paginas import (
    TINTA,
    TIPOS,
    desenhar_capa,
    desenhar_sumario,
    desenhar_texto,
    linhas_do_sumario,
    paginar_sumario,
    primeiras_paginas,
)
from caderno_texto import blocos_de_markdown

EXPEDIENTE = os.path.join(RAIZ, "_data", "caderno-expediente.md")
APRESENTACAO = os.path.join(RAIZ, "_data", "caderno-apresentacao.md")
SAIDA = os.path.join(RAIZ, "assets", "anais", "2026", "caderno-resumos-7-caminhos-2026.pdf")

# A faixa bege do rodapé dos resumos ocupa y 769–842; os logos ficam centralizados
# entre x≈120 e x≈490, então a margem direita está livre.
CAIXA_FOLIO = fitz.Rect(500, 798, 560, 818)


def ler_markdown(caminho):
    if not os.path.exists(caminho):
        return []
    with open(caminho, encoding="utf-8") as arquivo:
        return blocos_de_markdown(arquivo.read())


def carimbar_folio(pagina, numero):
    pagina.insert_font(fontname="dmmono", fontfile=TIPOS["dmmono"])
    pagina.insert_textbox(
        CAIXA_FOLIO, str(numero),
        fontname="dmmono", fontsize=9, color=TINTA, align=fitz.TEXT_ALIGN_RIGHT,
    )


def montar_outline(itens, numero_por_ordem):
    outline = []
    sessao_corrente = None
    for item in itens:
        if item["sessao"] != sessao_corrente:
            sessao_corrente = item["sessao"]
            outline.append([1, item["sessao"], numero_por_ordem[item["ordem"]]])
        outline.append([2, item["titulo"], numero_por_ordem[item["ordem"]]])
    return outline


def gerar():
    itens = carregar_itens()
    conferir_contra_programacao(itens, carregar_programacao())

    blocos_expediente = ler_markdown(EXPEDIENTE)
    blocos_apresentacao = ler_markdown(APRESENTACAO)

    # Primeira passada: descobrir quantas páginas o pré-textual ocupa.
    esboco = fitz.open()
    desenhar_capa(esboco)
    if blocos_expediente:
        desenhar_texto(esboco, blocos_expediente)
    if blocos_apresentacao:
        desenhar_texto(esboco, blocos_apresentacao)
    paginas_antes_do_sumario = len(esboco)
    paginas_de_linhas = paginar_sumario(linhas_do_sumario(itens))
    paginas_antes = paginas_antes_do_sumario + len(paginas_de_linhas)
    esboco.close()

    numeros = primeiras_paginas(itens, paginas_antes)
    numero_por_ordem = {item["ordem"]: numero for item, numero in zip(itens, numeros)}

    # Segunda passada: montar de verdade, já com os números certos.
    doc = fitz.open()
    desenhar_capa(doc)
    if blocos_expediente:
        desenhar_texto(doc, blocos_expediente)
    if blocos_apresentacao:
        desenhar_texto(doc, blocos_apresentacao)
    if len(doc) != paginas_antes_do_sumario:
        raise RuntimeError(
            "o pré-textual mudou de tamanho entre as passadas: %d vs %d"
            % (len(doc), paginas_antes_do_sumario)
        )
    desenhar_sumario(doc, paginas_de_linhas, numero_por_ordem)

    for item in itens:
        resumo = fitz.open(os.path.join(RAIZ, item["arquivo"]))
        doc.insert_pdf(resumo)
        resumo.close()

    for indice in range(paginas_antes, len(doc)):
        carimbar_folio(doc[indice], indice + 1)

    doc.set_toc(montar_outline(itens, numero_por_ordem))
    doc.set_metadata({
        "title": "Caderno de Resumos — 7º Seminário Caminhos do Contemporâneo",
        "author": "LabMAES — UDESC CEART",
        "subject": "Resumos das comunicações orais e pôsteres apresentados de 18 a 23 de agosto de 2026",
        "keywords": "Caminhos do Contemporâneo; LabMAES; UDESC; moda; artes; ensino; sociedade",
    })
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    doc.save(SAIDA, garbage=4, deflate=True)
    doc.close()
    return SAIDA, itens, numero_por_ordem, paginas_antes
```

- [ ] **Step 4: Rodar e confirmar que passa**

```bash
python -m unittest discover -s tools -p "test_caderno.py" -v
```

Esperado: `Ran 19 tests` e `OK`.

- [ ] **Step 5: Commit**

```bash
git add tools/gerar_caderno.py tools/test_caderno.py
git commit -m "Monta o caderno com fólios, marcadores e metadados"
```

---

## Task 12: Verificação pós-geração

**Files:**
- Modify: `tools/gerar_caderno.py`
- Modify: `tools/test_caderno.py`

- [ ] **Step 1: Escrever os testes que falham**

Acrescente a `tools/test_caderno.py`, antes do bloco `if __name__`:

```python
from gerar_caderno import cobertura_de_tokens, ler_markdown


class TestLerMarkdown(unittest.TestCase):
    def test_arquivo_inexistente_devolve_lista_vazia(self):
        """A apresentação pode não existir ainda; a seção é simplesmente omitida."""
        self.assertEqual(ler_markdown("/caminho/que/nao/existe.md"), [])


class TestCoberturaDeTokens(unittest.TestCase):
    def test_aceita_variacao_de_caixa_acento_e_plural(self):
        cobertura = cobertura_de_tokens(
            "Narrativas compartilhadas: costuras, escola e memórias",
            "  \n Narrativas compartilhadas: \nCosturas, escola e memória. \n Beatriz Monteiro",
        )

        self.assertGreaterEqual(cobertura, 0.6)

    def test_recusa_texto_de_outro_trabalho(self):
        cobertura = cobertura_de_tokens(
            "Narrativas compartilhadas: costuras, escola e memórias",
            "Caminhar, coletar, imprimir: a caminhada como proposta artística",
        )

        self.assertLess(cobertura, 0.6)
```

- [ ] **Step 2: Rodar e confirmar que falha**

```bash
python -m unittest discover -s tools -p "test_caderno.py" -v
```

Esperado: `ImportError: cannot import name 'cobertura_de_tokens'`.

- [ ] **Step 3: Implementar**

Acrescente ao final de `tools/gerar_caderno.py`:

```python
def cobertura_de_tokens(titulo, texto_da_pagina):
    """Fração dos tokens do título presentes na página.

    Os títulos da programação NÃO são idênticos aos dos PDFs — há diferença de
    caixa, acento e número (memórias/memória). Comparação exata reprovaria
    pareamentos corretos.
    """
    from parear_resumos import sem_acento, tokens

    esperados = tokens(titulo)
    if not esperados:
        return 1.0
    presentes = tokens(texto_da_pagina)
    radicais = {t.rstrip("s") for t in presentes}
    encontrados = {t for t in esperados if t in presentes or t.rstrip("s") in radicais}
    return len(encontrados) / len(esperados)


def verificar(caminho, itens, numero_por_ordem, paginas_antes):
    problemas = []
    doc = fitz.open(caminho)

    esperado = paginas_antes + sum(item["paginas"] for item in itens)
    if len(doc) != esperado:
        problemas.append("total de páginas: %d, esperado %d" % (len(doc), esperado))

    for item in itens:
        indice = numero_por_ordem[item["ordem"]] - 1
        cobertura = cobertura_de_tokens(item["titulo"], doc[indice].get_text())
        if cobertura < 0.6:
            problemas.append(
                "item %d (%s): a página %d não parece ser deste trabalho (cobertura %.2f)"
                % (item["ordem"], item["autores"], indice + 1, cobertura)
            )

    for numero in range(paginas_antes):
        for link in doc[numero].get_links():
            if link["kind"] == fitz.LINK_GOTO and not 0 <= link["page"] < len(doc):
                problemas.append("link do sumário aponta para a página %d" % link["page"])

    outline = doc.get_toc()
    nivel1 = len([linha for linha in outline if linha[0] == 1])
    nivel2 = len([linha for linha in outline if linha[0] == 2])
    sessoes = len({item["sessao"] for item in itens})
    if (nivel1, nivel2) != (sessoes, len(itens)):
        problemas.append(
            "outline com %d sessões e %d trabalhos, esperado %d e %d"
            % (nivel1, nivel2, sessoes, len(itens))
        )

    doc.close()
    return problemas


def main():
    caminho, itens, numero_por_ordem, paginas_antes = gerar()
    problemas = verificar(caminho, itens, numero_por_ordem, paginas_antes)
    doc = fitz.open(caminho)
    print("gravado: %s" % os.path.relpath(caminho, RAIZ))
    print("páginas: %d   pré-textual: %d   tamanho: %.1f MB" % (
        len(doc), paginas_antes, os.path.getsize(caminho) / 1048576,
    ))
    doc.close()
    for problema in problemas:
        print("PROBLEMA: %s" % problema)
    if problemas:
        print("\n%d problema(s). O arquivo foi gravado, mas NÃO deve ser publicado." % len(problemas))
        return 1
    print("\nverificação completa: sem problemas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Rodar e confirmar que passa**

```bash
python -m unittest discover -s tools -p "test_caderno.py" -v
```

Esperado: `Ran 22 tests` e `OK`.

- [ ] **Step 5: Commit**

```bash
git add tools/gerar_caderno.py tools/test_caderno.py
git commit -m "Verifica o caderno gerado: páginas, pareamento, links e outline"
```

---

## Task 13: Gerar o caderno de verdade

**Files:**
- Create: `_data/caderno-expediente.md`, `_data/caderno-apresentacao.md`
- Create: `assets/anais/2026/caderno-resumos-7-caminhos-2026.pdf`

- [ ] **Step 1: Criar os arquivos de texto**

O conteúdo vem do usuário. Peça a ele a lista de comissões e o texto de abertura. Enquanto não chegarem, crie `_data/caderno-expediente.md` com a estrutura e os dados que já são públicos no site:

```markdown
# Expediente

## Realização

- LabMAES — Laboratório de Moda, Artes, Ensino e Sociedade
- UDESC CEART — Centro de Artes, Design e Moda
- Fapesc — Fundação de Amparo à Pesquisa e Inovação do Estado de Santa Catarina

## Contato

- labmaes.ceart@udesc.br
```

Deixe `_data/caderno-apresentacao.md` **inexistente** até o usuário entregar o texto — o gerador omite a seção e a paginação se ajusta sozinha.

- [ ] **Step 2: Gerar**

```bash
python tools/gerar_caderno.py
```

Esperado: `verificação completa: sem problemas`, com `páginas:` acima de 145.

Se aparecer `PROBLEMA: item N ... não parece ser deste trabalho`, o pareamento está errado naquele item. Corrija `_data/caderno.json` e gere de novo. **Não baixe o limiar de 0,6** para fazer o aviso sumir.

- [ ] **Step 3: Conferência visual, com olho humano**

```bash
python -c "
import fitz
doc = fitz.open('assets/anais/2026/caderno-resumos-7-caminhos-2026.pdf')
for n in (0, 1, 2, 3, doc.page_count - 1):
    doc[n].get_pixmap(dpi=110).save('conferencia-%02d.png' % n)
print('outline:', len(doc.get_toc()), 'entradas')
"
```

Abra as cinco imagens e confirme: a capa traz 18-23; o sumário lista as quatro sessões; a última página tem o fólio na faixa bege, à direita dos logos, sem sobrepor nada. Apague as imagens depois.

- [ ] **Step 4: Commit**

```bash
git add _data/caderno-expediente.md assets/anais/2026/caderno-resumos-7-caminhos-2026.pdf
git commit -m "Gera o caderno de resumos do 7º Caminhos"
```

---

## Task 14: Publicar no site

**Files:**
- Modify: `eventos/caminhos-do-contemporaneo/2026/programacao/index.njk:20`
- Modify: `eventos/caminhos-do-contemporaneo/2026/submissoes/index.njk:85`

Padrão de botão do repositório: `<a class="button button--secondary" href="…" download aria-label="…">`.

- [ ] **Step 1: Botão na Programação**

Em `programacao/index.njk`, dentro de `<div class="prog-header__text">`, logo **depois** do `<p class="section-body">` que fecha na linha 20, acrescente:

```html
          <div class="submissao-card__actions">
            <a class="button button--secondary"
               href="/assets/anais/2026/caderno-resumos-7-caminhos-2026.pdf"
               download
               aria-label="Baixar o caderno de resumos com os trabalhos apresentados">
              Baixar caderno de resumos ↓
            </a>
          </div>
```

- [ ] **Step 2: Botão em Submissões**

Em `submissoes/index.njk`, dentro da seção `S2: Resultado da avaliação`, logo **depois** do `</div>` que fecha `event-card-grid` (linha 87) e **antes** do `</div>` do `container`, acrescente:

```html
      <p class="section-body section-content">O caderno de resumos reúne todos os trabalhos aprovados, na ordem em que serão apresentados. Não substitui os anais, que serão publicados com ISBN após o envio dos textos finais.</p>
      <div class="submissao-card__actions">
        <a class="button button--secondary"
           href="/assets/anais/2026/caderno-resumos-7-caminhos-2026.pdf"
           download
           aria-label="Baixar o caderno de resumos com os trabalhos aprovados">
          Baixar caderno de resumos ↓
        </a>
      </div>
```

- [ ] **Step 3: Construir e conferir que o PDF é servido**

```bash
npx @11ty/eleventy
ls -la _site/assets/anais/2026/caderno-resumos-7-caminhos-2026.pdf
grep -c "caderno-resumos-7-caminhos-2026.pdf" _site/eventos/caminhos-do-contemporaneo/2026/programacao/index.html _site/eventos/caminhos-do-contemporaneo/2026/submissoes/index.html
```

Esperado: o PDF existe em `_site/` e cada arquivo HTML traz `1` ocorrência.

- [ ] **Step 4: Conferir no navegador**

Suba o servidor com `preview_start` (nunca com Bash) e verifique, com `read_page`, que o botão aparece nas duas páginas e que o `href` aponta para o PDF. Lembre da armadilha conhecida: depois de `resize_window`, recarregue a página antes de medir estilos computados.

- [ ] **Step 5: Confirmar que `/anais/` continua intacta**

```bash
git diff --stat eventos/caminhos-do-contemporaneo/2026/anais/index.njk
```

Esperado: saída vazia. A página de Anais não deve ter sido tocada.

- [ ] **Step 6: Commit**

```bash
git add eventos/caminhos-do-contemporaneo/2026/programacao/index.njk eventos/caminhos-do-contemporaneo/2026/submissoes/index.njk
git commit -m "Publica o caderno de resumos na Programação e em Submissões"
```

---

## Task 15: Documentar e fechar

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Rodar a suíte inteira**

```bash
python -m unittest discover -s tools -p "test_*.py" -v
```

Esperado: `OK`, com 46 testes (13 do cabeçalho, 11 do pareamento, 22 do caderno).

- [ ] **Step 2: Documentar o fluxo no README**

Acrescente à seção de ferramentas do `README.md`:

```markdown
### Caderno de resumos (`assets/anais/2026/`)

Fluxo em três etapas, todas reproduzíveis:

1. `python tools/corrigir_cabecalho.py ORIGEM DESTINO` — troca a imagem de
   cabeçalho dos PDFs de resumo pelo mestre `assets/graphics/cabecalho-caminhos-2026.png`.
   Cabeçalho e rodapé têm a mesma dimensão (794×113): a distinção é pela posição.
2. `python tools/parear_resumos.py CORRIGIDOS --gravar` — casa cada arquivo com
   sua linha da programação, grava `_data/caderno.json` e copia os PDFs
   numerados para `assets/anais/2026/resumos/`. **A tabela precisa de revisão
   humana antes de gravar.** Depois disso o JSON é a fonte de verdade.
3. `python tools/gerar_caderno.py` — monta o caderno, verifica e grava.

Textos editáveis sem tocar no código: `_data/caderno-expediente.md` e
`_data/caderno-apresentacao.md`. Se o segundo não existir, a seção é omitida.

Pendências deste conjunto: o caderno não tem ISBN (os anais com ISBN saem após
22/10/2026) e `cartaz_caminhos.jpg` e o KV em PDF seguem com a data antiga.
```

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "Documenta o fluxo do caderno de resumos"
```

- [ ] **Step 4: Entregar ao usuário**

Informe que o `push` precisa ser feito por ele, num terminal interativo:

```bash
git push -u origin caderno-resumos
```

Liste o que ficou pendente de conteúdo: a lista de comissões para o expediente e
o texto de apresentação. Basta editar os dois arquivos em `_data/` e rodar
`python tools/gerar_caderno.py` de novo — a paginação e o sumário se reajustam
sozinhos.
