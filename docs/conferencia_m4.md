# M4 — Roteiro de revisão e conferência manual

## 1. Estado e preparação

**Implementado e testado automaticamente; conferência manual pendente.** O desenvolvedor autorizou commits locais sem parar em cada etapa nesta sessão. Essa autorização não substitui aprovação do código ou conferência visual. M4 ainda não está concluído.

O trabalho foi dividido em duas branches locais, sem merge ou alteração no remoto:

- `feat/m4-1-2-3-4-add-map-loader`: análise, validação e leitura UTF-8.
- `feat/m4-5-6-load-maps-from-command-line`: seleção do arquivo e integração. Esta branch contém também os commits da primeira e é o ponto de revisão do conjunto.

A base é `1887add`, integração de M3-7 pelo PR #14. Para inspecionar os commits e as alterações, sem modificar nada:

```sh
git status --short --branch
git log --oneline 1887add..HEAD
git diff 1887add..HEAD -- src/retro_fps/map_loader.py
git diff 1887add..HEAD -- src/retro_fps/__main__.py
```

Na raiz do projeto, ative o ambiente existente e execute:

```sh
source .venv/bin/activate
python -m pytest
python -m ruff check .
python -m ruff format --check .
git diff --check
```

Foram aprovados 490 testes nesta entrega. Instalação em ambiente novo não foi realizada; não há dependências novas. Caso haja falhas após outras edições, registre a saída antes de concluir a validação.

## 2. Como os dados chegam à janela

```text
arquivo UTF-8 → load_map → parse_map → MapData(world, player) → run
```

`load_map` apenas lê; `parse_map` entende e valida o conteúdo. Os graus do arquivo viram radianos no jogador. A câmera continua sendo derivada do jogador a cada quadro. A especificação completa está em [formato_mapa.md](formato_mapa.md); não é necessário decorar as regras para conferir os exemplos.

O raio padrão é 0.2. No teste da sala, centro x=1.3 está a 0.3 da face da parede: raio 0.2 cabe e raio 0.3 toca. O carregador e o movimento recebem a mesma configuração para não discordarem sobre esse volume.

## 3. Duas cenas reais

```sh
python -m retro_fps --help
python -m retro_fps maps/room.map
python -m retro_fps maps/corridor.map
```

Feche cada janela antes de iniciar a seguinte. W/S avançam e recuam, A/D deslocam lateralmente e as setas giram. Escape ou botão de fechar encerram. O caminho agora é obrigatório: executar sem argumentos mostra o uso e termina sem janela, com código 2. Caminhos relativos partem do diretório atual; caminhos com espaços devem ficar entre aspas.

**Sala:** deve corresponder à sala de M3, com início no centro, olhando para leste. Avance até as paredes, deslize com diagonais, gire e recue. O círculo não deve entrar nas paredes.

**Corredor externo:** este arquivo mede 8 × 5 e contém obstáculos; não é o corredor vazio 9 × 5 de estudo. O início fica em (1.5,1.5), olhando para leste. Percorra a passagem superior até a direita, desça pela direita e explore o trecho inferior direito. Volte pela passagem superior, desça pela esquerda e explore o trecho inferior esquerdo. Tente aproximar-se obliquamente dos cantos, recue e confira a resposta dos controles e do encerramento. Não há objetivo ou condição de vitória.

Confirme se ambos carregam, se as geometrias diferem como descrito e se a navegação continua funcional. Esta conferência não é uma medição de desempenho.

## 4. Editar uma cópia e recarregar

Estes comandos criam um diretório temporário e mantêm os originais intactos. Execute no mesmo terminal para preservar a variável:

```sh
m4_check_dir=$(mktemp -d)
cp maps/room.map "$m4_check_dir/editavel.map"
python -m retro_fps "$m4_check_dir/editavel.map"
```

Feche a janela. Acrescente uma parede na célula (3,2), sem alterar o início:

```sh
python - "$m4_check_dir/editavel.map" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
lines = path.read_text(encoding="utf-8").splitlines()
lines[3] = "10011"
path.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY
python -m retro_fps "$m4_check_dir/editavel.map"
```

A parede frontal deve aparecer mais próxima: antes a face estava em x=4, a 1.5 do início x=2.5; agora está em x=3, a 0.5. A projeção pode ocupar toda a imagem por recorte. A mudança só aparece ao executar novamente; não existe recarga em tempo real.

## 5. Conferir erros sem janela

No mesmo terminal, prepare cópias inválidas:

```sh
python - "$m4_check_dir" <<'PY'
from pathlib import Path
import sys

target = Path(sys.argv[1])
original = Path("maps/room.map").read_text(encoding="utf-8")
cases = {
    "irregular.map": original.replace("10001", "1001", 1),
    "borda.map": original.replace("11111", "11011", 1),
    "parede.map": original.replace("PLAYER 2.5 2.5 0", "PLAYER 0.5 2.5 0"),
    "contato.map": original.replace("PLAYER 2.5 2.5 0", "PLAYER 1.2 2.5 0"),
    "nao_finito.map": original.replace("PLAYER 2.5 2.5 0", "PLAYER nan 2.5 0"),
}
for name, text in cases.items():
    (target / name).write_text(text, encoding="utf-8")
(target / "codificacao.map").write_bytes(b"MAP\n111\n1\xff1\n111\nPLAYER 1.5 1.5 0\n")
print(target)
PY
python -m retro_fps "$m4_check_dir/ausente.map"
python -m retro_fps "$m4_check_dir/irregular.map"
python -m retro_fps "$m4_check_dir/borda.map"
python -m retro_fps "$m4_check_dir/parede.map"
python -m retro_fps "$m4_check_dir/contato.map"
python -m retro_fps "$m4_check_dir/nao_finito.map"
python -m retro_fps "$m4_check_dir/codificacao.map"
```

Cada chamada deve terminar com erro e **sem janela**, contendo o caminho e um motivo em português, sem traceback de mapa. As linhas esperadas são: irregular 3, borda 2, parede/contato/número 7 e codificação 3. Arquivo ausente informa caminho e razão de leitura, sem inventar linha. Os casos inválidos retornam código 2; `echo $?` imediatamente após uma chamada permite conferir.

## 6. O que confirmar depois

Informe se os dois mapas abriram e foram navegáveis, se a edição da cópia apareceu na nova execução e se os erros corresponderam ao esperado. Se algo divergir, envie comando, mensagem e observação. Revisão do código, relato de aprendizagem e conferência manual serão registrados com suas palavras ou sua confirmação, sem presumir aprovação.

Integração das branches e eventual push/PR seguem dependendo de autorização. M5 não foi iniciado.
