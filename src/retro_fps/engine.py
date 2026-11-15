"""Ciclo inicial da aplicação; a coordenação da sessão evoluirá em M0–M5."""

import pygame

from retro_fps.config import WindowConfig


def run(config: WindowConfig | None = None) -> None:
    """Apresente uma cor sólida e o intervalo em segundos no título da janela."""
    if config is None:
        config = WindowConfig()

    try:
        pygame.display.init()
        screen = pygame.display.set_mode((config.width, config.height))
        pygame.display.set_caption(config.title)
        clock = pygame.time.Clock()
        running = True

        while running:
            # tick retorna milissegundos: 16 ms correspondem a 0.016 segundo.
            delta_time = clock.tick(config.frame_limit) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    running = False

            if not running:
                break

            screen.fill(config.background_color)
            pygame.display.flip()
            pygame.display.set_caption(f"{config.title} | dt: {delta_time:.3f} s")
    finally:
        pygame.quit()
