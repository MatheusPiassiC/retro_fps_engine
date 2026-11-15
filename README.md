# RetroFPS Engine

Projeto universitário de estudo para aprender a construir uma engine 2.5D em Python, com referência conceitual em Wolfenstein 3D.

A entrega mínima planejada é carregar um mapa externo e explorá-lo em primeira pessoa, com raycasting próprio e colisões. A engine deverá ser importável e reutilizável por aplicações diferentes; regras de jogo pertencem às aplicações.

## Estado atual

Planejamento revisado para avaliação e estrutura inicial preparada. Os módulos contêm apenas descrições de responsabilidade. Ainda não há janela, renderização, movimento, carregador ou testes comportamentais implementados. Os mapas são exemplos da sintaxe proposta.

## Documentação

- [Missão](docs/missao.md)
- [Roadmap para revisão](docs/roadmap.md)
- [GitHub Flow, branches, marcos e issues](docs/fluxo_desenvolvimento.md)
- [Pilha tecnológica](docs/pilha_tecnologica.md)
- [Arquitetura e responsabilidades](docs/arquitetura.md)
- [Formato de mapa e coordenadas](docs/formato_mapa.md)
- [Validação explicada](docs/validacao.md)
- [Uso de IA e aprendizagem](docs/uso_ia.md)

## Preparação do ambiente

Python 3.12 é a versão de referência proposta. A compatibilidade e as versões instaladas serão verificadas em M0.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m retro_fps
```

No Windows, a ativação do ambiente usa `.venv\Scripts\Activate.ps1` no PowerShell. A instalação exige acesso ao índice de pacotes. O último comando atualmente exibe apenas uma mensagem informando o estado do projeto.

## Verificação

```sh
python -m pytest
python -m ruff check .
python -m ruff format --check .
```

Ainda não existem testes da engine. A ausência de testes não representa aprovação do funcionamento. O registro reproduzível de versões será criado após a validação do ambiente em M0.

## Próximo passo

Revisar o roadmap e, em seguida, implementar M0: ambiente verificado, janela responsiva e encerramento normal. A demonstração de exploração será desenvolvida em `examples/exploration/`.
