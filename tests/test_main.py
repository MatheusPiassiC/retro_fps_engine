"""Seleção de arquivo e diagnóstico da demonstração antes da janela."""

import subprocess
import sys
from pathlib import Path

import pygame
import pytest

from retro_fps import engine
from retro_fps.__main__ import main
from retro_fps.player import MovementConfig
from retro_fps.renderer import WALL_X_COLOR

MAPS = Path(__file__).resolve().parents[1] / "maps"


@pytest.mark.parametrize(
    "filename, size, position",
    [
        ("room.map", (5, 5), (2.5, 2.5)),
        ("corridor.map", (8, 5), (1.5, 1.5)),
    ],
)
def test_cli_forwards_map_and_same_movement_configuration(
    monkeypatch, filename, size, position
):
    calls = []
    monkeypatch.setattr(engine, "run", lambda **kwargs: calls.append(kwargs))
    main([str(MAPS / filename)])
    assert len(calls) == 1
    call = calls[0]
    assert (call["world"].width, call["world"].height) == size
    assert call["player"].position == position
    assert call["player"].angle == 0
    assert call["movement_config"] == MovementConfig()


@pytest.mark.parametrize(
    "arguments, code", [([], 2), (["--help"], 0), (["--invalido"], 2)]
)
def test_cli_usage_does_not_start_engine(monkeypatch, capsys, arguments, code):
    def unexpected(**kwargs):
        pytest.fail("Não deve abrir sessão para ajuda ou argumentos inválidos.")

    monkeypatch.setattr(engine, "run", unexpected)
    with pytest.raises(SystemExit) as error:
        main(arguments)
    assert error.value.code == code
    output = capsys.readouterr()
    assert "MAPA" in output.out + output.err


@pytest.mark.parametrize(
    "content",
    [
        None,
        "MAP\n111\n101\n111\nPLAYER 0.5 1.5 0",
        "MAP\n111\n10\n111\nPLAYER 1.5 1.5 0",
    ],
)
def test_cli_invalid_file_never_opens_window(tmp_path, monkeypatch, capsys, content):
    path = tmp_path / "erro.map"
    if content is not None:
        path.write_text(content, encoding="utf-8")

    def unexpected_init():
        pytest.fail("Mapa inválido deve falhar antes de inicializar display.")

    monkeypatch.setattr(pygame.display, "init", unexpected_init)
    with pytest.raises(SystemExit) as error:
        main([str(path)])
    assert error.value.code == 2
    message = capsys.readouterr().err
    assert str(path) in message
    assert "Traceback" not in message


@pytest.mark.parametrize("filename", ["room.map", "corridor.map"])
def test_cli_renders_shipped_map_and_exits_with_real_event(filename, monkeypatch):
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    frames = []

    def flip():
        frames.append(pygame.display.get_surface().copy())
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    monkeypatch.setattr(pygame.display, "flip", flip)
    try:
        main([str(MAPS / filename)])
        assert len(frames) == 1
        assert frames[0].get_size() == (640, 480)
        # O raio central encontra uma face vertical em ambos os arquivos;
        # no meio da imagem deve haver parede, não apenas piso ou fundo.
        assert frames[0].get_at((320, 240))[:3] == WALL_X_COLOR
        assert not pygame.display.get_init()
    finally:
        pygame.quit()


def test_module_help_and_bad_path_work_from_another_directory(tmp_path):
    for args, expected in [(["--help"], 0), ([str(tmp_path / "ausente.map")], 2)]:
        result = subprocess.run(
            [sys.executable, "-m", "retro_fps", *args],
            cwd=tmp_path,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == expected
        assert "pygame" not in result.stdout.lower()
        assert "Traceback" not in result.stderr
