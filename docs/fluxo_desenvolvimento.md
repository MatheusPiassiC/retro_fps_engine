# Fluxo de desenvolvimento — GitHub Flow

## 1. Organização do trabalho

O projeto seguirá GitHub Flow: uma branch principal integrável e branches curtas para mudanças específicas, incorporadas por pull request (PR). A branch principal será chamada `main` nesta documentação; se o repositório usar outro nome, aplicar o fluxo à sua branch padrão.

Cada trabalho será identificado pelo marco e pelo número da tarefa na lista do roadmap. As “issues” citadas no planejamento são descrições locais de trabalho; não há exigência de criar issues ou milestones no GitHub.

Por exemplo, **M0-1** é a primeira tarefa do Marco 0 (instalar o pacote), **M0-2** é a segunda (registrar versões) e **M0-3** é a terceira (criar a janela). A numeração das tarefas reinicia em cada marco. Esses identificadores não correspondem a números de issues do GitHub e devem ser mantidos estáveis ao revisar o planejamento.

## 2. Ciclo de uma tarefa

1. Escolher uma tarefa do marco atual e identificar seu código local, como `M0-2`.
2. Descrever o objetivo, as dependências, os limites e os critérios de aceitação na documentação da tarefa ou no PR, usando o roadmap como referência.
3. Partir da branch principal atualizada e criar uma branch para a feature. Correções e documentação também usam branches próprias.
4. Implementar em alterações pequenas, acrescentando testes e documentação conforme a necessidade. Referenciar marco e tarefa nas atualizações de progresso.
5. Abrir um PR para a branch principal, referenciando o código local da tarefa e explicando comportamento, validação e limitações. Um PR em rascunho pode apoiar a revisão enquanto o trabalho está incompleto.
6. Revisar o diff e conferir os critérios da tarefa. Mesmo em trabalho individual, registrar a revisão e compreender os algoritmos antes da integração.
7. Integrar o PR quando estiver pronto, registrar a conclusão da tarefa e remover a branch da feature após a integração.
8. Atualizar as evidências do marco. Concluir todas as tarefas previstas não substitui verificar os critérios globais de conclusão do marco.

O foco de cada branch é uma feature ou mudança coesa, preferencialmente associada a uma tarefa principal. Um marco inteiro não deve se tornar uma única branch longa. Caso uma feature cresça demais, dividi-la em tarefas e entregas menores.

Este projeto local não exige uma implantação em produção a cada PR. A branch principal deve preservar o estado de funcionamento alcançado até então, sem exigir recursos de marcos futuros.

## 3. Convenções de identificação

Os exemplos abaixo usam a tarefa local M0-3 do roadmap.

| Item | Convenção | Exemplo |
|---|---|---|
| Marco do roadmap | `M<n> — <resultado do marco>` | `M0 — Ambiente e ciclo da aplicação` |
| Tarefa local | `M<marco>-<tarefa>: <ação e resultado>` | `M0-3: Criar janela Pygame responsiva` |
| Branch | `<tipo>/m<marco>-<tarefa>-<descricao-em-ingles>` | `feat/m0-3-create-pygame-window` |
| Commit | `<tipo>: [M<marco>-<tarefa>] <alteração>` | `feat: [M0-3] cria janela e trata encerramento` |
| Título do PR | `[M<marco>-<tarefa>] <resultado>` | `[M0-3] Criar janela Pygame responsiva` |
| Comunicação e registros | `M<marco>-<tarefa>: <descrição>` | `M0-3: criar janela Pygame` |

Tipos iniciais: `feat` para funcionalidade, `fix` para correção, `docs` para documentação, `test` para testes, `refactor` para reorganização sem mudança intencional de comportamento e `chore` para manutenção do ambiente. Esses nomes são uma convenção do projeto, não uma exigência do GitHub Flow.

O identificador `m0-3` significa Marco 0, tarefa 3. Nos nomes de branch, usar `m` minúsculo e um hífen entre o número da tarefa e a descrição, sem parênteses ou colchetes. As demais referências a marcos continuam usando `M0`, `M1` e assim por diante.

Para nomes de branch:

- Escrever a descrição em inglês, em letras minúsculas, com palavras separadas por hífens: `create-pygame-window`.
- Trocar espaços por hífens; não usar sublinhados ou acentos na descrição.
- Usar uma ação e um objeto específicos. Evitar nomes genéricos como `fix/bug`, `feat/novas-coisas` ou `branch-joao`.
- Preservar o prefixo do tipo e a referência de marco e tarefa. Por exemplo, `feat/m0-3-create-pygame-window` informa a entrega e sua rastreabilidade.

Exemplos de aplicação da convenção:

| Preferir | Evitar | Motivo |
|---|---|---|
| `feat/m0-3-create-pygame-window` | `feat/m0-3-create_pygame_window` | Separar palavras com hífens, sem sublinhados |
| `feat/m0-3-create-pygame-window` | `feat/m0-3-create pygame window` | Não usar espaços |
| `fix/m0-3-handle-window-close` | `fix/m0-3-bug` | Descrever o comportamento corrigido |
| `docs/m0-3-explain-window-controls` | `branch-joao` | Identificar tipo, marco, tarefa e finalidade |

Exemplo de criação de branch com a convenção atual:

```sh
git switch -c 'feat/m0-3-create-pygame-window'
```

Use o código da tarefa correspondente no roadmap. Os textos das descrições e dos PRs permanecem em português. Um commit deve representar uma alteração compreensível; não é obrigatório ter apenas um commit por tarefa.

## 4. Conteúdo mínimo da descrição da tarefa

```markdown
## Referência
M0-3 — Criar janela Pygame responsiva

## Objetivo
Abrir uma janela Pygame responsiva e permitir encerramento normal.

## Aprendizado
Entender inicialização, eventos, quadros e liberação de recursos.

## Escopo
Criar janela e processar eventos de encerramento. Sem renderizar mapas.

## Dependências
Indicar as tarefas necessárias ou informar que não há dependências.

## Critérios de aceitação
- A janela abre no ambiente documentado.
- Escape e o botão de fechar encerram a aplicação normalmente.
- O encerramento libera os recursos inicializados.

## Validação
Registrar os comandos e a conferência manual executados, com resultados.
```

Esta descrição pode ficar no PR ou em um registro local pertinente; não é necessário cadastrá-la como issue no GitHub.

## 5. Conteúdo mínimo do PR

Descrever o problema e o comportamento resultante, indicar marco e tarefa, resumir a validação realizada e registrar limitações relevantes. Informar verificações não executadas sem apresentá-las como aprovadas.

Referenciar a tarefa com seu código, por exemplo `M0-3`, e explicar se a entrega é completa ou parcial. Não usar `Closes #3` ou `Refs #3` para identificadores locais, pois essa sintaxe aponta para itens reais do GitHub.

Concluir uma tarefa não conclui automaticamente o marco.

## 6. Assistência por IA

Ao iniciar uma tarefa de implementação, identificar seu código local e a branch. Não solicitar criação ou número de issue no GitHub como pré-requisito. Os registros de aprendizado e validação também devem incluir o código da tarefa e branch ou PR quando disponíveis.

Documentar o fluxo não cria branches ou PRs. Caso issues do GitHub sejam adotadas futuramente, registrar a associação com as tarefas locais explicitamente, sem presumir que seus números coincidam.

## 7. Referências

- [GitHub Flow — documentação oficial](https://docs.github.com/en/get-started/using-github/github-flow).
