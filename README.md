# RetroFPS Engine

Projeto universitário de estudo para aprender a construir uma engine 2.5D em Python, com referência conceitual em Wolfenstein 3D.

A entrega mínima planejada é carregar um mapa externo e explorá-lo em primeira pessoa, com raycasting próprio e colisões. A engine deverá ser importável e reutilizável por aplicações diferentes; regras de jogo pertencem às aplicações.

## Estado atual

M0 e M1 concluídos no ambiente atual. M2 está em andamento, com M2-1 a M2-5 implementadas e aprovadas: o comando `python -m retro_fps` apresenta uma sala estática em perspectiva, com paredes em tons diferentes por orientação, teto e piso de cor sólida. O desenvolvedor confirmou a conferência visual de M2-5. A janela padrão mede 640 × 480; a imagem interna de 320 × 200 é ampliada para 640 × 400, centralizada com faixas pretas acima e abaixo. Escape ou o botão de fechar encerram a aplicação.

Ainda não há movimento, colisões ou carregador de mapas. Os arquivos em `maps/` são exemplos da sintaxe proposta; a sala atual é construída em memória. M2-6 fará a comparação controlada entre sala e corredor.

## Documentação

- [Missão](docs/missao.md)
- [Roadmap para revisão](docs/roadmap.md)
- [GitHub Flow, branches, marcos e tarefas](docs/fluxo_desenvolvimento.md)
- [Pilha tecnológica](docs/pilha_tecnologica.md)
- [Arquitetura e responsabilidades](docs/arquitetura.md)
- [Formato de mapa e coordenadas](docs/formato_mapa.md)
- [Validação explicada](docs/validacao.md)
- [Uso de IA e aprendizagem](docs/uso_ia.md)

## Preparação do ambiente

Python 3.12 é a versão de referência. Em M0-2 foram conferidas as versões instaladas no ambiente existente com Python 3.12.3 e Pop!_OS 24.04 LTS. Consulte o [registro do ambiente](docs/validacao.md#7-m0-2--versões-do-ambiente) para as evidências e limitações.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m retro_fps
```

No Windows, a ativação do ambiente usa `.venv\Scripts\Activate.ps1` no PowerShell. A instalação exige acesso ao índice de pacotes. O último comando abre a sala estática e exige uma sessão gráfica disponível. Escape ou o botão de fechar encerram a aplicação.

### Instalação com as versões registradas

O arquivo [requirements-dev.txt](requirements-dev.txt) registra as versões das dependências instaladas em M0-2. Para usar essas versões, após criar e ativar o ambiente virtual conforme acima, substitua o comando de instalação por:

```sh
python -m pip install -c requirements-dev.txt -e '.[dev]'
```

O `pyproject.toml` define as dependências e os intervalos de compatibilidade; `-c` restringe a instalação às versões registradas. O pacote local continua editável. Python, pip e ferramentas usadas na construção do pacote não são fixados por esse arquivo.

Estas são instruções de reprodução; a instalação em um ambiente novo não foi executada em M0-2, por decisão do desenvolvedor.

### Configuração inicial

`WindowConfig`, em `retro_fps.config`, reúne dimensões em pixels, título, limite de quadros por segundo e cor RGB (três canais de 0 a 255). Os padrões são 640 × 480, título `RetroFPS Engine`, limite de 60 quadros por segundo e fundo azul `(40, 80, 120)`.

A chamada `run()` sem dados de cena preserva o modo anterior de fundo sólido. É possível fornecer outra configuração sem editar a coordenação:

```python
from retro_fps.config import WindowConfig
from retro_fps.engine import run

run(WindowConfig(width=800, height=600, frame_limit=30, background_color=(80, 40, 40)))
```

O título exibe `dt`, o intervalo medido em segundos, arredondado a três casas. O limite de frequência não garante uma taxa exata de quadros.

### Sala estática e resolução interna

`RenderConfig`, também em `retro_fps.config`, define `internal_width=320` e `internal_height=200`. Para apresentar a sala olhando para um canto:

```python
from math import pi
from retro_fps.camera import Camera
from retro_fps.config import RenderConfig
from retro_fps.engine import run
from retro_fps.study_world import create_study_world

run(
    world=create_study_world(),
    origin=(2.5, 2.5),
    camera=Camera(pi / 4),
    render_config=RenderConfig(),
)
```

Mundo, origem e câmera devem ser fornecidos juntos. A configuração de renderização exige uma cena. A ampliação preserva a proporção da imagem, usando faixas pretas no espaço restante. A cena fica parada; ainda não há controles de movimento.

## Verificação

```sh
python -m pytest
python -m ruff check .
python -m ruff format --check .
```

A suíte contém 201 casos: 17 de loop/configuração em `tests/test_engine.py`, cinco de desenho em `tests/test_renderer.py`, 29 de projeção em `tests/test_projection.py`, 46 de câmera em `tests/test_camera.py`, 81 de raios em `tests/test_raycasting.py`, 20 de mundo em `tests/test_world.py` e três da sala temporária em `tests/test_study_world.py`. Eles verificam dimensões, consultas, limites, imutabilidade, entradas inválidas, geometria da sala, cantos e saída dentro do orçamento de avanços. Esses resultados não validam os componentes ainda não implementados. As versões instaladas estão registradas em `requirements-dev.txt`; isso não comprova o funcionamento da engine.

## Próximo passo

Após integrar M2-4/M2-5 por PR, continuar M2-6: comparar sala e corredor com a geometria esperada. O contrato implementado de `World` está na [arquitetura](docs/arquitetura.md#11-mundo-implementado-em-m1-1). A demonstração de exploração será desenvolvida em `examples/exploration/`.
