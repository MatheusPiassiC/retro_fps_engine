"""Confira a geometria da sala de estudo pelo desenho previsto em M1."""

from retro_fps.study_world import create_study_world


def test_study_room_dimensions():
    world = create_study_world()
    assert world.width == 5
    assert world.height == 5


def test_study_room_has_solid_border():
    world = create_study_world()
    # Dez células nas linhas superior/inferior e seis nas laterais.
    border = (
        [(x, 0) for x in range(5)]
        + [(x, 4) for x in range(5)]
        + [(0, y) for y in range(1, 4)]
        + [(4, y) for y in range(1, 4)]
    )
    for x, y in border:
        assert world.cell_at(x, y) == 1, (x, y)


def test_study_room_has_free_interior():
    world = create_study_world()
    # O interior tem três colunas e três linhas: nove células livres.
    for y in range(1, 4):
        for x in range(1, 4):
            assert world.cell_at(x, y) == 0, (x, y)
