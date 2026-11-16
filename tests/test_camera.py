"""Casos geométricos de câmera com resultados conhecidos antes do cálculo."""

from dataclasses import FrozenInstanceError
from math import hypot, pi, sqrt, tau

import pytest

from retro_fps.camera import Camera
from retro_fps.raycasting import cast_ray
from retro_fps.study_world import create_study_world


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


@pytest.mark.parametrize("angle", [0, pi / 2, pi, 3 * pi / 2])
def test_single_column_points_forward(angle):
    camera = Camera(angle, pi / 2)
    assert camera.ray_direction(0, 1) == pytest.approx(
        camera.direction, rel=1e-12, abs=1e-12
    )


@pytest.mark.parametrize(
    "width, offsets",
    [(3, (-2 / 3, 0, 2 / 3)), (4, (-0.75, -0.25, 0.25, 0.75))],
)
def test_columns_use_centers_with_symmetric_offsets(width, offsets):
    # Leste, FOV 90 graus: frente=(1,0), plano=(0,1), raio=(1,u).
    camera = Camera(0, pi / 2)
    for column, offset in enumerate(offsets):
        assert camera.ray_direction(column, width) == pytest.approx(
            (1, offset), rel=1e-12, abs=1e-12
        )


def test_rotated_camera_preserves_image_left_and_right():
    # Olhando para sul, esquerda da imagem é leste e direita é oeste.
    camera = Camera(pi / 2, pi / 2)
    assert camera.ray_direction(0, 3) == pytest.approx((2 / 3, 1), rel=1e-12, abs=1e-12)
    assert camera.ray_direction(2, 3) == pytest.approx(
        (-2 / 3, 1), rel=1e-12, abs=1e-12
    )


@pytest.mark.parametrize("angle", [0, pi / 7, pi / 2, pi])
def test_lateral_ray_is_not_normalized_but_has_unit_forward_component(angle):
    camera = Camera(angle, pi / 2)
    ray_x, ray_y = camera.ray_direction(0, 3)
    forward_x, forward_y = camera.direction
    # Comprimento de (1,-2/3): sqrt(1+4/9)=sqrt(13)/3.
    assert hypot(ray_x, ray_y) == pytest.approx(sqrt(13) / 3, rel=1e-12, abs=1e-12)
    assert ray_x * forward_x + ray_y * forward_y == pytest.approx(
        1, rel=1e-12, abs=1e-12
    )


@pytest.mark.parametrize("column, cell_y", [(0, 1), (1, 2), (2, 3)])
def test_column_rays_have_constant_depth_to_front_wall(column, cell_y):
    # x=2.5+t atinge x=4 em t=1.5 para todos os raios.
    # y=2.5+t*u dá 1.5, 2.5 e 3.5: linhas 1, 2 e 3.
    camera = Camera(0, pi / 2)
    hit = cast_ray(create_study_world(), (2.5, 2.5), camera.ray_direction(column, 3))
    assert hit is not None
    assert (hit.cell_x, hit.cell_y, hit.side) == (4, cell_y, "x")
    assert hit.parameter == pytest.approx(1.5, rel=1e-12, abs=1e-12)


@pytest.mark.parametrize("column, width", [(0.0, 3), (0, 3.0), (True, 3), (0, True)])
def test_column_and_width_require_integers(column, width):
    with pytest.raises(TypeError):
        Camera(0).ray_direction(column, width)


@pytest.mark.parametrize("width", [0, -1])
def test_nonpositive_width_is_rejected(width):
    with pytest.raises(ValueError):
        Camera(0).ray_direction(0, width)


@pytest.mark.parametrize("column", [-1, 3])
def test_column_outside_image_is_rejected(column):
    with pytest.raises(IndexError):
        Camera(0).ray_direction(column, 3)
