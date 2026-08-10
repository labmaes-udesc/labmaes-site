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
