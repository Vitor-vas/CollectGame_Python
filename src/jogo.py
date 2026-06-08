import pygame
import random

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    CAMINHO_RECORDE,
    CAMINHO_SPRITES,
    CAMINHO_BACKGROUND,
)

from src.funcoes import (
    calcular_pontos,
    jogador_perdeu,
    limitar_valor,
    verificar_colisao,
    tomar_dano,
)
from src.sprites import pegar_sprite
from src.dados import (
    salvar_recorde,
    carregar_recorde,
)


def executar_jogo():
    """Executa o loop principal do jogo e controla estado, colisões e pontuação."""
    pygame.init()
    

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)

    background = pygame.image.load(CAMINHO_BACKGROUND).convert()
    background = pygame.transform.scale(background, (LARGURA_TELA, ALTURA_TELA))

    relogio = pygame.time.Clock()
    rodando = True

    # 1. Carregando as imagens recortadas do Spritesheet


    # Jogador: usando tamanho 110x110 para capturar o quadrado perfeitamente
    # Personagem Knight - primeiro sprite de frente
    player_image = pegar_sprite(
        CAMINHO_SPRITES,
        x=4,
        y=83,
        width=115,
        height=136,
        scale=0.5
    )

# Gema pequena - primeira gema azul
    gem_image = pegar_sprite(
        CAMINHO_SPRITES,
        x=9,
        y=430,
        width=90,
        height=109,
        scale=0.5
    )

# Baú de tesouro - caso queira usar no lugar da gema
    chest_image = pegar_sprite(
        CAMINHO_SPRITES,
        x=1034,
        y=430,
        width=96,
        height=109,
        scale=0.5
    )

# Morcego - primeiro morcego marrom
    bat_image = pegar_sprite(
        CAMINHO_SPRITES,
        x=0,
        y=616,
        width=123,
        height=118,
        scale=0.5
    )
    
    # 2. Criando a estrutura de Sprites usando Dicionários
    jogador = {
        "imagem": player_image,
        "rect": player_image.get_rect(topleft=(100, 100))
    }

    gemas = []
    
    inimigos = []
    
    tesouro = {
        "imagem": chest_image,
        "rect": chest_image.get_rect(topleft=(200, 500))
    }


    velocidade = 5
    pontos = 0
    vidas = 3
    recorde = carregar_recorde(CAMINHO_RECORDE)

    # Loop principal: processa entrada, atualiza estado e renderiza a cena.
    while rodando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        teclas = pygame.key.get_pressed()

        # Movimentação alterando direto os eixos X e Y do retângulo do jogador
        if teclas[pygame.K_LEFT]:
            jogador["rect"].x -= velocidade
        if teclas[pygame.K_RIGHT]:
            jogador["rect"].x += velocidade
        if teclas[pygame.K_UP]:
            jogador["rect"].y -= velocidade
        if teclas[pygame.K_DOWN]:
            jogador["rect"].y += velocidade

        # Limitando o jogador dentro das bordas da tela usando as propriedades do Rect
        jogador["rect"].x = limitar_valor(jogador["rect"].x, 0, LARGURA_TELA - jogador["rect"].width)
        jogador["rect"].y = limitar_valor(jogador["rect"].y, 0, ALTURA_TELA - jogador["rect"].height)

        #VERIFICAR COLISAO TESOURO
        if verificar_colisao(jogador["rect"], tesouro["rect"]):
            tesouroChance = random.randint(0,10)
            
            if teclas[pygame.K_e]:
                if tesouroChance > 5:
                    novo_inimigo = {
                        "imagem": bat_image,
                        "rect": bat_image.get_rect(topleft=(
                            random.randint(0, LARGURA_TELA - 100),
                            random.randint(0, ALTURA_TELA - 100)
                        ))
                    }
                    inimigos.append(novo_inimigo)
                else:
                    nova_gema = {
                        "imagem": gem_image,
                        "rect": gem_image.get_rect(topleft=(
                            random.randint(0, LARGURA_TELA - 100),
                            random.randint(0, ALTURA_TELA - 100)
                        ))
                    }
                    gemas.append(nova_gema)
                    
                tesouro["rect"].x += 80
                tesouro["rect"].y += 50

                if tesouro["rect"].x > LARGURA_TELA - tesouro["rect"].width:
                    tesouro["rect"].x = 50
                if tesouro["rect"].y > ALTURA_TELA - tesouro["rect"].height:
                    tesouro["rect"].y = 50

        for inimigo in inimigos:
            if verificar_colisao(jogador["rect"], inimigo["rect"]):
                vidas = tomar_dano(vidas, 1)
                inimigo["rect"].x += 80
                inimigo["rect"].y += 50

        for gema in gemas[:]:
            if verificar_colisao(jogador["rect"], gema["rect"]):
                pontos = calcular_pontos(pontos, 10)
                gemas.remove(gema)

        # Regras de fim de jogo e recorde
        if jogador_perdeu(vidas):
            rodando = False

        if pontos > recorde:
            recorde = pontos
            salvar_recorde(CAMINHO_RECORDE, recorde)

        pygame.display.set_caption(
            f"{TITULO_JOGO} | Pontos: {pontos} | Recorde: {recorde} | Vidas: {vidas}"
        )

        tela.blit(background, (0, 0))

        # Desenhando os elementos na tela passando a imagem e o rect de cada dicionário
        tela.blit(jogador["imagem"], jogador["rect"])
        tela.blit(tesouro["imagem"], tesouro["rect"])
        for inimigo in inimigos:
            tela.blit(inimigo["imagem"], inimigo["rect"])
        for gema in gemas:
            tela.blit(gema["imagem"], gema["rect"])

        pygame.display.flip()

    pygame.quit()