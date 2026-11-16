"""Demonstração de navegação em um mapa externo indicado na linha de comando."""

import argparse
from pathlib import Path

from retro_fps.map_loader import MapLoadError, load_map
from retro_fps.player import MovementConfig


def main(argv: list[str] | None = None) -> None:
    """Carregue antes de abrir a janela; informe falhas sem traceback de mapa."""
    parser = argparse.ArgumentParser(
        description="Explore um mapa com WASD e setas esquerda/direita. Escape encerra.",
    )
    parser.add_argument(
        "map_path", type=Path, metavar="MAPA", help="caminho do arquivo .map UTF-8"
    )
    args = parser.parse_args(argv)
    movement_config = MovementConfig()
    try:
        data = load_map(args.map_path, movement_config=movement_config)
    except MapLoadError as error:
        parser.error(str(error))

    # O carregamento e --help funcionam sem importar/inicializar Pygame.
    from retro_fps.engine import run

    run(world=data.world, player=data.player, movement_config=movement_config)


if __name__ == "__main__":
    main()
