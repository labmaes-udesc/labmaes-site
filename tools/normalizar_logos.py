"""Normalização óptica das logos de apoiadoras.

Recorte, remoção de fundo, escala por área de tinta e caixa uniforme.
Nenhuma etapa distorce marca: só recorte, escala proporcional e margem
transparente. Proporções e cores permanecem intactas.
"""
import math

from PIL import Image, ImageChops, ImageDraw, ImageFilter

# Limiar de "quase branco" para detectar fundo em imagens sem alfa.
LIMIAR_BRANCO = 18


def caixa_de_tinta(im: Image.Image) -> tuple:
    """Caixa delimitadora do desenho, descartando a moldura de fundo.

    Com canal alfa, o fundo é o transparente. Sem alfa, o fundo é o branco.
    Retorna (esquerda, topo, direita, base) no formato do PIL.
    """
    tem_alfa = im.mode in ("RGBA", "LA") or "transparency" in im.info
    if tem_alfa:
        mascara = im.convert("RGBA").getchannel("A")
        mascara = mascara.point(lambda v: 255 if v > 8 else 0)
    else:
        rgb = im.convert("RGB")
        branco = Image.new("RGB", rgb.size, (255, 255, 255))
        diferenca = ImageChops.difference(rgb, branco).convert("L")
        mascara = diferenca.point(lambda v: 255 if v > LIMIAR_BRANCO else 0)

    caixa = mascara.getbbox()
    return caixa if caixa else (0, 0, im.size[0], im.size[1])


# Cor sentinela usada no preenchimento por inundação. Improvável em logo.
SENTINELA = (255, 0, 254)
# Tolerância do preenchimento: absorve o degradê de compressão JPEG.
TOLERANCIA_FLOOD = 40


def remover_fundo(im: Image.Image) -> Image.Image:
    """Transforma o fundo em transparência, preservando o branco interno.

    O fundo é definido como a região conectada às bordas da imagem — não
    como "todo pixel branco". É essa distinção que impede que o miolo
    branco de um brasão vire buraco.

    Imagens que já trazem canal alfa são devolvidas como estão: o
    fornecedor já resolveu o recorte.
    """
    if im.mode in ("RGBA", "LA") or "transparency" in im.info:
        return im.convert("RGBA")

    rgb = im.convert("RGB")
    largura, altura = rgb.size

    inundada = rgb.copy()
    for ponto in [(0, 0), (largura - 1, 0), (0, altura - 1), (largura - 1, altura - 1)]:
        ImageDraw.floodfill(inundada, ponto, SENTINELA, thresh=TOLERANCIA_FLOOD)

    # Máscara do primeiro plano: 255 onde NÃO foi inundado.
    canais = inundada.split()
    igual_sentinela = Image.new("L", rgb.size, 0)
    for canal, valor in zip(canais, SENTINELA):
        proximo = canal.point(lambda v, alvo=valor: 255 if abs(v - alvo) < 8 else 0)
        igual_sentinela = ImageChops.lighter(igual_sentinela, ImageChops.invert(proximo))
    frente = igual_sentinela

    # Come 1px do contorno para eliminar o halo de compressão JPEG, e
    # suaviza a borda para o reescalonamento posterior não serrilhar.
    frente = frente.filter(ImageFilter.MinFilter(3))
    frente = frente.filter(ImageFilter.GaussianBlur(0.6))

    saida = rgb.convert("RGBA")
    saida.putalpha(frente)
    return saida


# Área de tinta alvo, em px² a 1x. Calibrada para que uma marca de
# proporção 2:1 chegue a 44 px de altura.
AREA_ALVO = 3872
ALTURA_MAX = 44
LARGURA_MAX = 150


def dimensoes_por_area(largura_tinta: int, altura_tinta: int) -> tuple:
    """Dimensões de destino que igualam a área de tinta entre marcas.

    Escala pela raiz da razão entre a área atual e a área alvo, e depois
    aplica os tetos de altura e largura. Na prática marcas quadradas e
    verticais batem no teto de altura — correto, porque um selo denso de
    44x44 já pesa mais no olho que um letreiro fino da mesma área.

    A proporção original é sempre preservada.
    """
    proporcao = largura_tinta / altura_tinta

    altura = math.sqrt(AREA_ALVO / proporcao)
    largura = altura * proporcao

    if altura > ALTURA_MAX:
        largura *= ALTURA_MAX / altura
        altura = ALTURA_MAX
    if largura > LARGURA_MAX:
        altura *= LARGURA_MAX / largura
        largura = LARGURA_MAX

    return max(1, round(largura)), max(1, round(altura))


# Fator de densidade da saída: 2x para telas retina.
ESCALA = 2
# Caixa uniforme de todos os arquivos gerados, em px reais.
CAIXA = (LARGURA_MAX * ESCALA, ALTURA_MAX * ESCALA)


def normalizar(im: Image.Image, upscale: int = 1) -> Image.Image:
    """Pipeline completo: recorte, alfa, escala por área e caixa uniforme.

    `upscale` amplia a origem antes de tudo, para marcas cuja resolução
    de partida é insuficiente. Use com parcimônia e confira o resultado
    a olho: ampliação não cria detalhe que não existe.
    """
    if upscale > 1:
        im = im.resize(
            (im.size[0] * upscale, im.size[1] * upscale), Image.LANCZOS
        )

    sem_fundo = remover_fundo(im)
    recortada = sem_fundo.crop(caixa_de_tinta(sem_fundo))

    largura, altura = dimensoes_por_area(recortada.size[0], recortada.size[1])
    redimensionada = recortada.resize(
        (largura * ESCALA, altura * ESCALA), Image.LANCZOS
    )

    tela = Image.new("RGBA", CAIXA, (0, 0, 0, 0))
    tela.paste(
        redimensionada,
        (
            (CAIXA[0] - redimensionada.size[0]) // 2,
            (CAIXA[1] - redimensionada.size[1]) // 2,
        ),
    )
    return tela


def main():
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from logos_apoio import APOIO, PASTA_ORIGEM, UPSCALE

    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    destino = os.path.join(raiz, "assets", "logos", "apoio")
    os.makedirs(destino, exist_ok=True)

    gerados = 0
    for slug, (nome, arquivo) in APOIO.items():
        if arquivo is None:
            print(f"  pulando {slug:<16} (usa SVG versionado)")
            continue

        origem = os.path.join(PASTA_ORIGEM, arquivo)
        saida = normalizar(Image.open(origem), upscale=UPSCALE.get(slug, 1))
        caminho = os.path.join(destino, f"{slug}.webp")
        saida.save(caminho, "WEBP", quality=92, method=6)

        peso = os.path.getsize(caminho) // 1024
        marca = " [UPSCALE]" if slug in UPSCALE else ""
        print(f"  {slug:<16} {saida.size[0]}x{saida.size[1]}  {peso:>3} KB{marca}")
        gerados += 1

    print(f"\n{gerados} arquivos gravados em assets/logos/apoio/")


if __name__ == "__main__":
    main()
