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
