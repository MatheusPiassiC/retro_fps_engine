# Uso de IA e registro de aprendizagem

## 1. Diretriz

A IA apoia explicações, planejamento, implementação, testes e documentação. O objetivo é construir compreensão ao longo do projeto. A aprovação de uma alteração não exige conhecimento prévio de todos os conceitos, mas exige oportunidade de entendê-los e verificar suas consequências.

Antes de incorporar um algoritmo central, solicitar um exemplo pequeno, o significado das variáveis e uma explicação de seus limites. Se a explicação não estiver clara, reduzir a tarefa antes de continuar.

## 2. Modelo de registro

- **Marco e tarefa (código local do roadmap):**
- **Tarefa, branch e PR (quando disponíveis):**
- **Ferramenta/modelo, quando conhecido:**
- **Pedido e contribuição relevante:**
- **Decisão adotada e justificativa:**
- **Verificação independente e resultado:**
- **Erro encontrado ou dúvida pendente:**
- **Aprendizado explicado com palavras próprias:**

Registrar contribuições relevantes e correções; não é necessário copiar integralmente todas as conversas. Requisitos adicionais da disciplina deverão ser incorporados quando forem informados.

## 3. Registro inicial — revisão do planejamento

- **Contribuição:** avaliação dos documentos e proposta de roadmap incremental, arquitetura reutilizável, convenções geométricas e estrutura de repositório.
- **Direção solicitada pelo desenvolvedor:** projeto de estudo, referência em Wolfenstein 3D, ausência de calendário e demonstração mínima de exploração.
- **Propostas:** núcleo independente de objetivos de jogo, raio físico do jogador de 0.2 unidade e mapas de grade com bordas fechadas. Esses parâmetros poderão ser revistos com experimentos.
- **Correção identificada:** o exemplo anterior posicionava o jogador em uma célula sólida; os mapas atuais usam início em área livre.
- **Verificação realizada:** sintaxe dos módulos Python e do TOML, existência dos destinos dos links locais, retangularidade e bordas dos dois mapas e espaço livre para o círculo inicial. A entrada provisória foi executada usando o código em `src/` e exibiu a mensagem esperada. Essas conferências foram feitas por um script pontual, sem criar testes artificiais para os módulos vazios.
- **Limites da verificação:** dependências não foram instaladas e a instalação editável ainda não foi validada. Não há implementação ou validação dos algoritmos da engine nesta etapa.
- **Pendente:** avaliação do planejamento pelo desenvolvedor e estudo dos conceitos nos primeiros marcos.

## 4. Registro — justificativas da stack e da arquitetura

- **Pedido:** explicar as ferramentas escolhidas, suas alternativas e o estilo arquitetural para apoiar o aprendizado.
- **Contribuição:** tabela de decisões da stack, limites aceitos, diagrama de dependências e distinção entre estilo arquitetural, padrões e princípios.
- **Decisão proposta:** arquitetura modular em um processo, com núcleo computacional independente da infraestrutura; uso planejado de Game Loop, composição e dependências fornecidas por parâmetros.
- **Precisão de escopo:** a proposta tem afinidade com a separação defendida pela arquitetura hexagonal, mas ainda não implementa suas portas e adaptadores formalmente.
- **Verificação:** revisão documental e conferência de links locais; nenhuma funcionalidade da engine foi acrescentada ou testada nesta alteração.

## 5. Registro — fluxo de desenvolvimento (proposta inicial)

- **Pedido:** adotar GitHub Flow e identificar o trabalho por marco e issue.
- **Contribuição:** documentação do ciclo issue → branch → implementação e validação → PR → integração, com convenções e exemplos.
- **Estado:** documentação preparada; nenhum item remoto ou branch foi criado nesta alteração. A exigência inicial de issues remotas foi substituída pela decisão da seção 9.

## 6. Registro — nomenclatura inicial de branches (substituída)

- **Pedido:** adotar nomes como `feat/(M0-3)create-pygame-window`, com hífens entre palavras e descrições específicas.
- **Contribuição:** atualização da convenção e das orientações para IA, incluindo exemplo de comando com o nome entre aspas.
- **Estado:** alteração documental; nenhum nome de branch existente foi alterado. Esta convenção foi substituída pela decisão registrada na seção 7; a regra atual está em [fluxo de desenvolvimento](fluxo_desenvolvimento.md).

## 7. Registro - preparação do ambiente

- **Marco e tarefa:** M0-1
- **Tarefa, branch e PR:** A tarefa envolcie preparar o ambiente, criação do .ven, e instalação de pactotes.
- **Decisão adotada e justificativa:** O padrão de nomenclatura de branches passa a ser `<tipo>/m<marco>-<tarefa>-<descricao-em-ingles>`, como `chore/mX-Y-install-editable-dev-environment`, substituindo X pelo marco e Y pelo número local da tarefa. O nome não inclui colchetes nem parênteses, simplificando o uso no zsh. A convenção anterior funcionava com o nome entre aspas.
- **Verificação independente e resultado:** O ambiente foi preparado com sucesso e as alterações foram feitas conforme o codex instruiu.

## 8. Registro — atualização da convenção de branches

- **Pedido:** aplicar à documentação a decisão de nomenclatura registrada na seção 7.
- **Contribuição:** atualização das regras e exemplos em `docs/fluxo_desenvolvimento.md` e `AGENTS.md`, preservando o registro histórico da convenção anterior.
- **Verificação:** revisão do diff, conferência dos nomes de exemplo com `git check-ref-format --branch` e busca de referências à convenção anterior.
- **Estado:** convenção documental atualizada; nenhuma branch foi criada ou renomeada nesta alteração.

## 9. Registro — identificação local das tarefas

- **Pedido:** esclarecer que as issues são descrições de tarefas, sem uso de issues reais do GitHub.
- **Decisão adotada:** usar os códigos locais do roadmap, como `M0-1` e `M0-2`, em branches, commits, PRs e evidências. A numeração reinicia em cada marco.
- **Contribuição:** alinhamento do fluxo, roadmap, orientações para IA e modelos de registro; preservação das decisões anteriores como histórico.
- **Verificação:** revisão do diff e busca de exigências antigas de numeração remota. Alteração apenas documental, sem criação de branches ou itens remotos.

## 10. Registro — M0-2: versões e instruções de reprodução

- **Marco e tarefa:** M0-2.
- **Branch:** `chore/m0-2-document-verified-environment`.
- **Pedido:** documentar as versões coletadas, sem realizar validação em outro ambiente virtual.
- **Decisão adotada:** manter `requirements-dev.txt` como registro das versões e documentar no README a instalação usando restrições (`-c`). A reprodução em ambiente novo não foi verificada nesta tarefa, conforme escolha do desenvolvedor.
- **Contribuição da IA:** conferência do arquivo com o ambiente existente e atualização do README, das evidências de validação e do progresso no roadmap.
- **Verificação e resultado:** versões de Python, pip, sistema e dependências consultadas; arquivo de versões coincide com `pip freeze --exclude-editable`. Conferir versões é distinto de validar comportamentos da engine.
- **Aprendizado com palavras próprias:** a preencher pelo desenvolvedor.

## 11. Registro — M0-3: ciclo inicial da janela

- **Marco e tarefa:** M0-3.
- **Branch:** `feat/m0-3-create-pygame-window`.
- **Pedido:** continuar a implementação conforme o roadmap.
- **Contribuição:** explicação do ciclo abrir → consultar eventos → encerrar; implementação pequena em `engine.py` e chamada por `__main__.py`, com documentação dos limites.
- **Decisão adotada:** inicializar apenas o display, usar `finally` para liberar recursos e limitar a frequência do loop; configuração e medição de tempo continuam nas tarefas seguintes.
- **Verificação:** script pontual com eventos reais na fila do Pygame usando display dummy, incluindo falha simulada na abertura; conferência visual posteriormente confirmada pelo desenvolvedor. Pytest ainda sem testes coletados.
- **Aprendizado com palavras próprias:** a preencher pelo desenvolvedor após a explicação do código e a conferência da janela.

- **Conclusão de M0-3:** após a explicação do código, o desenvolvedor confirmou a validação visual e solicitou o encerramento da tarefa. A IA atualizou o status e os registros, sem alterar a implementação.

## 12. Registro — branches com várias tarefas do mesmo marco

- **Pedido:** documentar o padrão para realizar M0-4 e M0-5 em uma entrega conjunta.
- **Decisão adotada:** listar os números locais das tarefas em ordem crescente na branch, como `feat/m0-4-5-add-frame-timing-and-window-config`; a lista não representa um intervalo. Commits e PRs usam referências explícitas, como `[M0-4, M0-5]`, conforme as tarefas abrangidas.
- **Contribuição:** inclusão das regras e exemplos no fluxo de desenvolvimento e alinhamento de `AGENTS.md`.
- **Verificação:** revisão documental, `git diff --check` e conferência dos nomes de exemplo com `git check-ref-format --branch`.
- **Estado:** convenção documentada; nenhuma branch criada e nenhuma implementação de M0-4 ou M0-5 realizada nesta alteração.

## 13. Registro — M0-4 e M0-5: tempo, desenho e configuração

- **Tarefas e branch:** M0-4 e M0-5; `feat/m0-4-5-add-frame-timing-and-window-config`.
- **Pedido:** implementar as duas tarefas em uma entrega coesa.
- **Contribuição:** explicação de milissegundos e segundos, implementação de `WindowConfig`, preenchimento e apresentação da superfície e exibição do intervalo no título.
- **Decisão adotada:** configuração pequena e imutável em módulo sem dependência gráfica; sem API de simulação, movimento ou abstrações de renderização nesta etapa.
- **Verificação:** script pontual com duas configurações, amostras de pixels da superfície real, relógio controlado de 20 ms, eventos de saída e entradas inválidas; conferência visual posteriormente confirmada pelo desenvolvedor. Pytest ainda não coleta testes.
- **Aprendizado com palavras próprias:** a preencher pelo desenvolvedor após revisar e executar a entrega.

- **Explicação complementar:** funcionamento de `WindowConfig`, anotações, `__init__` gerado pela dataclass, `__post_init__`, atributos de classe e instância e comparação com uma classe comum.
- **Conclusão:** o desenvolvedor confirmou a validação visual. A IA atualizou os registros para concluir M0-4, M0-5 e M0 no ambiente atual, mantendo explícitas as limitações e a integração por PR como etapa separada. Nenhuma alteração de código foi necessária para este registro.


## 14. Registro — M1-1: mundo e consulta de células

- **Tarefa e branch:** M1-1; `feat/m1-1-add-world-cell-queries`.
- **Pedido:** iniciar M1 apenas pela representação do mundo e consultas, com explicação anterior à implementação, verificações, conferência do desenvolvedor e documentação ao final.
- **Contribuição da IA:** leitura das especificações e registros; atualização das referências remotas para partir de M0 concluído e da tag `M0`; explicação de linhas, colunas, índices e imutabilidade; implementação de `World` e 20 casos de teste; execução das verificações e preparação de procedimento manual; atualização documental após a aprovação.
- **Decisões implementadas:** copiar a grade para tuplas e impedir sua substituição; validar estrutura e células; exigir índices inteiros; distinguir consulta direta fora da grade de consulta de solidez externa. Contrato e limites registrados na [arquitetura](arquitetura.md#11-mundo-implementado-em-m1-1), sem acrescentar dependências ou antecipar as tarefas seguintes.
- **Verificação automatizada pela IA:** 20 casos aprovados no pytest; Ruff, formatação e `git diff --check` aprovados após ajustar uma linha longa. Exemplos independentes e resultados na [validação](validacao.md#10-m1-1--representação-do-mundo-e-consulta-de-células).
- **Conferência do desenvolvedor:** aprovou explicitamente o código, confirmou o procedimento manual sugerido e relatou execução dos testes no pytest.
- **Estado:** M1-1 concluída; M1 continua em andamento; integração por PR é separada.
- **Aprendizado com palavras próprias:** ainda não registrado pelo desenvolvedor; aprovação e execução de testes não substituem esse relato.


## 15. Registro — M1-2: sala temporária em memória

- **Tarefa e branch:** M1-2; `feat/m1-2-add-temporary-study-room`.
- **Pedido:** implementar apenas M1-2, com explicação prévia, validação por partes e commit próprio; atualizar a documentação após aprovação.
- **Contribuição da IA:** explicação da contagem de paredes e células livres, criação de `create_study_world()` e três testes da geometria, execução das verificações, procedimento manual e atualização documental após a aprovação.
- **Decisão implementada:** cenário explícito em módulo separado de `World`, sem dependência gráfica ou leitura de arquivo; nenhuma implementação de M1-3.
- **Verificação:** 23 casos aprovados no pytest; Ruff, formatação e `git diff --check` aprovados. Evidências e limites na [validação de M1-2](validacao.md#11-m1-2--sala-temporária-em-memória).
- **Aprovação:** o desenvolvedor aprovou a entrega e autorizou a atualização documental; não relatou resultados manuais específicos nesta tarefa.
- **Estado:** M1-2 concluída; integração por PR separada. Commit previsto: `feat: [M1-2] adiciona sala temporária em memória`.
- **Aprendizado com palavras próprias:** ainda não registrado pelo desenvolvedor.


## 16. Registro — M1-3 e M1-4: percurso de raios

- **Branch:** `feat/m1-3-4-5-add-grid-raycasting`.
- **Contribuição:** planejamento em duas etapas, explicação de fronteiras e parâmetro, implementação de DDA e impacto imutável, 32 novos casos de teste e procedimento de conferência no interpretador.
- **Decisões:** direção sem normalização, saída retorna `None`, origem livre e coordenadas finitas obrigatórias; prioridade de x em empate escolhida pelo desenvolvedor para consolidação em M1-5.
- **Validação:** 55 casos totais aprovados; Ruff, formatação e diff sem erros. O desenvolvedor aprovou explicitamente a etapa e autorizou continuar, sem relatar resultados manuais específicos.
- **Estado:** M1-3/M1-4 concluídas; M1-5 será revisada separadamente; M1 continua em andamento. Aprendizado com palavras próprias ainda não registrado.


## 17. Registro — M1-5: cantos e limite de avanços

- **Branch:** `feat/m1-3-4-5-add-grid-raycasting`; segunda etapa da entrega conjunta.
- **Contribuição:** explicação do desempate em cantos e sua assimetria, justificativa do orçamento de largura + altura, implementação do limite e 39 novos casos de teste. Atualização documental após aprovação.
- **Decisão implementada:** manter a prioridade de x escolhida pelo desenvolvedor, sem tolerância de empate; não consultar a outra lateral apenas tocada. Esgotamento do orçamento causa `RuntimeError`.
- **Verificação:** 94 casos totais aprovados; Ruff, formatação e diff aprovados após ajuste de uma linha de teste. Resultados e limitações na [validação](validacao.md#13-m1-5--cantos-e-limite-de-avanços).
- **Aprovação:** o desenvolvedor respondeu “Aprovado!” após receber exemplos e procedimento manual; não relatou resultados específicos da execução manual.
- **Estado:** M1-5 concluída; M1-6 e encerramento de M1 pendentes. Aprendizado com palavras próprias ainda não registrado. Commit desta etapa: `feat: [M1-5] consolida desempate e limite do percurso`.

## 18. Registro — M1-6: revisão dos testes explicados

- **Branch:** `test/m1-6-review-raycasting-cases`.
- **Contribuição:** revisão dos critérios de M1 e cobertura existente; explicação prévia de impactos oblíquos em sala retangular e percurso longo; dez casos adicionais, sem alteração no algoritmo; tabela passo a passo e contas independentes na seção 14 da validação.
- **Automação:** 104 casos aprovados; Ruff, formatação e diff aprovados.
- **Validação do desenvolvedor:** confirmou “Está validado, pode prosseguir” após receber testes, explicação e procedimento de conferência.
- **Estado:** M1-6 e M1 concluídos no ambiente atual, após revisão dos critérios de aceitação. Integração por PR e eventual tag permanecem separadas.
- **Aprendizado com palavras próprias:** pendente; sugerido explicar por que dobrar a direção reduz t à metade sem mudar o ponto de impacto.


## 19. Registro — M2-1: geometria da câmera

- **Branch:** `feat/m2-1-2-3-add-camera-column-rays`; primeira etapa da entrega conjunta.
- **Contribuição:** explicação de vetores, perpendicularidade e campo de visão; implementação de `Camera` imutável e 24 testes; explicação complementar de `@property`, propriedades derivadas e ligação futura com DDA e projeção.
- **Decisões:** orientação por ângulo em radianos escolhida pelo desenvolvedor; campo de visão horizontal padrão de 60 graus; origem separada da câmera; nenhuma dependência nova.
- **Verificação:** 128 casos totais aprovados, Ruff, formatação e diff aprovados; evidências na seção 15 da validação.
- **Aprovação:** após a explicação, o desenvolvedor confirmou entendimento e autorizou os próximos passos. Não houve relato detalhado de resultados manuais; aprofundamento conceitual foi deixado para depois pelo desenvolvedor.
- **Estado:** M2-1 concluída; M2-2/M2-3 seguem na mesma branch. Aprendizado com palavras próprias ainda não registrado.


## 20. Registro — M2-2 e M2-3: raios por coluna

- **Branch:** `feat/m2-1-2-3-add-camera-column-rays`; segunda etapa da entrega conjunta.
- **Contribuição:** explicação de centros de colunas e profundidade frontal; implementação de `Camera.ray_direction()` sem normalização; 22 novos testes, incluindo integração com DDA; procedimento de conferência e documentação após validação.
- **Decisões implementadas:** largura interna fornecida por chamada, sem resolução fixa ou mudança na janela; validação de coluna e largura; origem e execução do DDA permanecem separadas da câmera.
- **Verificação:** 150 casos totais aprovados; Ruff, formatação e diff aprovados. Exemplos e limites na seção 16 da validação.
- **Validação:** o desenvolvedor confirmou “Considere validado, pode prosseguir”, sem relatar saídas manuais detalhadas. Aprendizado com palavras próprias ainda não registrado.
- **Estado:** M2-1/M2-2/M2-3 concluídas; M2 permanece em andamento. Integração por PR é separada.
