"""Ciclo inicial da aplicação; a coordenação da sessão evoluirá em M0–M5."""

import pygame

from retro_fps.camera import Camera
from retro_fps.config import RenderConfig, WindowConfig
from retro_fps.renderer import render_scene
from retro_fps.world import World


def run(
    config: WindowConfig | None = None,
    *,
    world: World | None = None,
    origin: tuple[float, float] | None = None,
    camera: Camera | None = None,
    render_config: RenderConfig | None = None,
) -> None:
    """Apresente uma cena estática ou, sem cena, o fundo sólido original."""
    scene_values = (world, origin, camera)
    has_scene = all(value is not None for value in scene_values)
    if any(value is not None for value in scene_values) and not has_scene:
        raise ValueError("Mundo, origem e câmera devem ser fornecidos juntos.")
    if render_config is not None and not has_scene:
        raise ValueError("A configuração de renderização exige uma cena.")
    if config is None:
        config = WindowConfig()

    try:
        pygame.display.init()
        screen = pygame.display.set_mode((config.width, config.height))
        internal_surface = None
        if has_scene:
            if render_config is None:
                render_config = RenderConfig()
            internal_surface = pygame.Surface(
                (render_config.internal_width, render_config.internal_height)
            )
            scale = min(
                config.width / render_config.internal_width,
                config.height / render_config.internal_height,
            )
            scaled_size = (
                max(1, int(render_config.internal_width * scale)),
                max(1, int(render_config.internal_height * scale)),
            )
            destination = (
                (config.width - scaled_size[0]) // 2,
                (config.height - scaled_size[1]) // 2,
            )
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

            if internal_surface is None:
                screen.fill(config.background_color)
            else:
                render_scene(internal_surface, world, origin, camera)
                screen.fill((0, 0, 0))
                screen.blit(
                    pygame.transform.scale(internal_surface, scaled_size), destination
                )
            pygame.display.flip()
            pygame.display.set_caption(f"{config.title} | dt: {delta_time:.3f} s")
    finally:
        pygame.quit()
