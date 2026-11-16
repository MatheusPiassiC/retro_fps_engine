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

    def ray_direction(self, column: int, width: int) -> tuple[float, float]:
        """Direção não normalizada pelo centro de uma coluna da imagem interna.

        Com direção frontal unitária e plano perpendicular, o parâmetro
        do DDA representa profundidade frontal. Não corrigir por cosseno.
        """
        if type(column) is not int or type(width) is not int:
            raise TypeError("Coluna e largura devem ser inteiros.")
        if width <= 0:
            raise ValueError("A largura interna deve ser positiva.")
        if not 0 <= column < width:
            raise IndexError("A coluna deve pertencer à largura interna.")

        offset = 2 * (column + 0.5) / width - 1
        direction_x, direction_y = self.direction
        plane_x, plane_y = self.plane
        return direction_x + offset * plane_x, direction_y + offset * plane_y
