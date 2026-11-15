"""Ciclo inicial da aplicação; a coordenação da sessão evoluirá em M0–M5."""

import pygame


def run() -> None:
    """Abra a janela e processe eventos até receber um pedido de encerramento."""
    try:
        pygame.display.init()
        pygame.display.set_mode((640, 480))
        pygame.display.set_caption("RetroFPS Engine")
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    running = False

            # Evite que a espera por eventos ocupe continuamente um núcleo da CPU.
            clock.tick(60)
    finally:
        pygame.quit()
