"""M2-6: compare imagens e impactos com contas das geometrias desenhadas."""

import pygame
import pytest

from retro_fps.camera import Camera
from retro_fps.projection import projected_wall_height
from retro_fps.raycasting import cast_ray
from retro_fps.renderer import (
    CEILING_COLOR,
    FLOOR_COLOR,
    WALL_X_COLOR,
    WALL_Y_COLOR,
    render_scene,
)
from retro_fps.study_world import create_study_corridor, create_study_world


def test_corridor_geometry_matches_drawing():
    world = create_study_corridor()
    assert (world.width, world.height) == (9, 5)
    for y in range(5):
        for x in range(9):
            assert world.cell_at(x, y) == (1 if x in (0, 8) or y in (0, 4) else 0)


def test_room_front_wall_is_flat_across_entire_image():
    # 11111  Origem (2.5,2.5), parede frontal em x=4: profundidade 1.5.
    # 10001  Com FOV 60, todos os raios atingem essa face, pois o maior
    # 10001  desvio lateral até a face é menor que 1.5 (meia sala).
    # 10001  Largura 32: altura=16*sqrt(3)/1.5, cerca de 18.475.
    # 11111  Imagem 32x24: intervalo [2,22), igual em todas as colunas.
    surface = pygame.Surface((32, 24))
    render_scene(surface, create_study_world(), (2.5, 2.5), Camera(0))
    for x in range(32):
        for y in range(24):
            expected = (
                CEILING_COLOR if y < 2 else WALL_X_COLOR if y < 22 else FLOOR_COLOR
            )
            assert surface.get_at((x, y))[:3] == expected


@pytest.mark.parametrize("column", [15, 16])
def test_halving_corridor_depth_doubles_unrounded_height(column):
    # 111111111  Face frontal em x=8. Origens 2.5 e 5.25:
    # 100000001  profundidades 5.5 e 2.75. O raio central de cada lado
    # 100000001  continua atingindo a face x em ambas as posições.
    # 100000001  Escala 16*sqrt(3): alturas cerca de 5.039 e 10.077.
    # 111111111
    world = create_study_corridor()
    camera = Camera(0)
    direction = camera.ray_direction(column, 32)
    heights = []
    for origin_x, expected_depth in ((2.5, 5.5), (5.25, 2.75)):
        hit = cast_ray(world, (origin_x, 2.5), direction)
        assert hit is not None
        assert (hit.cell_x, hit.cell_y, hit.side) == (8, 2, "x")
        assert hit.parameter == pytest.approx(expected_depth, rel=1e-12, abs=1e-12)
        heights.append(projected_wall_height(hit.parameter, 32, camera.field_of_view))
    assert heights[1] == pytest.approx(2 * heights[0], rel=1e-12, abs=1e-12)


@pytest.mark.parametrize("origin_x, top, bottom", [(2.5, 9, 15), (5.25, 6, 18)])
def test_corridor_front_wall_pixels_match_calculated_heights(origin_x, top, bottom):
    # Alturas não inteiras acima: recorte central produz [9,15) e [6,18).
    surface = pygame.Surface((32, 24))
    render_scene(surface, create_study_corridor(), (origin_x, 2.5), Camera(0))
    for x in (15, 16):
        for y in range(24):
            expected = (
                CEILING_COLOR
                if y < top
                else WALL_X_COLOR
                if y < bottom
                else FLOOR_COLOR
            )
            assert surface.get_at((x, y))[:3] == expected


def test_corridor_sides_are_taller_and_darker_than_distant_front():
    # Na coluna 0, u=-31/32. Para atingir y=1, t=1.5/(31/32*tan(30)).
    # A altura se simplifica para 16*(31/32)/1.5 = 31/3,
    # cerca de 10.333: intervalo [6,18), maior que o fundo [9,15).
    surface = pygame.Surface((32, 24))
    render_scene(surface, create_study_corridor(), (2.5, 2.5), Camera(0))
    for x in (0, 31):
        for y in range(24):
            expected = (
                CEILING_COLOR if y < 6 else WALL_Y_COLOR if y < 18 else FLOOR_COLOR
            )
            assert surface.get_at((x, y))[:3] == expected
    assert surface.get_at((15, 7))[:3] == CEILING_COLOR
    assert surface.get_at((15, 12))[:3] == WALL_X_COLOR


def test_corridor_near_front_wall_is_clipped_without_error():
    surface = pygame.Surface((32, 24))
    render_scene(surface, create_study_corridor(), (7.9999999, 2.5), Camera(0))
    for x in range(32):
        for y in range(24):
            assert surface.get_at((x, y))[:3] == WALL_X_COLOR
