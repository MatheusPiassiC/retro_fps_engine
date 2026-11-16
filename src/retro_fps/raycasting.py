"""Percurso DDA e impactos em grade, sem dependência gráfica."""

from dataclasses import dataclass
from math import floor, inf, isfinite
from typing import Literal

from retro_fps.world import World


@dataclass(frozen=True)
class RayHit:
    """Entrada em parede: célula, eixo da fronteira e parâmetro do raio.

    ``side='x'`` indica fronteira vertical; ``side='y'``, horizontal.
    O ponto atingido é ``origin + parameter * direction``. O parâmetro
    não é necessariamente uma distância: a direção não é normalizada.
    """

    cell_x: int
    cell_y: int
    side: Literal["x", "y"]
    parameter: float


def cast_ray(
    world: World,
    origin: tuple[float, float],
    direction: tuple[float, float],
) -> RayHit | None:
    """Percorra células até entrar em parede ou sair da grade (None).

    Origem e direção devem ser finitas; a origem deve estar em célula
    livre e a direção não pode ser nula. Violações causam ValueError.
    Em fronteiras, a célula inicial é definida pelo piso matemático.
    Em empate exato de cruzamentos, o eixo x é consultado primeiro.
    """
    origin_x, origin_y = origin
    direction_x, direction_y = direction
    if not all(isfinite(value) for value in (*origin, *direction)):
        raise ValueError("Origem e direção devem ter coordenadas finitas.")
    if direction_x == 0 and direction_y == 0:
        raise ValueError("A direção do raio não pode ser nula.")

    cell_x, cell_y = floor(origin_x), floor(origin_y)
    if not world.contains(cell_x, cell_y) or world.is_solid(cell_x, cell_y):
        raise ValueError("A origem do raio deve estar em uma célula livre da grade.")

    # Cada delta é o avanço em t necessário para cruzar uma célula inteira.
    # Eixos sem movimento nunca devem vencer a comparação de fronteiras.
    step_x = 1 if direction_x > 0 else -1
    step_y = 1 if direction_y > 0 else -1
    delta_x = abs(1 / direction_x) if direction_x != 0 else inf
    delta_y = abs(1 / direction_y) if direction_y != 0 else inf

    if direction_x > 0:
        next_x = (cell_x + 1 - origin_x) / direction_x
    elif direction_x < 0:
        next_x = (cell_x - origin_x) / direction_x
    else:
        next_x = inf

    if direction_y > 0:
        next_y = (cell_y + 1 - origin_y) / direction_y
    elif direction_y < 0:
        next_y = (cell_y - origin_y) / direction_y
    else:
        next_y = inf

    while True:
        if next_x <= next_y:
            parameter = next_x
            cell_x += step_x
            next_x += delta_x
            side = "x"
        else:
            parameter = next_y
            cell_y += step_y
            next_y += delta_y
            side = "y"

        # O exterior não representa uma parede real, mesmo sendo sólido
        # para a consulta que será usada por colisões.
        if not world.contains(cell_x, cell_y):
            return None
        if world.is_solid(cell_x, cell_y):
            return RayHit(cell_x, cell_y, side, parameter)
