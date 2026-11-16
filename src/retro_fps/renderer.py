"""Desenho de paredes coloridas numa superfície Pygame."""

import pygame

from retro_fps.camera import Camera
from retro_fps.projection import projected_wall_height, wall_span
from retro_fps.raycasting import cast_ray
from retro_fps.world import World

CEILING_COLOR = (40, 80, 120)
FLOOR_COLOR = (70, 60, 50)
WALL_X_COLOR = (190, 150, 90)
WALL_Y_COLOR = (133, 105, 63)


def render_scene(
    surface: pygame.Surface,
    world: World,
    origin: tuple[float, float],
    camera: Camera,
) -> None:
    """Desenhe a cena sem alterar mundo, origem ou câmera.

    Colunas sem impacto preservam teto e piso. A tonalidade distingue
    orientação de faces; não simula iluminação física.
    """
    width, height = surface.get_size()
    surface.fill(CEILING_COLOR)
    surface.fill(FLOOR_COLOR, (0, height // 2, width, height - height // 2))
    for column in range(width):
        hit = cast_ray(world, origin, camera.ray_direction(column, width))
        if hit is None:
            continue
        projected_height = projected_wall_height(
            hit.parameter, width, camera.field_of_view
        )
        top, bottom = wall_span(projected_height, height)
        color = WALL_X_COLOR if hit.side == "x" else WALL_Y_COLOR
        surface.fill(color, (column, top, 1, bottom - top))
