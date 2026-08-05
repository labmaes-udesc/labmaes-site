"""Testes das funções puras de normalização de logos.

Roda com a biblioteca padrão:
    python -m unittest discover -s tools -p "test_*.py" -v
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image, ImageDraw

from normalizar_logos import (
    caixa_de_tinta,
    remover_fundo,
    dimensoes_por_area,
    AREA_ALVO,
    ALTURA_MAX,
    LARGURA_MAX,
)


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


if __name__ == "__main__":
    unittest.main()
