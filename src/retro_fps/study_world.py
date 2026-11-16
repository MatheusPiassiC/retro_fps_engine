"""Sala temporária em memória para o estudo de M1, sem dependência gráfica."""

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
