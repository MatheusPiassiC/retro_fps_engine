"""Geometria e percursos dos arquivos reais, sem alterar os cenários de estudo."""

from pathlib import Path

import pytest

from retro_fps.map_loader import load_map
from retro_fps.player import MovementCommand, MovementConfig, update_player_in_world
from retro_fps.raycasting import cast_ray

MAPS = Path(__file__).resolve().parents[1] / "maps"


@pytest.mark.parametrize(
    "filename, cell, depth", [("room.map", (4, 2), 1.5), ("corridor.map", (7, 1), 5.5)]
)
def test_file_start_has_known_east_wall(filename, cell, depth):
    data = load_map(MAPS / filename)
    hit = cast_ray(data.world, data.player.position, (1, 0))
    assert (hit.cell_x, hit.cell_y) == cell
    assert hit.parameter == pytest.approx(depth)


def test_corridor_routes_have_clearance_for_player_circle():
    config = MovementConfig()
    data = load_map(MAPS / "corridor.map", movement_config=config)
    state = data.player
    # Topo até a direita, desce e volta; depois explora o ramal inferior esquerdo.
    segments = [
        (MovementCommand(1), 50, (6.5, 1.5)),
        (MovementCommand(strafe=1), 20, (6.5, 3.5)),
        (MovementCommand(-1), 10, (5.5, 3.5)),
        (MovementCommand(1), 10, (6.5, 3.5)),
        (MovementCommand(strafe=-1), 20, (6.5, 1.5)),
        (MovementCommand(-1), 50, (1.5, 1.5)),
        (MovementCommand(strafe=1), 20, (1.5, 3.5)),
        (MovementCommand(1), 20, (3.5, 3.5)),
    ]
    for command, count, expected in segments:
        for _ in range(count):
            state = update_player_in_world(data.world, state, command, config, 0.1)
        # Cada chamada solicita 0.1 unidade; os trechos seguem centros de células.
        assert state.position == pytest.approx(expected, abs=1e-12)
        assert state.angle == 0


def test_edited_file_changes_known_ray_after_reload(tmp_path):
    path = tmp_path / "editavel.map"
    path.write_bytes((MAPS / "room.map").read_bytes())
    before = load_map(path)
    # Nova parede na célula (3,2), face x=3 a 0.5 da origem x=2.5.
    lines = path.read_text(encoding="utf-8").splitlines()
    lines[3] = "10011"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    after = load_map(path)
    assert cast_ray(
        before.world, before.player.position, (1, 0)
    ).parameter == pytest.approx(1.5)
    assert cast_ray(
        after.world, after.player.position, (1, 0)
    ).parameter == pytest.approx(0.5)
