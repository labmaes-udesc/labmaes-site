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
    amostras,
    amostras_do_arquivo,
    classificar_imagens,
    conferir,
    corrigir,
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

    def test_aceita_documento_sem_rodape(self):
        # Alguns resumos reais (ex.: karine daniela silvana - upcycling.pdf) não
        # têm nenhuma imagem 794x113 no rodapé. Isso não é motivo para recusar
        # o documento: a posição já separa cabeçalho de rodapé, então a
        # ausência de rodapé não cria risco de trocar a imagem errada.
        doc = pdf_sintetico(paginas=2, rodape=False)

        xref = validar(doc, *classificar_imagens(doc))

        self.assertIn(xref, classificar_imagens(doc)[0])

    def test_recusa_cabecalho_que_tambem_aparece_como_rodape(self):
        # A imagem do cabeçalho não pode também estar desenhada na posição de
        # rodapé — essa é a checagem que efetivamente protege o rodapé de ser
        # trocado por engano, já que não exigimos mais que o rodapé exista.
        doc = fitz.open()
        pagina = doc.new_page(width=LARGURA_PAGINA, height=ALTURA_PAGINA)
        imagem = png_solido((10, 20, 30))
        pagina.insert_image(fitz.Rect(1.3, 0.7, 596.3, 85.3), stream=imagem)
        pagina.insert_image(fitz.Rect(0, 769, 595, 842), stream=imagem)

        with self.assertRaises(CabecalhoInvalido) as erro:
            validar(doc, *classificar_imagens(doc))

        self.assertIn("rodapé", str(erro.exception))


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
        entrada = self._gravar(pdf_sintetico(paginas=2, pular_cabecalho_em=(1,)))
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


if __name__ == "__main__":
    unittest.main()
