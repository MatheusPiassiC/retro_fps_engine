"""Estado e intenções de movimento, sem dependência de teclado ou janela."""

from dataclasses import dataclass
from math import cos, hypot, isfinite, pi, sin, tau


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
    """Intenções discretas: avanço, giro e lateral; positivo aponta à direita."""

    forward: int = 0
    turn: int = 0
    strafe: int = 0

    def __post_init__(self) -> None:
        for value in (self.forward, self.turn, self.strafe):
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
    # Frente e direita são perpendiculares. Dividir pelo comprimento da
    # intenção impede que a diagonal (comprimento sqrt(2)) seja mais rápida.
    scale = (
        config.move_speed
        * delta_time
        / max(1.0, hypot(command.forward, command.strafe))
    )
    front_x, front_y = cos(angle), sin(angle)
    offset_x = scale * (command.forward * front_x - command.strafe * front_y)
    offset_y = scale * (command.forward * front_y + command.strafe * front_x)
    x, y = state.position
    return PlayerState((x + offset_x, y + offset_y), angle)
