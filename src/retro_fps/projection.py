"""Projeção de paredes de altura 1 e recorte vertical, sem Pygame."""

from math import ceil, floor, isfinite, pi, tan

MIN_DEPTH = 0.000001


def projected_wall_height(depth: float, width: int, field_of_view: float) -> float:
    """Converta profundidade frontal em altura em pixels, antes do recorte.

    O campo de visão horizontal usa radianos. A direção do raio deve seguir
    a convenção da câmera: não aplicar uma correção adicional por cosseno.
    Profundidades menores que MIN_DEPTH são limitadas a esse mínimo.
    """
    if type(width) is not int:
        raise TypeError("A largura interna deve ser inteira.")
    if width <= 0:
        raise ValueError("A largura interna deve ser positiva.")
    if not isfinite(depth) or depth < 0:
        raise ValueError("A profundidade deve ser finita e não negativa.")
    if not isfinite(field_of_view) or not 0 < field_of_view < pi:
        raise ValueError("O campo de visão deve estar entre 0 e pi radianos.")

    scale = width / (2 * tan(field_of_view / 2))
    return scale / max(depth, MIN_DEPTH)


def wall_span(projected_height: float, height: int) -> tuple[int, int]:
    """Retorne [top, bottom), centralizado e limitado à altura da imagem.

    Topo arredonda para baixo e base para cima. Altura zero produz um
    intervalo vazio; paredes que cobrem a imagem são recortadas antes
    de converter seus limites em inteiros.
    """
    if type(height) is not int:
        raise TypeError("A altura interna deve ser inteira.")
    if height <= 0:
        raise ValueError("A altura interna deve ser positiva.")
    if not isfinite(projected_height) or projected_height < 0:
        raise ValueError("A altura projetada deve ser finita e não negativa.")
    if projected_height == 0:
        return height // 2, height // 2
    if projected_height >= height:
        return 0, height

    return floor((height - projected_height) / 2), ceil((height + projected_height) / 2)
