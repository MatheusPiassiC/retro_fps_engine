"""Casos pequenos de M1-1, conferíveis por linhas e colunas."""

from dataclasses import FrozenInstanceError

import pytest

from retro_fps.world import World


def test_rectangular_grid_dimensions_and_cells():
    # Três colunas e duas linhas; (1, 0) difere de (0, 1).
    world = World([[0, 1, 0], [0, 0, 1]])
    assert world.width == 3
    assert world.height == 2
    assert world.cell_at(1, 0) == 1
    assert world.cell_at(0, 1) == 0
    assert world.cell_at(2, 1) == 1
    assert world.contains(0, 0)
    assert world.contains(2, 1)
    assert world.is_solid(1, 0)
    assert not world.is_solid(0, 1)


@pytest.mark.parametrize("x, y", [(-1, 0), (0, -1), (3, 0), (0, 2)])
def test_outside_each_edge(x, y):
    world = World([[0, 0, 0], [0, 0, 0]])
    assert not world.contains(x, y)
    assert world.is_solid(x, y)
    with pytest.raises(IndexError):
        world.cell_at(x, y)


def test_world_copies_input_and_remains_immutable():
    grid = [[0, 1]]
    world = World(grid)
    grid[0][0] = 1
    grid.append([1, 1])
    assert world.grid == ((0, 1),)
    with pytest.raises(TypeError):
        world.grid[0][0] = 1
    with pytest.raises(FrozenInstanceError):
        world.grid = ((1,),)


@pytest.mark.parametrize(
    "grid",
    [[], [[]], [[0], []], [[0], [0, 1]], [[2]], [[-1]], [["0"]], [[0.0]], [[True]]],
)
def test_invalid_grid_is_rejected(grid):
    with pytest.raises(ValueError):
        World(grid)


@pytest.mark.parametrize("x, y", [(0.5, 0), (0, 1.0), (True, 0), (0, "1")])
def test_queries_require_integer_indices(x, y):
    world = World([[0]])
    for query in (world.contains, world.cell_at, world.is_solid):
        with pytest.raises(TypeError):
            query(x, y)


def test_single_cell_and_open_edges_are_allowed_in_memory():
    # Tamanho mínimo e borda fechada são regras do carregador futuro.
    world = World(((0,),))
    assert world.width == world.height == 1
    assert world.cell_at(0, 0) == 0
    assert not world.is_solid(0, 0)
