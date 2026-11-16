# Estratégia de validação e aprendizado

## 1. Estado e princípio

Este documento reúne verificações propostas e evidências de M0, M1-1 e M1-2. A suíte contém testes comportamentais de mundo; ainda não há resultados de desempenho medidos. Cada teste deve dizer qual comportamento protege e por que o resultado esperado faz sentido.

Não se espera que o desenvolvedor já conheça computação gráfica. Antes de aceitar um teste, a implementação deverá vir acompanhada de uma explicação acessível e de um exemplo que possa ser conferido com desenho e contas simples.

## 2. Exemplo independente de raycasting

Considere esta sala, com índices de zero a quatro:

```text
11111
10001
10001
10001
11111
```

O centro `(2.5, 2.5)` fica no meio da sala. Um raio para leste tem direção `(1, 0)`. A parede à direita começa em `x = 4`; portanto, o percurso até ela mede `4 - 2.5 = 1.5`. O impacto pertence à célula `(4, 2)`.

Para oeste, norte e sul, a distância também é 1.5 nesta sala. Esses exemplos permitem conferir sinais, índices e direções sem depender de uma imagem renderizada.

O parâmetro de um raio não é sempre seu comprimento euclidiano: depende do tamanho de seu vetor de direção. Os testes deverão explicitar essa convenção. Um caso diagonal que atinge exatamente um canto deverá seguir a política de desempate definida em M1.

## 3. Casos por componente

| Componente | Verificações | Razão |
|---|---|---|
| Mundo | Dimensões, consultas e limites | Evitar trocar linha e coluna e acessar índices indevidos |
| Carregador | Exemplos válidos, sintaxe inválida, bordas abertas, NaN, infinito e spawn sem espaço | Impedir sessões com dados inconsistentes |
| DDA | Quatro direções, componente nula, direção negativa, canto, raio nulo e limite | Conferir percurso e término |
| Projeção | Dobrar profundidade reduz altura à metade antes do recorte | Conferir a relação inversa entre distância e tamanho aparente |
| Movimento | Intervalos distintos com mesmo tempo total, abaixo do limite | Conferir unidades e integração de velocidade |
| Colisão | Parede frontal, canto, deslizamento, contato e grande deslocamento | Conferir volume e evitar atravessamentos |
| Integração | Arquivo para mundo, início válido, comandos e sessão | Conferir contratos entre componentes |

Usar tolerâncias explícitas para números reais. Não exigir igualdade exata quando houver arredondamento. Preparar pequenos casos com resultados conhecidos, evitando gerar o resultado esperado com o mesmo algoritmo sob teste.

## 4. Inspeção visual

Conferir sala frontal, corredor, rotação, aproximação de paredes e navegação junto a cantos. Verificar que paredes correspondem ao mapa e que uma parede plana não parece curvada por erro de profundidade.

Testes matemáticos e inspeção visual se complementam. Testes gráficos automatizados por comparação de imagens ficam adiados até haver necessidade concreta.

## 5. Evidências por marco

Ao concluir um marco, acrescentar uma entrada com:

- Código local da tarefa (por exemplo, M0-2), branch ou PR quando disponíveis, e comando ou procedimento executado.
- Ambiente e configuração relevantes.
- Resultado esperado e observado.
- Explicação do resultado e limitações encontradas.

Se houver medição de FPS, registrar resolução interna, mapa, máquina e forma de medição. Uma medida isolada não comprova desempenho em todas as situações.

## 6. Comandos planejados

Após preparar o ambiente conforme o README:

```sh
python -m pytest
python -m ruff check .
python -m ruff format --check .
```

A pasta `tests/` contém os primeiros testes comportamentais, introduzidos em M1-1. Os registros de M0 preservam o resultado histórico de ausência de testes; as evidências de mundo e sala estão nas seções 10 e 11.

## 7. M0-2 — Versões do ambiente

- **Tarefa:** M0-2 — registrar versões efetivamente verificadas e instruções de reprodução.
- **Branch:** `chore/m0-2-document-verified-environment`.
- **Ambiente observado:** Pop!_OS 24.04 LTS, x86_64, kernel Linux `7.2.6-76070206-generic`, glibc 2.39, Python 3.12.3 e pip 24.0, no ambiente virtual `.venv`.
- **Procedimento:** leitura de `/etc/os-release`, consulta a `sys.version` e `platform.platform()`, execução de `python -m pip --version` e `python -m pip freeze --exclude-editable` usando o Python da `.venv`.
- **Resultado esperado:** o arquivo de versões corresponde às dependências instaladas, sem incluir o caminho do projeto editável.
- **Resultado observado:** o conteúdo de `requirements-dev.txt`, criado pelo desenvolvedor, coincide com a saída de `pip freeze --exclude-editable`.

| Pacote | Versão instalada |
|---|---|
| iniconfig | 2.3.1 |
| packaging | 26.3 |
| pluggy | 1.7.0 |
| pygame | 2.6.1 |
| Pygments | 2.21.0 |
| pytest | 9.2.0 |
| ruff | 0.17.5 |

As instruções de instalação com essas versões estão no README. O arquivo de versões é uma fotografia do ambiente existente; não fixa o interpretador, o sistema operacional ou todas as ferramentas de construção do pacote.

**Limitações:** por decisão do desenvolvedor, não foi criada outra `.venv` nem repetida a instalação em ambiente novo nesta tarefa. A conferência de versões não comprova compatibilidade com outras máquinas ou funcionamento da engine. Não foram executados pytest, Ruff ou `pip check` nesta atualização documental, e não são atribuídos resultados a esses comandos neste registro. A repetição da instalação em ambiente limpo continua prevista em M6.

## 8. M0-3 — Ciclo inicial da janela

- **Branch:** `feat/m0-3-create-pygame-window`.
- **Implementação:** `engine.run()` abre a janela e encerra com Escape ou `QUIT`; `finally` libera os recursos mesmo após erro na abertura.
- **Ambiente:** Python 3.12.3, Pygame 2.6.1, SDL 2.28.4, com `SDL_VIDEODRIVER=dummy` na verificação automatizada pontual.
- **Procedimento automatizado:** script pontual executando o loop real, publicando na fila do Pygame, separadamente, um evento `QUIT` e um `KEYDOWN` com Escape logo após criar o display. Após cada retorno, verificou-se `pygame.display.get_init() == False`. Uma terceira execução simulou erro em `set_mode` e verificou propagação do erro e desinicialização do display.
- **Resultado esperado e observado:** as duas solicitações encerram o loop e liberam o display; a falha simulada também libera o display. Esses casos conferem comportamento de encerramento sem depender de imports ou sintaxe apenas.
- **Suíte:** `python -m pytest` não coletou testes e retornou código 5; o script pontual não integra a suíte.
- **Verificações estáticas:** `python -m ruff check .`, `python -m ruff format --check .` e `git diff --check` passaram, usando o Python da `.venv` para o Ruff.
- **Limitação:** o driver dummy não apresenta uma janela real. A conferência visual foi realizada separadamente pelo desenvolvedor, que confirmou sua conclusão. Esse relato complementa a verificação automatizada; não foi observado diretamente pela IA.

### Procedimento de conferência manual

1. Ativar a `.venv` e executar `python -m retro_fps` em uma sessão gráfica.
2. Conferir título e janela de 640 × 480 pixels; mover a janela e verificar que responde ao sistema.
3. Pressionar Escape: esperar fechamento e retorno ao terminal sem traceback.
4. Executar novamente e clicar no botão de fechar: esperar o mesmo resultado.
5. Registrar os resultados observados.

**Resultado informado pelo desenvolvedor:** a janela abriu preta e pôde ser fechada; após a explicação do código e do procedimento acima, o desenvolvedor confirmou que realizou a validação visual e solicitou a conclusão da tarefa. M0-3 concluído com base nessa confirmação e nas verificações automatizadas registradas acima.

Ainda não há desenho explícito de cor sólida ou mapa nesta etapa. Esses elementos não são critérios desta conferência.

## 9. M0-4 e M0-5 — Tempo, desenho e configuração

- **Branch:** `feat/m0-4-5-add-frame-timing-and-window-config`.
- **M0-4 implementado:** conversão de milissegundos para segundos, exibição do intervalo no título e apresentação da superfície preenchida com cor sólida.
- **M0-5 implementado:** `WindowConfig` concentra dimensões, título, limite de frequência e cor, com validação antes de abrir a janela.
- **Verificação pontual:** script com `SDL_VIDEODRIVER=dummy` executou o loop com configuração padrão (640 × 480, azul, limite 60) e alternativa (320 × 240, vermelho, limite 30). Foram conferidos tamanho e pixels no canto superior esquerdo, centro e canto inferior direito da superfície no momento da apresentação.
- **Tempo esperado e observado:** relógio controlado retornando 20 ms produziu `dt: 0.020 s` no título, pois um segundo tem 1000 ms. Esse caso confere a conversão; não mede a precisão do relógio real nem o desempenho.
- **Encerramento:** após um quadro, eventos reais de `QUIT` e Escape foram publicados na fila nas duas execuções, respectivamente; ambas retornaram e desinicializaram o display, sem apresentar um segundo quadro.
- **Configuração inválida:** largura zero, altura negativa, limite zero, canal de cor 256 e cor com dois canais foram rejeitados com `ValueError`, sem inicializar o display.
- **Suíte:** pytest continua sem testes coletados (código 5); as verificações acima são scripts pontuais, não testes incorporados à suíte.
- **Limitação:** driver dummy não comprova aparência ou comportamento do gerenciador de janelas. A conferência visual foi realizada separadamente pelo desenvolvedor, que confirmou sua conclusão; não foi observada diretamente pela IA.

### Procedimento de conferência manual

1. Executar `python -m retro_fps` com a `.venv` ativa: esperar fundo azul uniforme e título com `dt` em segundos.
2. Observar o intervalo por alguns segundos: perto do limite 60, valores na ordem de 0.016 s são plausíveis, mas não exigir valor constante ou exato.
3. Repetir fechamento com Escape e pelo botão da janela.
4. Executar o exemplo de configuração alternativa do README: esperar janela de 800 × 600, fundo avermelhado e limite 30, sem exigir taxa exata.
5. Registrar os resultados por tarefa antes de concluir M0-4, M0-5 e o marco M0.

- **Conferências finais desta entrega:** `run()` sem argumentos também foi executado com relógio real e driver dummy, conferindo tamanho, cor padrão, título em segundos e liberação do display. `python -m ruff check .`, `python -m ruff format --check .` e `git diff --check` passaram.

**Conclusão informada pelo desenvolvedor:** após a explicação do loop, da configuração, das anotações e da dataclass, o desenvolvedor confirmou ter realizado a validação visual da entrega conjunta. M0-4 e M0-5 concluídos com base nessa confirmação e nas verificações pontuais acima. Não foram fornecidas novas medições de desempenho.

**Conclusão de M0:** pacote instalado no ambiente atual, versões registradas, janela com eventos de encerramento, intervalo em segundos, cor sólida e configuração inicial implementados. As verificações estáticas passaram; pytest executa, mas ainda não coleta testes (código 5). A instalação em ambiente limpo não foi repetida, conforme decisão registrada em M0-2. O encerramento do marco não representa validação dos algoritmos futuros da engine nem integração automática da branch.


## 10. M1-1 — Representação do mundo e consulta de células

- **Branch:** `feat/m1-1-add-world-cell-queries`, criada a partir de `origin/main` após buscar a conclusão de M0 e a tag `M0`.
- **Implementação:** `World` em `retro_fps.world`, com grade imutável, dimensões e consultas. O [contrato implementado](arquitetura.md#11-mundo-implementado-em-m1-1) distingue acesso à célula de consulta de solidez fora dos limites.
- **Ambiente automatizado:** Python 3.12.3 e pytest 9.2.0 da `.venv` existente.
- **Validação automatizada:** `.venv/bin/python -m pytest` aprovou 20 casos em `tests/test_world.py`; `.venv/bin/python -m ruff check .`, `.venv/bin/python -m ruff format --check .` e `git diff --check` passaram. A primeira conferência de formatação pediu uma quebra de linha, aplicada antes da repetição bem-sucedida.

### Exemplos e resultados esperados

A grade retangular abaixo tem três colunas e duas linhas:

```text
010
001
```

Assim, largura e altura devem ser 3 e 2. A célula `(1, 0)` é parede, enquanto `(0, 1)` é livre: resultados diferentes ajudam a detectar troca entre linha e coluna. A última célula `(2, 1)` também é parede.

Os testes conferem ainda:

- **Quatro limites:** `(-1, 0)`, `(0, -1)`, `(3, 0)` e `(0, 2)` ficam fora de uma grade 3 × 2. `contains` retorna falso, `is_solid` retorna verdadeiro e `cell_at` lança `IndexError`. Os negativos não podem acessar o lado oposto da grade.
- **Cópia e imutabilidade:** após construir o mundo com `[[0, 1]]`, alterar a lista original e acrescentar uma linha não muda `((0, 1),)` no mundo. Alterar a tupla ou substituir o atributo é rejeitado.
- **Grades inválidas:** nove casos cobrem ausência de células, linhas irregulares, valores fora de 0/1 e tipos inadequados. Todos devem causar `ValueError`.
- **Índices inválidos:** quatro pares com números reais, booleano ou texto devem causar `TypeError` em todas as consultas, sem conversão implícita.
- **Grade mínima em memória:** uma única célula livre é aceita; regras de mapas externos pertencem a M4.

### Conferência manual e aprovação

O procedimento sugerido foi criar `World([[0, 1, 0], [0, 0, 1]])` no interpretador e conferir dimensões `(3, 2)`, células `(1, 0) == 1` e `(0, 1) == 0`, ausência de `(-1, 0)`, solidez externa e `IndexError` no acesso direto externo.

**Resultado informado pelo desenvolvedor:** aprovou o código, confirmou ter testado o procedimento sugerido e também executado os testes com pytest. Esse relato foi recebido separadamente da execução automatizada pela IA; a conferência manual não foi observada diretamente pela IA e não exigia janela.

**Conclusão:** M1-1 concluída com implementação, testes automatizados e aprovação do desenvolvedor. M1 permanece em andamento. Sala padrão, raycasting, colisões, carregador e renderização não foram implementados nem validados nesta tarefa. Integração por PR permanece uma etapa separada.


## 11. M1-2 — Sala temporária em memória

- **Branch:** `feat/m1-2-add-temporary-study-room`.
- **Implementação:** `create_study_world()` constrói um `World` com a sala 5 × 5 do exemplo da seção 2, sem janela ou leitura de arquivo.
- **Resultados esperados, explicados antes da implementação:** cinco linhas de cinco células; 16 paredes (cinco na linha superior, cinco na inferior e seis nas laterais intermediárias); nove células livres (interior 3 × 3). A célula `(0, 2)` é parede, `(2, 2)` é livre e `(4, 2)` é parede.
- **Validação automatizada pela IA:** três testes novos em `tests/test_study_world.py` conferem dimensões, cada célula da borda e cada célula do interior. Os 23 casos da suíte passaram com Python 3.12.3 e pytest 9.2.0 da `.venv`. Também passaram Ruff, conferência de formatação e `git diff --check`.
- **Comandos executados:** `.venv/bin/python -m pytest`, `.venv/bin/python -m ruff check .`, `.venv/bin/python -m ruff format --check .` e `git diff --check`.
- **Conferência manual sugerida:** importar `create_study_world`, imprimir cada linha como uma sequência de 0/1, comparar com o desenho da seção 2 e consultar dimensões, borda esquerda, centro e borda direita. Resultados esperados: `(5, 5)`, `1`, `0` e `1`, respectivamente.
- **Aprovação do desenvolvedor:** após receber a implementação, os resultados automatizados e o procedimento manual, respondeu “Aprovado, pode atualizar a documentação”. A aprovação foi explícita; não houve relato detalhado dos resultados manuais nem de execução própria do pytest nesta tarefa. Esses passos não são apresentados como observados pela IA.
- **Conclusão:** M1-2 concluída com testes automatizados e aprovação do desenvolvedor; M1 continua em andamento. Raycasting, carregamento e apresentação gráfica do mapa não fazem parte desta entrega. Integração por PR permanece separada.
