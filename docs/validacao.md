# Estratégia de validação e aprendizado

## 1. Estado e princípio

Este documento reúne verificações propostas e evidências de M0 e M1. A suíte contém testes comportamentais de mundo, sala e raios; ainda não há resultados de desempenho medidos. Cada teste deve dizer qual comportamento protege e por que o resultado esperado faz sentido.

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

O parâmetro de um raio não é sempre seu comprimento euclidiano: depende do tamanho de seu vetor de direção. Os testes explicitam essa convenção. Casos diagonais que atingem exatamente um canto seguem a prioridade de x documentada na seção 13.

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

A pasta `tests/` contém os primeiros testes comportamentais, introduzidos em M1-1. Os registros de M0 preservam o resultado histórico de ausência de testes; as evidências de mundo, sala e raios estão nas seções 10 a 14.

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


## 12. M1-3 e M1-4 — Percurso de raios

- **Branch:** `feat/m1-3-4-5-add-grid-raycasting`; primeira etapa, aprovada antes de iniciar M1-5.
- **Implementação:** DDA, `RayHit`, componentes nulas, direções negativas, saída sem impacto e validação de origem/direção.
- **Resultados independentes:** na sala 5 × 5, origem `(2.5, 2.5)`, leste/oeste/sul/norte atingem respectivamente `(4, 2)`, `(0, 2)`, `(2, 4)` e `(2, 0)`, com parâmetro `1.5`. A face da parede oeste fica em `x=1`, não em `x=0`. Direção `(2, 0)` chega a `x=4` com parâmetro `0.75`. Direção `(1, 0.5)` chega com `t=1.5` a `(4, 3.25)`, célula `(4, 3)`.
- **Automação pela IA:** 32 novos casos verificam os exemplos, quatro saídas em mapa aberto, parede interna, origem em fronteira, direção nula, origem inválida e coordenadas não finitas. Os 55 casos totais passaram com `.venv/bin/python -m pytest`; Ruff, formatação e `git diff --check` também passaram. Ambiente: Python 3.12.3, pytest 9.2.0.
- **Conferência sugerida:** executar no interpretador os raios para leste, oeste, direção `(2, 0)`, saída de mapa aberto e direção nula, comparando `RayHit`, `None` e `ValueError` com os exemplos explicados.
- **Aprovação:** o desenvolvedor respondeu “Eu aprovo, podemos ir para a próxima etapa”. Não houve relato detalhado da execução manual nesta etapa; a aprovação não é registrada como observação direta de testes manuais pela IA.
- **Limites:** M1-5 ainda será consolidada e revisada separadamente. Não há renderização ou colisões; M1-6 e o marco M1 não estão concluídos.


## 13. M1-5 — Cantos e limite de avanços

- **Branch:** `feat/m1-3-4-5-add-grid-raycasting`; segunda etapa, após aprovação e commit `b7c20aa` de M1-3/M1-4.
- **Implementação:** prioridade de x em empate exato consolidada por testes; percurso limitado a largura + altura avanços, com `RuntimeError` para esgotamento inesperado. Não há tolerância para transformar quase empates em empates.
- **Exemplo explicado antes da implementação:** origem `(2.5, 2.5)`, direção `(1, 1)`, sala 5 × 5. Em `t=0.5`, consulta `(3, 2)` e depois `(3, 3)` no mesmo parâmetro. Em `t=1.5`, retorna parede `(4, 3)`, lado `"x"`, ponto geométrico `(4, 4)`.
- **Consequência da política:** partindo de `(0.5, 0.5)` em direção `(1, 1)`, uma parede em `(1, 0)` é atingida por x em `t=0.5`; se apenas `(1, 1)` for parede, é atingida por y no mesmo parâmetro. Uma parede apenas em `(0, 1)` não é consultada; numa grade 3 × 3 sem outras paredes, o retorno é `None`.
- **Automação pela IA:** 39 novos casos cobrem quatro quadrantes em cantos, as três disposições de parede acima, dois quase empates e 30 combinações de direções e grades abertas (1 × 1, 1 × 40, 40 × 1, 2 × 40 e 40 × 2). Essas saídas ocorrem dentro do orçamento, sem `RuntimeError`. O ramo de falha interna não foi forçado por simulação.
- **Resultado:** `.venv/bin/python -m pytest` aprovou os 94 casos totais com Python 3.12.3 e pytest 9.2.0. Ruff passou; a primeira conferência de formatação pediu uma quebra de linha em teste, aplicada antes de repetir Ruff, formatação e `git diff --check`, todos aprovados.
- **Conferência manual sugerida:** executar os dois exemplos apresentados ao desenvolvedor: diagonal da sala, esperando `RayHit(4, 3, 'x', 1.5)`, e grade aberta com parede apenas na lateral não visitada, esperando `None`.
- **Aprovação:** após receber explicação, exemplos e resultados, o desenvolvedor respondeu “Aprovado!”. Não houve relato detalhado da execução manual; aprovação explícita e resultados automatizados permanecem evidências distintas.
- **Conclusão:** M1-5 concluída. M1-6 e o encerramento de M1 permanecem pendentes; integração por PR é separada. Esta entrega não valida renderização ou colisões.

## 14. M1-6 — Revisão dos testes e explicação do percurso

**Estado:** M1-6 concluída, com testes automatizados aprovados, explicação do percurso e validação confirmada pelo desenvolvedor.

**Branch:** `test/m1-6-review-raycasting-cases`, a partir da `main` com M1-3/M1-4/M1-5 integradas.

### Percurso conferível sem executar o algoritmo

Na sala da seção 2, a origem `(2.5, 2.5)` está na célula `(2, 2)`. Para direção `(1, 0)`, a equação é `x = 2.5 + t`, `y = 2.5`. Cada nova fronteira vertical está uma unidade adiante; não há cruzamentos horizontais.

| Passo | Fronteira | Conta para t | Célula consultada | Resultado |
|---|---|---|---|---|
| Início | Nenhuma | 0 | `(2, 2)` | Livre |
| 1 | `x=3` | `3 - 2.5 = 0.5` | `(3, 2)` | Livre |
| 2 | `x=4` | `4 - 2.5 = 1.5` | `(4, 2)` | Parede; lado `"x"` |

O retorno deve ser `RayHit(4, 2, 'x', 1.5)`. Para direção `(2, 0)`, a equação muda para `x = 2.5 + 2t`; chegar a `x=4` exige `t=0.75`. O ponto de impacto continua igual. As contas não dependem da implementação do DDA.

### Complementos desta revisão

Sala retangular de largura 7 e altura 5:

```text
1111111
1000001
1000001
1000001
1111111
```

A origem `(3.5, 2.5)` e as direções `(±0.5, ±1)` atingem faces horizontais em `t=1.5`: ao sul, `y=4`; ao norte, `y=1`, face inferior das células da linha 0. O impacto em x é `3.5 ± 0.75`: coluna 4 ou 2. Quatro novos casos conferem célula, lado `"y"` e parâmetro. Esses exemplos foram explicados antes de escrever os testes.

Seis novos casos ampliam as saídas em mapas abertos para uma grade 40 × 40. Na diagonal `(1, 1)` partindo de `(0.5, 0.5)`, são 39 pares de avanços internos e mais um avanço em x para sair: 79, dentro do orçamento 80. O teste confere a saída sem erro; não instrumenta nem conta os avanços internos.

### Evidências e limites

- `.venv/bin/python -m pytest`: 104 casos aprovados (81 de raios, 20 de mundo e três de sala), com Python 3.12.3 e pytest 9.2.0.
- `.venv/bin/python -m ruff check .`, `.venv/bin/python -m ruff format --check .` e `git diff --check`: aprovados.
- Os testes anteriores cobrem direções cardinais, componentes nulas, sinais negativos, saída, raio nulo, origem inválida, fronteiras e cantos. As seções 10 a 13 preservam exemplos e resultados históricos.
- Nenhum algoritmo foi alterado nesta tarefa. Os testes usam geometrias pequenas e valores calculados por equações, sem gerar a resposta esperada pelo DDA.
- Não foi simulada a falha interna de esgotamento do orçamento. Não há medição de desempenho, validação de renderização ou promessa de precisão para escalas numéricas extremas de ponto flutuante.
- **Validação pelo desenvolvedor:** após receber os resultados, a explicação e o procedimento de conferência, confirmou “Está validado, pode prosseguir”. A confirmação é registrada separadamente da execução automatizada pela IA; não foram relatadas saídas detalhadas nem uma explicação com palavras próprias. Não foi necessária inspeção gráfica.


### Encerramento de M1

Os critérios do roadmap foram conferidos: raio para leste com impacto em `x=4` e parâmetro `1.5`, quatro direções cardinais, rejeição do raio nulo e término dos casos de canto segundo a política documentada. A sala em memória, consultas de mundo, saída da grade e orçamento de avanços também têm cobertura. Os resultados foram acompanhados de desenhos, contas independentes e explicação passo a passo.

Com a validação final do desenvolvedor, M1 está concluído no ambiente atual. Integração de M1-6 por PR e eventual tag são etapas separadas. Renderização, movimento, colisões e carregamento de arquivos permanecem para os marcos seguintes.


## 15. M2-1 — Geometria da câmera

- **Branch:** `feat/m2-1-2-3-add-camera-column-rays`, criada após atualizar a main com M1-6 integrada e tag `M1`.
- **Exemplos explicados antes do código:** para leste, direção `(1, 0)` e plano para sul; para sul, direção `(0, 1)` e plano para oeste. Em campo de visão de 90 graus, o comprimento do plano é 1; no padrão 60 graus, é `1/sqrt(3)`.
- **Automação:** 24 novos casos verificam quatro direções cardinais, orientação do plano, direção unitária, perpendicularidade, comprimento do plano, normalização, valores inválidos e imutabilidade. Tolerâncias de `1e-12` para resultados trigonométricos. Negativo próximo de zero também verifica que o resto arredondado a `2*pi` é representado como zero.
- **Resultados:** 128 casos totais aprovados com `.venv/bin/python -m pytest`; Ruff, formatação e `git diff --check` aprovados. Ambiente: Python 3.12.3, pytest 9.2.0.
- **Conferência sugerida:** construir câmeras para leste e sul, comparar os vetores, normalizar -90 graus e verificar rejeição de campo de visão igual a pi. Não exige janela.
- **Aprovação:** após receber resultados e procedimento, o desenvolvedor pediu explicação de `@property`, implementação e interação com o projeto. A explicação foi fornecida; respondeu “Entendido” e autorizou continuar. Não relatou saídas manuais detalhadas.
- **Limites:** esta etapa não gera raios por coluna, não desenha nem move jogador. M2 permanece em andamento.


## 16. M2-2 e M2-3 — Raios pelos centros das colunas

- **Branch:** `feat/m2-1-2-3-add-camera-column-rays`; segunda etapa, após aprovação e commit `7f47d05` de M2-1.
- **Exemplos explicados antes do código:** olhando para leste com campo de visão de 90 graus, três colunas usam posições laterais `-2/3`, `0`, `2/3`, produzindo direções `(1, u)`. Quatro colunas usam `-0.75`, `-0.25`, `0.25`, `0.75`; nenhuma aponta exatamente para o centro.
- **Resultados independentes:** na sala 5 × 5, origem `(2.5, 2.5)`, os três raios atingem `x=4` com parâmetro `1.5`. As coordenadas y são `1.5`, `2.5` e `3.5`, portanto células `(4, 1)`, `(4, 2)` e `(4, 3)`, lado x. O raio lateral mede `sqrt(13)/3`, maior que 1, mas sua componente frontal continua sendo 1. Isso verifica que a direção não foi normalizada e que o DDA fornece profundidade frontal constante.
- **Automação:** 22 casos novos cobrem coluna única, centros e simetria com larguras par e ímpar, rotação, comprimento e componente frontal, integração com DDA e entradas inválidas. Tolerâncias de `1e-12` para resultados reais.
- **Resultados:** `.venv/bin/python -m pytest` aprovou os 150 casos totais (46 de câmera, 81 de raios, 20 de mundo e três de sala). Ruff passou; após ajuste de formatação de um teste, Ruff, formatação e `git diff --check` passaram. Ambiente: Python 3.12.3 e pytest 9.2.0.
- **Conferência sugerida:** gerar as três direções no interpretador, lançá-las com `cast_ray` na sala e comparar direções, células, lado e parâmetro com a tabela apresentada ao desenvolvedor. Não exige janela.
- **Validação do desenvolvedor:** após receber os resultados e o procedimento, confirmou “Considere validado, pode prosseguir”. A confirmação é registrada separadamente da execução automatizada pela IA; não foram relatadas saídas manuais detalhadas.
- **Conclusão:** M2-2/M2-3 concluídas; M2 continua em andamento, com projeção, desenho e conferência visual pendentes. Integração por PR é uma etapa separada.


## 17. M2-4 — Projeção e recorte

- **Branch:** `feat/m2-4-5-render-static-perspective`; primeira etapa.
- **Exemplos prévios:** largura 320, FOV 90 graus, escala 160; profundidades 2 e 4 produzem alturas 80 e 40, com intervalos `(60, 140)` e `(80, 120)` numa imagem de altura 200. Profundidade zero usa o mínimo de 0.000001 e resulta em recorte de tela inteira.
- **Automação:** 29 casos novos conferem alturas conhecidas, relação inversa com profundidade, proteção próxima de zero, arredondamento, recorte, altura zero e entradas inválidas. Os 179 casos totais passaram com `.venv/bin/python -m pytest`; Ruff, formatação e `git diff --check` passaram. Python 3.12.3, pytest 9.2.0.
- **Conferência sugerida:** executar no interpretador as contas de profundidades 2, 4 e zero e comparar alturas e intervalos acima. Não há janela nesta etapa.
- **Aprovação:** o desenvolvedor respondeu “EU aprovo, pode seguir” após receber os resultados e procedimento. Não foram relatadas saídas manuais detalhadas; aprovação e automação são evidências separadas.
- **Estado:** M2-4 concluída; desenho e validação visual permanecem em M2-5. M2 continua em andamento.


## 18. M2-5 — Primeira imagem em perspectiva

- **Branch:** `feat/m2-4-5-render-static-perspective`; segunda etapa, após aprovação e commit `c9e4f42` de M2-4.
- **Implementação:** desenho por colunas em superfície interna, cores por orientação, piso/teto sólidos, ampliação proporcional centralizada, cena opcional no executor e sala estática pelo comando principal.
- **Exemplos prévios:** cada coluna interna tem largura 1; a imagem 320 × 200 ocupa 640 × 400 na janela 640 × 480, deixando faixas de 40 pixels. Desenhar [top,bottom) exige altura `bottom-top`.
- **Testes de desenho:** cinco casos com superfícies reais verificam fundo sem impacto, faces x/y e alinhamento frontal, parede próxima e impacto de profundidade zero. Para largura 12, visão de 60 graus e profundidade 1.5, a altura é `4*sqrt(3)`, cerca de 6.928: em altura 10, ocupa [1,9). O resultado foi calculado independentemente do DDA.
- **Ajuste durante a verificação:** o exemplo inicial de visão de 90 graus produziu altura próxima de 4, ligeiramente maior por ponto flutuante; piso/teto matemáticos ampliaram o intervalo. O teste de pixels foi substituído por um exemplo distante de uma fronteira inteira, sem alterar o algoritmo. As contas de projeção continuam verificadas com tolerância explícita.
- **Testes de loop/configuração:** 17 casos cobrem cena e fundo sólido, encerramento com eventos reais de Escape/QUIT na fila após um quadro, liberação do display, tamanho interno, cores e faixas pretas, cenas incompletas e dimensões inválidas. O driver dummy não apresenta janela real.
- **Resultados automatizados:** 201 casos totais aprovados com Python 3.12.3 e pytest 9.2.0. Ruff, formatação e `git diff --check` aprovados após ajustes de formatação e uso de literais de dicionário nos testes.
- **Procedimento visual fornecido:** executar `python -m retro_fps`; conferir parede frontal alinhada, teto/piso, faixas pretas e encerramento. Repetir com `Camera(pi/4)` para observar o canto e as tonalidades diferentes das faces.
- **Conferência pelo desenvolvedor:** após receber o procedimento, confirmou “Funcionou. Pode seguir”. Essa confirmação da execução real é separada dos testes com driver dummy; não foi observada diretamente pela IA nem constitui medição de desempenho.
- **Conclusão:** M2-5 concluída com conferência visual confirmada. M2 permanece em andamento até M2-6; integração por PR é separada. Ainda não há movimento, colisões ou carregamento de mapas.

## 19. M2-6 — Comparação controlada de sala e corredor

**Branch:** `test/m2-6-validate-room-and-corridor`, criada a partir da main com M2-4/M2-5 integradas.

**Estado:** M2-6 concluída com testes automatizados e comparação visual das quatro cenas confirmada pelo desenvolvedor.

### Geometria e contas anteriores aos testes

A sala permanece 5 × 5. O novo `create_study_corridor()` retorna um mundo 9 × 5, temporário e em memória:

```text
111111111
100000001
100000001
100000001
111111111
```

Todas as cenas usam `Camera(0)`, olhando para leste com visão de 60 graus. Na sala, origem `(2.5, 2.5)`, a face frontal fica em x=4, profundidade 1.5. No corredor, a face fica em x=8: origem `(2.5, 2.5)` dá profundidade 5.5; origem `(5.25, 2.5)` dá 2.75. A profundidade cai pela metade e a altura não arredondada dobra. A relação se aplica à face frontal; raios laterais podem atingir outras paredes.

Para largura interna 32, a escala é `16*sqrt(3)`. Numa imagem 32 × 24:

| Cena | Profundidade frontal | Altura aproximada | Intervalo após arredondamento |
|---|---|---|---|
| Sala | 1.5 | 18.475 | [2,22) |
| Corredor distante | 5.5 | 5.039 | [9,15) |
| Corredor próximo | 2.75 | 10.077 | [6,18) |

Na sala, todos os raios atingem a face frontal. No corredor, as colunas centrais atingem o fundo e as extremas atingem faces y. Na coluna extrema da imagem 32 × 24, a altura da parede lateral é `31/3`, cerca de 10.333: intervalo [6,18), mais alto e mais escuro que o fundo distante.

### Evidências automatizadas

Oito novos casos em `tests/test_perspective_scenarios.py` conferem geometria do corredor, pixels da sala inteira, dois raios centrais com profundidades conhecidas, alturas antes do arredondamento, pixels do fundo nas duas posições, laterais e recorte muito próximo da parede. Os testes reutilizam os componentes implementados; os resultados esperados vêm das contas acima, sem executar um segundo DDA para produzi-los.

`.venv/bin/python -m pytest`: 209 casos aprovados, com Python 3.12.3 e pytest 9.2.0. Ruff, formatação e `git diff --check` passaram. Nenhum algoritmo de câmera, DDA ou projeção foi alterado. Testes de pixels não comprovam por si só aparência na janela real ou desempenho.

### Procedimento de conferência visual

Com a `.venv` ativa, abrir `python` e executar:

```python
from retro_fps.camera import Camera
from retro_fps.engine import run
from retro_fps.study_world import create_study_world, create_study_corridor

run(world=create_study_world(), origin=(2.5, 2.5), camera=Camera(0))
run(world=create_study_corridor(), origin=(2.5, 2.5), camera=Camera(0))
run(world=create_study_corridor(), origin=(5.25, 2.5), camera=Camera(0))
run(world=create_study_corridor(), origin=(7.9999999, 2.5), camera=Camera(0))
```

Cada chamada bloqueia até fechar sua janela; depois apresenta a próxima. Comparar:

1. Sala: parede frontal com topo/base horizontais, piso e teto visíveis.
2. Corredor distante: fundo menor que na sala; laterais escuras crescendo em direção às bordas, sem curvar a face frontal plana.
3. Corredor próximo: fundo aproximadamente duas vezes mais alto que no corredor distante, considerando arredondamento de pixels.
4. Muito próximo: parede ocupa toda a área da imagem, mantendo as faixas pretas de apresentação, e a janela continua encerrando normalmente.

Informar se as quatro cenas correspondem ao esperado. Não há movimento nesta etapa; a comparação muda a origem entre execuções. M2-6 não acrescenta carregador de arquivos nem seleção de cenário ao comando principal.


### Confirmação e encerramento de M2

Após receber o procedimento, o desenvolvedor confirmou que todos os testes funcionaram e relatou ter visto o resultado funcionando. Essa confirmação da conferência das quatro cenas é distinta dos 209 casos automatizados executados pela IA; a janela real não foi observada diretamente pela IA.

Os critérios do roadmap foram conferidos: face frontal plana alinhada, parede distante menor, metade da altura não arredondada ao dobrar a profundidade e recorte seguro perto da parede. A sala e o corredor foram comparados com contas e imagens, sem correção adicional de fish-eye. M2 está concluído no ambiente atual. Integração por PR e eventual tag são etapas separadas; nenhuma tag foi criada nesta tarefa. Movimento, colisões e carregamento permanecem fora desta entrega.


## 20. M3-1 — Estado do jogador e comandos lógicos

- **Branch:** `feat/m3-1-2-3-add-player-movement`; primeira entrega do grupo. Base: main em `55673d2`, contendo `5558bd7`, sincronizada com origin após fetch.
- **Conceitos prévios:** comando `(1, -1)` solicita avanço e giro à esquerda, sem executar movimento; ângulos separados por uma volta representam a mesma orientação.
- **Contas independentes:** -pi/2 + 2*pi = 3*pi/2; 5*pi/2 - 2*pi = pi/2. Três valores independentes em cada comando produzem nove combinações. Alterar a lista de posição após a construção não deve alterar o estado copiado.
- **Automação:** 42 novos casos verificam cópia, imutabilidade, normalização angular, coordenadas e ângulos não finitos, comandos padrão, nove combinações e rejeição de tipos/valores inválidos. Os 251 testes totais passaram; Ruff, formatação e `git diff --check` passaram.
- **Conferência sugerida:** construir jogador em `(2.5, 2.5)` com ângulo -pi/2 e imprimir estado e comandos padrão e `(1, -1)`. Esperado: posição preservada, ângulo aproximadamente 4.712389 e intenções preservadas. Não exige janela.
- **Validação do desenvolvedor:** confirmou “Pode seguir, está validado”, sem relatar saídas manuais específicas. Essa aprovação é distinta da automação.
- **Limites:** ainda sem cálculo de movimento, teclado, colisões ou alteração visual; M3 permanece em andamento.


## 21. M3-2/M3-3 — Movimento independente da janela

- **Branch:** `feat/m3-1-2-3-add-player-movement`; segunda entrega, após `fb2cfc9` de M3-1.
- **Contas prévias:** a 1 unidade/s, 0.1 s desloca 0.1 unidade. Partindo de `(2.5, 2.5)`, avanço para leste resulta em `(2.6, 2.5)` e para sul em `(2.5, 2.6)`. A pi/2 rad/s, 0.1 s gira pi/20 rad, ou 9 graus. Girar 90 graus à direita antes de avançar uma unidade leva de `(2.5, 2.5)` para `(2.5, 3.5)` quando o início olha para leste.
- **Automação:** 30 casos novos verificam cardinais, recuo, giro, ordem das operações, repouso, tempo zero, equivalência temporal no avanço reto/giro isolado, configuração e entradas inválidas. 281 testes totais aprovados; Ruff, formatação e `git diff --check` aprovados.
- **Conferência sugerida:** no interpretador, avançar por 0.1 s, girar por 0.1 s e imprimir o estado original para conferir sua preservação. Não há mudança visual nesta entrega.
- **Validação do desenvolvedor:** confirmou “Pode seguir, está validado também”, sem relatar saídas manuais específicas.
- **Limites:** teclado e ligação da câmera pendentes; sem colisões ou proteção para passos grandes. M3-3 concluída; M3-2 aguarda integração dos controles.


## 22. M3-2 — Teclado e câmera derivados do jogador

- **Branch:** `feat/m3-1-2-3-add-player-movement`; terceira entrega, após `d77651e`.
- **Contas independentes:** com intervalo controlado de 100 ms, velocidade linear 1 e angular 5*pi, cada quadro gira 90 graus e desloca 0.1 unidade na nova direção. Partindo de `(2.5, 2.5)` para leste, os dois quadros pressionados resultam em `(2.5, 2.6)` para sul e `(2.4, 2.6)` para oeste. Soltar mantém esse estado.
- **Automação anterior à conferência visual:** 15 casos novos de tradução de teclas, cancelamento, quadros consecutivos, liberação, origem/ângulo/FOV no renderizador, encerramento e parâmetros inválidos. 296 testes passaram; Ruff, formatação e diff passaram. Display dummy não comprova aparência real.
- **Procedimento visual:** executar `python -m retro_fps`; dar toques curtos em W/S e setas; conferir aproximação/afastamento, giro, parada ao soltar, cancelamento e encerramento. Evitar entrar em paredes.
- **Conferência do desenvolvedor:** confirmou “Está validado” e descreveu o movimento como semelhante a tanque. A IA não observou diretamente a janela; não foram relatados resultados individuais de cada item.
- **Estado:** primeiro grupo M3-1/M3-2/M3-3 concluído; M3 permanece em andamento, sem colisões ou navegação segura.

- **Conferência antes do commit:** com a edição local do desenvolvedor em `study_world.py` (célula `(1, 2)` transformada em parede), a suíte resultou em 289 aprovados e sete falhas que dependem da sala original. A edição foi preservada e excluída do commit. Em cópia temporária de código e testes, usando apenas a sala original obtida de HEAD, os 296 testes passaram. Ruff, formatação e diff passaram na árvore local.


## 23. M3-2 — Extensão lateral e diagonal

- **Branch:** `feat/m3-1-2-3-add-player-movement`; extensão solicitada após `79885ec`.
- **Contas independentes:** olhando para leste, direita é sul: D por 0.1 s a 1 unidade/s leva `(2.5, 2.5)` a `(2.5, 2.6)`. Para W+D, Pitágoras exige componentes iguais de 0.1/sqrt(2), aproximadamente 0.0707107: a soma dos quadrados é 0.01 e a distância total é 0.1. Ao olhar para sul, D leva para oeste. O ângulo não muda sem comando de giro.
- **Automação:** 43 casos adicionais (incluindo expansão das parametrizações) cobrem comandos laterais, domínio de valores, orientações, quatro diagonais, giro antes da diagonal, subdivisão temporal, tradução de A/D e cancelamentos. Integração confere W+D no desenho e parada ao soltar, com tempo controlado.
- **Resultados:** 339 casos aprovados em cópia temporária com sala original obtida de HEAD. Na árvore local: 332 aprovados e as mesmas sete falhas de geometria causadas pela parede editada pelo desenvolvedor. A edição permanece intacta. Ruff, formatação e `git diff --check` passaram.
- **Procedimento manual proposto:** executar `python -m retro_fps`; com toques curtos, verificar A/D sem giro, W+D e W+A, S+D e S+A, cancelamento A+D e parada ao soltar. Girar com uma seta e repetir A/D para conferir orientação relativa. Evitar paredes, especialmente a parede local na célula `(1, 2)`.
- **Conferência do desenvolvedor:** confirmou “Muito bem, está validado” após receber o procedimento. Não relatou resultados individuais; a IA não observou diretamente a janela.
- **Estado:** extensão concluída com implementação, automação e conferência manual confirmada. Sem colisões, limitação temporal ou subdivisão espacial.

- **Verificação final após aprovação:** `study_world.py` já não apresenta diferença local; a suíte foi executada diretamente na árvore de trabalho e os 339 casos passaram. Ruff, formatação e `git diff --check` também passaram. O registro anterior das sete falhas descreve a execução com a sala então editada.
