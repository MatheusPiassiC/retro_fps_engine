# Fluxo de desenvolvimento — GitHub Flow

## 1. Organização do trabalho

O projeto seguirá GitHub Flow: uma branch principal integrável e branches curtas para mudanças específicas, incorporadas por pull request (PR). A branch principal será chamada `main` nesta documentação; se o repositório usar outro nome, aplicar o fluxo à sua branch padrão.

Cada trabalho será identificado pelo marco do roadmap e por uma issue do GitHub. O roadmap descreve os resultados maiores; as issues dividem cada marco em tarefas pequenas e verificáveis.

Exemplo de referência: **Marco 0 (M0), issue #3: criar janela Pygame**. Esse número é ilustrativo; não indica uma issue já criada.

Os números de issues são atribuídos pelo GitHub no repositório e não reiniciam a cada marco. Um marco pode conter várias issues. O número do marco corresponde ao identificador do roadmap: M0 é Marco 0, M1 é Marco 1, e assim por diante.

## 2. Ciclo de uma tarefa

1. Escolher uma tarefa do marco atual e criar ou localizar a issue correspondente.
2. Registrar na issue o objetivo, as dependências, os limites e os critérios de aceitação. Associá-la ao milestone do GitHub correspondente ao marco, quando configurado.
3. Partir da branch principal atualizada e criar uma branch para a feature. Correções e documentação também usam branches próprias.
4. Implementar em alterações pequenas, acrescentando testes e documentação conforme a necessidade. Referenciar marco e issue nas atualizações de progresso.
5. Abrir um PR para a branch principal, vinculando a issue e explicando comportamento, validação e limitações. Um PR em rascunho pode apoiar a revisão enquanto o trabalho está incompleto.
6. Revisar o diff e conferir os critérios da issue. Mesmo em trabalho individual, registrar a revisão e compreender os algoritmos antes da integração.
7. Integrar o PR quando estiver pronto, encerrar a issue resolvida e remover a branch da feature após a integração.
8. Atualizar as evidências do marco. Concluir todas as issues previstas não substitui verificar os critérios globais de conclusão do marco.

O foco de cada branch é uma feature ou mudança coesa, preferencialmente vinculada a uma issue principal. Um marco inteiro não deve se tornar uma única branch longa. Caso uma feature cresça demais, dividi-la em issues e entregas menores.

Este projeto local não exige uma implantação em produção a cada PR. A branch principal deve preservar o estado de funcionamento alcançado até então, sem exigir recursos de marcos futuros.

## 3. Convenções de identificação

Os exemplos abaixo usam a issue fictícia #3.

| Item | Convenção | Exemplo |
|---|---|---|
| Milestone no GitHub | `M<n> — <resultado do marco>` | `M0 — Ambiente e ciclo da aplicação` |
| Título da issue | `[M<n>] <ação e resultado>` | `[M0] Criar janela Pygame responsiva` |
| Branch | `<tipo>/(M<marco>-<issue>)<descricao-em-ingles>` | `feat/(M0-3)create-pygame-window` |
| Commit | `<tipo>: [M<n> #<numero>] <alteração>` | `feat: [M0 #3] cria janela e trata encerramento` |
| Título do PR | `[M<n> #<numero>] <resultado>` | `[M0 #3] Criar janela Pygame responsiva` |
| Comunicação e registros | `Marco <n> (M<n>), issue #<numero>: <tarefa>` | `Marco 0 (M0), issue #3: criar janela Pygame` |

Tipos iniciais: `feat` para funcionalidade, `fix` para correção, `docs` para documentação, `test` para testes, `refactor` para reorganização sem mudança intencional de comportamento e `chore` para manutenção do ambiente. Esses nomes são uma convenção do projeto, não uma exigência do GitHub Flow.

O identificador `(M0-3)` significa Marco 0, issue #3. Manter o `M` maiúsculo e não inserir separador entre o fechamento do parêntese e a descrição.

Para nomes de branch:

- Escrever a descrição em inglês, em letras minúsculas, com palavras separadas por hífens: `create-pygame-window`.
- Trocar espaços por hífens; não usar sublinhados ou acentos na descrição.
- Usar uma ação e um objeto específicos. Evitar nomes genéricos como `fix/bug`, `feat/novas-coisas` ou `branch-joao`.
- Preservar o prefixo do tipo e a referência de marco e issue. Por exemplo, `feat/(M0-3)create-pygame-window` informa a entrega e sua rastreabilidade.

Exemplos de aplicação da convenção (números ilustrativos):

| Preferir | Evitar | Motivo |
|---|---|---|
| `feat/(M0-3)create-pygame-window` | `feat/(M0-3)create_pygame_window` | Separar palavras com hífens, sem sublinhados |
| `feat/(M0-3)create-pygame-window` | `feat/(M0-3)create pygame window` | Não usar espaços |
| `fix/(M0-4)handle-window-close` | `fix/(M0-4)bug` | Descrever o comportamento corrigido |
| `docs/(M0-5)explain-window-controls` | `branch-joao` | Identificar tipo, marco, issue e finalidade |

Ao passar um nome de branch com parênteses ao shell, colocá-lo entre aspas:

```sh
git switch -c 'feat/(M0-3)create-pygame-window'
```

O comando é ilustrativo e só deve ser usado com o número real da issue correspondente. Os textos de issues e PRs permanecem em português. Um commit deve representar uma alteração compreensível; não é obrigatório ter apenas um commit por issue.

## 4. Conteúdo mínimo da issue

```markdown
## Referência
Marco 0 (M0) — Ambiente e ciclo da aplicação

## Objetivo
Abrir uma janela Pygame responsiva e permitir encerramento normal.

## Aprendizado
Entender inicialização, eventos, quadros e liberação de recursos.

## Escopo
Criar janela e processar eventos de encerramento. Sem renderizar mapas.

## Dependências
Indicar as issues necessárias ou informar que não há dependências.

## Critérios de aceitação
- A janela abre no ambiente documentado.
- Escape e o botão de fechar encerram a aplicação normalmente.
- O encerramento libera os recursos inicializados.

## Validação
Registrar os comandos e a conferência manual executados, com resultados.
```

Criar a issue antes de usar seu número nas referências definitivas. Não inventar identificadores nem assumir que uma lista local determina a numeração do GitHub.

## 5. Conteúdo mínimo do PR

Descrever o problema e o comportamento resultante, indicar marco e issue, resumir a validação realizada e registrar limitações relevantes. Informar verificações não executadas sem apresentá-las como aprovadas.

Usar `Closes #3` na descrição quando o PR resolver integralmente a issue #3. Ao integrar na branch padrão, o GitHub pode encerrar a issue automaticamente. Para uma contribuição parcial, usar `Refs #3`, manter a issue aberta e explicar o que falta.

Um PR pode mencionar outras issues relacionadas; só deve encerrar aquelas cujos critérios tenham sido atendidos. O marco não é concluído automaticamente pelo encerramento de uma única issue.

## 6. Assistência por IA

Ao iniciar uma tarefa de implementação, identificar marco, issue e branch. Se o número ainda não existir, preparar o escopo para cadastro sem atribuir um número fictício. Os registros de aprendizado e validação também devem incluir essas referências quando disponíveis.

Documentar o fluxo não cria branches, milestones, issues ou PRs no GitHub. Esses itens serão preparados quando o trabalho correspondente for iniciado.

## 7. Referências

- [GitHub Flow — documentação oficial](https://docs.github.com/en/get-started/using-github/github-flow).
- [Vincular pull request a issue e encerramento automático](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue).
