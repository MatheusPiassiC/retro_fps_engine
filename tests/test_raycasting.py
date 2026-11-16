"""Resultados calculados por fronteiras da grade, antes do DDA."""

import pytest

from retro_fps.raycasting import cast_ray
from retro_fps.study_world import create_study_world
from retro_fps.world import World


@pytest.mark.parametrize(
    "direction, cell, side, parameter",
    [
        ((1, 0), (4, 2), "x", 1.5),
        ((-1, 0), (0, 2), "x", 1.5),
        ((0, 1), (2, 4), "y", 1.5),
        ((0, -1), (2, 0), "y", 1.5),
        ((2, 0), (4, 2), "x", 0.75),
        ((1, 0.5), (4, 3), "x", 1.5),
    ],
)
def test_known_room_hits(direction, cell, side, parameter):
    # Leste: x=4; oeste: x=1; sul: y=4; norte: y=1.
    # Em (1, 0.5), x=4 implica t=1.5 e y=3.25, portanto linha 3.
    hit = cast_ray(create_study_world(), (2.5, 2.5), direction)
    assert hit is not None
    assert (hit.cell_x, hit.cell_y) == cell
    assert hit.side == side
    assert hit.parameter == pytest.approx(parameter, rel=1e-12, abs=1e-12)


@pytest.mark.parametrize("direction", [(1, 0), (-1, 0), (0, 1), (0, -1)])
def test_open_world_has_no_wall_at_its_limits(direction):
    world = World([[0, 0, 0], [0, 0, 0]])
    assert cast_ray(world, (1.5, 0.5), direction) is None


def test_internal_wall_is_hit_before_outer_border():
    # A parede interna começa em x=2, a 0.5 unidade da origem.
    world = World([[1, 1, 1, 1, 1], [1, 0, 1, 0, 1], [1, 1, 1, 1, 1]])
    hit = cast_ray(world, (1.5, 1.5), (1, 0))
    assert hit is not None
    assert (hit.cell_x, hit.cell_y, hit.side) == (2, 1, "x")
    assert hit.parameter == pytest.approx(0.5, abs=1e-12)


@pytest.mark.parametrize(
    "origin, direction, cell, side, parameter",
    [
        ((1.0, 2.5), (-1, 0), (0, 2), "x", 0.0),
        ((2.5, 1.0), (0, -1), (2, 0), "y", 0.0),
        ((1.0, 2.5), (1, 0), (4, 2), "x", 3.0),
    ],
)
def test_origin_on_cell_boundary(origin, direction, cell, side, parameter):
    hit = cast_ray(create_study_world(), origin, direction)
    assert hit is not None
    assert (hit.cell_x, hit.cell_y) == cell
    assert hit.side == side
    assert hit.parameter == pytest.approx(parameter, rel=1e-12, abs=1e-12)


@pytest.mark.parametrize(
    "origin, direction",
    [
        ((2.5, 2.5), (0, 0)),
        ((-0.1, 2.5), (1, 0)),
        ((5.0, 2.5), (-1, 0)),
        ((2.5, -0.1), (0, 1)),
        ((2.5, 5.0), (0, -1)),
        ((0.5, 2.5), (1, 0)),
    ]
    + [
        (origin, direction)
        for value in (float("nan"), float("inf"), -float("inf"))
        for origin, direction in (
            ((value, 2.5), (1, 0)),
            ((2.5, value), (1, 0)),
            ((2.5, 2.5), (value, 0)),
            ((2.5, 2.5), (1, value)),
        )
    ],
)
def test_invalid_ray_is_rejected(origin, direction):
    with pytest.raises(ValueError):
        cast_ray(create_study_world(), origin, direction)
