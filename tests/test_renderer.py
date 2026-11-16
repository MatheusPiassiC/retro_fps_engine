"""Pixels reais de superfícies, sem depender de janela visível."""

from math import pi

import pygame
import pytest

from retro_fps.camera import Camera
from retro_fps.renderer import (
    CEILING_COLOR,
    FLOOR_COLOR,
    WALL_X_COLOR,
    WALL_Y_COLOR,
    render_scene,
)
from retro_fps.study_world import create_study_world
from retro_fps.world import World


def test_no_hit_preserves_ceiling_and_floor():
    surface = pygame.Surface((8, 10))
    render_scene(surface, World([[0]]), (0.5, 0.5), Camera(0))
    for x in range(8):
        for y in range(10):
            assert surface.get_at((x, y))[:3] == (
                CEILING_COLOR if y < 5 else FLOOR_COLOR
            )


@pytest.mark.parametrize("angle, color", [(0, WALL_X_COLOR), (pi / 2, WALL_Y_COLOR)])
def test_front_wall_height_and_side_color(angle, color):
    # Largura 12, FOV 60: escala 6*sqrt(3). Profundidade 1.5:
    # altura 4*sqrt(3), cerca de 6.928; intervalo [1,9). Os raios centrais
    # atingem a mesma face frontal e devem manter topo/base alinhados.
    surface = pygame.Surface((12, 10))
    render_scene(surface, create_study_world(), (2.5, 2.5), Camera(angle, pi / 3))
    for x in range(2, 10):
        for y in range(10):
            expected = CEILING_COLOR if y < 1 else color if y < 9 else FLOOR_COLOR
            assert surface.get_at((x, y))[:3] == expected


@pytest.mark.parametrize("origin", [(3.999999999, 2.5), (1.0, 2.5)])
def test_near_or_zero_depth_fills_column_without_error(origin):
    surface = pygame.Surface((1, 10))
    angle = 0 if origin[0] > 3 else pi
    render_scene(surface, create_study_world(), origin, Camera(angle))
    for y in range(10):
        assert surface.get_at((0, y))[:3] == WALL_X_COLOR
