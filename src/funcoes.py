def calcular_pontos(pontos_atual, pontos_ganhos):
    """Soma os pontos ganhos à pontuação atual."""
    return pontos_atual + pontos_ganhos


def tomar_dano(vida_atual, dano):
    """Reduz a vida atual com base no dano recebido."""
    return vida_atual - dano


def jogador_perdeu(vidas):
    """Indica se o jogador ficou sem vidas."""
    return vidas <= 0


def limitar_valor(valor, minimo, maximo):
    """Mantém um valor dentro do intervalo [minimo, maximo]."""
    if valor < minimo:
        return minimo
    if valor > maximo:
        return maximo
    return valor


def verificar_colisao(retangulo_1, retangulo_2):
    """Verifica sobreposição entre dois retângulos do Pygame."""
    return retangulo_1.colliderect(retangulo_2)

def iniciar_jogo(estado_atual, espaco_pressionado):
    """Transiciona do menu para o estado de jogo ao pressionar espaço."""
    if estado_atual == "menu" and espaco_pressionado:
        return "jogando"
    return estado_atual


def verificar_fim_de_jogo(estado_atual, vidas):
    """Transiciona para o estado de fim de jogo quando as vidas acabam."""
    if estado_atual == "jogando" and jogador_perdeu(vidas):
        return "fim"
    return estado_atual


def reiniciar_jogo(estado_atual, r_pressionado):
    """Retorna ao menu a partir da tela de fim quando R é pressionado."""
    if estado_atual == "fim" and r_pressionado:
        return "menu"
    return estado_atual