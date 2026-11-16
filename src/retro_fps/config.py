"""Configuração inicial da janela, independente da inicialização gráfica."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RenderConfig:
    """Resolução interna em pixels, independente das dimensões da janela."""

    internal_width: int = 320
    internal_height: int = 200

    def __post_init__(self) -> None:
        if any(
            type(value) is not int or value <= 0
            for value in (self.internal_width, self.internal_height)
        ):
            raise ValueError("As dimensões internas devem ser inteiros positivos.")


@dataclass(frozen=True)
class WindowConfig:
    """Dimensões em pixels, limite de quadros por segundo e cor RGB."""

    width: int = 640
    height: int = 480
    title: str = "RetroFPS Engine"
    frame_limit: int = 60
    background_color: tuple[int, int, int] = (40, 80, 120)

    def __post_init__(self) -> None:
        """Rejeite valores inválidos antes de inicializar a janela."""
        if any(
            type(value) is not int or value <= 0
            for value in (self.width, self.height, self.frame_limit)
        ):
            raise ValueError(
                "Dimensões e limite de quadros devem ser inteiros positivos."
            )
        if len(self.background_color) != 3 or any(
            type(channel) is not int or not 0 <= channel <= 255
            for channel in self.background_color
        ):
            raise ValueError("A cor RGB deve conter três inteiros entre 0 e 255.")
