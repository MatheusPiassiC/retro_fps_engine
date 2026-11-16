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


@pytest.mark.parametrize(
    "pressed, expected",
    [
        ((), (0, 0)),
        ((pygame.K_w,), (1, 0)),
        ((pygame.K_s,), (-1, 0)),
        ((pygame.K_LEFT,), (0, -1)),
        ((pygame.K_RIGHT,), (0, 1)),
        ((pygame.K_w, pygame.K_LEFT), (1, -1)),
        ((pygame.K_w, pygame.K_s, pygame.K_LEFT, pygame.K_RIGHT), (0, 0)),
    ],
)
def test_keyboard_translates_to_logical_command(monkeypatch, pressed, expected):
    from collections import defaultdict

    keys = defaultdict(bool, {key: True for key in pressed})
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: keys)
    command = engine.read_movement_command()
    assert (command.forward, command.turn) == expected


@pytest.mark.parametrize("event_type", [pygame.QUIT, pygame.KEYDOWN])
def test_mobile_scene_updates_from_held_keys_then_stops_on_release(
    dummy_display, monkeypatch, event_type
):
    from collections import defaultdict
    from math import pi

    from retro_fps.player import MovementConfig, PlayerState
    from retro_fps.study_world import create_study_world

    class Clock:
        def tick(self, frame_limit):
            return 100  # 100 ms = 0.1 s, determinado sem depender do relógio real.

    frames = []
    key_reads = []
    original_render = engine.render_scene

    def keys():
        key_reads.append(True)
        # Dois quadros pressionados; no terceiro, teclas soltas.
        return defaultdict(
            bool, {pygame.K_w: len(frames) < 2, pygame.K_RIGHT: len(frames) < 2}
        )

    def render(surface, world, origin, camera):
        frames.append((origin, camera.angle, camera.field_of_view))
        original_render(surface, world, origin, camera)

    def flip():
        if len(frames) == 3:
            attributes = (
                {"key": pygame.K_ESCAPE} if event_type == pygame.KEYDOWN else {}
            )
            pygame.event.post(pygame.event.Event(event_type, attributes))

    monkeypatch.setattr(pygame.time, "Clock", Clock)
    monkeypatch.setattr(pygame.key, "get_pressed", keys)
    monkeypatch.setattr(engine, "render_scene", render)
    monkeypatch.setattr(pygame.display, "flip", flip)
    initial = PlayerState((2.5, 2.5), 0)
    engine.run(
        world=create_study_world(),
        player=initial,
        movement_config=MovementConfig(move_speed=1, turn_speed=5 * pi),
        field_of_view=pi / 2,
    )
    # Primeiro gira 90 graus e avança 0.1 ao sul; depois 90 graus e 0.1 a oeste.
    assert len(frames) == len(key_reads) == 3
    assert frames[0][0] == pytest.approx((2.5, 2.6), abs=1e-12)
    assert frames[0][1] == pytest.approx(pi / 2)
    assert frames[1][0] == pytest.approx((2.4, 2.6), abs=1e-12)
    assert frames[1][1] == pytest.approx(pi)
    assert frames[2] == frames[1]
    assert all(frame[2] == pi / 2 for frame in frames)
    assert initial == PlayerState((2.5, 2.5), 0)
    assert not pygame.display.get_init()


@pytest.mark.parametrize(
    "case", ["no_world", "origin", "camera", "config_only", "fov_only", "invalid_fov"]
)
def test_invalid_mobile_scene_is_rejected_before_display(monkeypatch, case):
    from retro_fps.player import MovementConfig, PlayerState

    kwargs = {"world": World([[0]]), "player": PlayerState((0.5, 0.5), 0)}
    if case == "no_world":
        del kwargs["world"]
    elif case == "origin":
        kwargs["origin"] = (0.5, 0.5)
    elif case == "camera":
        kwargs["camera"] = Camera(0)
    elif case == "config_only":
        kwargs = {"movement_config": MovementConfig()}
    elif case == "fov_only":
        kwargs = {"field_of_view": 1}
    else:
        kwargs["field_of_view"] = 0

    def unexpected_init():
        pytest.fail("Display não deve iniciar para parâmetros móveis inválidos.")

    monkeypatch.setattr(pygame.display, "init", unexpected_init)
    with pytest.raises(ValueError):
        engine.run(**kwargs)
