"""Contratos do estado e dos comandos; nenhum movimento é executado ainda."""

from dataclasses import FrozenInstanceError
from math import pi, tau

import pytest

from retro_fps.player import MovementCommand, PlayerState


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
def test_independent_command_combinations(forward, turn):
    command = MovementCommand(forward, turn)
    assert command.forward == forward
    assert command.turn == turn


@pytest.mark.parametrize("attribute", ["forward", "turn"])
@pytest.mark.parametrize("value", [-2, 2])
def test_out_of_range_command_is_rejected(attribute, value):
    with pytest.raises(ValueError):
        MovementCommand(**{attribute: value})


@pytest.mark.parametrize("attribute", ["forward", "turn"])
@pytest.mark.parametrize("value", [True, False, 1.0, "1", None])
def test_noninteger_command_is_rejected(attribute, value):
    with pytest.raises(TypeError):
        MovementCommand(**{attribute: value})


def test_command_is_immutable():
    command = MovementCommand()
    with pytest.raises(FrozenInstanceError):
        command.forward = 1
