"""Contas independentes: escala 160 e paredes centralizadas em y=100."""

from math import pi

import pytest

from retro_fps.projection import projected_wall_height, wall_span


@pytest.mark.parametrize("depth, expected", [(1, 160), (2, 80), (4, 40)])
def test_known_heights_before_rounding(depth, expected):
    # Largura 320 e FOV 90 graus: 320/(2*tan(45 graus))=160.
    assert projected_wall_height(depth, 320, pi / 2) == pytest.approx(
        expected, rel=1e-12, abs=1e-12
    )


def test_doubling_depth_halves_unclipped_height():
    near = projected_wall_height(1.5, 320, pi / 3)
    far = projected_wall_height(3, 320, pi / 3)
    assert far == pytest.approx(near / 2, rel=1e-12, abs=1e-12)


@pytest.mark.parametrize("depth", [0, 1e-12, 1e-6])
def test_near_depth_is_protected_and_fills_screen(depth):
    projected_height = projected_wall_height(depth, 320, pi / 2)
    assert projected_height == pytest.approx(160_000_000, rel=1e-12)
    assert wall_span(projected_height, 200) == (0, 200)


@pytest.mark.parametrize(
    "projected_height, height, expected",
    [
        (80, 200, (60, 140)),
        (40, 200, (80, 120)),
        (79.5, 200, (60, 140)),
        (80, 201, (60, 141)),
        (200, 200, (0, 200)),
        (1e300, 200, (0, 200)),
        (0, 200, (100, 100)),
        (0, 201, (100, 100)),
    ],
)
def test_centering_rounding_and_clipping(projected_height, height, expected):
    assert wall_span(projected_height, height) == expected


@pytest.mark.parametrize("value", [-1, float("nan"), float("inf"), -float("inf")])
def test_invalid_depth_or_projected_height_is_rejected(value):
    with pytest.raises(ValueError):
        projected_wall_height(value, 320, pi / 2)
    with pytest.raises(ValueError):
        wall_span(value, 200)


@pytest.mark.parametrize("value", [0, -1, pi, float("nan"), float("inf")])
def test_invalid_field_of_view_is_rejected(value):
    with pytest.raises(ValueError):
        projected_wall_height(2, 320, value)


@pytest.mark.parametrize("value", [True, 200.0, "200"])
def test_dimensions_require_integers(value):
    with pytest.raises(TypeError):
        projected_wall_height(2, value, pi / 2)
    with pytest.raises(TypeError):
        wall_span(80, value)


@pytest.mark.parametrize("value", [0, -1])
def test_dimensions_require_positive_values(value):
    with pytest.raises(ValueError):
        projected_wall_height(2, value, pi / 2)
    with pytest.raises(ValueError):
        wall_span(80, value)
