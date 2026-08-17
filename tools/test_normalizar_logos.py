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
    normalizar,
    AREA_ALVO,
    ALTURA_MAX,
    LARGURA_MAX,
    CAIXA,
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

    def test_traco_fino_escuro_sobrevive(self):
        """Regressão: a erosão do halo apagava texto fino de 1px.

        Um traço de 1 px em cinza médio é o que sobra de uma letra de
        texto secundário num original de ~150 px.
        """
        im = Image.new("RGB", (100, 100), (255, 255, 255))
        ImageDraw.Draw(im).line([(10, 50), (89, 50)], fill=(150, 150, 150), width=1)

        saida = remover_fundo(im)

        self.assertGreater(saida.getpixel((50, 50))[3], 128)

    def test_cinza_claro_nao_e_absorvido_pelo_fundo(self):
        """Regressão: tolerância 40 no floodfill engolia cinza-claro.

        O floodfill do PIL compara pela SOMA das diferenças por canal
        contra o pixel semente. (245,245,245) soma 30: passava com
        tolerância 40 e é barrado com 16.
        """
        im = Image.new("RGB", (100, 100), (255, 255, 255))
        ImageDraw.Draw(im).rectangle([40, 40, 59, 59], fill=(245, 245, 245))

        saida = remover_fundo(im)

        self.assertGreater(saida.getpixel((50, 50))[3], 128)

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


if __name__ == "__main__":
    unittest.main()
