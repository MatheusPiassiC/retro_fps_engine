"""Análise de mapas externos, sem inicializar recursos gráficos."""

import re
from dataclasses import dataclass
from math import isfinite, radians

from retro_fps.collision import can_occupy
from retro_fps.player import MovementConfig, PlayerState
from retro_fps.world import World


class MapLoadError(ValueError):
    """Erro de mapa com origem e linha, quando a falha é localizável."""

    def __init__(self, message: str, *, source: str, line: int | None = None):
        self.source = source
        self.line = line
        self.message = message
        location = source if line is None else f"{source}:{line}"
        super().__init__(f"{location}: {message}")


@dataclass(frozen=True)
class MapData:
    """Mundo e início validados, sem estado de janela ou regras de jogo."""

    world: World
    player: PlayerState


_NUMBER = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")


def parse_map(
    text: str,
    *,
    movement_config: MovementConfig | None = None,
    source: str = "<texto>",
) -> MapData:
    """Analise a sintaxe MAP/grade/PLAYER e valide o volume inicial.

    Aceita LF ou CRLF e uma quebra final opcional; não remove espaços
    das linhas da grade nem corrige bordas ou posições inválidas.
    O ângulo do arquivo é em graus e o estado retornado usa radianos.
    """
    if movement_config is None:
        movement_config = MovementConfig()
    lines = text.replace("\r\n", "\n").split("\n")
    if lines[-1] == "":
        lines.pop()
    if not lines or lines[0] != "MAP":
        raise MapLoadError(
            "A primeira linha deve ser exatamente MAP.", source=source, line=1
        )

    rows = []
    player_line = None
    for number, content in enumerate(lines[1:], start=2):
        if content.startswith("PLAYER"):
            player_line = number
            if number != len(lines):
                raise MapLoadError(
                    "Não é permitido conteúdo após PLAYER.",
                    source=source,
                    line=number + 1,
                )
            break
        if not content or any(cell not in "01" for cell in content):
            raise MapLoadError(
                "A grade deve conter apenas 0 e 1, sem espaços ou linhas vazias.",
                source=source,
                line=number,
            )
        if rows and len(content) != len(rows[0]):
            raise MapLoadError(
                "As linhas da grade devem ter a mesma largura.",
                source=source,
                line=number,
            )
        rows.append(content)

    if player_line is None:
        raise MapLoadError(
            "Falta a linha PLAYER x y angulo.", source=source, line=len(lines) + 1
        )
    if len(rows) < 3 or len(rows[0]) < 3:
        raise MapLoadError(
            "A grade deve ter pelo menos 3 linhas e 3 colunas.", source=source, line=2
        )
    for number, row in enumerate(rows, start=2):
        is_edge = number == 2 or number == player_line - 1
        if (is_edge and "0" in row) or row[0] != "1" or row[-1] != "1":
            raise MapLoadError(
                "A borda externa deve ser inteiramente sólida.",
                source=source,
                line=number,
            )

    # Apenas espaços ASCII separam os campos; não aceitar tabs ou comentários.
    match = re.fullmatch(r"PLAYER +([^ ]+) +([^ ]+) +([^ ]+)", lines[player_line - 1])
    if match is None:
        raise MapLoadError(
            "Use PLAYER x y angulo, com quatro campos separados por espaços.",
            source=source,
            line=player_line,
        )
    values = match.groups()
    if not all(_NUMBER.fullmatch(value) for value in values):
        raise MapLoadError(
            "PLAYER exige três números decimais finitos com ponto, sem comentários.",
            source=source,
            line=player_line,
        )
    x, y, angle = (float(value) for value in values)
    if not all(isfinite(value) for value in (x, y, angle)):
        raise MapLoadError(
            "Os valores de PLAYER devem ser finitos.", source=source, line=player_line
        )

    world = World([[int(cell) for cell in row] for row in rows])
    if not can_occupy(world, (x, y), movement_config.radius):
        raise MapLoadError(
            "O início deve acomodar o círculo sem tocar paredes ou sair do mapa.",
            source=source,
            line=player_line,
        )
    return MapData(world, PlayerState((x, y), radians(angle % 360)))
