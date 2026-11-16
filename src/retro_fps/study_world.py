"""Cenários temporários em memória para estudo, sem dependência gráfica."""

from retro_fps.world import World


def create_study_world() -> World:
    """Crie uma sala 5 × 5 com borda sólida e interior livre."""
    return World(
        (
            (1, 1, 1, 1, 1),
            (1, 0, 0, 0, 1),
            (1, 0, 0, 0, 1),
            (1, 0, 0, 0, 1),
            (1, 1, 1, 1, 1),
        )
    )


def create_study_corridor() -> World:
    """Crie o corredor 9 × 5 de M2-6, com borda sólida e interior livre."""
    return World(
        (
            (1, 1, 1, 1, 1, 1, 1, 1, 1),
            (1, 0, 0, 0, 0, 0, 0, 0, 1),
            (1, 0, 0, 0, 0, 0, 0, 0, 1),
            (1, 0, 0, 0, 0, 0, 0, 0, 1),
            (1, 1, 1, 1, 1, 1, 1, 1, 1),
        )
    )
