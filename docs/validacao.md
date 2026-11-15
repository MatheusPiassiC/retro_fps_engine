# Estratégia de validação e aprendizado

## 1. Estado e princípio

Este documento propõe verificações futuras; ainda não há testes da engine implementados nem resultados de desempenho medidos. Cada teste deve dizer qual comportamento protege e por que o resultado esperado faz sentido.

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

O parâmetro de um raio não é sempre seu comprimento euclidiano: depende do tamanho de seu vetor de direção. Os testes deverão explicitar essa convenção. Um caso diagonal que atinge exatamente um canto deverá seguir a política de desempate definida em M1.

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

A pasta `tests/` está reservada. Enquanto não houver testes, o pytest poderá terminar com o código de ausência de testes; isso não deve ser registrado como validação da engine. Os primeiros testes comportamentais serão criados junto com M1.
