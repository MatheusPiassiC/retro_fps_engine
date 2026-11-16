# Orientações para assistência ao projeto

## Objetivo

Este é um projeto universitário de aprendizagem. Não presumir conhecimento prévio de computação gráfica. Explicar os conceitos e os resultados esperados com exemplos pequenos antes de incorporar algoritmos centrais.

## Escopo e arquitetura

- Seguir `docs/roadmap.md`; M0 foi concluído no ambiente atual; M1 está em andamento, com M1-1 a M1-5 implementadas, testadas e aprovadas pelo desenvolvedor; M1-6 permanece pendente.
- Usar Wolfenstein 3D como referência conceitual, dentro dos limites de `docs/missao.md`.
- Manter regras de jogo fora de `src/retro_fps/`. O núcleo não importa exemplos.
- Manter mundo, carregamento, raycasting e colisões independentes da inicialização gráfica.
- Não adicionar engines prontas, bibliotecas de raycasting ou novas dependências sem justificativa concreta.
- Evitar abstrações antecipadas e alterações extensas que dificultem a revisão.

## Convenções

- Documentação e explicações em português; identificadores Python em inglês.
- Coordenadas, unidades, ângulos e volume seguem `docs/formato_mapa.md` e `docs/arquitetura.md`.
- Novas decisões devem explicitar se são propostas ou comportamentos implementados.
- Manter mudanças pequenas e atualizar documentos afetados, sem duplicar especificações.

## Fluxo de desenvolvimento

- Seguir GitHub Flow conforme `docs/fluxo_desenvolvimento.md`, com branches curtas por feature ou mudança coesa e integração por PR.
- Identificar tarefas e atualizações pelo código local do roadmap: `M0-1` é a primeira tarefa do Marco 0; `M0-2` é a segunda.
- As issues são apenas descrições locais de tarefas; não exigir criação de issues ou milestones no GitHub. Os códigos locais não representam números do GitHub.
- Usar branches como `feat/m0-3-create-pygame-window` e referências como `[M0-3]` em commits e PRs.
- Nos nomes de branch, usar `<tipo>/m<marco>-<tarefa>-<descricao-em-ingles>`, com `m` minúsculo e descrição específica em inglês, com palavras minúsculas separadas por hífens, sem espaços, sublinhados, parênteses ou colchetes.
- Para reunir tarefas do mesmo marco em uma mudança coesa, listar seus números em ordem crescente: `feat/m0-4-5-add-frame-timing-and-window-config`. Os números indicam tarefas incluídas, não um intervalo. Usar referências explícitas como `[M0-4, M0-5]` em commits que abranjam ambas e no PR, conforme `docs/fluxo_desenvolvimento.md`.
- Antes da integração, conferir critérios da tarefa, verificações pertinentes e documentação. Registrar referências no histórico de aprendizado e validação.

## Verificação

Após instalar o ambiente conforme o README, usar `python -m pytest`, `python -m ruff check .` e `python -m ruff format --check .` conforme o escopo da mudança.

O ciclo da janela, a configuração inicial, o desenho de cor sólida, as consultas do mundo, a sala temporária em memória e o percurso de raios estão implementados; os demais módulos permanecem esqueleto. A suíte contém testes comportamentais de mundo e da sala temporária e de raios em `tests/test_world.py`, `tests/test_study_world.py` e `tests/test_raycasting.py`. Não declarar funcionalidades validadas por verificar apenas imports ou sintaxe. Ao implementar, explicar por que o resultado de cada teste relevante é esperado, usando casos independentes do algoritmo.

Registrar contribuições relevantes de IA em `docs/uso_ia.md`. Não tratar desconhecimento do desenvolvedor como aprovação automática de decisões.
