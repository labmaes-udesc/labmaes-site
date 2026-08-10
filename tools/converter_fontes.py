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
