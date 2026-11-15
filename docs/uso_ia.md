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
