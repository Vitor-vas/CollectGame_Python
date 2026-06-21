def calcular_pontos(pontos_atual, pontos_ganhos):
    return pontos_atual + pontos_ganhos


def tomar_dano(vida_atual, dano):
    return vida_atual - dano


def jogador_perdeu(vidas):
    return vidas <= 0


def limitar_valor(valor, minimo, maximo):
    if valor < minimo:
        return minimo
    if valor > maximo:
        return maximo
    return valor


def verificar_colisao(retangulo_1, retangulo_2):
    return retangulo_1.colliderect(retangulo_2)

def iniciar_jogo(estado_atual, espaco_pressionado):
    if estado_atual == "menu" and espaco_pressionado:
        return "jogando"
    return estado_atual


def verificar_fim_de_jogo(estado_atual, vidas):
    if estado_atual == "jogando" and jogador_perdeu(vidas):
        return "fim"
    return estado_atual


def reiniciar_jogo(estado_atual, r_pressionado):
    if estado_atual == "fim" and r_pressionado:
        return "menu"
    return estado_atual

def pode_usar_porta(pontos, pontos_necessarios):
    return pontos >= pontos_necessarios


def trocar_sala(sala_atual):
    if sala_atual == 1:
        return 2
    return 1

def porta_disponivel(sala_atual, sala_da_porta):
    return sala_atual == sala_da_porta