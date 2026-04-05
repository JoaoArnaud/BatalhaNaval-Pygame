import pygame
from configuracao import LARGURA_TELA, ALTURA_TELA, BRANCO
from tabuleiro import criar_tabuleiro, desenhar_tabuleiro

def main():
    pygame.init()

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Batalha Naval")

    tabuleiro = criar_tabuleiro()

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        tela.fill(BRANCO)

        desenhar_tabuleiro(tela, tabuleiro)

        pygame.display.flip()

    pygame.quit()

main()