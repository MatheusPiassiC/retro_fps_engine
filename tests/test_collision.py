"""Círculos com folgas e distâncias conhecidas, sem janela ou movimento."""

import pytest

from retro_fps.collision import can_occupy
from retro_fps.world import World


@pytest.mark.parametrize(
    "position, expected",
    [((3.7, 2.5), True), ((3.8, 2.5), False), ((3.9, 2.5), False), ((4.5, 2.5), False)],
)
def test_distance_to_wall_face(position, expected):
    world = World([[0, 0, 0, 0, 1] for _ in range(5)])
    assert can_occupy(world, position, 0.2) is expected


@pytest.mark.parametrize(
    "position, expected",
    [((1.7, 1.6), False), ((1.6, 1.6), True), ((1.8, 1.8), False)],
)
def test_distance_to_wall_corner(position, expected):
    world = World(
        [[0] * 5 for _ in range(2)] + [[0, 0, 1, 0, 0]] + [[0] * 5 for _ in range(2)]
    )
    # Canto em (2,2): distâncias 0.5 (triângulo 3-4-5), sqrt(0.32) > 0.5,
    # e sqrt(0.08) < 0.5. A caixa do círculo cruza a célula nos três casos.
    assert can_occupy(world, position, 0.5) is expected


@pytest.mark.parametrize(
    "position", [(0.2, 2), (3.8, 2), (2, 0.2), (2, 3.8), (-1, 2), (5, 2)]
)
def test_open_map_exterior_is_blocked(position):
    assert not can_occupy(World([[0] * 4 for _ in range(4)]), position, 0.2)


def test_free_space_and_large_circle():
    world = World([[0] * 4 for _ in range(4)])
    assert can_occupy(world, (2, 2), 0.2)
    assert not can_occupy(world, (2, 2), 2)


@pytest.mark.parametrize("radius", [0, -0.2, float("nan"), float("inf")])
def test_invalid_radius(radius):
    with pytest.raises(ValueError):
        can_occupy(World([[0]]), (0.5, 0.5), radius)


@pytest.mark.parametrize("position", [(float("nan"), 2), (2, float("inf"))])
def test_invalid_position(position):
    with pytest.raises(ValueError):
        can_occupy(World([[0]]), position, 0.2)


@pytest.mark.parametrize(
    "position, expected",
    [((1.3, 2.5), True), ((1.2, 2.5), False), ((1.1, 2.5), False)],
)
def test_wall_on_negative_side_includes_tangent_cell(position, expected):
    world = World([[1, 0, 0, 0, 0] for _ in range(5)])
    assert can_occupy(world, position, 0.2) is expected
