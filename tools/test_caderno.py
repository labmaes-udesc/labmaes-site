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
