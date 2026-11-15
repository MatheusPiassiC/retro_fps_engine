# Roadmap — RetroFPS Engine

## 1. Proposta para revisão

Este planejamento organiza um projeto universitário de aprendizagem. Não pressupõe experiência prévia com computação gráfica. O estudo dos conceitos faz parte de cada marco e não precisa estar concluído antes do início do projeto.

A referência conceitual é Wolfenstein 3D: mundo em grade, paredes verticais e exploração em primeira pessoa. A entrega mínima é uma engine reutilizável com uma demonstração de navegação. Objetivos, combate e reprodução completa do jogo de referência não são obrigatórios.

Não há datas ou estimativas de horas neste planejamento. O avanço depende das evidências de conclusão. Todos os marcos abaixo estão pendentes; a preparação de documentos e arquivos não significa que seus comportamentos já foram implementados.

O ciclo de trabalho será: entender uma ideia, especificar uma pequena mudança, implementar, verificar, explicar o resultado e atualizar a documentação. Esse uso de especificações será leve e incremental.

## 2. Escopo e prioridades

### Entrega obrigatória

- Pacote Python importável por uma aplicação externa.
- Raycasting próprio em grade, com paredes de altura uniforme e piso e teto de cor sólida.
- Movimento para frente e para trás e rotação horizontal.
- Colisão considerando o volume do jogador e os limites do mapa.
- Mapas externos validados, com pelo menos dois exemplos.
- Demonstração simples que use a engine sem duplicar seus algoritmos.
- Testes explicados, instruções de execução e registro de aprendizado e uso de IA.

### Extensões após o núcleo

Texturas, minimapa para o usuário, deslocamento lateral, objetos, portas, sprites com oclusão, objetivos e reinicialização de partidas. Uma visualização 2D de depuração pode ser antecipada se ajudar a entender um erro, sem se tornar um requisito de produto.

Inimigos, armas, combate e editor visual ficam adiados. Desníveis, mapas originais de Wolfenstein ou Doom e renderização 3D geral ficam fora do escopo inicial.

## 3. Visão dos marcos

| Marco | Resultado demonstrável | Dependência | Prioridade |
|---|---|---|---|
| M0 | Ambiente validado e janela responsiva | Revisão deste planejamento | Obrigatória |
| M1 | Interseções de raios conferidas em mapa pequeno | M0 | Obrigatória |
| M2 | Sala em perspectiva com câmera fixa | M1 | Obrigatória |
| M3 | Navegação com colisões no mapa em memória | M2 | Obrigatória |
| M4 | Dois mapas externos carregados e exploráveis | M3 | Obrigatória |
| M5 | Aplicação externa usando a engine | M4 | Obrigatória |
| M6 | Entrega validada, documentada e explicável | M5 | Obrigatória |
| M7 | Uma extensão escolhida e validada | M6 | Opcional |

Testes e documentação acompanham cada marco. M6 consolida essas verificações, sem adiá-las para o final.

## 4. M0 — Ambiente e ciclo da aplicação

**Aprender:** ambiente virtual, pacote Python, eventos, quadros e diferença entre inicializar uma biblioteca e implementar uma engine.

**Tarefas:**

1. Instalar o pacote em modo editável com as ferramentas de desenvolvimento.
2. Registrar versões efetivamente verificadas e instruções de reprodução.
3. Criar janela Pygame, loop, captura de eventos e encerramento com liberação de recursos.
4. Medir o intervalo entre quadros em segundos e apresentar uma superfície de cor sólida.
5. Definir uma configuração inicial pequena, evitando números espalhados pelo código.

**Entrega:** janela executável e instruções conferidas.

**Aceitação:** o pacote é importável após a instalação; a janela responde; Escape e o botão de fechar encerram normalmente; os comandos de verificação funcionam no ambiente preparado.

**Limite:** sem mapa, projeção, inventário ou sistema de cenas. A mensagem de estado existente no esqueleto não conclui M0.

## 5. M1 — Mundo e primeiro raio

**Aprender:** coordenadas contínuas, índices da grade, vetor de direção e percurso de células pelo DDA, algoritmo que avança entre fronteiras da grade.

**Tarefas:**

1. Implementar a representação do mundo e consulta de células.
2. Usar temporariamente uma sala 5 × 5 em memória, com borda sólida e interior livre.
3. Implementar um raio sem dependência gráfica, retornando célula, lado e parâmetro de impacto.
4. Tratar componentes nulas da direção, direções negativas e saída dos limites.
5. Definir desempate em cruzamentos exatos de cantos e um limite de iterações adequado às dimensões do mundo.
6. Escrever testes com desenhos e resultados calculados antes da implementação.

**Entrega:** interseções conferidas por testes e por uma explicação passo a passo.

**Aceitação:** na sala descrita em [validacao.md](validacao.md), o raio de origem `(2.5, 2.5)` e direção `(1, 0)` encontra a parede em `x = 4`, com parâmetro `1.5`; direções cardinais funcionam; raio nulo é rejeitado; casos de canto terminam conforme a regra documentada.

**Limite:** mapa em memória apenas para estudo; sem carregador de arquivos ou renderização completa.

## 6. M2 — Primeira imagem em perspectiva

**Aprender:** plano da câmera, campo de visão, profundidade perpendicular e projeção de altura em colunas.

**Tarefas:**

1. Definir direção unitária da câmera e vetor perpendicular com comprimento derivado do campo de visão.
2. Calcular um raio para o centro de cada coluna da resolução interna.
3. Usar direções não normalizadas, coerentes com a profundidade perpendicular do DDA.
4. Converter profundidade em altura projetada; limitar o desenho à tela e proteger distâncias próximas de zero.
5. Desenhar paredes coloridas, piso e teto; distinguir lados de parede por tonalidade para facilitar a inspeção.
6. Comparar uma sala e um corredor controlados com a geometria esperada.

**Entrega:** imagem estática em perspectiva, apresentada pelo Pygame.

**Aceitação:** uma parede frontal plana mantém o topo alinhado; elementos mais distantes aparecem menores; a mesma parede, ao dobro da profundidade, tem aproximadamente metade da altura antes do arredondamento e do recorte; a apresentação não trava diante de uma parede próxima.

**Limite:** sem texturas ou sprites. Não aplicar uma correção adicional de fish-eye à formulação que já fornece profundidade perpendicular.

## 7. M3 — Movimento e colisão

**Aprender:** orientação, velocidade, intervalo entre atualizações, volume físico e diferença entre testar um destino e percorrer um deslocamento.

**Tarefas:**

1. Separar comando lógico de movimento das teclas que o produzem.
2. Implementar avanço, recuo e giro; configurar controles iniciais W/S e setas esquerda/direita.
3. Usar velocidades por segundo e ângulos internos em radianos.
4. Representar o jogador por um círculo de raio inicial 0.2 unidade.
5. Verificar colisão círculo-retângulo e resolver deslocamento por eixos para permitir deslizar.
6. Limitar o intervalo aceito a 0.1 segundo por atualização e subdividir o deslocamento em passos de até 0.1 unidade, conforme a proposta arquitetural.
7. Verificar cantos, aproximações oblíquas e movimentos grandes; manter as funções testáveis sem janela.

**Entrega:** cenário em memória explorável com paredes sólidas.

**Aceitação:** avanço, recuo e giro acompanham os comandos; em espaço livre, simulações com diferentes subdivisões de tempo abaixo do limite dão deslocamentos equivalentes dentro de tolerância; o círculo não entra em paredes; é possível deslizar; comandos oblíquos e passos grandes não atravessam obstáculos; sair da grade é impedido.

**Limite:** sem pulo, câmera vertical ou deslocamento lateral obrigatório. O descarte de tempo acima do limite deve estar documentado, sem prometer equivalência após uma pausa longa.

## 8. M4 — Mapas externos

**Aprender:** diferença entre analisar texto, validar dados e construir o estado de uma aplicação.

**Tarefas:**

1. Implementar a sintaxe de [formato_mapa.md](formato_mapa.md).
2. Separar análise de conteúdo da abertura do arquivo, facilitando os testes.
3. Validar grade, bordas, valores numéricos e espaço para o círculo do jogador.
4. Produzir mensagens localizáveis de erro sem iniciar uma sessão inválida.
5. Substituir o mapa temporário pelos arquivos em `maps/`.
6. Permitir indicar o caminho do mapa ao executar a demonstração, sem editar código.

**Entrega:** navegação em `room.map` e `corridor.map`.

**Aceitação:** ambos os arquivos funcionam; editar uma célula válida muda o cenário após recarregar; arquivo inexistente, grade irregular, borda aberta, spawn em parede e valores não finitos são rejeitados; testes de arquivo usam diretórios temporários.

**Limite:** sem interpretar regras específicas de jogo e sem editor visual.

## 9. M5 — Uso por uma aplicação externa

**Aprender:** API pública, composição de componentes e direção de dependências.

**Tarefas:**

1. Consolidar a API mínima de mundo, carregamento, configuração e sessão, com exemplos de chamada.
2. Permitir que a aplicação forneça comandos e coordene atualização e desenho. Um executor de conveniência pode manter o loop para o caso simples.
3. Implementar `examples/exploration` como aplicação que importa o pacote instalado.
4. Manter apresentação de instruções e seleção de cenário no exemplo; manter mecanismos reutilizáveis na engine.
5. Executar dois mapas e pelo menos duas configurações sem alterar os arquivos do núcleo.

**Entrega:** exemplo externo curto com instruções próprias.

**Aceitação:** o exemplo não copia DDA, colisões ou projeção; o núcleo não importa o exemplo; os componentes geométricos podem ser usados sem inicializar Pygame; outra aplicação pode carregar um mundo e controlar a sessão pela API documentada.

**Limite:** não construir um framework genérico de plugins, um sistema de entidades ou um segundo jogo completo apenas para demonstrar reutilização.

## 10. M6 — Consolidação e entrega acadêmica

**Aprender:** medir desempenho, identificar limites e demonstrar funcionamento com evidências reproduzíveis.

**Tarefas:**

1. Executar os testes e verificações estáticas; corrigir problemas do núcleo.
2. Percorrer manualmente os dois mapas, testar encerramento e repetir a instalação em ambiente limpo.
3. Medir desempenho na resolução interna proposta, registrando máquina, mapa e configuração. Usar 30 FPS como meta inicial; investigar o custo antes de adicionar dependências.
4. Finalizar instruções de execução, controles, API mínima e limitações conhecidas.
5. Registrar as decisões e contribuições de IA e preparar uma explicação dos algoritmos com um exemplo desenhado.
6. Preparar um percurso demonstrável, sem depender de alterações no código durante a apresentação.

**Entrega:** engine navegável, exemplo reutilizando o pacote e documentação coerente com o comportamento real.

**Aceitação global:** outra pessoa consegue instalar e explorar um mapa; duas geometrias externas funcionam; colisões e renderização estão verificadas; as responsabilidades estão separadas; o desenvolvedor consegue explicar o percurso de um raio, a altura de uma parede e a resolução de um movimento bloqueado.

**Limite:** defeitos relevantes devem ser corrigidos ou explicitados. Extensões não substituem a conclusão do núcleo.

## 11. M7 — Extensões opcionais

Escolher uma extensão por vez após M6, com uma especificação curta e novos critérios de aceitação.

| Extensão | Dependências e verificação mínima |
|---|---|
| Texturas de parede | Coordenada de impacto; orientação correta e ausência de regressão de navegação |
| Minimapa | Transformação de coordenadas; posição e direção coerentes com a visão principal |
| Deslocamento lateral | Composição e normalização de comandos; sem aumento indevido de velocidade diagonal |
| Sprites | Projeção e profundidade por coluna; objetos ocultos pelas paredes certas |
| Objetivo simples | Regra na aplicação externa; objetivo visível, alcançável e reconhecido |
| Portas | Estado geométrico e colisão coerentes; especificação própria antes de implementar |

Se for escolhido um jogo com chave e saída, a representação dos objetos, o bloqueio de interação através de paredes, a vitória e o reinício passam a fazer parte da aceitação dessa extensão. Inventário e vitória continuam sendo regras do jogo.

## 12. Como trabalhar com IA e acompanhar progresso

Para cada tarefa, registrar objetivo, comportamento esperado, exemplo verificável, alteração feita e resultado. Usar [uso_ia.md](uso_ia.md) para contribuições relevantes e [validacao.md](validacao.md) para evidências.

A IA deve explicar os conceitos necessários antes de propor mudanças extensas. Quando o desenvolvedor ainda não souber avaliar um teste, apresentar o desenho, as contas e a razão do resultado esperado. A falta de conhecimento prévio é um ponto de partida de estudo, não um motivo para aceitar automaticamente o resultado gerado.

O marco só muda para concluído após a execução das verificações e a explicação de seus resultados. Se o aprendizado mostrar que uma decisão foi inadequada, registrar o motivo, rever a proposta e repetir os casos afetados.

## 13. Riscos e resposta

| Risco | Resposta planejada |
|---|---|
| Dificuldade com geometria | Começar com uma sala pequena e um raio; desenhar e calcular antes de generalizar |
| Testes reproduzirem erro da implementação | Derivar exemplos independentes e combinar matemática, testes e inspeção visual |
| Arquitetura crescer antes da necessidade | Introduzir contratos pequenos; adiar abstrações até existir um uso concreto |
| Regras da demonstração invadirem a engine | Revisar dependências e manter objetivos no exemplo externo |
| Colisões falharem em cantos ou travamentos | Validar volume, subpassos e limites de tempo com casos específicos |
| Desempenho insuficiente | Medir e reduzir resolução interna antes de otimizar a matemática ou adotar bibliotecas |
| Acúmulo de código incompreendido | Diminuir a tarefa e explicar o componente antes de prosseguir |

O primeiro passo após a revisão deste planejamento é M0. Não é necessário detalhar antecipadamente as extensões para começar a aprender com a implementação.
