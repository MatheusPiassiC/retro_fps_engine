"""Consulta do espaço ocupado pelo círculo, sem dependência gráfica."""

from math import floor, hypot, isclose, isfinite

from retro_fps.world import World


def can_occupy(world: World, position: tuple[float, float], radius: float) -> bool:
    """Informe se o círculo cabe sem tocar paredes ou limites da grade.

    Raio e coordenadas devem ser finitos; o raio deve ser positivo.
    Uma tolerância relativa de 1e-12 na distância considera contato os
    arredondamentos próximos da tangência, de forma conservadora.
    Esta consulta de destino não verifica o caminho até a posição.
    """
    x, y = position
    if not all(isfinite(value) for value in (x, y, radius)) or radius <= 0:
        raise ValueError("Coordenadas devem ser finitas e o raio finito e positivo.")
    if (
        x - radius <= 0
        or y - radius <= 0
        or x + radius >= world.width
        or y + radius >= world.height
    ):
        return False

    # Inclua a célula anterior à borda mínima: ela pode tocar a caixa
    # exatamente pela sua face direita/inferior, inclusive após arredondamento.
    for cell_y in range(floor(y - radius) - 1, floor(y + radius) + 1):
        for cell_x in range(floor(x - radius) - 1, floor(x + radius) + 1):
            if not world.is_solid(cell_x, cell_y):
                continue
            nearest_x = min(max(x, cell_x), cell_x + 1)
            nearest_y = min(max(y, cell_y), cell_y + 1)
            distance = hypot(x - nearest_x, y - nearest_y)
            if distance <= radius or isclose(distance, radius, rel_tol=1e-12):
                return False
    return True
