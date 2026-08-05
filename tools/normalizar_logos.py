"""Normalização óptica das logos de apoiadoras.

Recorte, remoção de fundo, escala por área de tinta e caixa uniforme.
Nenhuma etapa distorce marca: só recorte, escala proporcional e margem
transparente. Proporções e cores permanecem intactas.
"""
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
