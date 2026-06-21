from src.funcoes import calcular_pontos, jogador_perdeu, limitar_valor, tomar_dano, verificar_colisao, iniciar_jogo, verificar_fim_de_jogo, reiniciar_jogo, pode_usar_porta, trocar_sala, porta_disponivel
import pygame

#pontos
def test_calcular_pontos():
    assert calcular_pontos(10, 5) == 15

def test_calcular_pontos_do_zero():
    assert calcular_pontos(0, 10) == 10

def test_calcular_pontos_valor_grande():
    assert calcular_pontos(9990, 10) == 10000

#condicao de derrota
def test_jogador_perdeu_com_zero_vidas():
    assert jogador_perdeu(0) is True

def test_jogador_nao_perdeu_com_vidas():
    assert jogador_perdeu(3) is False

def test_jogador_perdeu_com_vidas_negativas():
    assert jogador_perdeu(-1) is True

#limites
def test_limitar_valor_abaixo_do_minimo():
    assert limitar_valor(-5, 0, 100) == 0

def test_limitar_valor_acima_do_maximo():
    assert limitar_valor(150, 0, 100) == 100

def test_limitar_valor_dentro_do_intervalo():
    assert limitar_valor(50, 0, 100) == 50

def test_limitar_valor_exatamente_no_minimo():
    assert limitar_valor(0, 0, 100) == 0

def test_limitar_valor_exatamente_no_maximo():
    assert limitar_valor(100, 0, 100) == 100

#tomar dano
def test_tomar_dano_reduz_vida():
    assert tomar_dano(3, 1) == 2

def test_tomar_dano_multiplo():
    assert tomar_dano(3, 2) == 1

def test_tomar_dano_chega_a_zero():
    assert tomar_dano(1, 1) == 0

#colisao
def test_verificar_colisao_colidindo():
    pygame.init()
    rect1 = pygame.Rect(0, 0, 50, 50)
    rect2 = pygame.Rect(25, 25, 50, 50)
    assert verificar_colisao(rect1, rect2) is True

def test_verificar_colisao_sem_colisao():
    pygame.init()
    rect1 = pygame.Rect(0, 0, 50, 50)
    rect2 = pygame.Rect(200, 200, 50, 50)
    assert verificar_colisao(rect1, rect2) is False

def test_verificar_colisao_adjacentes():
    pygame.init()
    rect1 = pygame.Rect(0, 0, 50, 50)
    rect2 = pygame.Rect(50, 0, 50, 50)
    assert verificar_colisao(rect1, rect2) is False


#menus
def test_iniciar_jogo_transiciona_do_menu():
    assert iniciar_jogo("menu", True) == "jogando"
    assert iniciar_jogo("menu", False) == "menu"
    assert iniciar_jogo("jogando", True) == "jogando"


def test_verificar_fim_de_jogo():
    assert verificar_fim_de_jogo("jogando", 0) == "fim"
    assert verificar_fim_de_jogo("jogando", 1) == "jogando"
    assert verificar_fim_de_jogo("menu", 0) == "menu"


def test_reiniciar_jogo():
    assert reiniciar_jogo("fim", True) == "menu"
    assert reiniciar_jogo("fim", False) == "fim"
    assert reiniciar_jogo("jogando", True) == "jogando"

#sala2
def test_pode_usar_porta():
    assert pode_usar_porta(100, 100) is True
    assert pode_usar_porta(150, 100) is True
    assert pode_usar_porta(99, 100) is False


def test_trocar_sala():
    assert trocar_sala(1) == 2
    assert trocar_sala(2) == 1

def test_porta_disponivel():
    assert porta_disponivel(1, 1) is True
    assert porta_disponivel(2, 1) is False