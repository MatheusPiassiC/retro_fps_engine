"""Estado e intenções de movimento, sem dependência de teclado ou janela."""

from dataclasses import dataclass
from math import isfinite, tau


@dataclass(frozen=True)
class PlayerState:
    """Posição contínua e orientação em radianos, sem validar colisões."""

    position: tuple[float, float]
    angle: float

    def __post_init__(self) -> None:
        position = tuple(self.position)
        if len(position) != 2 or not all(isfinite(value) for value in position):
            raise ValueError("A posição deve conter duas coordenadas finitas.")
        if not isfinite(self.angle):
            raise ValueError("O ângulo do jogador deve ser finito.")
        object.__setattr__(self, "position", position)
        normalized_angle = self.angle % tau
        # Um negativo muito próximo de zero pode arredondar o resto para tau.
        object.__setattr__(
            self, "angle", 0.0 if normalized_angle == tau else normalized_angle
        )


@dataclass(frozen=True)
class MovementCommand:
    """Intenções discretas: positivo avança/gira à direita; zero não solicita."""

    forward: int = 0
    turn: int = 0

    def __post_init__(self) -> None:
        for value in (self.forward, self.turn):
            if type(value) is not int:
                raise TypeError("Os comandos devem ser inteiros, sem booleanos.")
            if value not in (-1, 0, 1):
                raise ValueError("Os comandos devem ser -1, 0 ou 1.")
