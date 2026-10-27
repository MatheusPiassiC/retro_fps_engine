# Roadmap do Projeto — RetroFPS Engine

## 1. Objetivo

Este documento estabelece o planejamento de desenvolvimento da RetroFPS Engine, organizando o trabalho em etapas incrementais que conduzam da definição dos requisitos à entrega de uma engine funcional acompanhada de um jogo demonstrativo.

O planejamento segue os princípios do *Spec-Driven Development* (SDD): as funcionalidades serão especificadas antes de sua implementação, os critérios de aceitação orientarão a validação e as decisões técnicas serão documentadas ao longo do desenvolvimento.

O projeto será dividido em duas fases principais, correspondentes às etapas da disciplina. A primeira terá como objetivo construir o núcleo funcional da engine. A segunda será dedicada à construção do jogo demonstrativo, à validação dos requisitos e ao refinamento da solução.

O desenvolvimento deverá priorizar a implementação dos algoritmos fundamentais pelo próprio projeto, evitando dependência de engines prontas para realizar a renderização central do ambiente.

## 2. Visão geral das fases

| Fase | Período | Objetivo principal | Resultado esperado |
|---|---|---|---|
| Fase 1 — Núcleo da engine | 28/10 a 16/11/2026 | Implementar e validar os mecanismos essenciais de renderização e navegação | Engine capaz de carregar e renderizar um cenário navegável |
| Fase 2 — Jogo demonstrativo | 17/11 a 30/11/2026 | Construir uma experiência jogável sobre a engine e consolidar a documentação | Jogo simples, funcional e demonstrável |
| Apresentação | 01/12 a 08/12/2026 | Demonstrar o funcionamento e explicar a implementação | Apresentação técnica com demonstração prática |

As datas representam o calendário previsto da disciplina. As etapas internas poderão ser reorganizadas conforme o progresso, desde que os critérios de conclusão das fases sejam preservados.

## 3. Fase 0 — Especificação e planejamento

**Objetivo:** transformar a missão do projeto em requisitos verificáveis e estabelecer uma base de desenvolvimento organizada.

**Período previsto:** início do projeto, antes da implementação do núcleo.

### Atividades

1. Definir os requisitos funcionais da engine.
2. Definir os requisitos não funcionais, incluindo modularidade, testabilidade e facilidade de execução.
3. Estabelecer os limites do escopo obrigatório e das funcionalidades opcionais.
4. Especificar o formato inicial dos arquivos de mapa.
5. Definir as responsabilidades dos principais módulos.
6. Criar o repositório GitHub e configurar o ambiente Python.
7. Estabelecer critérios de aceitação para as funcionalidades essenciais.
8. Criar o backlog inicial, ordenando as tarefas por dependência e prioridade.

### Entregáveis

- Documento de requisitos;
- Especificação inicial do formato dos mapas;
- Estrutura inicial do repositório;
- Ambiente de desenvolvimento configurado;
- Backlog priorizado;
- Critérios de aceitação definidos.

### Critérios de conclusão

- Os requisitos essenciais estão documentados e podem ser verificados.
- O escopo obrigatório está separado das extensões opcionais.
- O projeto pode ser executado no ambiente de desenvolvimento.
- As principais responsabilidades arquiteturais estão definidas.

**Dependência:** nenhuma. Esta etapa estabelece a base para as demais.

---

## 4. Fase 1 — Desenvolvimento do núcleo da engine

**Período:** 28/10 a 16/11/2026.

**Objetivo:** desenvolver uma engine capaz de carregar um cenário externo, renderizá-lo em perspectiva pseudo-3D e permitir que o jogador navegue pelo ambiente sem atravessar paredes.

Esta fase concentra o maior risco técnico do projeto: a implementação correta do raycasting e sua integração com a movimentação e as colisões.

### Etapa 1.1 — Estrutura básica da aplicação

**Objetivo:** estabelecer a infraestrutura mínima para executar a engine.

Atividades:

- Criar a estrutura modular do projeto.
- Configurar o Pygame.
- Implementar a janela da aplicação.
- Criar o ciclo principal de execução.
- Implementar o tratamento de eventos de teclado.
- Definir a atualização e a apresentação dos quadros.
- Implementar o encerramento correto da aplicação.

**Entregável:** aplicação executável com janela gráfica, entrada de teclado e ciclo principal funcionando.

**Critérios de aceitação:**

- A aplicação inicia sem erros.
- A janela permanece responsiva.
- Os eventos de teclado são processados.
- A aplicação pode ser encerrada normalmente.

**Prioridade:** obrigatória.

### Etapa 1.2 — Representação do mundo e carregamento de mapas

**Objetivo:** permitir que os cenários sejam definidos em arquivos externos, sem depender de alterações no código-fonte da engine.

Atividades:

- Definir a estrutura de dados que representa o mapa.
- Implementar o carregador de arquivos `.map`.
- Converter o conteúdo dos arquivos em uma representação utilizável pela engine.
- Implementar consultas para identificar paredes e espaços livres.
- Validar dimensões, limites e caracteres permitidos.
- Verificar se a posição inicial do jogador é válida.
- Tratar arquivos inexistentes ou malformados.

**Entregável:** módulo de mundo capaz de carregar e validar cenários externos.

**Critérios de aceitação:**

- Um mapa válido é carregado corretamente.
- A engine consegue consultar se uma célula representa uma parede.
- Mapas inválidos são rejeitados com mensagens compreensíveis.
- A posição inicial do jogador está dentro do cenário e em uma área livre.
- A alteração do arquivo de mapa permite modificar o cenário sem alterar o código da engine.

**Prioridade:** obrigatória.

### Etapa 1.3 — Estado e movimentação do jogador

**Objetivo:** implementar a representação do jogador e sua movimentação no ambiente.

Atividades:

- Representar a posição do jogador em coordenadas bidimensionais.
- Representar sua orientação por um ângulo.
- Implementar movimentação para frente e para trás.
- Implementar rotação horizontal.
- Definir velocidade de deslocamento e rotação.
- Utilizar o tempo decorrido entre atualizações para calcular os movimentos.
- Separar o estado do jogador da lógica de renderização.

**Entregável:** módulo de jogador com posição, orientação e movimentação funcionais.

**Critérios de aceitação:**

- O jogador pode se deslocar e girar.
- A movimentação é consistente em diferentes taxas de atualização.
- A orientação da câmera acompanha a rotação do jogador.
- O estado do jogador pode ser atualizado sem depender diretamente do código de desenho.

**Prioridade:** obrigatória.

### Etapa 1.4 — Implementação das colisões

**Objetivo:** impedir que o jogador atravesse as paredes do cenário.

Atividades:

- Implementar a verificação de colisão entre a posição proposta e o mapa.
- Integrar as verificações ao processo de movimentação.
- Evitar que o jogador ultrapasse os limites do cenário.
- Tratar movimentação diagonal.
- Evitar que o jogador fique preso em paredes durante o deslocamento.
- Definir uma aproximação simples para o tamanho físico do jogador, se necessária.

**Entregável:** sistema de colisões integrado à movimentação.

**Critérios de aceitação:**

- O jogador não atravessa paredes.
- O jogador não consegue sair dos limites válidos do cenário.
- O movimento diagonal não permite atravessar obstáculos.
- O jogador consegue se deslocar ao longo de uma parede sem ficar bloqueado desnecessariamente.

**Prioridade:** obrigatória.

### Etapa 1.5 — Algoritmo de raycasting

**Objetivo:** implementar o mecanismo central de renderização pseudo-3D.

Atividades:

- Definir os parâmetros da câmera e seu campo de visão.
- Determinar a direção de cada raio lançado a partir da câmera.
- Implementar o algoritmo DDA (*Digital Differential Analyzer*) para percorrer a grade do mapa.
- Detectar a primeira parede atingida por cada raio.
- Calcular a distância entre a câmera e o ponto de impacto.
- Corrigir o efeito *fish-eye* utilizando a distância perpendicular à direção central da câmera.
- Tratar raios paralelos às linhas da grade e outros casos-limite.
- Definir limites seguros para a busca de interseções.

**Entregável:** módulo de raycasting capaz de calcular as interseções entre os raios e as paredes do cenário.

**Critérios de aceitação:**

- Os raios detectam corretamente as paredes do mapa.
- As distâncias calculadas são coerentes com a geometria do cenário.
- O algoritmo não entra em ciclos infinitos quando encontra entradas inválidas ou situações-limite.
- A renderização não apresenta distorções graves decorrentes de um cálculo incorreto da distância perpendicular.

**Prioridade:** obrigatória.

**Observação:** esta etapa deverá ser testada isoladamente sempre que possível. Erros no cálculo das interseções comprometem toda a renderização subsequente.

### Etapa 1.6 — Renderização pseudo-3D

**Objetivo:** converter os resultados do raycasting em uma representação visual navegável do cenário.

Atividades:

- Calcular a altura projetada das paredes a partir da distância perpendicular.
- Desenhar as paredes como colunas verticais.
- Definir parâmetros básicos de projeção.
- Representar paredes e espaços livres com cores distintas.
- Ajustar a resolução e o campo de visão.
- Integrar o renderizador ao estado do jogador e ao mapa.
- Avaliar a viabilidade de adicionar cores diferentes conforme a distância.

**Entregável:** renderizador funcional para ambientes 2.5D.

**Critérios de aceitação:**

- O cenário é exibido em perspectiva pseudo-3D.
- Corredores e paredes correspondem à geometria definida no mapa.
- A imagem se atualiza corretamente quando o jogador se movimenta ou gira.
- A renderização funciona com pelo menos dois mapas diferentes.

**Prioridade:** obrigatória.

### Etapa 1.7 — Integração, testes e validação do núcleo

**Objetivo:** consolidar os módulos e garantir que o núcleo da engine funcione de maneira integrada.

Atividades:

- Integrar mapa, jogador, colisões e renderizador.
- Testar cenários de diferentes dimensões e configurações.
- Criar testes automatizados para carregamento de mapas e colisões.
- Verificar os casos-limite do raycasting.
- Corrigir problemas de integração.
- Documentar a instalação e a execução.
- Registrar limitações conhecidas.

**Entregável:** primeira versão funcional da RetroFPS Engine.

**Critérios de aceitação:**

- A aplicação carrega um mapa externo e permite explorá-lo em primeira pessoa.
- O jogador consegue se movimentar e girar.
- As colisões impedem a passagem através das paredes.
- A renderização acompanha corretamente a posição e a orientação do jogador.
- A aplicação pode ser executada seguindo as instruções do README.
- Os principais componentes possuem responsabilidades identificáveis.

**Prioridade:** obrigatória.

### Marco M1 — Engine navegável

Ao final da Fase 1, deverá existir uma versão demonstrável da engine com:

- Carregamento de mapas externos;
- Movimentação em primeira pessoa;
- Colisões;
- Raycasting implementado pelo projeto;
- Renderização pseudo-3D;
- Estrutura modular;
- Testes dos componentes essenciais.

**Este marco é a prioridade máxima da primeira fase.** Texturas, inimigos, portas interativas e outros recursos não deverão comprometer sua conclusão.

---

## 5. Fase 2 — Construção do jogo demonstrativo

**Período:** 17/11 a 30/11/2026.

**Objetivo:** demonstrar a utilidade da engine por meio de um jogo pequeno, completo e executável, sem perder o foco nos objetivos técnicos do projeto.

A segunda fase deverá reutilizar os componentes da engine, evitando duplicar a implementação de movimentação, colisões ou renderização dentro da lógica específica do jogo.

### Etapa 2.1 — Definição da experiência jogável

**Objetivo:** estabelecer um objetivo simples que permita demonstrar as funcionalidades da engine.

A proposta inicial é um jogo de exploração e fuga: o jogador precisa encontrar uma chave e alcançar uma saída.

Atividades:

- Definir o objetivo principal.
- Desenhar um cenário com início, percurso, chave e saída.
- Definir as condições de vitória.
- Estabelecer as interações necessárias.
- Definir a duração esperada da demonstração.

**Entregável:** especificação curta do jogo demonstrativo.

**Critérios de aceitação:**

- O jogo possui um objetivo compreensível.
- O cenário permite concluir o objetivo.
- As regras podem ser implementadas sem modificar desnecessariamente o núcleo da engine.

**Prioridade:** obrigatória.

### Etapa 2.2 — Texturas e refinamento visual

**Objetivo:** melhorar a apresentação do cenário e facilitar a identificação dos elementos do ambiente.

Atividades:

- Implementar a aplicação de texturas às paredes, caso o renderizador ainda não ofereça esse recurso.
- Determinar a coordenada de impacto para selecionar a parte correta da textura.
- Escalar a textura de acordo com a projeção da parede.
- Permitir que diferentes paredes utilizem texturas distintas.
- Ajustar a apresentação visual para a demonstração.

**Entregável:** cenário com representação visual aprimorada.

**Critérios de aceitação:**

- As texturas são projetadas de maneira coerente com as paredes.
- Diferentes tipos de parede podem ser identificados visualmente.
- A adição de texturas não compromete a navegação ou as colisões.

**Prioridade:** desejável. Caso a renderização básica ainda apresente falhas, a correção dos problemas terá precedência sobre as texturas.

### Etapa 2.3 — Sistema de interação

**Objetivo:** implementar os mecanismos necessários para que o jogador interaja com o cenário.

Atividades:

- Definir uma representação para objetos interativos.
- Implementar uma chave que possa ser coletada.
- Registrar o estado de coleta da chave.
- Implementar uma saída que dependa da chave.
- Verificar a proximidade do jogador e o comando de interação.
- Exibir mensagens simples para orientar o jogador.

**Entregável:** sistema de interação integrado à engine.

**Critérios de aceitação:**

- A chave pode ser coletada.
- O estado da coleta é mantido durante a partida.
- A saída só pode ser utilizada quando as condições forem satisfeitas.
- O jogador recebe uma indicação compreensível quando uma interação não é permitida.

**Prioridade:** obrigatória para a demonstração planejada.

**Dependência:** a engine deve oferecer movimentação, colisões e consulta ao estado do mundo.

### Etapa 2.4 — Representação visual dos objetos interativos

**Objetivo:** tornar os elementos relevantes do jogo visíveis no ambiente.

Atividades:

- Definir como chaves e saídas serão representadas.
- Implementar uma forma simples de visualização dos objetos.
- Avaliar o uso de sprites projetados na perspectiva da câmera.
- Evitar que objetos sejam desenhados sobre paredes que deveriam ocultá-los, se for adotada a projeção de sprites.
- Integrar a representação visual ao estado dos objetos.

**Entregável:** objetos identificáveis visualmente durante a exploração.

**Critérios de aceitação:**

- O jogador consegue identificar a chave e a saída.
- Os objetos aparecem em posições coerentes com o mapa.
- Os objetos coletados ou utilizados refletem seu estado atualizado.

**Prioridade:** desejável, mas recomendada para que o jogo demonstrativo seja compreensível sem depender exclusivamente de instruções externas.

**Observação:** a projeção de sprites pode exigir um mecanismo de comparação de profundidade, como um *z-buffer* por coluna. Se a implementação completa desse mecanismo exceder o prazo, uma representação visual mais simples poderá ser adotada, desde que a limitação seja documentada.

### Etapa 2.5 — Interface e ciclo de jogo

**Objetivo:** tornar o jogo compreensível e permitir que a experiência seja concluída sem intervenção do desenvolvedor.

Atividades:

- Exibir instruções básicas de controle.
- Mostrar mensagens relacionadas à coleta da chave e ao uso da saída.
- Implementar o estado de vitória.
- Permitir reiniciar a partida.
- Definir o comportamento de encerramento do jogo.
- Revisar o tratamento de entradas e erros.

**Entregável:** jogo demonstrativo com início, objetivo e conclusão.

**Critérios de aceitação:**

- O jogador compreende como se movimentar e interagir.
- A conclusão do objetivo é reconhecida pelo sistema.
- A partida pode ser reiniciada.
- O jogo não depende de alterações manuais no código durante a execução normal.

**Prioridade:** obrigatória.

### Etapa 2.6 — Testes de integração e regressão

**Objetivo:** garantir que as novas funcionalidades não comprometam os mecanismos fundamentais da engine.

Atividades:

- Testar o fluxo completo do jogo.
- Verificar a coleta da chave e a condição de saída.
- Revalidar movimentação e colisões.
- Testar diferentes mapas.
- Corrigir problemas de integração.
- Executar os testes automatizados.
- Verificar o comportamento em uma execução limpa do projeto.

**Entregável:** versão integrada e validada da engine com o jogo demonstrativo.

**Critérios de aceitação:**

- O jogo pode ser concluído do início ao fim.
- Os testes essenciais continuam passando.
- A movimentação e as colisões permanecem funcionais.
- A execução não depende de arquivos ou configurações locais não documentados.

**Prioridade:** obrigatória.

### Etapa 2.7 — Documentação e preparação da apresentação

**Objetivo:** consolidar os resultados técnicos e preparar uma demonstração reproduzível.

Atividades:

- Finalizar o README.
- Documentar a arquitetura e as principais decisões técnicas.
- Explicar o funcionamento do raycasting e da projeção de paredes.
- Documentar os requisitos de execução.
- Registrar as limitações conhecidas.
- Documentar o uso de IA generativa.
- Preparar uma demonstração que percorra o cenário e conclua o objetivo.
- Revisar o histórico de versões e a organização do repositório.

**Entregável:** versão final documentada e pronta para apresentação.

**Critérios de aceitação:**

- Outra pessoa consegue instalar as dependências e executar o projeto seguindo as instruções.
- A arquitetura e os algoritmos principais podem ser explicados.
- O uso de IA está documentado de acordo com os requisitos da disciplina.
- A demonstração pode ser executada sem depender de alterações de última hora no código.

**Prioridade:** obrigatória.

### Marco M2 — Projeto concluído

Ao final da Fase 2, o projeto deverá oferecer:

- Uma engine 2.5D implementada em Python;
- Renderização central por raycasting próprio;
- Carregamento de mapas externos;
- Movimentação e colisões;
- Um jogo demonstrativo com objetivo e condição de vitória;
- Testes automatizados para os componentes essenciais;
- Documentação de instalação, arquitetura e uso;
- Registro do uso de IA generativa;
- Repositório organizado e pronto para avaliação.

---

## 6. Funcionalidades opcionais e critérios de priorização

As funcionalidades opcionais só deverão ser iniciadas quando o núcleo da engine e o fluxo principal do jogo estiverem funcionando.

| Funcionalidade | Valor para o projeto | Prioridade |
|---|---|---|
| Texturas nas paredes | Melhora significativamente a apresentação visual | Alta, após o núcleo |
| Minimap 2D | Facilita a orientação e demonstra a representação interna do mapa | Média |
| Iluminação simplificada | Acrescenta profundidade visual | Baixa |
| Portas interativas adicionais | Amplia as possibilidades de interação | Média |
| Sprites com oclusão correta | Permite representar objetos em perspectiva | Média |
| Inimigos simples | Introduz comportamento de entidades | Baixa |
| Sistema de armas e combate | Amplia o jogo, mas exige novos mecanismos | Baixa |
| Editor visual de mapas | Facilita a criação de cenários, mas amplia bastante o escopo | Baixa |
| Suporte direto a mapas originais de Doom | Aproxima o projeto de uma arquitetura diferente e mais complexa | Fora do escopo inicial |

A ordem deverá ser adaptada ao progresso real. Em caso de atraso, funcionalidades opcionais serão removidas do planejamento antes de reduzir o tempo reservado para testes, documentação ou conclusão do jogo demonstrativo.

## 7. Estratégia de testes e validação

Os testes serão incorporados ao desenvolvimento, em vez de concentrados exclusivamente no final.

### Testes unitários

Deverão verificar o comportamento isolado dos componentes, principalmente:

- Carregamento e validação de mapas;
- Consultas ao mundo;
- Cálculos de movimentação;
- Detecção de colisões;
- Cálculos geométricos do raycasting.

### Testes de integração

Deverão verificar a interação entre os módulos:

- Carregamento do mapa e inicialização do jogador;
- Movimentação e colisões;
- Estado do jogador e renderização;
- Interações e estado do jogo;
- Fluxo completo de vitória e reinicialização.

### Validação visual

A renderização será validada por meio de cenários controlados, incluindo corredores, paredes próximas, mudanças de orientação e mapas com diferentes geometrias.

A inspeção visual será complementada por testes dos cálculos matemáticos sempre que possível. Uma imagem aparentemente correta não garante, isoladamente, que o algoritmo esteja correto em todos os casos.

## 8. Uso de inteligência artificial generativa

A IA generativa será utilizada como ferramenta de apoio ao planejamento, à implementação, à explicação dos algoritmos, à criação de testes e à documentação.

O processo deverá preservar a compreensão técnica do desenvolvedor e permitir a validação independente dos resultados produzidos.

O uso de IA deverá seguir estas práticas:

1. Especificar o comportamento esperado antes de solicitar a implementação de uma funcionalidade.
2. Dividir tarefas grandes em alterações menores e verificáveis.
3. Solicitar explicações dos algoritmos e das decisões técnicas.
4. Revisar o código gerado antes de incorporá-lo ao projeto.
5. Executar testes e analisar os casos-limite.
6. Registrar contribuições relevantes da IA, incluindo falhas identificadas e correções realizadas.
7. Documentar as decisões técnicas finais, independentemente de terem sido propostas pelo desenvolvedor ou pela IA.

A avaliação do projeto deverá considerar não apenas o resultado executável, mas também a capacidade de explicar e justificar a implementação.

## 9. Gestão de riscos

| Risco | Impacto | Mitigação |
|---|---|---|
| Complexidade do raycasting | Alto | Implementar e testar o algoritmo isoladamente antes da integração |
| Dificuldades com colisões | Alto | Utilizar cenários pequenos e testes de movimentação próximos às paredes |
| Renderização incorreta | Alto | Validar cálculos geométricos com casos controlados |
| Crescimento excessivo do escopo | Alto | Priorizar os marcos obrigatórios e adiar extensões |
| Problemas de integração | Médio | Integrar os módulos incrementalmente |
| Desempenho insuficiente | Médio | Começar com resolução e quantidade de raios moderadas |
| Falta de tempo para documentação | Médio | Atualizar a documentação durante o desenvolvimento |
| Dependência excessiva de código gerado por IA | Alto | Revisar, testar e explicar cada componente incorporado |

O principal mecanismo de mitigação será a existência de marcos intermediários funcionais. Se uma funcionalidade opcional ameaçar o cumprimento do prazo, ela deverá ser removida ou simplificada.

## 10. Estimativa de esforço

As estimativas abaixo representam horas efetivas de desenvolvimento, incluindo implementação, depuração e validação. Não representam horas corridas do calendário.

| Etapa | Estimativa |
|---|---:|
| Especificação e planejamento | 3–5 h |
| Estrutura básica da aplicação | 2–3 h |
| Representação do mundo e carregamento de mapas | 3–5 h |
| Movimentação do jogador | 2–4 h |
| Colisões | 3–5 h |
| Raycasting | 5–9 h |
| Renderização pseudo-3D | 3–5 h |
| Integração e testes do núcleo | 4–7 h |
| Texturas e refinamentos | 3–6 h |
| Interações, chave e saída | 5–8 h |
| Representação visual dos objetos | 2–5 h |
| Interface e ciclo de jogo | 2–4 h |
| Testes finais e correções | 3–5 h |
| Documentação e apresentação | 4–7 h |
| **Total estimado** | **44–78 h** |

A estimativa não inclui o desenvolvimento de inimigos, combate, editor visual ou suporte a mapas originais de Doom.

Recomenda-se reservar uma margem adicional de aproximadamente 20% para imprevistos, o que leva o planejamento a cerca de **53–94 horas de disponibilidade total**.

Caso o tempo efetivamente disponível seja menor, a redução de escopo deverá ocorrer primeiro nas funcionalidades opcionais, mantendo o objetivo de entregar uma engine navegável e um jogo demonstrativo concluído.

## 11. Critérios globais de sucesso

O projeto será considerado bem-sucedido quando:

1. A engine renderizar um cenário externo em perspectiva pseudo-3D.
2. O jogador puder explorar o cenário com movimentação e colisões funcionais.
3. O carregamento de mapas não exigir alterações no código-fonte.
4. O jogo demonstrativo possuir um objetivo que possa ser concluído.
5. Os componentes centrais forem organizados de forma modular e testável.
6. O projeto puder ser executado a partir de instruções documentadas.
7. As principais decisões técnicas e o uso de IA forem documentados.
8. O desenvolvedor conseguir explicar o funcionamento dos algoritmos e justificar as escolhas de implementação.

## 12. Próximos passos do SDD

O roadmap define a sequência de desenvolvimento, mas não substitui as especificações de cada funcionalidade.

A próxima etapa será detalhar os requisitos funcionais e não funcionais, incluindo os critérios de aceitação do núcleo da engine. Em seguida, deverão ser definidos os contratos entre módulos, as estruturas de dados e os cenários de teste.

A implementação deverá começar apenas quando houver especificação suficiente para a primeira tarefa, sem exigir que todos os detalhes do projeto estejam definidos antecipadamente.

O processo será incremental: especificar, implementar, testar, revisar e atualizar a documentação. O roadmap também poderá ser revisado quando evidências de implementação demonstrarem que alguma estimativa, dependência ou decisão precisa ser ajustada.