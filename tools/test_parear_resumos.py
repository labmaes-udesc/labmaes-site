"""Testes do pareamento entre arquivos de resumo e linhas da programação.

    python -m unittest discover -s tools -p "test_*.py" -v
"""
import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import fitz

import parear_resumos as modulo
from parear_resumos import (
    gravar,
    itens_da_programacao,
    montar,
    nome_destino,
    parear,
    pontuar,
    sem_acento,
    tokens,
)


def _pdf_sintetico(caminho, paginas=1):
    """Cria um PDF mínimo válido, para não depender de arquivos reais nos testes."""
    doc = fitz.open()
    for _ in range(paginas):
        doc.new_page()
    doc.save(caminho)
    doc.close()


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


class TestMontar(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.arquivo_programacao = os.path.join(self.tmp, "programacao.json")
        self.pasta_corrigidos = os.path.join(self.tmp, "corrigidos")
        os.makedirs(os.path.join(self.pasta_corrigidos, "CO"))
        os.makedirs(os.path.join(self.pasta_corrigidos, "PO"))
        self._programacao_original = modulo.PROGRAMACAO

    def tearDown(self):
        modulo.PROGRAMACAO = self._programacao_original
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_levanta_erro_claro_quando_falta_arquivo_para_um_item(self):
        programacao = [
            {
                "data": "2026-08-20",
                "atividades": [
                    {
                        "tipo": "Comunicações Orais",
                        "titulo": "Sessão única",
                        "local": "Auditório",
                        "programa": [
                            {"hora": "13h40", "autores": "Felipe Fonseca", "titulo": "Tecendo caminhos"},
                            {"hora": "13h50", "autores": "Angelica Neumaier", "titulo": "Caminhar coletar imprimir"},
                        ],
                    }
                ],
            }
        ]
        with open(self.arquivo_programacao, "w", encoding="utf-8") as saida:
            json.dump(programacao, saida)
        modulo.PROGRAMACAO = self.arquivo_programacao

        # só um arquivo para dois itens — alguém sempre fica sem par.
        _pdf_sintetico(
            os.path.join(self.pasta_corrigidos, "CO", "felipe fonseca - tecendo caminhos.pdf")
        )

        with self.assertRaises(ValueError) as ctx:
            montar(self.pasta_corrigidos)

        mensagem = str(ctx.exception)
        self.assertIn("2", mensagem)
        self.assertIn("Angelica Neumaier", mensagem)
        self.assertIn("Caminhar coletar imprimir", mensagem)


class TestGravar(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.origem = os.path.join(self.tmp, "origem.pdf")
        _pdf_sintetico(self.origem, paginas=2)

        self.raiz = os.path.join(self.tmp, "repo")
        self.destino_resumos = os.path.join(self.raiz, "assets", "anais", "2026", "resumos")
        self.caderno = os.path.join(self.raiz, "_data", "caderno.json")
        os.makedirs(os.path.dirname(self.caderno))

        self.registros = [{
            "ordem": 1,
            "modalidade": "CO",
            "autores": "Felipe Fonseca",
            "titulo": "Tecendo caminhos",
            "origem": "origem.pdf",
            "arquivo": "assets/anais/2026/resumos/01-fonseca-tecendo-caminhos.pdf",
            "paginas": 2,
            "_nota": 1.0,
            "_caminho_origem": self.origem,
        }]

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _grava(self, forcar=False):
        return gravar(
            self.registros,
            forcar=forcar,
            caderno=self.caderno,
            destino_resumos=self.destino_resumos,
            raiz=self.raiz,
        )

    def test_grava_quando_o_caderno_nao_existe(self):
        resultado = self._grava()

        self.assertTrue(resultado)
        self.assertTrue(os.path.exists(self.caderno))
        self.assertTrue(os.path.exists(os.path.join(self.raiz, self.registros[0]["arquivo"])))

    def test_recusa_sobrescrever_caderno_existente(self):
        with open(self.caderno, "w", encoding="utf-8") as saida:
            json.dump({"itens": [{"correcao": "manual"}]}, saida)

        resultado = self._grava()

        self.assertFalse(resultado)
        with open(self.caderno, encoding="utf-8") as entrada:
            self.assertEqual(json.load(entrada), {"itens": [{"correcao": "manual"}]})
        self.assertFalse(os.path.exists(os.path.join(self.raiz, self.registros[0]["arquivo"])))

    def test_forcar_sobrescreve_caderno_existente(self):
        with open(self.caderno, "w", encoding="utf-8") as saida:
            json.dump({"itens": [{"correcao": "manual"}]}, saida)

        resultado = self._grava(forcar=True)

        self.assertTrue(resultado)
        with open(self.caderno, encoding="utf-8") as entrada:
            conteudo = json.load(entrada)
        self.assertEqual(conteudo["itens"][0]["ordem"], 1)

    def test_remove_chaves_internas_do_json_gravado(self):
        self._grava()

        with open(self.caderno, encoding="utf-8") as entrada:
            conteudo = json.load(entrada)

        chaves = conteudo["itens"][0].keys()
        self.assertFalse(any(chave.startswith("_") for chave in chaves))


if __name__ == "__main__":
    unittest.main()
