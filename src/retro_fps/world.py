"""Representação da grade e consultas de células, sem dependência gráfica."""

from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True, init=False)
class World:
    """Grade imutável: 0 é livre, 1 é parede; acesso interno por grid[y][x]."""

    grid: tuple[tuple[int, ...], ...]

    def __init__(self, grid: Sequence[Sequence[int]]) -> None:
        rows = tuple(tuple(row) for row in grid)
        if not rows or not rows[0]:
            raise ValueError("A grade deve conter pelo menos uma célula.")
        if any(len(row) != len(rows[0]) for row in rows):
            raise ValueError("A grade deve ser retangular.")
        if any(
            type(cell) is not int or cell not in (0, 1) for row in rows for cell in row
        ):
            raise ValueError("As células devem ser inteiros 0 (livre) ou 1 (parede).")
        object.__setattr__(self, "grid", rows)

    @property
    def width(self) -> int:
        """Número de colunas da grade."""
        return len(self.grid[0])

    @property
    def height(self) -> int:
        """Número de linhas da grade."""
        return len(self.grid)

    def contains(self, x: int, y: int) -> bool:
        """Informe se os índices inteiros pertencem à grade."""
        if type(x) is not int or type(y) is not int:
            raise TypeError("Os índices de célula devem ser inteiros.")
        return 0 <= x < self.width and 0 <= y < self.height

    def cell_at(self, x: int, y: int) -> int:
        """Retorne a célula; rejeite índices fora da grade com IndexError."""
        if not self.contains(x, y):
            raise IndexError(f"Célula ({x}, {y}) fora da grade.")
        return self.grid[y][x]

    def is_solid(self, x: int, y: int) -> bool:
        """Informe se há parede; o exterior da grade também é sólido."""
        return not self.contains(x, y) or self.grid[y][x] == 1
