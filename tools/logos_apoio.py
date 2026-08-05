"""Tabela das instituições apoiadoras do 7º Caminhos do Contemporâneo.

Fonte única da verdade: o script de normalização lê ORIGEM daqui e o
gerador de JSON lê NOME daqui. Para acrescentar uma apoiadora, adicione
uma linha em APOIO e rode `python tools/normalizar_logos.py`.
"""

# Diretório com os arquivos brutos, fora do repositório.
PASTA_ORIGEM = r"C:\Users\Windows 10\Downloads\Logos-20260805T212938Z-1-001\Logos"

# slug -> (nome por extenso para o alt, arquivo de origem)
# `arquivo` None significa que a marca não passa pelo pipeline raster
# (usa um SVG já versionado em assets/logos/).
APOIO = {
    "abepem":          ("ABEPEM", None),
    "ufsc":            ("Universidade Federal de Santa Catarina", "ufsc.jfif"),
    "ufrj":            ("Universidade Federal do Rio de Janeiro", "ufrj.png"),
    "ifsc":            ("Instituto Federal de Santa Catarina", "ifsc.png"),
    "uem":             ("Universidade Estadual de Maringá", "uem.png"),
    "feevale":         ("Universidade Feevale", "feevale.jfif"),
    "cesusc":          ("Faculdade CESUSC", "cesusc.png"),
    "uniban":          ("Universidade Bandeirante de São Paulo", "uniban.png"),
    "mackenzie":       ("Universidade Presbiteriana Mackenzie", "mkz.webp"),
    "umontreal":       ("Université de Montréal", "umontreal.webp"),
    "uminho":          ("Universidade do Minho", "uminho.jfif"),
    "lusofona":        ("Universidade Lusófona", "uluso.png"),
    "ibero":           ("Universidad Iberoamericana",
                        "universidad-iberoamericana-ibero-logo-vector.png"),
    "moura-lacerda":   ("Instituição Universitária Moura Lacerda",
                        "logo_centro-universitario-moura-lacerda_F5o24S.png"),
    "belas-artes":     ("Centro Universitário Belas Artes de São Paulo", "ba.png"),
    "faeb":            ("Federação de Arte Educadores do Brasil", "faeb.png"),
    "aaesc":           ("Associação dos Arte Educadores de Santa Catarina", "aaesc.jfif"),
    "amae":            ("AMAE", "logo-amae.webp"),
    "came":            ("Casa dos Açores — Museu Etnográfico", "came.jfif"),
    "iema":            ("Instituto de Educação, Ciência e Tecnologia do Maranhão", "iema.png"),
    "seduc-bc":        ("Secretaria de Educação de Balneário Camboriú", "seduc bc.jfif"),
    "cep-edgar-morin": ("Centro de Estudos e Pesquisas Edgar Morin",
                        "Logo-CEP-EDGAR-MORIN.webp"),
}

# Marcas cuja resolução de origem é insuficiente e que precisam de
# ampliação antes da normalização. Valor = fator de ampliação.
UPSCALE = {
    "amae": 4,
}

# Caminho final de cada marca no site, por slug.
# A ABEPEM aponta para o SVG já versionado.
DESTINO_ESPECIAL = {
    "abepem": "/assets/logos/logo-abepem.svg",
}

REALIZACAO = [
    ("labmaes", "LabMAES", "/assets/logos/logo-labmaes-vermelho.svg"),
    ("udesc-ceart", "UDESC CEART", "/assets/logos/logo-ceart.svg"),
    ("fapesc", "Fapesc", "/assets/logos/logo-fapesc.svg"),
]


def caminho_publico(slug: str) -> str:
    """URL pública da logo de uma apoiadora."""
    if slug in DESTINO_ESPECIAL:
        return DESTINO_ESPECIAL[slug]
    return f"/assets/logos/apoio/{slug}.webp"
