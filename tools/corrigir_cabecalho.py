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
    """Devolve (xrefs de cabeçalho, xrefs de rodapé, {xref: páginas em que ocorre}).

    Usa `get_image_info(xrefs=True)`, que reporta apenas as imagens
    efetivamente desenhadas no stream de conteúdo da página — ao contrário de
    `get_images(full=True)`, que também lista entradas órfãs do dicionário de
    recursos (por exemplo, sobras deixadas por `Page.replace_image` depois de
    `garbage=4`, que trocam o xref desenhado sem remover o antigo dos
    recursos). Sem esse filtro, um cabeçalho já corrigido pode parecer ter
    dois xrefs distintos quando na verdade só um está de fato na página.
    """
    cabecalho = set()
    rodape = set()
    ocorrencias = {}
    for numero, pagina in enumerate(doc):
        for informacao in pagina.get_image_info(xrefs=True):
            xref = informacao.get("xref")
            largura, altura = informacao.get("width"), informacao.get("height")
            if not xref or (largura, altura) != (LARGURA_CABECALHO, ALTURA_CABECALHO):
                continue
            y0 = informacao["bbox"][1]
            if y0 < Y_MAXIMO_CABECALHO:
                cabecalho.add(xref)
                ocorrencias.setdefault(xref, set()).add(numero)
            elif y0 > Y_MINIMO_RODAPE:
                rodape.add(xref)
    return cabecalho, rodape, ocorrencias


def _resolver_cabecalho_unico(doc, cabecalho):
    """Reduz o conjunto de xrefs candidatos a cabeçalho a um único xref.

    Em alguns resumos reais, o mesmo cabeçalho já vem duplicado em mais de
    um objeto de imagem no PDF original — por exemplo `jessica ana cleia -
    Arte vestível.pdf` guarda o cabeçalho nos xrefs 5 e 44, e `Maria Ivis
    Valdecir - O design têxtil na indústria.pdf` nos xrefs 5 e 72, os dois
    casos com conteúdo de pixels idêntico. O motivo mais provável é que
    esses documentos foram montados juntando páginas de origens diferentes,
    cada uma trazendo sua própria cópia da mesma imagem de cabeçalho. Isso
    faz `classificar_imagens` enxergar xrefs distintos que, pixel a pixel,
    são o mesmo cabeçalho. Só é um cabeçalho "distinto" de verdade quando o
    conteúdo dos pixels difere.
    """
    candidatos = sorted(cabecalho)
    referencia = amostras(doc, candidatos[0])
    for outro in candidatos[1:]:
        if amostras(doc, outro) != referencia:
            raise CabecalhoInvalido(
                "%d imagens distintas de cabeçalho: %s" % (len(cabecalho), candidatos)
            )
    return candidatos[0]


def validar(doc, cabecalho, rodape, ocorrencias):
    """Confere as invariantes e devolve o único xref de cabeçalho.

    Um rodapé de fato presente não é exigido: alguns resumos legítimos não
    têm nenhuma imagem 794x113 no rodapé (`karine daniela silvana -
    upcycling.pdf`) ou têm uma imagem de rodapé com outra resolução, como
    1639x260 (`Beatriz Mara - Narrativas compartilhadas.pdf`) — nenhum dos
    dois casos corre risco de ter o rodapé trocado por engano, porque a
    posição (`Y_MAXIMO_CABECALHO` / `Y_MINIMO_RODAPE`) já separa cabeçalho
    de rodapé, e a checagem abaixo garante que o xref do cabeçalho nunca
    também apareça como rodapé. Exigir um rodapé 794x113 para aceitar o
    documento não protegia nada além disso, e rejeitava esses dois PDFs
    válidos.
    """
    if not cabecalho:
        raise CabecalhoInvalido("nenhuma imagem 794x113 no topo das páginas")
    xref = _resolver_cabecalho_unico(doc, cabecalho)
    paginas_cobertas = set()
    for candidato in cabecalho:
        paginas_cobertas |= ocorrencias.get(candidato, set())
    faltando = sorted(set(range(len(doc))) - paginas_cobertas)
    if faltando:
        raise CabecalhoInvalido("cabeçalho ausente nas páginas %s" % faltando)
    if xref in rodape:
        raise CabecalhoInvalido("o xref %d aparece como cabeçalho e como rodapé" % xref)
    return xref


def amostras(doc, xref):
    """Bytes decodificados da imagem, sem canal alfa."""
    pixmap = fitz.Pixmap(doc, xref)
    if pixmap.alpha:
        pixmap = fitz.Pixmap(pixmap, 0)
    return pixmap.samples


def amostras_do_arquivo(caminho):
    pixmap = fitz.Pixmap(caminho)
    if pixmap.alpha:
        pixmap = fitz.Pixmap(pixmap, 0)
    return pixmap.samples


def corrigir(entrada, saida, mestre):
    """Grava em `saida` uma cópia de `entrada` com o cabeçalho substituído.

    Alguns resumos guardam o cabeçalho como mais de um objeto de imagem
    distinto no PDF original (mesmo conteúdo de pixels, xrefs diferentes) —
    provavelmente porque o documento foi montado juntando páginas de
    origens diferentes, cada uma com sua própria cópia da mesma imagem de
    cabeçalho (ver `_resolver_cabecalho_unico`). `Page.replace_image` só
    altera o objeto identificado pelo xref informado, então é preciso
    repetir a troca para CADA xref candidato a cabeçalho aceito por
    `validar`, não só para o canônico — senão as páginas cujo cabeçalho
    vive num objeto diferente ficam com a data antiga.
    """
    doc = fitz.open(entrada)
    try:
        cabecalho, rodape, ocorrencias = classificar_imagens(doc)
        xref = validar(doc, cabecalho, rodape, ocorrencias)
        for candidato in sorted(cabecalho):
            pagina = next(iter(ocorrencias[candidato]))
            doc[pagina].replace_image(candidato, filename=str(mestre))
        doc.save(str(saida), garbage=4, deflate=True)
    finally:
        doc.close()
    return xref


def conferir(caminho, mestre):
    """Levanta CabecalhoInvalido se o PDF não estiver com o cabeçalho mestre."""
    doc = fitz.open(caminho)
    try:
        xref = validar(doc, *classificar_imagens(doc))
        # amostras precisa do doc aberto: um Pixmap de documento fechado é inválido
        obtido = amostras(doc, xref)
    finally:
        doc.close()
    esperado = amostras_do_arquivo(mestre)
    if obtido != esperado:
        raise CabecalhoInvalido("o cabeçalho de %s não é o mestre" % os.path.basename(caminho))


def corrigir_pasta(origem, destino, mestre):
    """Corrige todos os PDFs de `origem`, preservando os nomes. Devolve (ok, falhas)."""
    os.makedirs(destino, exist_ok=True)
    ok = []
    falhas = []
    for nome in sorted(os.listdir(origem)):
        if not nome.lower().endswith(".pdf"):
            continue
        entrada = os.path.join(origem, nome)
        saida = os.path.join(destino, nome)
        try:
            texto_antes = [pagina.get_text() for pagina in fitz.open(entrada)]
            paginas_antes = len(texto_antes)
            corrigir(entrada, saida, mestre)
            conferir(saida, mestre)
            doc = fitz.open(saida)
            texto_depois = [pagina.get_text() for pagina in doc]
            doc.close()
            if texto_depois != texto_antes:
                raise CabecalhoInvalido("o texto extraído mudou")
            if len(texto_depois) != paginas_antes:
                raise CabecalhoInvalido("a contagem de páginas mudou")
            ok.append(nome)
            doc_saida = fitz.open(saida)
            _, rodape_saida, _ = classificar_imagens(doc_saida)
            doc_saida.close()
            if not rodape_saida:
                print("OK (sem rodapé) %s" % nome)
            else:
                print("OK      %s" % nome)
        except CabecalhoInvalido as erro:
            if os.path.exists(saida):
                os.remove(saida)
            falhas.append((nome, str(erro)))
            print("FALHOU  %s — %s" % (nome, erro))
    return ok, falhas


def main(argumentos):
    if len(argumentos) != 2:
        print(__doc__)
        return 2
    origem, destino = argumentos
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mestre = os.path.join(raiz, "assets", "graphics", "cabecalho-caminhos-2026.png")
    ok, falhas = corrigir_pasta(origem, destino, mestre)
    print("\n%d corrigidos, %d falhas" % (len(ok), len(falhas)))
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
