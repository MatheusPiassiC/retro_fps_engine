"""Integração do loop com display dummy e eventos reais na fila."""

import pygame
import pytest

from retro_fps import engine
from retro_fps.camera import Camera
from retro_fps.config import RenderConfig, WindowConfig
from retro_fps.renderer import CEILING_COLOR, FLOOR_COLOR
from retro_fps.world import World


@pytest.fixture
def dummy_display(monkeypatch):
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    yield
    pygame.quit()


@pytest.mark.parametrize("event_type", [pygame.QUIT, pygame.KEYDOWN])
@pytest.mark.parametrize("with_scene", [False, True])
def test_frame_presentation_and_exit(
    dummy_display, monkeypatch, event_type, with_scene
):
    original_flip = pygame.display.flip
    original_render = engine.render_scene
    frames = []
    internal_sizes = []

    def render(surface, world, origin, camera):
        internal_sizes.append(surface.get_size())
        original_render(surface, world, origin, camera)

    def flip():
        screen = pygame.display.get_surface()
        frames.append(screen.copy())
        original_flip()
        attributes = {"key": pygame.K_ESCAPE} if event_type == pygame.KEYDOWN else {}
        pygame.event.post(pygame.event.Event(event_type, attributes))

    monkeypatch.setattr(engine, "render_scene", render)
    monkeypatch.setattr(pygame.display, "flip", flip)
    kwargs = (
        {"world": World([[0]]), "origin": (0.5, 0.5), "camera": Camera(0)}
        if with_scene
        else {}
    )
    engine.run(**kwargs)
    assert len(frames) == 1  # Não apresenta novo quadro após o evento de saída.
    assert not pygame.display.get_init()
    frame = frames[0]
    assert frame.get_size() == (640, 480)
    if with_scene:
        assert internal_sizes == [(320, 200)]
        for y, color in (
            (0, (0, 0, 0)),
            (39, (0, 0, 0)),
            (40, CEILING_COLOR),
            (239, CEILING_COLOR),
            (240, FLOOR_COLOR),
            (439, FLOOR_COLOR),
            (440, (0, 0, 0)),
            (479, (0, 0, 0)),
        ):
            for x in (0, 320, 639):
                assert frame.get_at((x, y))[:3] == color
    else:
        assert not internal_sizes
        assert frame.get_at((320, 240))[:3] == WindowConfig().background_color


@pytest.mark.parametrize(
    "kwargs",
    [
        {"world": World([[0]])},
        {"origin": (0.5, 0.5)},
        {"camera": Camera(0)},
        {"world": World([[0]]), "camera": Camera(0)},
        {"render_config": RenderConfig()},
    ],
)
def test_incomplete_scene_is_rejected_before_display(monkeypatch, kwargs):
    def unexpected_init():
        pytest.fail("Display não deve ser inicializado para cena incompleta.")

    monkeypatch.setattr(pygame.display, "init", unexpected_init)
    with pytest.raises(ValueError):
        engine.run(**kwargs)


@pytest.mark.parametrize("value", [0, -1, True, 320.0])
@pytest.mark.parametrize("name", ["internal_width", "internal_height"])
def test_render_dimensions_are_positive_integers(name, value):
    with pytest.raises(ValueError):
        RenderConfig(**{name: value})
