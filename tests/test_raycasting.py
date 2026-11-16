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


@pytest.mark.parametrize(
    "direction, cell",
    [((1, 1), (4, 3)), ((-1, 1), (0, 3)), ((1, -1), (4, 1)), ((-1, -1), (0, 1))],
)
def test_exact_corner_prioritizes_x_in_each_quadrant(direction, cell):
    # Em t=0.5 atravessa um canto interno; em t=1.5 entra na borda.
    hit = cast_ray(create_study_world(), (2.5, 2.5), direction)
    assert hit is not None
    assert (hit.cell_x, hit.cell_y) == cell
    assert hit.side == "x"
    assert hit.parameter == pytest.approx(1.5, abs=1e-12)


def test_corner_hits_first_lateral_wall():
    # 010   O raio toca (1, 1) em t=0.5. Consulta (1, 0) primeiro.
    # 000
    # 000
    world = World([[0, 1, 0], [0, 0, 0], [0, 0, 0]])
    hit = cast_ray(world, (0.5, 0.5), (1, 1))
    assert hit is not None
    assert (hit.cell_x, hit.cell_y, hit.side) == (1, 0, "x")
    assert hit.parameter == pytest.approx(0.5, abs=1e-12)


def test_corner_hits_diagonal_wall_after_free_x_step():
    # 000   Após consultar (1, 0), entra em (1, 1) por y no mesmo t.
    # 010
    # 000
    world = World([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    hit = cast_ray(world, (0.5, 0.5), (1, 1))
    assert hit is not None
    assert (hit.cell_x, hit.cell_y, hit.side) == (1, 1, "y")
    assert hit.parameter == pytest.approx(0.5, abs=1e-12)


def test_corner_does_not_visit_other_lateral_cell():
    # 000   (0, 1) é apenas tocada: a política visita (1, 0) e (1, 1).
    # 100   Sem outra parede, o raio sai da grade.
    # 000
    world = World([[0, 0, 0], [1, 0, 0], [0, 0, 0]])
    assert cast_ray(world, (0.5, 0.5), (1, 1)) is None


@pytest.mark.parametrize(
    "direction, cell, side, parameter",
    [
        ((1, 1 + 1e-10), (3, 4), "y", 1.5 / (1 + 1e-10)),
        ((1, 1 - 1e-10), (4, 3), "x", 1.5),
    ],
)
def test_near_corner_is_not_treated_as_exact_tie(direction, cell, side, parameter):
    # y ligeiramente mais rápido alcança a borda inferior antes da direita.
    hit = cast_ray(create_study_world(), (2.5, 2.5), direction)
    assert hit is not None
    assert (hit.cell_x, hit.cell_y) == cell
    assert hit.side == side
    assert hit.parameter == pytest.approx(parameter, rel=1e-12, abs=1e-12)


@pytest.mark.parametrize(
    "width, height", [(1, 1), (1, 40), (40, 1), (2, 40), (40, 2), (40, 40)]
)
@pytest.mark.parametrize(
    "direction", [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1)]
)
def test_open_rectangles_exit_within_iteration_budget(width, height, direction):
    world = World([[0] * width for _ in range(height)])
    # Origem próxima a uma ponta permite percursos longos nos mapas estreitos.
    assert cast_ray(world, (0.5, 0.5), direction) is None


@pytest.mark.parametrize(
    "direction, cell",
    [
        ((0.5, 1), (4, 4)),
        ((-0.5, 1), (2, 4)),
        ((0.5, -1), (4, 0)),
        ((-0.5, -1), (2, 0)),
    ],
)
def test_oblique_ray_hits_horizontal_wall_in_rectangular_room(direction, cell):
    # 1111111  Origem (3.5, 2.5); faces horizontais em y=1 e y=4.
    # 1000001  Para ambos os sentidos de y, t=1.5.
    # 1000001  x=3.5 +/- 0.5*1.5: 4.25 (coluna 4) ou 2.75 (coluna 2).
    # 1000001
    # 1111111
    world = World(
        [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1],
        ]
    )
    hit = cast_ray(world, (3.5, 2.5), direction)
    assert hit is not None
    assert (hit.cell_x, hit.cell_y) == cell
    assert hit.side == "y"
    assert hit.parameter == pytest.approx(1.5, rel=1e-12, abs=1e-12)
