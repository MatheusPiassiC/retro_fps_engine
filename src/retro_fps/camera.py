"""Geometria da câmera no plano do mapa, sem dependência gráfica."""

from dataclasses import dataclass
from math import cos, isfinite, pi, sin, tan, tau


@dataclass(frozen=True)
class Camera:
    """Orientação e campo de visão horizontal em radianos.

    A posição é fornecida separadamente ao lançar raios. O eixo y do
    mapa cresce para baixo; ângulos positivos giram no sentido horário.
    """

    angle: float
    field_of_view: float = pi / 3

    def __post_init__(self) -> None:
        if not isfinite(self.angle):
            raise ValueError("O ângulo da câmera deve ser finito.")
        if not isfinite(self.field_of_view) or not 0 < self.field_of_view < pi:
            raise ValueError("O campo de visão deve estar entre 0 e pi radianos.")
        normalized_angle = self.angle % tau
        # Um negativo muito próximo de zero pode arredondar o resto para tau.
        object.__setattr__(
            self, "angle", 0.0 if normalized_angle == tau else normalized_angle
        )

    @property
    def direction(self) -> tuple[float, float]:
        """Direção frontal unitária: comprimento igual a uma unidade."""
        return cos(self.angle), sin(self.angle)

    @property
    def plane(self) -> tuple[float, float]:
        """Vetor perpendicular para a direita da imagem, de tamanho tan(FOV/2)."""
        scale = tan(self.field_of_view / 2)
        return -sin(self.angle) * scale, cos(self.angle) * scale
