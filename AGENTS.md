# Orientações para assistência ao projeto

## Objetivo

Este é um projeto universitário de aprendizagem. Não presumir conhecimento prévio de computação gráfica. Explicar os conceitos e os resultados esperados com exemplos pequenos antes de incorporar algoritmos centrais.

## Escopo e arquitetura

- Seguir `docs/roadmap.md`; o planejamento está em revisão e a implementação ainda não começou.
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

## Verificação

Após instalar o ambiente conforme o README, usar `python -m pytest`, `python -m ruff check .` e `python -m ruff format --check .` conforme o escopo da mudança.

Os módulos atuais são esqueleto; não há testes comportamentais. Não declarar funcionalidades validadas por verificar apenas imports ou sintaxe. Ao implementar, explicar por que o resultado de cada teste relevante é esperado, usando casos independentes do algoritmo.

Registrar contribuições relevantes de IA em `docs/uso_ia.md`. Não tratar desconhecimento do desenvolvedor como aprovação automática de decisões.
