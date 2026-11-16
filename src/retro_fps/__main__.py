"""Ponto de entrada para a sala estática de estudo."""

from retro_fps.camera import Camera
from retro_fps.engine import run
from retro_fps.study_world import create_study_world


def main() -> None:
    """Apresente a sala de estudo com câmera fixa olhando para leste."""
    run(world=create_study_world(), origin=(2.5, 2.5), camera=Camera(0))


if __name__ == "__main__":
    main()
