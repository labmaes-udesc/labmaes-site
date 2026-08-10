"""Casa cada PDF de resumo com sua linha da programação e grava _data/caderno.json.

A heurística roda UMA vez, é revisada por gente e o resultado aprovado vira fonte
de verdade. Depois disso o gerador do caderno lê o JSON, nunca a heurística.

Uso (a partir da raiz do repositório):
    python tools/parear_resumos.py CORRIGIDOS         # só mostra a tabela
    python tools/parear_resumos.py CORRIGIDOS --gravar  # grava JSON e copia PDFs

Testes:
    python -m unittest discover -s tools -p "test_*.py" -v
"""
import json
import os
import re
import shutil
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROGRAMACAO = os.path.join(RAIZ, "_data", "programacao.json")
CADERNO = os.path.join(RAIZ, "_data", "caderno.json")
DESTINO_RESUMOS = os.path.join(RAIZ, "assets", "anais", "2026", "resumos")

PALAVRAS_VAZIAS = {
    "de", "da", "do", "das", "dos", "para", "com", "sem", "por", "em", "na", "no",
    "nas", "nos", "que", "uma", "uns", "umas", "ao", "aos", "sobre", "entre",
}
TRATAMENTOS = {"dr", "dra", "prof", "profa", "me", "ms", "msc", "phd"}


def sem_acento(texto):
    decomposto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in decomposto if not unicodedata.combining(c))


def tokens(texto):
    palavras = re.findall(r"[a-z0-9]+", sem_acento(texto).lower())
    return {p for p in palavras if len(p) >= 3 and p not in PALAVRAS_VAZIAS}


def pontuar(nome_arquivo, autores, titulo):
    """0 a 1. Metade do peso para a autoria, metade para o título."""
    base = os.path.splitext(os.path.basename(nome_arquivo))[0]
    esquerda, separador, direita = base.partition(" - ")
    if not separador:
        esquerda, direita = base, base
    tokens_esquerda, tokens_direita = tokens(esquerda), tokens(direita)
    nota_autores = (
        len(tokens_esquerda & tokens(autores)) / len(tokens_esquerda) if tokens_esquerda else 0.0
    )
    nota_titulo = (
        len(tokens_direita & tokens(titulo)) / len(tokens_direita) if tokens_direita else 0.0
    )
    return 0.5 * nota_autores + 0.5 * nota_titulo


def parear(itens, arquivos_por_modalidade):
    """Atribuição gulosa global. Devolve {índice do item: (arquivo, nota)}."""
    candidatos = []
    for indice, item in enumerate(itens):
        for arquivo in arquivos_por_modalidade.get(item["modalidade"], []):
            candidatos.append((pontuar(arquivo, item["autores"], item["titulo"]), indice, arquivo))
    candidatos.sort(key=lambda t: (-t[0], t[1], t[2]))
    escolhido = {}
    usados = set()
    for nota, indice, arquivo in candidatos:
        if indice in escolhido or arquivo in usados:
            continue
        escolhido[indice] = (arquivo, nota)
        usados.add(arquivo)
    return escolhido


def _slug(texto, limite):
    palavras = [
        p for p in re.findall(r"[a-z0-9]+", sem_acento(texto).lower())
        if len(p) >= 3 and p not in PALAVRAS_VAZIAS
    ]
    return "-".join(palavras[:limite])


def nome_destino(ordem, autores, titulo):
    primeiro = autores.split(";")[0]
    partes = [
        p for p in re.findall(r"[A-Za-zÀ-ÿ']+", primeiro)
        if sem_acento(p).lower().strip(".") not in TRATAMENTOS
    ]
    # Sant'Anna vira "santanna", não "sant": o apóstrofo não parte o sobrenome.
    sobrenome = _slug(partes[-1].replace("'", ""), 1) if partes else "autoria"
    return "%02d-%s-%s.pdf" % (ordem, sobrenome, _slug(titulo, 4))


def itens_da_programacao(programacao):
    """Achata o campo `programa` das atividades, em ordem cronológica."""
    itens = []
    ordem = 0
    for dia in programacao:
        for atividade in dia["atividades"]:
            blocos = atividade.get("paralelas") or [atividade]
            for bloco in blocos:
                for trabalho in bloco.get("programa") or []:
                    ordem += 1
                    itens.append({
                        "ordem": ordem,
                        "sessao": bloco.get("titulo", ""),
                        "modalidade": "PO" if "Pôster" in bloco.get("tipo", "") else "CO",
                        "data": dia.get("data", ""),
                        "hora": trabalho.get("hora", ""),
                        "local": bloco.get("local", ""),
                        "autores": trabalho["autores"],
                        "titulo": trabalho["titulo"],
                    })
    return itens
