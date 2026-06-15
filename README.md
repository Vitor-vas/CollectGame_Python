# Nome do Jogo

Collect Game

Projeto final da disciplina de Introdução a Algoritmos/Programação, desenvolvido com Python e Pygame.




## Integrantes do grupo

- João Vitor Portes Rocha Soares
- Guilherme Luiz Santos Chebile
- Vitor Ladeia Sepulveda
- Vitor Augusto 
- Lucca Xavier

## Estrutura do projeto

- `main.py`: ponto de entrada da aplicação.
- `src/`: código-fonte principal do jogo (loop, regras, sprites e dados).
- `assets/`: imagens, fontes e sons.
- `data/`: arquivos persistentes (recorde/ranking).
- `tests/`: testes unitários com `pytest`.
- `docs/`: documentação do projeto, incluindo proposta inicial.

## Descrição do jogo

O Collect Game é um jogo single player que tem como objetivo sobreviver e fazer o máximo de pontos abrindo baús e coletando itens.

## Objetivo do jogador

O jogador precisa percorrer o mapa para que posssa abrir baús e coletar itens para que ele consiga fazer a maior pontuação possível.

## Regras do jogo

O jogador possui 3 vidas. Caso encoste em um inimigo ao longo do mapa o jogador perde uma vida. 
O jogador precisa abrir um baú apertando 'E' no teclado.
O jogo é finalizado ao ter todas as vidas esgotadas.
O jogador precisa fazer o máximo de pontos possíveis.
O jogador consegue 10 pontos ao coletar uma gema.


## Controles

- Seta para cima: mover para cima
- Seta para baixo: mover para baixo
- Seta para esquerda: mover para esquerda
- Seta para direita: mover para direita
- Tecla 'E': Para abrir o baú
- ESC: sair do jogo

## Como executar o projeto

python main.py

### 1. Clonar o repositório

```bash
git https://github.com/Vitor-vas/CollectGame_Python
cd COLLECTGAME_PYTHON
pip install -r requirements.txt
python main.py
```

## Como executar os testes

```bash
python -m pytest tests/test_logica.py -v
```


