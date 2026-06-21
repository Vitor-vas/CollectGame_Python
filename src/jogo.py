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
    CAMINHO_BACKGROUND_SALA2,
    BRANCO,
    PRETO,
    CINZA,
    VERMELHO,
    ESTADO_MENU,
    ESTADO_JOGANDO,
    ESTADO_FIM,
    CAMINHO_SOM_DANO,
    CAMINHO_SOM_MOEDA,
    CAMINHO_SOM_MORTE,
    SALA_1,
    SALA_2,
    PONTOS_PARA_PORTA,
)

from src.funcoes import (
    calcular_pontos,
    jogador_perdeu,
    limitar_valor,
    verificar_colisao,
    tomar_dano,
    iniciar_jogo,
    verificar_fim_de_jogo,
    reiniciar_jogo,
    pode_usar_porta,
    trocar_sala,
    porta_disponivel,
)
from src.sprites import pegar_sprite
from src.dados import (
    salvar_recorde,
    carregar_recorde,
)


def criar_jogador(player_image):
    return {"imagem": player_image, "rect": player_image.get_rect(topleft=(100, 100))}


def criar_tesouro(chest_image):
    return {"imagem": chest_image, "rect": chest_image.get_rect(topleft=(200, 500))}


def desenhar_tela_inicio(tela, fonte_titulo, fonte_texto):
    tela.fill(PRETO)
    titulo = fonte_titulo.render(TITULO_JOGO, True, BRANCO)
    instrucao = fonte_texto.render("Pressione ESPACO para iniciar", True, CINZA)
    tela.blit(titulo, titulo.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 40)))
    tela.blit(instrucao, instrucao.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 30)))


def desenhar_tela_fim(tela, fonte_titulo, fonte_texto, pontos, recorde):
    tela.fill(PRETO)
    titulo = fonte_titulo.render("You Died", True, VERMELHO)
    placar = fonte_texto.render(f"Pontos: {pontos}   Recorde: {recorde}", True, CINZA)
    instrucao = fonte_texto.render("Pressione R para reiniciar ou ESC para sair", True, CINZA)
    tela.blit(titulo, titulo.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 60)))
    tela.blit(placar, placar.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2)))
    tela.blit(instrucao, instrucao.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 50)))

def executar_jogo():
    pygame.init()
    

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)

    background_sala1 = pygame.image.load(CAMINHO_BACKGROUND).convert()
    background_sala1 = pygame.transform.scale(background_sala1, (LARGURA_TELA, ALTURA_TELA))

    background_sala2 = pygame.image.load(CAMINHO_BACKGROUND_SALA2).convert()
    background_sala2 = pygame.transform.scale(background_sala2, (LARGURA_TELA, ALTURA_TELA))

    som_dano = pygame.mixer.Sound(CAMINHO_SOM_DANO)
    som_moeda = pygame.mixer.Sound(CAMINHO_SOM_MOEDA)
    som_morte = pygame.mixer.Sound(CAMINHO_SOM_MORTE)

    fonte_titulo = pygame.font.Font(None, 64)
    fonte_texto = pygame.font.Font(None, 28)

    relogio = pygame.time.Clock()
    rodando = True
    estado = ESTADO_MENU
    sala_atual = SALA_1

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
    gem_image_sala1 = pegar_sprite(
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
    bat_image_sala1 = pegar_sprite(
        CAMINHO_SPRITES, 
        x=0, 
        y=616, 
        width=123, 
        height=118, 
        scale=0.5
    )

    gem_image_sala2 = pegar_sprite(
        CAMINHO_SPRITES, 
        x=9, 
        y=430, 
        width=90, 
        height=109, 
        scale=0.5
    )
    
    bat_image_sala2 = pegar_sprite(
        CAMINHO_SPRITES, 
        x=535,
        y=734,
        width=123,
        height=118,
        scale=0.5
    )
    
    jogador = criar_jogador(player_image)
    tesouro = criar_tesouro(chest_image)
    gemas = []
    inimigos = []
    porta = {"rect": pygame.Rect(LARGURA_TELA // 2 - 40, ALTURA_TELA - 50, 80, 50)}

    velocidade = 5
    pontos = 0
    vidas = 3
    recorde = carregar_recorde(CAMINHO_RECORDE)

    # Loop principal: processa entrada, atualiza estado e renderiza a cena.
    while rodando:
        relogio.tick(FPS)

        espaco_pressionado = False
        r_pressionado = False

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    espaco_pressionado = True
                if evento.key == pygame.K_r:
                    r_pressionado = True
                if evento.key == pygame.K_ESCAPE and estado == ESTADO_FIM:
                    rodando = False

        estado = iniciar_jogo(estado, espaco_pressionado)

        novo_estado = reiniciar_jogo(estado, r_pressionado)
        if novo_estado != estado and novo_estado == ESTADO_MENU:
            jogador = criar_jogador(player_image)
            tesouro = criar_tesouro(chest_image)
            gemas = []
            inimigos = []
            pontos = 0
            vidas = 3
            sala_atual = SALA_1
        estado = novo_estado

        if estado == ESTADO_MENU:
            desenhar_tela_inicio(tela, fonte_titulo, fonte_texto)

        elif estado == ESTADO_JOGANDO:
            teclas = pygame.key.get_pressed()

            if sala_atual == SALA_1:
                fundo_atual = background_sala1
                imagem_gema_atual = gem_image_sala1
                imagem_inimigo_atual = bat_image_sala1
            else:
                fundo_atual = background_sala2
                imagem_gema_atual = gem_image_sala2
                imagem_inimigo_atual = bat_image_sala2

            if teclas[pygame.K_LEFT]:
                jogador["rect"].x -= velocidade
            if teclas[pygame.K_RIGHT]:
                jogador["rect"].x += velocidade
            if teclas[pygame.K_UP]:
                jogador["rect"].y -= velocidade
            if teclas[pygame.K_DOWN]:
                jogador["rect"].y += velocidade

            jogador["rect"].x = limitar_valor(jogador["rect"].x, 0, LARGURA_TELA - jogador["rect"].width)
            jogador["rect"].y = limitar_valor(jogador["rect"].y, 0, ALTURA_TELA - jogador["rect"].height)

            if verificar_colisao(jogador["rect"], tesouro["rect"]):
                tesouroChance = random.randint(0, 10)

                if teclas[pygame.K_e]:
                    if tesouroChance > 5:
                        novo_inimigo = {
                            "imagem": imagem_inimigo_atual,
                            "rect": imagem_inimigo_atual.get_rect(topleft=(
                                random.randint(0, LARGURA_TELA - 100),
                                random.randint(0, ALTURA_TELA - 100)
                            ))
                        }
                        inimigos.append(novo_inimigo)
                    else:
                        nova_gema = {
                            "imagem": imagem_gema_atual,
                            "rect": imagem_gema_atual.get_rect(topleft=(
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
                    som_dano.play()
                    inimigo["rect"].x += 80
                    inimigo["rect"].y += 50

            for gema in gemas[:]:
                if verificar_colisao(jogador["rect"], gema["rect"]):
                    pontos = calcular_pontos(pontos, 10)
                    som_moeda.play()
                    gemas.remove(gema)

            # Interação com a porta
            colidindo_porta = porta_disponivel(sala_atual, SALA_1) and verificar_colisao(jogador["rect"], porta["rect"])
            if colidindo_porta and teclas[pygame.K_e] and pode_usar_porta(pontos, PONTOS_PARA_PORTA):
                sala_atual = trocar_sala(sala_atual)
                gemas = []
                inimigos = []
                jogador["rect"].topleft = (LARGURA_TELA // 2, ALTURA_TELA // 2)

            estado_anterior = estado
            estado = verificar_fim_de_jogo(estado, vidas)
            if estado != estado_anterior and estado == ESTADO_FIM:
                som_morte.play()

            if pontos > recorde:
                recorde = pontos
                salvar_recorde(CAMINHO_RECORDE, recorde)

            pygame.display.set_caption(
                f"{TITULO_JOGO} | Sala: {sala_atual} | Pontos: {pontos} | Recorde: {recorde} | Vidas: {vidas}"
            )

            tela.blit(fundo_atual, (0, 0))
            tela.blit(jogador["imagem"], jogador["rect"])
            tela.blit(tesouro["imagem"], tesouro["rect"])
            for inimigo in inimigos:
                tela.blit(inimigo["imagem"], inimigo["rect"])
            for gema in gemas:
                tela.blit(gema["imagem"], gema["rect"])

            if colidindo_porta:
                if pode_usar_porta(pontos, PONTOS_PARA_PORTA):
                    dica = fonte_texto.render("Pressione E para entrar", True, BRANCO)
                else:
                    dica = fonte_texto.render(
                        f"Pontos insuficientes ({pontos}/{PONTOS_PARA_PORTA})", True, BRANCO
                    )
                tela.blit(dica, dica.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA - 70)))

        elif estado == ESTADO_FIM:
            desenhar_tela_fim(tela, fonte_titulo, fonte_texto, pontos, recorde)

        pygame.display.flip()

    pygame.quit()