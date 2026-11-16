"""Mapas de texto com estrutura e geometria conhecidas sem abrir janela."""

from dataclasses import FrozenInstanceError
from math import pi

import pytest

from retro_fps.map_loader import MapLoadError, parse_map
from retro_fps.player import MovementConfig

ROOM = "MAP\n11111\n10001\n10001\n10001\n11111\nPLAYER 2.5 2.5 0"


@pytest.mark.parametrize("newline", ["\n", "\r\n"])
@pytest.mark.parametrize("final_newline", [False, True])
def test_parse_room_geometry_and_start(newline, final_newline):
    text = ROOM.replace("\n", newline) + (newline if final_newline else "")
    data = parse_map(text)
    assert (data.world.width, data.world.height) == (5, 5)
    assert sum(row.count(0) for row in data.world.grid) == 9
    assert data.player.position == (2.5, 2.5)
    assert data.player.angle == 0


@pytest.mark.parametrize(
    "degrees, expected", [(90, pi / 2), (-90, 3 * pi / 2), (450, pi / 2), (720, 0)]
)
def test_degrees_are_converted_and_normalized(degrees, expected):
    data = parse_map(ROOM.replace("PLAYER 2.5 2.5 0", f"PLAYER 2.5 2.5 {degrees}"))
    assert data.player.angle == pytest.approx(expected, abs=1e-12)


@pytest.mark.parametrize(
    "text, line, reason",
    [
        ("", 1, "MAP"),
        (ROOM.replace("MAP", "map", 1), 1, "MAP"),
        ("\ufeff" + ROOM, 1, "MAP"),
        (ROOM.replace("10001", "1001", 1), 3, "largura"),
        (ROOM.replace("10001", "10a01", 1), 3, "0 e 1"),
        (ROOM.replace("10001", " 10001", 1), 3, "0 e 1"),
        (ROOM.replace("10001", "10 01", 1), 3, "0 e 1"),
        (ROOM.replace("10001", "", 1), 3, "vazias"),
        (ROOM + "\n\n", 8, "após PLAYER"),
        (ROOM + "\nPLAYER 2.5 2.5 0", 8, "após PLAYER"),
        (ROOM + "\n11111", 8, "após PLAYER"),
        (ROOM.rsplit("\n", 1)[0], 7, "Falta"),
        ("MAP\nPLAYER 1.5 1.5 0", 2, "3 linhas"),
        ("MAP\n111\n111\nPLAYER 1.5 1.5 0", 2, "3 linhas"),
        ("MAP\n11\n11\n11\nPLAYER 1.5 1.5 0", 2, "3 linhas"),
        (ROOM.replace("11111", "11011", 1), 2, "borda"),
        (ROOM.replace("10001", "00001", 1), 3, "borda"),
        (ROOM.replace("10001", "10000", 1), 3, "borda"),
        (ROOM.replace("11111\nPLAYER", "11011\nPLAYER"), 6, "borda"),
    ],
)
def test_invalid_structure_reports_source_and_line(text, line, reason):
    with pytest.raises(MapLoadError) as error:
        parse_map(text, source="estudo.map")
    assert error.value.source == "estudo.map"
    assert error.value.line == line
    assert f"estudo.map:{line}:" in str(error.value)
    assert reason in str(error.value)


@pytest.mark.parametrize(
    "suffix",
    [
        "2.5 2.5",
        "2.5 2.5 0 extra",
        "2,5 2.5 0",
        "nan 2.5 0",
        "2.5 inf 0",
        "2.5 2.5 -inf",
        "1e999 2.5 0",
        "2.5 2.5 0 # comentário",
        "2_0 2.5 0",
        "2.5\t2.5 0",
        "2.5 2.5 0 ",
    ],
)
def test_invalid_player_fields(suffix):
    with pytest.raises(MapLoadError) as error:
        parse_map(ROOM.rsplit("\n", 1)[0] + "\nPLAYER " + suffix)
    assert error.value.line == 7


@pytest.mark.parametrize(
    "position", ["-1 2.5", "5 2.5", "0.5 2.5", "1.1 2.5", "1.2 2.5", "3.8 2.5"]
)
def test_spawn_outside_wall_or_touching_wall_is_rejected(position):
    with pytest.raises(MapLoadError, match="círculo"):
        parse_map(ROOM.replace("2.5 2.5 0", position + " 0"))


def test_spawn_uses_same_configured_radius_as_movement():
    text = ROOM.replace("2.5 2.5 0", "1.3 2.5 0")
    assert parse_map(
        text, movement_config=MovementConfig(radius=0.2)
    ).player.position == (1.3, 2.5)
    with pytest.raises(MapLoadError, match="círculo"):
        parse_map(text, movement_config=MovementConfig(radius=0.3))


def test_map_data_is_immutable():
    data = parse_map(ROOM)
    with pytest.raises(FrozenInstanceError):
        data.player = None


def test_minimum_map_and_decimal_scientific_notation():
    data = parse_map("MAP\n111\n101\n111\nPLAYER +1.5 1.5e0 9e1")
    assert data.world.width == data.world.height == 3
    assert data.player.angle == pytest.approx(pi / 2)
