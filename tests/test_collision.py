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


@pytest.mark.parametrize(
    "start, displacement, expected",
    [
        ((2.5, 2.5), (0.1, 0.1), (2.6, 2.6)),
        ((2.5, 2.5), (-0.1, -0.1), (2.4, 2.4)),
        ((3.75, 2.5), (0.1, 0.1), (3.75, 2.6)),
        ((1.25, 2.5), (-0.1, 0.1), (1.25, 2.6)),
        ((2.5, 3.75), (0.1, 0.1), (2.6, 3.75)),
        ((2.5, 1.25), (0.1, -0.1), (2.6, 1.25)),
        ((3.75, 3.75), (0.1, 0.1), (3.75, 3.75)),
        ((2.5, 2.5), (0, 0), (2.5, 2.5)),
    ],
)
def test_axes_preserve_free_motion_and_block_walls(start, displacement, expected):
    from retro_fps.collision import resolve_movement
    from retro_fps.study_world import create_study_world

    result = resolve_movement(create_study_world(), start, displacement, 0.2)
    assert result == pytest.approx(expected, abs=1e-12)
    assert can_occupy(create_study_world(), result, 0.2)


def test_x_is_resolved_before_y_at_corner():
    from retro_fps.collision import resolve_movement

    world = World(
        [[0] * 5 for _ in range(2)] + [[0, 0, 1, 0, 0]] + [[0] * 5 for _ in range(2)]
    )
    # Centro (1.8,1.8) está a sqrt(0.08)>0.2 do canto (2,2).
    # x até 1.9 cabe: distância sqrt(0.05)>0.2.
    # y até 1.9 após x bloquearia: distância sqrt(0.02)<0.2.
    result = resolve_movement(world, (1.8, 1.8), (0.1, 0.1), 0.2)
    assert result == pytest.approx((1.9, 1.8), abs=1e-12)


def test_repeated_steps_slide_along_wall():
    from retro_fps.collision import resolve_movement
    from retro_fps.study_world import create_study_world

    world = create_study_world()
    position = (3.75, 2.0)
    for _ in range(5):
        position = resolve_movement(world, position, (0.1, 0.1), 0.2)
        assert can_occupy(world, position, 0.2)
    assert position == pytest.approx((3.75, 2.5), abs=1e-12)


@pytest.mark.parametrize("start", [(0.5, 0.5), (3.8, 2.5), (-1, 2.5)])
def test_invalid_start_is_rejected_by_resolver(start):
    from retro_fps.collision import resolve_movement
    from retro_fps.study_world import create_study_world

    with pytest.raises(ValueError):
        resolve_movement(create_study_world(), start, (0, 0), 0.2)


@pytest.mark.parametrize("displacement", [(float("nan"), 0), (0, float("inf"))])
def test_nonfinite_displacement_is_rejected(displacement):
    from retro_fps.collision import resolve_movement

    with pytest.raises(ValueError):
        resolve_movement(
            World([[0] * 5 for _ in range(5)]), (2.5, 2.5), displacement, 0.2
        )


@pytest.mark.parametrize(
    "start, displacement, expected",
    [((0.25, 2), (-0.1, 0.1), (0.25, 2.1)), ((3.75, 2), (0.1, -0.1), (3.75, 1.9))],
)
def test_open_map_bounds_also_allow_sliding(start, displacement, expected):
    from retro_fps.collision import resolve_movement

    world = World([[0] * 4 for _ in range(4)])
    assert resolve_movement(world, start, displacement, 0.2) == pytest.approx(expected)
