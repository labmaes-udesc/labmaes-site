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
