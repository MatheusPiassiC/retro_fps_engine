"""Casos geométricos de câmera com resultados conhecidos antes do cálculo."""

from dataclasses import FrozenInstanceError
from math import hypot, pi, sqrt, tau

import pytest

from retro_fps.camera import Camera


@pytest.mark.parametrize(
    "angle, direction, plane",
    [
        (0, (1, 0), (0, 1)),
        (pi / 2, (0, 1), (-1, 0)),
        (pi, (-1, 0), (0, -1)),
        (3 * pi / 2, (0, -1), (1, 0)),
    ],
)
def test_cardinal_direction_and_right_hand_plane(angle, direction, plane):
    # FOV de 90 graus: tan(45 graus)=1, sem escala lateral adicional.
    camera = Camera(angle, pi / 2)
    assert camera.direction == pytest.approx(direction, rel=1e-12, abs=1e-12)
    assert camera.plane == pytest.approx(plane, rel=1e-12, abs=1e-12)


@pytest.mark.parametrize("angle", [0, pi / 7, pi / 2, pi, 5 * pi / 4])
def test_direction_is_unit_and_plane_is_perpendicular(angle):
    camera = Camera(angle)
    dx, dy = camera.direction
    px, py = camera.plane
    assert hypot(dx, dy) == pytest.approx(1, rel=1e-12, abs=1e-12)
    # Produto escalar zero: os vetores são perpendiculares.
    assert dx * px + dy * py == pytest.approx(0, abs=1e-12)
    # FOV padrão de 60 graus: tan(30 graus)=1/sqrt(3).
    assert hypot(px, py) == pytest.approx(1 / sqrt(3), rel=1e-12, abs=1e-12)


@pytest.mark.parametrize(
    "angle, expected",
    [(-pi / 2, 3 * pi / 2), (tau, 0), (5 * pi / 2, pi / 2), (-1e-20, 0)],
)
def test_angle_is_normalized_to_one_turn(angle, expected):
    camera = Camera(angle)
    assert 0 <= camera.angle < tau
    assert camera.angle == pytest.approx(expected, rel=1e-12, abs=1e-12)


@pytest.mark.parametrize("angle", [float("nan"), float("inf"), -float("inf")])
def test_nonfinite_angle_is_rejected(angle):
    with pytest.raises(ValueError):
        Camera(angle)


@pytest.mark.parametrize(
    "field_of_view", [0, -pi / 3, pi, tau, float("nan"), float("inf"), -float("inf")]
)
def test_invalid_field_of_view_is_rejected(field_of_view):
    with pytest.raises(ValueError):
        Camera(0, field_of_view)


def test_camera_is_immutable():
    camera = Camera(0)
    with pytest.raises(FrozenInstanceError):
        camera.angle = pi
