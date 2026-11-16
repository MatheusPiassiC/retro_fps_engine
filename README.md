# RetroFPS Engine

Projeto universitário de estudo para aprender a construir uma engine 2.5D em Python, com referência conceitual em Wolfenstein 3D.

A entrega mínima planejada é carregar um mapa externo e explorá-lo em primeira pessoa, com raycasting próprio e colisões. A engine deverá ser importável e reutilizável por aplicações diferentes; regras de jogo pertencem às aplicações.

## Estado atual

M0 concluído no ambiente atual: a entrada do pacote abre uma janela de 640 × 480 pixels com fundo azul e intervalo entre quadros em segundos no título. Escape ou o botão de fechar encerram a aplicação. O desenvolvedor confirmou a conferência visual de M0-3 e da entrega conjunta M0-4 e M0-5. M1 concluído no ambiente atual: M1-1 implementou a representação do mundo e consultas de células; M1-2 acrescentou uma sala temporária 5 × 5 em memória. As duas tarefas têm testes comportamentais e aprovação do desenvolvedor. M1-3/M1-4 implementaram consultas de raios sem dependência gráfica, aprovadas pelo desenvolvedor. M1-5 consolidou cantos e limite de avanços, também com aprovação. M1-6 revisou os testes e as explicações, com validação final confirmada pelo desenvolvedor. Ainda não há renderização de mapas, movimento ou carregador. Os mapas são exemplos da sintaxe proposta.

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

No Windows, a ativação do ambiente usa `.venv\Scripts\Activate.ps1` no PowerShell. A instalação exige acesso ao índice de pacotes. O último comando abre a janela inicial e exige uma sessão gráfica disponível. Escape ou o botão de fechar encerram a aplicação.

### Instalação com as versões registradas

O arquivo [requirements-dev.txt](requirements-dev.txt) registra as versões das dependências instaladas em M0-2. Para usar essas versões, após criar e ativar o ambiente virtual conforme acima, substitua o comando de instalação por:

```sh
python -m pip install -c requirements-dev.txt -e '.[dev]'
```

O `pyproject.toml` define as dependências e os intervalos de compatibilidade; `-c` restringe a instalação às versões registradas. O pacote local continua editável. Python, pip e ferramentas usadas na construção do pacote não são fixados por esse arquivo.

Estas são instruções de reprodução; a instalação em um ambiente novo não foi executada em M0-2, por decisão do desenvolvedor.

### Configuração inicial

`WindowConfig`, em `retro_fps.config`, reúne dimensões em pixels, título, limite de quadros por segundo e cor RGB (três canais de 0 a 255). Os padrões são 640 × 480, título `RetroFPS Engine`, limite de 60 quadros por segundo e fundo azul `(40, 80, 120)`.

É possível fornecer outra configuração sem editar a coordenação:

```python
from retro_fps.config import WindowConfig
from retro_fps.engine import run

run(WindowConfig(width=800, height=600, frame_limit=30, background_color=(80, 40, 40)))
```

O título exibe `dt`, o intervalo medido em segundos, arredondado a três casas. O limite de frequência não garante uma taxa exata de quadros.

## Verificação

```sh
python -m pytest
python -m ruff check .
python -m ruff format --check .
```

A suíte contém 104 casos: 81 de raios em `tests/test_raycasting.py`, 20 de mundo em `tests/test_world.py` e três da sala temporária em `tests/test_study_world.py`. Eles verificam dimensões, consultas, limites, imutabilidade, entradas inválidas, geometria da sala, cantos e saída dentro do orçamento de avanços. Esses resultados não validam os componentes ainda não implementados. As versões instaladas estão registradas em `requirements-dev.txt`; isso não comprova o funcionamento da engine.

## Próximo passo

Após integrar M1-6 por PR, iniciar M2-1: direção da câmera e plano perpendicular para a primeira imagem em perspectiva. O contrato implementado de `World` está na [arquitetura](docs/arquitetura.md#11-mundo-implementado-em-m1-1). A demonstração de exploração será desenvolvida em `examples/exploration/`.
