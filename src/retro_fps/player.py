"""Estado e intenções de movimento, sem dependência de teclado ou janela."""

from dataclasses import dataclass
from math import cos, isfinite, pi, sin, tau


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


@dataclass(frozen=True)
class MovementConfig:
    """Velocidades linear em unidades/s e angular em radianos/s."""

    move_speed: float = 1.0
    turn_speed: float = pi / 2

    def __post_init__(self) -> None:
        for speed in (self.move_speed, self.turn_speed):
            if not isfinite(speed) or speed <= 0:
                raise ValueError("As velocidades devem ser finitas e positivas.")


def update_player(
    state: PlayerState,
    command: MovementCommand,
    config: MovementConfig,
    delta_time: float,
) -> PlayerState:
    """Gire e depois desloque na nova direção, sem colisão ou limite de tempo.

    O tempo é dado em segundos. Avançar enquanto gira aproxima uma curva
    por segmentos retos; subdividir o tempo pode alterar essa trajetória.
    """
    if not isfinite(delta_time) or delta_time < 0:
        raise ValueError("O intervalo deve ser finito e não negativo.")
    angle = state.angle + command.turn * config.turn_speed * delta_time
    distance = command.forward * config.move_speed * delta_time
    x, y = state.position
    return PlayerState((x + distance * cos(angle), y + distance * sin(angle)), angle)
