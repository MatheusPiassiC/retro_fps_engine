"""Contratos do estado, comandos e movimento sem janela."""

from dataclasses import FrozenInstanceError
from math import hypot, pi, sqrt, tau

import pytest

from retro_fps.player import MovementCommand, MovementConfig, PlayerState, update_player


def test_position_is_preserved_and_copied():
    position = [2.5, 1.5]
    player = PlayerState(position, 0)
    position[0] = 9
    assert player.position == (2.5, 1.5)
    assert player.angle == 0


@pytest.mark.parametrize(
    "angle, expected",
    [(0, 0), (-pi / 2, 3 * pi / 2), (tau, 0), (5 * pi / 2, pi / 2), (-1e-20, 0)],
)
def test_angle_is_normalized(angle, expected):
    player = PlayerState((2.5, 2.5), angle)
    assert 0 <= player.angle < tau
    assert player.angle == pytest.approx(expected, abs=1e-12)


@pytest.mark.parametrize(
    "position",
    [(), (1,), (1, 2, 3), (float("nan"), 0), (0, float("inf")), (-float("inf"), 0)],
)
def test_invalid_position_is_rejected(position):
    with pytest.raises(ValueError):
        PlayerState(position, 0)


@pytest.mark.parametrize("angle", [float("nan"), float("inf"), -float("inf")])
def test_nonfinite_angle_is_rejected(angle):
    with pytest.raises(ValueError):
        PlayerState((2.5, 2.5), angle)


@pytest.mark.parametrize("attribute, value", [("position", (1, 1)), ("angle", pi)])
def test_player_is_immutable(attribute, value):
    player = PlayerState((2.5, 2.5), 0)
    with pytest.raises(FrozenInstanceError):
        setattr(player, attribute, value)


def test_default_command_requests_no_movement():
    assert MovementCommand() == MovementCommand(0, 0)


@pytest.mark.parametrize("forward", [-1, 0, 1])
@pytest.mark.parametrize("turn", [-1, 0, 1])
@pytest.mark.parametrize("strafe", [-1, 0, 1])
def test_independent_command_combinations(forward, turn, strafe):
    command = MovementCommand(forward, turn, strafe)
    assert command.forward == forward
    assert command.turn == turn
    assert command.strafe == strafe


@pytest.mark.parametrize("attribute", ["forward", "turn", "strafe"])
@pytest.mark.parametrize("value", [-2, 2])
def test_out_of_range_command_is_rejected(attribute, value):
    with pytest.raises(ValueError):
        MovementCommand(**{attribute: value})


@pytest.mark.parametrize("attribute", ["forward", "turn", "strafe"])
@pytest.mark.parametrize("value", [True, False, 1.0, "1", None])
def test_noninteger_command_is_rejected(attribute, value):
    with pytest.raises(TypeError):
        MovementCommand(**{attribute: value})


def test_command_is_immutable():
    command = MovementCommand()
    with pytest.raises(FrozenInstanceError):
        command.forward = 1


@pytest.mark.parametrize(
    "angle, forward, expected",
    [
        (0, 1, (2.6, 2.5)),
        (0, -1, (2.4, 2.5)),
        (pi / 2, 1, (2.5, 2.6)),
        (pi, 1, (2.4, 2.5)),
        (3 * pi / 2, 1, (2.5, 2.4)),
    ],
)
def test_movement_in_cardinal_directions(angle, forward, expected):
    state = PlayerState((2.5, 2.5), angle)
    result = update_player(state, MovementCommand(forward), MovementConfig(), 0.1)
    assert result.position == pytest.approx(expected, abs=1e-12)
    assert result.angle == state.angle
    assert state.position == (2.5, 2.5)


@pytest.mark.parametrize("turn, expected", [(1, pi / 20), (-1, 39 * pi / 20)])
def test_turning_keeps_position(turn, expected):
    state = PlayerState((2.5, 2.5), 0)
    result = update_player(state, MovementCommand(turn=turn), MovementConfig(), 0.1)
    assert result.angle == pytest.approx(expected, abs=1e-12)
    assert result.position == state.position


def test_turn_is_applied_before_translation():
    # Em 1 s a 90 graus/s, o giro leva de leste a sul; avança uma unidade em y.
    result = update_player(
        PlayerState((2.5, 2.5), 0), MovementCommand(1, 1), MovementConfig(), 1
    )
    assert result.position == pytest.approx((2.5, 3.5), abs=1e-12)
    assert result.angle == pytest.approx(pi / 2)


@pytest.mark.parametrize(
    "command, elapsed", [(MovementCommand(), 0.1), (MovementCommand(1, 1), 0)]
)
def test_no_command_or_zero_time_preserves_state(command, elapsed):
    state = PlayerState((2.5, 2.5), pi / 4)
    assert update_player(state, command, MovementConfig(), elapsed) == state


@pytest.mark.parametrize(
    "command",
    [
        MovementCommand(1),
        MovementCommand(-1),
        MovementCommand(strafe=1),
        MovementCommand(1, strafe=-1),
        MovementCommand(turn=1),
        MovementCommand(turn=-1),
    ],
)
def test_straight_motion_or_turn_matches_two_half_steps(command):
    state = PlayerState((2.5, 2.5), pi / 4)
    config = MovementConfig()
    single = update_player(state, command, config, 0.1)
    half = update_player(state, command, config, 0.05)
    split = update_player(half, command, config, 0.05)
    assert split.position == pytest.approx(single.position, abs=1e-12)
    assert split.angle == pytest.approx(single.angle, abs=1e-12)


def test_custom_speeds_and_angle_normalization():
    # Meia volta a pi rad/s por 1 s; recuar 2 unidades olhando para oeste leva a leste.
    result = update_player(
        PlayerState((2.5, 2.5), tau),
        MovementCommand(-1, 1),
        MovementConfig(move_speed=2, turn_speed=pi),
        1,
    )
    assert result.position == pytest.approx((4.5, 2.5), abs=1e-12)
    assert result.angle == pytest.approx(pi)


@pytest.mark.parametrize("elapsed", [-0.1, float("nan"), float("inf"), -float("inf")])
def test_invalid_elapsed_time_is_rejected(elapsed):
    with pytest.raises(ValueError):
        update_player(
            PlayerState((0, 0), 0), MovementCommand(), MovementConfig(), elapsed
        )


@pytest.mark.parametrize("attribute", ["move_speed", "turn_speed"])
@pytest.mark.parametrize("speed", [0, -1, float("nan"), float("inf"), -float("inf")])
def test_invalid_speed_is_rejected(attribute, speed):
    with pytest.raises(ValueError):
        MovementConfig(**{attribute: speed})


def test_movement_config_defaults_and_immutability():
    config = MovementConfig()
    assert config.move_speed == 1
    assert config.turn_speed == pi / 2
    with pytest.raises(FrozenInstanceError):
        config.move_speed = 2


@pytest.mark.parametrize(
    "angle, strafe, expected",
    [
        (0, 1, (2.5, 2.6)),
        (0, -1, (2.5, 2.4)),
        (pi / 2, 1, (2.4, 2.5)),
        (pi, 1, (2.5, 2.4)),
        (3 * pi / 2, 1, (2.6, 2.5)),
    ],
)
def test_strafe_follows_orientation_without_turning(angle, strafe, expected):
    result = update_player(
        PlayerState((2.5, 2.5), angle),
        MovementCommand(strafe=strafe),
        MovementConfig(),
        0.1,
    )
    assert result.position == pytest.approx(expected, abs=1e-12)
    assert result.angle == angle


@pytest.mark.parametrize("forward", [-1, 1])
@pytest.mark.parametrize("strafe", [-1, 1])
def test_diagonal_has_same_speed_as_straight_motion(forward, strafe):
    # Pitágoras: duas componentes de 0.1/sqrt(2) têm comprimento total 0.1.
    result = update_player(
        PlayerState((0, 0), 0),
        MovementCommand(forward=forward, strafe=strafe),
        MovementConfig(),
        0.1,
    )
    assert result.position == pytest.approx(
        (forward * 0.1 / sqrt(2), strafe * 0.1 / sqrt(2)), abs=1e-12
    )
    assert hypot(*result.position) == pytest.approx(0.1, abs=1e-12)
    assert result.angle == 0


def test_diagonal_and_strafe_use_new_angle_after_turn():
    # Giro até sul: frente=sul e direita=oeste, portanto diagonal sudoeste.
    result = update_player(
        PlayerState((0, 0), 0), MovementCommand(1, 1, 1), MovementConfig(), 1
    )
    assert result.position == pytest.approx((-1 / sqrt(2), 1 / sqrt(2)), abs=1e-12)
    assert result.angle == pytest.approx(pi / 2)


@pytest.mark.parametrize("radius", [0, -0.2, float("nan"), float("inf")])
def test_invalid_player_radius_is_rejected(radius):
    with pytest.raises(ValueError):
        MovementConfig(radius=radius)


def test_player_radius_default_and_immutability():
    config = MovementConfig()
    assert config.radius == 0.2
    with pytest.raises(FrozenInstanceError):
        config.radius = 0.3
