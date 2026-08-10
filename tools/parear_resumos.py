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


def arquivos_por_modalidade(pasta_corrigidos):
    mapa = {}
    for modalidade in ("PO", "CO"):
        pasta = os.path.join(pasta_corrigidos, modalidade)
        mapa[modalidade] = sorted(
            os.path.join(pasta, nome)
            for nome in os.listdir(pasta)
            if nome.lower().endswith(".pdf")
        )
    return mapa


def montar(pasta_corrigidos):
    import fitz

    programacao = json.load(open(PROGRAMACAO, encoding="utf-8"))
    itens = itens_da_programacao(programacao)
    mapa = arquivos_por_modalidade(pasta_corrigidos)
    escolhido = parear(itens, mapa)

    registros = []
    for indice, item in enumerate(itens):
        arquivo, nota = escolhido[indice]
        doc = fitz.open(arquivo)
        paginas = len(doc)
        doc.close()
        registro = dict(item)
        registro["origem"] = os.path.basename(arquivo)
        registro["arquivo"] = "assets/anais/2026/resumos/" + nome_destino(
            item["ordem"], item["autores"], item["titulo"]
        )
        registro["paginas"] = paginas
        registro["_nota"] = round(nota, 3)
        registro["_caminho_origem"] = arquivo
        registros.append(registro)
    return registros


def imprimir_tabela(registros):
    """Menor confiança primeiro — é onde a revisão humana precisa olhar."""
    print("%-5s %-6s %-4s %-42s %s" % ("NOTA", "MODAL", "ORD", "PROGRAMAÇÃO (autores)", "ARQUIVO"))
    for registro in sorted(registros, key=lambda r: r["_nota"]):
        print("%-5.2f %-6s %-4d %-42s %s" % (
            registro["_nota"],
            registro["modalidade"],
            registro["ordem"],
            registro["autores"][:42],
            registro["origem"],
        ))


def gravar(registros):
    os.makedirs(DESTINO_RESUMOS, exist_ok=True)
    limpos = []
    for registro in registros:
        shutil.copyfile(registro["_caminho_origem"], os.path.join(RAIZ, registro["arquivo"]))
        limpo = {c: registro[c] for c in registro if not c.startswith("_")}
        limpos.append(limpo)
    with open(CADERNO, "w", encoding="utf-8", newline="\n") as saida:
        json.dump({"itens": limpos}, saida, ensure_ascii=False, indent=2)
        saida.write("\n")
    print("gravados %d PDFs em %s" % (len(limpos), os.path.relpath(DESTINO_RESUMOS, RAIZ)))
    print("gravado %s" % os.path.relpath(CADERNO, RAIZ))


def main(argumentos):
    if not argumentos:
        print(__doc__)
        return 2
    registros = montar(argumentos[0])
    imprimir_tabela(registros)
    if "--gravar" in argumentos:
        gravar(registros)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
