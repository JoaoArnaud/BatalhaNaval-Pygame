import pygame
from config import (
    LINHAS, COLUNAS, TAMANHO_CELULA,
    X_TABULEIRO, Y_TABULEIRO,
    PRETO, AZUL, AZUL_ESCURO, VERDE, VERMELHO
)

def criar_tabuleiro():
    tabuleiro = []

    for linha in range(LINHAS):
        nova_linha = []
        for coluna in range(COLUNAS):
            nova_linha.append(0)
        tabuleiro.append(nova_linha)

    return tabuleiro


def desenhar_tabuleiro(tela, tabuleiro, mostrar_navios=True):
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            x = X_TABULEIRO + coluna * TAMANHO_CELULA
            y = Y_TABULEIRO + linha * TAMANHO_CELULA

            retangulo = pygame.Rect(x, y, TAMANHO_CELULA, TAMANHO_CELULA)

            valor = tabuleiro[linha][coluna]

            cor = AZUL

            if valor == 1 and mostrar_navios:
                cor = VERDE
            elif valor == 2:
                cor = AZUL_ESCURO
            elif valor == 3:
                cor = VERMELHO

            pygame.draw.rect(tela, cor, retangulo)
            pygame.draw.rect(tela, PRETO, retangulo, 1)


def obter_celula_mouse(posicao_mouse):
    x_mouse, y_mouse = posicao_mouse

    if x_mouse < X_TABULEIRO or y_mouse < Y_TABULEIRO:
        return None

    coluna = (x_mouse - X_TABULEIRO) // TAMANHO_CELULA
    linha = (y_mouse - Y_TABULEIRO) // TAMANHO_CELULA

    if 0 <= linha < LINHAS and 0 <= coluna < COLUNAS:
        return linha, coluna

    return None


def pode_posicionar_navio(tabuleiro, linha, coluna, tamanho_navio):
    if coluna + tamanho_navio > COLUNAS:
        return False

    for i in range(tamanho_navio):
        if tabuleiro[linha][coluna + i] != 0:
            return False

    return True


def posicionar_navio(tabuleiro, linha, coluna, tamanho_navio):
    for i in range(tamanho_navio):
        tabuleiro[linha][coluna + i] = 1


def contar_navios(tabuleiro):
    quantidade = 0

    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            if tabuleiro[linha][coluna] == 1:
                quantidade += 1

    return quantidade // 3


def encontrar_navio_completo(tabuleiro, linha, coluna):
    if tabuleiro[linha][coluna] != 1:
        return []

    inicio_coluna = coluna
    while inicio_coluna > 0 and tabuleiro[linha][inicio_coluna - 1] == 1:
        inicio_coluna -= 1

    partes_navio = []
    coluna_atual = inicio_coluna

    while coluna_atual < COLUNAS and tabuleiro[linha][coluna_atual] == 1:
        partes_navio.append((linha, coluna_atual))
        coluna_atual += 1

    return partes_navio


def atacar_celula(tabuleiro, linha, coluna):
    valor = tabuleiro[linha][coluna]

    if valor == 2 or valor == 3:
        return "repetido"

    if valor == 1:
        partes_navio = encontrar_navio_completo(tabuleiro, linha, coluna)

        for parte_linha, parte_coluna in partes_navio:
            tabuleiro[parte_linha][parte_coluna] = 3

        return "acerto"

    if valor == 0:
        tabuleiro[linha][coluna] = 2
        return "agua"


def contar_navios_destruidos(tabuleiro):
    quantidade = 0

    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            if tabuleiro[linha][coluna] == 3:
                quantidade += 1

    return quantidade // 3


def todos_navios_destruidos(tabuleiro):
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            if tabuleiro[linha][coluna] == 1:
                return False

    return True
