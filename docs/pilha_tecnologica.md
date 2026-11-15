# Pilha tecnológica — RetroFPS Engine

## 1. Diretrizes

Este é um projeto de aprendizagem. As escolhas abaixo são uma base inicial para experimentação e poderão ser revistas mediante evidências. O recorte visual é inspirado em Wolfenstein 3D; a arquitetura detalhada está em [arquitetura.md](arquitetura.md).

## 2. Linguagem e apresentação gráfica

- **Python 3.12:** versão de referência inicial. Versões posteriores dependerão de verificação de compatibilidade; o projeto ainda não possui uma matriz de versões validada.
- **Pygame 2.x:** janela, eventos, teclado, relógio, desenho e apresentação de imagens. Raycasting, projeção, colisões e carregamento de mapas serão próprios.
- **Biblioteca padrão:** matemática, caminhos de arquivos, estruturas de dados e tratamento de erros.

O primeiro renderizador utilizará paredes coloridas e piso e teto de cor sólida. A resolução interna proposta é 320 × 200, ampliada para a janela. O campo de visão horizontal inicial será de 60 graus. Esses valores são parâmetros revisáveis, não requisitos de fidelidade ao jogo de referência.

A primeira meta de desempenho será sustentar aproximadamente 30 FPS no computador de demonstração. Ela deverá ser medida com mapa e configuração registrados, e não considerada uma garantia antecipada. Aumentar a resolução só será prioridade depois de validar a geometria.

## 3. Dependências adicionais

**pytest** será a ferramenta de testes dos componentes matemáticos e de dados. **Ruff** será usado para verificações estáticas e formatação. São ferramentas de desenvolvimento, separadas da dependência de execução.

**NumPy** fica adiado. Sua adoção depende de medição que mostre uma necessidade concreta e de uma explicação do benefício. A implementação inicial deve favorecer cálculos legíveis em Python.

Não serão utilizadas engines prontas ou bibliotecas de raycasting para substituir o núcleo que o projeto pretende estudar.

## 4. Ambiente e empacotamento

O projeto utilizará ambiente virtual e `pyproject.toml` para metadados, dependências diretas e configurações das ferramentas. O código importável estará em `src/retro_fps/`.

Os intervalos de versão no arquivo de configuração expressam compatibilidade pretendida; não garantem um ambiente idêntico. Em M0, após instalar e verificar as ferramentas, será criado um registro das versões efetivamente usadas para reprodução. Não serão inventadas versões fixas antes dessa validação.

Os comandos estão no [README](../README.md). A preparação atual disponibiliza apenas o pacote e uma mensagem de estado; a janela e a engine serão implementadas após a revisão do planejamento.

## 5. Cenários e recursos

Os mapas serão arquivos textuais `.map`, em UTF-8. A versão inicial suporta células livres, paredes e uma posição de início. Sintaxe, coordenadas e regras de validação estão em [formato_mapa.md](formato_mapa.md).

Texturas futuras ficam em `assets/textures/`. O projeto deverá usar recursos próprios ou com permissão de uso e registrar sua origem. A referência a Wolfenstein 3D não implica reutilização de seus recursos.

## 6. Controle de versão

Git registrará mudanças pequenas e coerentes. O trabalho seguirá [GitHub Flow](fluxo_desenvolvimento.md), com branches por feature, tarefas locais associadas aos marcos e integração por pull request. A hospedagem remota e sua visibilidade seguirão os requisitos efetivamente informados pela disciplina; esta documentação não presume que o repositório precise ser privado.

A documentação, os testes e os exemplos evoluirão junto com o código. Novas dependências e alterações relevantes no formato de mapa exigirão justificativa e atualização dos documentos correspondentes.

## 7. Referências técnicas

- [Tutorial de raycasting de Lode Vandevenne](https://lodev.org/cgtutor/raycasting.html): DDA, plano da câmera e distância perpendicular. O tutorial usa C++; os conceitos deverão ser compreendidos antes de adaptados.
- [Documentação do relógio do Pygame](https://www.pygame.org/docs/ref/time.html): medição do intervalo entre quadros.
- [Python Packaging User Guide — organização com src](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/): separação entre pacote importável e arquivos do repositório.

As referências orientam o estudo; o projeto não depende de copiar uma implementação completa.

## 8. Justificativa das escolhas e alternativas

As justificativas abaixo são decisões deste projeto, considerando aprendizagem, escopo e quantidade de ferramentas a dominar. Não constituem uma classificação geral das tecnologias.

| Escolha | Por que usar aqui | Alternativa considerada e motivo para não adotá-la agora | Custo ou limite aceito |
|---|---|---|---|
| Python | É a linguagem escolhida para o estudo e permite expressar geometria com pouco código de infraestrutura | C, C++ ou Rust permitiriam estudar outros aspectos de desempenho e memória, mas acrescentariam uma segunda frente de aprendizagem | Laços intensivos de raycasting podem limitar a resolução; medir antes de otimizar |
| Python 3.12 como referência | Estabelece uma base concreta para preparar o ambiente | Exigir sempre a versão mais recente tornaria a configuração um alvo móvel | A versão não é requisito matemático da engine; será revista se a instalação indicar necessidade |
| Pygame | Oferece janela, superfícies, eventos e relógio, mantendo o controle explícito do ciclo da aplicação e dos desenhos | Pyglet também oferece janela e multimídia, com suporte a OpenGL; essa rota acrescentaria conceitos gráficos que não precisamos para desenhar as primeiras colunas. Godot resolveria problemas além do recorte, mas usar sua renderização central contrariaria a missão | O renderizador fica acoplado às superfícies do Pygame, embora a geometria permaneça independente |
| Biblioteca padrão | `math`, `pathlib` e estruturas simples atendem à matemática e à leitura inicial | NumPy é útil para operações em lote, mas o primeiro DDA avança uma célula por vez e deve permanecer fácil de acompanhar | Não presumir que Python puro alcançará qualquer meta de desempenho |
| pytest | Funções de teste com `assert`, parametrização e recursos de preparação facilitam repetir casos geométricos e testar arquivos temporários | `unittest` é uma opção válida sem dependência adicional; preferimos a forma concisa dos testes deste projeto | Mais uma dependência de desenvolvimento; resultados esperados continuam precisando de justificativa |
| Ruff | Reúne lint e formatação em uma ferramenta, reduzindo configurações separadas | Black com Flake8 também atenderia, mas exigiria coordenar ferramentas distintas | As regras selecionadas não provam correção matemática e não substituem testes ou revisão |
| `venv` e pip | São suficientes para isolar o ambiente e instalar o pacote com um fluxo pequeno | Poetry ou uv poderiam administrar mais etapas, mas não há necessidade demonstrada de acrescentá-los agora | O registro reproduzível de versões ainda precisa ser preparado; ambiente virtual sozinho não fixa versões |
| `pyproject.toml` e setuptools | Centralizam metadados e ferramentas e permitem instalar uma biblioteca importável, inclusive em modo editável | Apenas `requirements.txt` listaria dependências, mas não definiria por si só o pacote. Hatchling é outra opção de backend; não há requisito atual que motive uma troca | Setuptools é uma escolha prática inicial, não uma exigência da arquitetura |
| Organização `src/` | Separa o pacote importável de documentação e exemplos e incentiva conferir sua instalação | Uma organização plana seria mais curta, mas pode permitir imports locais que ocultam falhas de empacotamento | É necessário instalar o pacote no ambiente para o fluxo normal de desenvolvimento |
| Texto próprio `.map` | Deixa a grade visível e torna o carregador um exercício pequeno e explícito de análise e validação | JSON evitaria uma parte da análise de sintaxe e seria uma escolha válida; o formato próprio foi mantido por seu valor didático e legibilidade da grade | Precisamos manter uma especificação, mensagens de erro e testes; não evoluir isso para uma linguagem complexa |
| Git | Permite comparar alterações, recuperar versões e revisar contribuições pequenas de IA | Cópias manuais de pastas não oferecem o mesmo histórico estruturado | Commits precisam ser feitos com intenção; o uso da ferramenta sozinho não garante um histórico útil |

### Raycasting também é uma escolha técnica

O raycasting em grade combina diretamente com o recorte inspirado em Wolfenstein 3D: encontrar paredes num plano e projetar sua altura. Ele permite estudar perspectiva sem implementar uma cadeia completa de triângulos, transformações e rasterização 3D.

Uma renderização 3D geral permitiria formas e alturas mais variadas, ao custo de ampliar muito o problema. O limite aceito é explícito: o núcleo inicial trabalha com células e paredes de altura uniforme. Essa decisão condiciona os jogos que poderão usar a engine.

### Quando reconsiderar

Revisar uma ferramenta quando uma medição, dificuldade de instalação ou recurso necessário justificar a mudança. Por exemplo, se a apresentação não alcançar a meta após os ajustes simples, identificar primeiro se o custo está no DDA, no desenho ou no escalonamento da imagem. Uma biblioteca numérica só ajuda se atuar sobre o custo identificado.

### Fontes sobre as ferramentas

- [Pygame: documentação e ciclo básico](https://www.pygame.org/docs/).
- [Pyglet: recursos e suporte a OpenGL](https://docs.pyglet.org/en/latest/).
- [pytest: testes com assert e recursos de teste](https://www.pytest.org/en/latest/).
- [Ruff: linter](https://docs.astral.sh/ruff/linter/) e [formatador](https://docs.astral.sh/ruff/formatter/).

As fontes descrevem capacidades das ferramentas. A preferência por uma delas no projeto é uma decisão contextual registrada acima.
