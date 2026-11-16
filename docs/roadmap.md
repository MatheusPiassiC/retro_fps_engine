# Roadmap — RetroFPS Engine

## 1. Proposta para revisão

Este planejamento organiza um projeto universitário de aprendizagem. Não pressupõe experiência prévia com computação gráfica. O estudo dos conceitos faz parte de cada marco e não precisa estar concluído antes do início do projeto.

A referência conceitual é Wolfenstein 3D: mundo em grade, paredes verticais e exploração em primeira pessoa. A entrega mínima é uma engine reutilizável com uma demonstração de navegação. Objetivos, combate e reprodução completa do jogo de referência não são obrigatórios.

Não há datas ou estimativas de horas neste planejamento. O avanço depende das evidências de conclusão. M0, M1 e M2 estão concluídos no ambiente atual, M3 está em andamento e os demais marcos estão pendentes; a preparação de documentos e arquivos não significa que seus comportamentos já foram implementados.

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

| Marco | Resultado demonstrável | Dependência | Prioridade | Estado |
|---|---|---|---|---|
| M0 | Ambiente validado e janela responsiva | Revisão deste planejamento | Obrigatória | Concluído (tag `M0`) |
| M1 | Interseções de raios conferidas em mapa pequeno | M0 | Obrigatória | Concluído |
| M2 | Sala em perspectiva com câmera fixa | M1 | Obrigatória | Concluído |
| M3 | Navegação com colisões no mapa em memória | M2 | Obrigatória | Em andamento |
| M4 | Dois mapas externos carregados e exploráveis | M3 | Obrigatória | Pendente |
| M5 | Aplicação externa usando a engine | M4 | Obrigatória | Pendente |
| M6 | Entrega validada, documentada e explicável | M5 | Obrigatória | Pendente |
| M7 | Uma extensão escolhida e validada | M6 | Opcional | Pendente |

Testes e documentação acompanham cada marco. M6 consolida essas verificações, sem adiá-las para o final.

## 4. M0 — Ambiente e ciclo da aplicação

**Aprender:** ambiente virtual, pacote Python, eventos, quadros e diferença entre inicializar uma biblioteca e implementar uma engine.

**Tarefas:**

1. Instalar o pacote em modo editável com as ferramentas de desenvolvimento. **Concluída (M0-1):** instalação confirmada pelo desenvolvedor e versões conferidas em M0-2.
2. Registrar versões efetivamente verificadas e instruções de reprodução. **Concluída (M0-2):** versões do ambiente existente registradas e instruções documentadas; instalação em ambiente novo não verificada nesta tarefa. Ver [evidências](validacao.md#7-m0-2--versões-do-ambiente).
3. Criar janela Pygame, loop, captura de eventos e encerramento com liberação de recursos. **Concluída (M0-3), com conferência visual confirmada pelo desenvolvedor:** ver [evidências e procedimento manual](validacao.md#8-m0-3--ciclo-inicial-da-janela).
4. Medir o intervalo entre quadros em segundos e apresentar uma superfície de cor sólida. **Concluída (M0-4), com conferência visual confirmada pelo desenvolvedor:** ver [evidências](validacao.md#9-m0-4-e-m0-5--tempo-desenho-e-configuração).
5. Definir uma configuração inicial pequena, evitando números espalhados pelo código. **Concluída (M0-5), na mesma entrega de M0-4:** configuração de janela em `WindowConfig`; conferência visual confirmada pelo desenvolvedor.

**Estado:** M0 concluído e integrado, com tag `M0`, instalação relatada pelo desenvolvedor, versões registradas, verificações pontuais e estáticas e validação visual confirmada. Na conclusão de M0, pytest ainda não coletava testes; reprodução em ambiente limpo não verificada nesta etapa, conforme registro de M0-2.

**Entrega:** janela executável e instruções conferidas.

**Aceitação:** o pacote é importável após a instalação; a janela responde; Escape e o botão de fechar encerram normalmente; os comandos de verificação funcionam no ambiente preparado.

**Limite:** sem mapa, projeção, inventário ou sistema de cenas. A mensagem de estado existente no esqueleto não conclui M0.

## 5. M1 — Mundo e primeiro raio

**Aprender:** coordenadas contínuas, índices da grade, vetor de direção e percurso de células pelo DDA, algoritmo que avança entre fronteiras da grade.

**Tarefas:**

1. Implementar a representação do mundo e consulta de células. **Concluída (M1-1):** `World` imutável, dimensões, consultas e limites implementados; 20 casos automatizados aprovados, código aprovado e conferência manual confirmada pelo desenvolvedor. Ver [evidências](validacao.md#10-m1-1--representação-do-mundo-e-consulta-de-células).
2. Usar temporariamente uma sala 5 × 5 em memória, com borda sólida e interior livre. **Concluída (M1-2):** `create_study_world()` implementada, três novos testes aprovados e entrega aprovada pelo desenvolvedor. Ver [evidências](validacao.md#11-m1-2--sala-temporária-em-memória).
3. Implementar um raio sem dependência gráfica, retornando célula, lado e parâmetro de impacto. **Concluída (M1-3):** DDA implementado e aprovado pelo desenvolvedor; ver [evidências](validacao.md#12-m1-3-e-m1-4--percurso-de-raios).
4. Tratar componentes nulas da direção, direções negativas e saída dos limites. **Concluída (M1-4):** direções cardinais, saída da grade e entradas inválidas testadas; entrega aprovada pelo desenvolvedor.
5. Definir desempate em cruzamentos exatos de cantos e um limite de iterações adequado às dimensões do mundo. **Concluída (M1-5):** prioridade de x em empate exato e orçamento de largura + altura implementados, testados e aprovados pelo desenvolvedor. Ver [evidências](validacao.md#13-m1-5--cantos-e-limite-de-avanços).
6. Escrever testes com desenhos e resultados calculados antes da implementação. **Concluída (M1-6):** cobertura revisada e complementada, 104 casos aprovados, percurso explicado e validação confirmada pelo desenvolvedor. Ver [evidências](validacao.md#14-m1-6--revisão-dos-testes-e-explicação-do-percurso).

**Estado:** M1 concluído no ambiente atual: critérios de aceitação cobertos por testes e explicações, com validação final confirmada pelo desenvolvedor. Integração de M1-6 por PR é uma etapa separada; não foi criada tag do marco nesta tarefa.

**Entrega:** interseções conferidas por testes e por uma explicação passo a passo.

**Aceitação:** na sala descrita em [validacao.md](validacao.md), o raio de origem `(2.5, 2.5)` e direção `(1, 0)` encontra a parede em `x = 4`, com parâmetro `1.5`; direções cardinais funcionam; raio nulo é rejeitado; casos de canto terminam conforme a regra documentada.

**Limite:** mapa em memória apenas para estudo; sem carregador de arquivos ou renderização completa.

## 6. M2 — Primeira imagem em perspectiva

**Aprender:** plano da câmera, campo de visão, profundidade perpendicular e projeção de altura em colunas.

**Tarefas:**

1. Definir direção unitária da câmera e vetor perpendicular com comprimento derivado do campo de visão. **Concluída (M2-1):** `Camera` implementada, 24 novos testes aprovados e etapa aprovada pelo desenvolvedor após explicação. Ver [evidências](validacao.md#15-m2-1--geometria-da-câmera).
2. Calcular um raio para o centro de cada coluna da resolução interna. **Concluída (M2-2):** `Camera.ray_direction()` implementado e validado pelo desenvolvedor; ver [evidências](validacao.md#16-m2-2-e-m2-3--raios-pelos-centros-das-colunas).
3. Usar direções não normalizadas, coerentes com a profundidade perpendicular do DDA. **Concluída (M2-3):** comprimento dos raios e profundidade frontal constante conferidos por testes integrados com o DDA; etapa validada pelo desenvolvedor.
4. Converter profundidade em altura projetada; limitar o desenho à tela e proteger distâncias próximas de zero. **Concluída (M2-4):** projeção independente de Pygame, recorte e proteção implementados, com 29 testes novos e aprovação do desenvolvedor. Ver [evidências](validacao.md#17-m2-4--projeção-e-recorte).
5. Desenhar paredes coloridas, piso e teto; distinguir lados de parede por tonalidade para facilitar a inspeção. **Concluída (M2-5):** sala estática apresentada pelo comando principal, com ampliação proporcional, testes de pixels e loop e conferência visual confirmada pelo desenvolvedor. Ver [evidências](validacao.md#18-m2-5--primeira-imagem-em-perspectiva).
6. Comparar uma sala e um corredor controlados com a geometria esperada. **Concluída (M2-6):** oito novos casos de geometria, impactos e pixels; comparação visual de quatro cenas confirmada pelo desenvolvedor. Ver [evidências](validacao.md#19-m2-6--comparação-controlada-de-sala-e-corredor).

**Estado:** M2 concluído no ambiente atual, com critérios geométricos cobertos por testes e conferência visual confirmada. Integração de M2-6 por PR e eventual tag são etapas separadas.

**Entrega:** imagem estática em perspectiva, apresentada pelo Pygame.

**Aceitação:** uma parede frontal plana mantém o topo alinhado; elementos mais distantes aparecem menores; a mesma parede, ao dobro da profundidade, tem aproximadamente metade da altura antes do arredondamento e do recorte; a apresentação não trava diante de uma parede próxima.

**Limite:** sem texturas ou sprites. Não aplicar uma correção adicional de fish-eye à formulação que já fornece profundidade perpendicular.

## 7. M3 — Movimento e colisão

**Aprender:** orientação, velocidade, intervalo entre atualizações, volume físico e diferença entre testar um destino e percorrer um deslocamento.

**Tarefas:**

1. Separar comando lógico de movimento das teclas que o produzem. **Concluída (M3-1):** estado imutável e comandos independentes do teclado aprovados pelo desenvolvedor; ver seção 20 da [validação](validacao.md).
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

O desenvolvimento seguirá [GitHub Flow](fluxo_desenvolvimento.md), com branches por feature e pull requests para a branch principal. Cada tarefa usa um identificador local formado pelo marco e sua posição na lista: **M0-1** corresponde à instalação editável; **M0-2**, ao registro de versões; **M0-3**, à criação da janela.

As issues são descrições locais de tarefas, sem cadastro obrigatório no GitHub. A numeração reinicia em cada marco e não corresponde a números de issues remotas. Cada tarefa terá escopo, dependências, aprendizado e critérios de aceitação. Uma branch resolve uma mudança coesa, sem concentrar todo o marco. Manter os identificadores já usados estáveis nas revisões do planejamento.

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
