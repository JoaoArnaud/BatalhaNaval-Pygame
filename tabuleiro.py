# tabuleiro.py

import pygame
from configuracao import LINHAS, COLUNAS, TAMANHO_CELULA, PRETO, AZUL

def criar_tabuleiro():
    tabuleiro = []

    for linha in range(LINHAS):
        nova_linha = []
        for coluna in range(COLUNAS):
            nova_linha.append(0)
        tabuleiro.append(nova_linha)

    return tabuleiro


def desenhar_tabuleiro(tela, tabuleiro):
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            x = 100 + coluna * TAMANHO_CELULA
            y = 100 + linha * TAMANHO_CELULA

            retangulo = pygame.Rect(x, y, TAMANHO_CELULA, TAMANHO_CELULA)

            pygame.draw.rect(tela, AZUL, retangulo)
            pygame.draw.rect(tela, PRETO, retangulo, 1)