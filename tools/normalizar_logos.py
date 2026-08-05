"""Normalização óptica das logos de apoiadoras.

Recorte, remoção de fundo, escala por área de tinta e caixa uniforme.
Nenhuma etapa distorce marca: só recorte, escala proporcional e margem
transparente. Proporções e cores permanecem intactas.
"""
from PIL import Image, ImageChops

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
