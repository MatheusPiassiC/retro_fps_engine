# Formato de mapa — versão inicial proposta

## 1. Estado

Esta é a especificação proposta para o carregador a implementar em M4. Os exemplos já seguem estas regras, mas ainda não há carregador funcional.

## 2. Sintaxe

Arquivo UTF-8, com a seguinte ordem:

```text
MAP
11111111
10000001
10110001
10000001
11111111
PLAYER 1.5 1.5 0
```

- A primeira linha contém exatamente `MAP`.
- Em seguida vêm as linhas da grade, compostas exclusivamente por `0` e `1`, sem espaços: `0` é livre e `1` é parede.
- A última linha de conteúdo é `PLAYER x y angulo`, com exatamente quatro campos separados por espaços.
- `x` e `y` são números reais finitos com ponto decimal; `angulo` é um número real finito em graus.
- Uma quebra de linha ao final é permitida. Linhas vazias internas, comentários, cabeçalhos adicionais e conteúdo após `PLAYER` não são aceitos nesta versão.
- Quebras de linha LF e CRLF são aceitas.

## 3. Coordenadas e medidas

A origem `(0, 0)` fica no canto superior esquerdo da grade. O eixo `x` cresce para a direita; o eixo `y`, para baixo. A consulta à grade usa `grade[linha][coluna]`, isto é, `grade[y][x]` para índices inteiros.

Cada célula mede uma unidade de lado. A célula de coluna 1 e linha 1 ocupa o intervalo entre 1 e 2 nos dois eixos; seu centro é `(1.5, 1.5)`. A célula que contém uma posição é obtida pelo piso matemático de suas coordenadas.

O ângulo zero aponta para leste, 90 graus para sul, 180 para oeste e 270 para norte. O sentido positivo é horário devido ao eixo `y` crescente para baixo. O arquivo usa graus por legibilidade; os cálculos internos usam radianos. Ângulos finitos fora de uma volta são normalizados.

A altura das paredes é uma unidade. A câmera inicial fica a meia altura; piso, teto e altura da câmera não variam no escopo básico.

## 4. Validação

O carregador deverá rejeitar:

- Arquivo ausente, ilegível ou com codificação inválida, informando o motivo.
- Ausência de `MAP`, de grade ou de uma única linha `PLAYER`.
- Grade menor que 3 × 3, não retangular ou com caracteres desconhecidos.
- Qualquer abertura na borda externa da grade.
- Números inválidos ou não finitos, como infinito e NaN.
- Jogador fora do cenário, dentro de parede ou sem espaço para seu volume completo.

O jogador será um círculo de raio inicial 0.2 unidade. A validação verifica a distância do centro às células sólidas próximas: o círculo não pode tocar nem sobrepor paredes no início. O mesmo raio usado na configuração de movimento deve ser usado na validação do spawn.

As mensagens deverão indicar caminho do arquivo e linha quando houver erro de sintaxe localizável. O carregador não deve criar um cenário parcialmente válido nem corrigir silenciosamente a grade.

Não será exigido que toda área livre seja alcançável. A demonstração deverá ter seu percurso verificado manualmente. Consultas fora da grade são tratadas como sólidas pela colisão; o raycasting também deve encerrar com segurança ao alcançar um limite.

## 5. Evolução

Chaves, saídas e regras de jogo não pertencem a esta sintaxe inicial. Um exemplo de jogo poderá manter sua própria configuração de objetivos separada do mapa geométrico.

Se novos materiais ou objetos genéricos forem necessários, o formato será revisado explicitamente, com exemplos e testes. O significado de arquivos existentes não deverá mudar silenciosamente.
