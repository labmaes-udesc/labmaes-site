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
