"""Ponto de entrada para movimento com colisões na sala de estudo."""

from retro_fps.engine import run
from retro_fps.player import PlayerState
from retro_fps.study_world import create_study_world


def main() -> None:
    """Apresente a sala com WASD, setas e colisões para o círculo do jogador."""
    run(world=create_study_world(), player=PlayerState((2.5, 2.5), 0))


if __name__ == "__main__":
    main()
