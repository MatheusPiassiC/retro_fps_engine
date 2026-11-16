"""Ciclo inicial da aplicação; a coordenação da sessão evoluirá em M0–M5."""

from math import pi

import pygame

from retro_fps.camera import Camera
from retro_fps.collision import can_occupy
from retro_fps.config import RenderConfig, WindowConfig
from retro_fps.player import (
    MovementCommand,
    MovementConfig,
    PlayerState,
    update_player_in_world,
)
from retro_fps.renderer import render_scene
from retro_fps.world import World


def run(
    config: WindowConfig | None = None,
    *,
    world: World | None = None,
    origin: tuple[float, float] | None = None,
    camera: Camera | None = None,
    render_config: RenderConfig | None = None,
    player: PlayerState | None = None,
    movement_config: MovementConfig | None = None,
    field_of_view: float | None = None,
) -> None:
    """Apresente cena estática, movimento com colisões ou fundo sólido.

    No modo móvel, forneça mundo e jogador; origem e câmera são derivadas
    do estado a cada quadro. O círculo inicial deve caber sem contato.
    """
    if player is not None:
        if world is None or origin is not None or camera is not None:
            raise ValueError(
                "Jogador exige mundo e não aceita origem ou câmera separadas."
            )
        if movement_config is None:
            movement_config = MovementConfig()
        if field_of_view is None:
            field_of_view = pi / 3
        Camera(player.angle, field_of_view)  # Valida antes de inicializar o display.
        if not can_occupy(world, player.position, movement_config.radius):
            raise ValueError("A posição inicial deve acomodar o círculo sem contato.")
        has_scene = True
    else:
        if movement_config is not None or field_of_view is not None:
            raise ValueError(
                "Configuração de movimento e campo de visão exigem jogador."
            )
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

            if player is not None:
                command = read_movement_command()
                player = update_player_in_world(
                    world, player, command, movement_config, delta_time
                )
                origin = player.position
                camera = Camera(player.angle, field_of_view)

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


def read_movement_command() -> MovementCommand:
    """Traduza teclas mantidas pressionadas; comandos opostos se cancelam."""
    keys = pygame.key.get_pressed()
    return MovementCommand(
        forward=int(keys[pygame.K_w]) - int(keys[pygame.K_s]),
        turn=int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]),
        strafe=int(keys[pygame.K_d]) - int(keys[pygame.K_a]),
    )
