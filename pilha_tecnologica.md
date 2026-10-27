# Pilha de Tecnologia — RetroFPS Engine

## 1. Linguagem de programação

**Python 3.12 ou superior, conforme a compatibilidade das dependências.**

Python será a linguagem principal do projeto. Sua sintaxe relativamente simples e seu ecossistema de bibliotecas permitem concentrar o esforço de desenvolvimento nos conceitos fundamentais da engine, como geometria, raycasting, projeção de perspectiva, movimentação e detecção de colisões.

A linguagem também facilita a organização do código em módulos, a implementação de testes automatizados e a experimentação com diferentes algoritmos de renderização.

## 2. Biblioteca gráfica e entrada de dados

**Pygame 2.x.**

O Pygame será utilizado para fornecer a infraestrutura básica de execução da aplicação, incluindo:

- Criação e gerenciamento da janela;
- Captura de eventos de teclado;
- Controle do ciclo principal da aplicação;
- Desenho de primitivas gráficas e imagens;
- Carregamento e apresentação de texturas;
- Reprodução de efeitos sonoros, caso sejam incorporados ao projeto.

O Pygame não deverá ser utilizado como substituto da implementação central da engine. O algoritmo de raycasting, a projeção das paredes, a movimentação do jogador, a lógica de colisões e o carregamento dos mapas serão desenvolvidos pelo próprio projeto.

Essa restrição garante que o trabalho explore efetivamente os fundamentos técnicos da renderização pseudo-3D, em vez de apenas integrar funcionalidades prontas de um motor de jogos.

## 3. Biblioteca para operações numéricas

**NumPy — opcional, condicionado à necessidade.**

O NumPy poderá ser utilizado para operações vetoriais, cálculos numéricos e manipulação de matrizes ou imagens, caso essas operações se mostrem úteis durante o desenvolvimento.

Entretanto, a implementação inicial deverá priorizar estruturas de dados e operações simples em Python sempre que isso não comprometer o desempenho necessário. Essa abordagem favorece a compreensão dos algoritmos e evita introduzir dependências sem uma justificativa concreta.

A necessidade do NumPy deverá ser reavaliada após a implementação inicial do renderizador.

## 4. Testes automatizados

**pytest.**

O pytest será utilizado para implementar testes automatizados dos componentes que não dependem diretamente da renderização gráfica.

Os testes deverão priorizar:

- Validação e carregamento de mapas;
- Verificação dos limites do cenário;
- Cálculos de movimentação e rotação;
- Detecção de colisões;
- Comportamento do jogador próximo às paredes;
- Tratamento de mapas inválidos e entradas inconsistentes.

Sempre que possível, os componentes deverão ser projetados para permitir testes independentes da janela gráfica. Isso reduz a dificuldade de depuração e facilita a identificação de erros nos algoritmos.

## 5. Controle de versão e hospedagem do código

**Git e GitHub.**

O Git será utilizado para registrar a evolução do projeto, permitindo acompanhar alterações, recuperar versões anteriores e organizar o desenvolvimento em etapas.

O GitHub será utilizado como repositório remoto privado, conforme os requisitos da disciplina. O repositório deverá conter o código-fonte, as instruções de execução, a documentação técnica e os registros relevantes do uso de inteligência artificial generativa.

Commits pequenos e descritivos deverão ser utilizados para facilitar a revisão do histórico de desenvolvimento.

## 6. Formato dos mapas

**Formato textual próprio, com extensão `.map`.**

Os cenários serão definidos em arquivos externos ao código-fonte, utilizando inicialmente uma representação baseada em uma grade bidimensional.

Cada célula representará um espaço livre ou uma parede. O arquivo também poderá definir a posição e a orientação inicial do jogador.

Exemplo conceitual:

    MAP
    11111111
    10000001
    10110001
    10000001
    11111111
    PLAYER 2.5 2.5 0

Nesse formato, `0` representa espaço livre, `1` representa parede e `PLAYER` define a posição inicial e o ângulo do jogador.

O carregador de mapas deverá interpretar e validar esses arquivos antes de disponibilizar o cenário para a engine. A especificação definitiva da sintaxe será estabelecida durante o detalhamento dos requisitos.

A adoção de um formato próprio permite demonstrar a independência entre a definição do cenário e a implementação da engine, além de facilitar a criação de novos mapas sem alterações no código-fonte.

## 7. Ambiente de desenvolvimento e dependências

O projeto deverá utilizar um ambiente virtual Python para isolar suas dependências e evitar conflitos com outros projetos instalados no sistema.

As dependências diretas deverão ser documentadas em um arquivo `requirements.txt`, permitindo a instalação reproduzível do ambiente de desenvolvimento.

A execução deverá ser possível a partir de instruções documentadas no README do repositório, sem exigir configurações manuais não registradas.

A compatibilidade deverá ser verificada no ambiente de desenvolvimento utilizado durante a disciplina.

## 8. Organização arquitetural

A implementação deverá ser organizada em módulos com responsabilidades bem definidas. A estrutura inicial proposta é:

    retro-fps-engine/
    ├── main.py
    ├── requirements.txt
    ├── README.md
    ├── assets/
    │   └── textures/
    ├── maps/
    │   └── demo.map
    ├── src/
    │   ├── engine.py
    │   ├── world.py
    │   ├── player.py
    │   ├── renderer.py
    │   ├── collision.py
    │   └── map_loader.py
    ├── tests/
    └── docs/

Essa estrutura é uma proposta inicial, sujeita a ajustes durante o detalhamento da arquitetura.

Os principais módulos terão as seguintes responsabilidades:

- **Engine:** coordenar o ciclo principal da aplicação e a comunicação entre os componentes.
- **World:** representar o cenário e disponibilizar operações de consulta ao mapa.
- **Player:** armazenar o estado do jogador e implementar os cálculos de movimentação e orientação.
- **Renderer:** implementar o raycasting e a renderização pseudo-3D do ambiente.
- **Collision:** verificar se os movimentos propostos são válidos e impedem a passagem através de paredes.
- **Map Loader:** interpretar e validar os arquivos externos que descrevem os cenários.

A separação deverá permitir que os componentes sejam desenvolvidos, testados e aprimorados com o mínimo possível de dependências mútuas.

## 9. Restrições tecnológicas

Para preservar os objetivos educacionais do projeto, serão adotadas as seguintes restrições:

- Não utilizar engines de jogos prontas, como Unity, Unreal Engine ou Godot, para implementar o núcleo de renderização.
- Não utilizar bibliotecas que já forneçam uma implementação completa de raycasting ou de renderização pseudo-3D como substitutas do algoritmo desenvolvido no projeto.
- Utilizar o Pygame como infraestrutura de janela, entrada e apresentação gráfica, mantendo sob responsabilidade do projeto os algoritmos centrais da engine.
- Evitar dependências adicionais sem justificativa técnica ou benefício claro.
- Priorizar componentes modulares, testáveis e documentados.

## 10. Critérios para revisão da pilha tecnológica

A pilha tecnológica deverá ser reavaliada se forem identificadas limitações relevantes de desempenho, compatibilidade ou complexidade de implementação.

A adoção de novas bibliotecas deverá ser justificada pela necessidade que motivou a mudança, considerando seu impacto na arquitetura e nos objetivos educacionais do projeto.

O critério principal para avaliar a adequação da pilha será sua capacidade de sustentar uma engine funcional, compreensível, testável e executável dentro do prazo da disciplina.