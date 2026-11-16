# RetroFPS Engine

Projeto universitário de estudo para aprender a construir uma engine 2.5D em Python, com referência conceitual em Wolfenstein 3D.

A entrega mínima planejada é carregar um mapa externo e explorá-lo em primeira pessoa, com raycasting próprio e colisões. A engine deverá ser importável e reutilizável por aplicações diferentes; regras de jogo pertencem às aplicações.

## Estado atual

M0, M1, M2 e M3 concluídos no ambiente atual: o comando `python -m retro_fps` apresenta uma sala em perspectiva com movimento com colisões, com paredes em tons diferentes por orientação, teto e piso de cor sólida. O desenvolvedor confirmou as conferências visuais da sala e do corredor em M2-5/M2-6. A janela padrão mede 640 × 480; a imagem interna de 320 × 200 é ampliada para 640 × 400, centralizada com faixas pretas acima e abaixo. Escape ou o botão de fechar encerram a aplicação.

M3 concluído com testes e conferência visual de navegação na sala, corredor e cenário com obstáculo confirmada pelo desenvolvedor. O carregador de mapas está implementado e testado, sem conferência manual de M4 ainda; o comando principal continua usando a sala em memória até a integração de M4-5/M4-6. Os arquivos em `maps/` seguem a sintaxe documentada. A comparação controlada entre sala e corredor foi concluída em M2-6.

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

No Windows, a ativação do ambiente usa `.venv\Scripts\Activate.ps1` no PowerShell. A instalação exige acesso ao índice de pacotes. O último comando abre a sala com movimento e colisões e exige uma sessão gráfica disponível. Escape ou o botão de fechar encerram a aplicação.

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

Mundo, origem e câmera devem ser fornecidos juntos. A configuração de renderização exige uma cena. A ampliação preserva a proporção da imagem, usando faixas pretas no espaço restante. Essa chamada preserva a cena estática. O comando principal usa o modo móvel descrito abaixo.

### Movimento e colisões — M3

`python -m retro_fps` usa W/S para avançar/recuar, A/D para deslocar lateralmente e setas esquerda/direita para girar. Manter uma tecla pressionada mantém o comando; teclas opostas se cancelam. Velocidades padrão: 1 unidade/s e pi/2 rad/s. O mouse ainda não tem função. A diagonal mantém a mesma velocidade total do movimento reto; A/D não alteram o ângulo. A extensão WASD está implementada e testada, com conferência manual confirmada pelo desenvolvedor.

O jogador ocupa um círculo de raio padrão 0.2 unidade. Paredes e limites bloqueiam o círculo; resolver x e depois y permite deslizar. Um eixo bloqueado conserva a coordenada anterior, podendo deixar pequena folga. O início deve acomodar o círculo sem contato.

Cada atualização usa no máximo 0.1 segundo, descartando o excedente também para o giro. O deslocamento é subdividido em passos de até min(0.1, raio) unidade. Isso reduz saltos sobre paredes; não é detecção contínua de colisões. Girar e mover simultaneamente continua sendo uma aproximação dependente da subdivisão temporal.

```python
from retro_fps.engine import run
from retro_fps.player import PlayerState, MovementConfig
from retro_fps.study_world import create_study_world

run(
    world=create_study_world(),
    player=PlayerState((2.5, 2.5), 0),
    movement_config=MovementConfig(),
)
```

O modo móvel exige mundo e jogador, sem `origin` ou `camera` separados. `field_of_view` pode configurar a visão horizontal em radianos (padrão pi/3); ele e `movement_config` exigem jogador. A posição e o ângulo do jogador alimentam o desenho a cada quadro.

## Verificação

```sh
python -m pytest
python -m ruff check .
python -m ruff format --check .
```

A suíte contém 475 casos de mundo, sala, raios, câmera, projeção, desenho, loop, comandos, movimento e colisões. Há verificações de volume, contato, cantos, deslizamento, descarte de tempo e subdivisão espacial. Os testes automatizados são distintos da conferência visual confirmada pelo desenvolvedor; M3-7 consolidou aproximações oblíquas, cantos, movimentos grandes, limites e percursos. As versões instaladas estão registradas em `requirements-dev.txt`.

## Próximo passo

Após integrar M3-7 por PR, iniciar o planejamento de M4: carregamento e validação de mapas externos. O contrato implementado de `World` está na [arquitetura](docs/arquitetura.md#11-mundo-implementado-em-m1-1). A demonstração de exploração será desenvolvida em `examples/exploration/`.
