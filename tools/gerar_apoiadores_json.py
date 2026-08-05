"""Gera _data/apoiadores.json a partir da tabela em logos_apoio.py."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from logos_apoio import APOIO, REALIZACAO, caminho_publico

raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
destino = os.path.join(raiz, "_data", "apoiadores.json")

dados = {
    "realizacao": [
        {"slug": slug, "nome": nome, "arquivo": arquivo}
        for slug, nome, arquivo in REALIZACAO
    ],
    "apoio": [
        {"slug": slug, "nome": nome, "arquivo": caminho_publico(slug)}
        for slug, (nome, _) in APOIO.items()
    ],
}

with open(destino, "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"{len(dados['realizacao'])} realizadores, {len(dados['apoio'])} apoiadoras")
