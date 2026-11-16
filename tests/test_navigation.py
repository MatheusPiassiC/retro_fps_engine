"""Validação integrada de navegação com expectativas geométricas independentes."""

from math import atan2, hypot, pi, sqrt

import pytest

from retro_fps.player import (
    MovementCommand,
    MovementConfig,
    PlayerState,
    update_player_in_world,
)
from retro_fps.study_world import create_study_world
from retro_fps.world import World


def create_pillar_world():
    """Obstáculo unitário em [3,4] × [3,4], com espaço livre em volta."""
    grid = [[0] * 7 for _ in range(7)]
    grid[3][3] = 1
    return World(grid)


@pytest.mark.parametrize("horizontal", [-1, 1])
@pytest.mark.parametrize("vertical", [-1, 1])
def test_oblique_approach_slides_in_each_quadrant(horizontal, vertical):
    # Direção de comprimento 1: (4/5, 3/5), com sinais escolhidos.
    angle = atan2(vertical * 3, horizontal * 4)
    start_x = 3.79 if horizontal > 0 else 1.21
    result = update_player_in_world(
        create_study_world(),
        PlayerState((start_x, 2.5), angle),
        MovementCommand(1),
        MovementConfig(),
        0.05,
    )
    # 0.04 em x sobreporia a parede; 0.03 em y permanece livre.
    assert result.position == pytest.approx((start_x, 2.5 + vertical * 0.03), abs=1e-12)


@pytest.mark.parametrize("horizontal", [-1, 1])
@pytest.mark.parametrize("vertical", [-1, 1])
def test_repeated_diagonal_motion_stays_outside_pillar_corners(horizontal, vertical):
    world = create_pillar_world()
    corner_x = 3 if horizontal > 0 else 4
    corner_y = 3 if vertical > 0 else 4
    state = PlayerState((corner_x - horizontal * 0.4, corner_y - vertical * 0.4), 0)
    for _ in range(30):
        state = update_player_in_world(
            world,
            state,
            MovementCommand(forward=horizontal, strafe=vertical),
            MovementConfig(),
            0.1,
        )
        # Ponto mais próximo conhecido neste quadrante é o canto fixo.
        # As coordenadas também não podem cruzar as faces rumo ao interior.
        x, y = state.position
        assert horizontal * (x - corner_x) < 0
        assert vertical * (y - corner_y) < 0
        assert hypot(x - corner_x, y - corner_y) > 0.2


@pytest.mark.parametrize(
    "angle, axis, positive",
    [(0, 0, True), (pi, 0, False), (pi / 2, 1, True), (3 * pi / 2, 1, False)],
)
@pytest.mark.parametrize("closed", [False, True])
def test_large_motion_cannot_cross_wall_or_open_map_boundary(
    angle, axis, positive, closed
):
    world = create_study_world() if closed else World([[0] * 5 for _ in range(5)])
    result = update_player_in_world(
        world,
        PlayerState((2.5, 2.5), angle),
        MovementCommand(1),
        MovementConfig(move_speed=100),
        5,
    )
    # Círculo deve permanecer entre faces + raio e faces - raio.
    lower, upper = (1.2, 3.8) if closed else (0.2, 4.8)
    coordinate = result.position[axis]
    assert lower < coordinate < upper
    assert abs(coordinate - (upper if positive else lower)) <= 0.100000000001
    assert result.position[1 - axis] == pytest.approx(2.5, abs=1e-12)


@pytest.mark.parametrize(
    "command",
    [
        MovementCommand(1),
        MovementCommand(strafe=-1),
        MovementCommand(1, strafe=1),
        MovementCommand(turn=1),
    ],
)
def test_free_space_matches_known_result_at_different_frame_intervals(command):
    world = World([[0] * 8 for _ in range(8)])
    results = []
    for count, elapsed in [(10, 0.1), (20, 0.05), (40, 0.025)]:
        state = PlayerState((3, 3), 0)
        for _ in range(count):
            state = update_player_in_world(
                world, state, command, MovementConfig(), elapsed
            )
        results.append(state)
    # Um segundo a 1 unidade/s; giro isolado de um quarto de volta.
    expected = {
        MovementCommand(1): ((4, 3), 0),
        MovementCommand(strafe=-1): ((3, 2), 0),
        MovementCommand(1, strafe=1): ((3 + 1 / sqrt(2), 3 + 1 / sqrt(2)), 0),
        MovementCommand(turn=1): ((3, 3), pi / 2),
    }[command]
    for state in results:
        assert state.position == pytest.approx(expected[0], abs=1e-12)
        assert state.angle == pytest.approx(expected[1], abs=1e-12)


def test_navigation_around_pillar_and_back_without_changing_orientation():
    world = create_pillar_world()
    state = PlayerState((2.5, 3.5), 0)
    # Contornar por cima: norte 1, leste 2, sul 1; voltar pelo mesmo caminho.
    segments = [
        (MovementCommand(strafe=-1), 10, (2.5, 2.5)),
        (MovementCommand(1), 20, (4.5, 2.5)),
        (MovementCommand(strafe=1), 10, (4.5, 3.5)),
        (MovementCommand(strafe=-1), 10, (4.5, 2.5)),
        (MovementCommand(-1), 20, (2.5, 2.5)),
        (MovementCommand(strafe=1), 10, (2.5, 3.5)),
    ]
    for command, count, expected in segments:
        for _ in range(count):
            state = update_player_in_world(world, state, command, MovementConfig(), 0.1)
            # Distância ao retângulo do obstáculo, calculada geometricamente.
            x, y = state.position
            gap_x = max(3 - x, 0, x - 4)
            gap_y = max(3 - y, 0, y - 4)
            assert hypot(gap_x, gap_y) > 0.2
        assert state.position == pytest.approx(expected, abs=1e-12)
        assert state.angle == 0
