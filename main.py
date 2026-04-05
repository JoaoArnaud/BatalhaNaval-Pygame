import pygame
from config import (
    LARGURA_TELA, ALTURA_TELA, BRANCO, PRETO, AMARELO,
    TOTAL_NAVIOS, TAMANHO_NAVIO
)
from tabuleiro import (
    criar_tabuleiro,
    desenhar_tabuleiro,
    obter_celula_mouse,
    pode_posicionar_navio,
    posicionar_navio,
    contar_navios,
    atacar_celula,
    todos_navios_destruidos,
    contar_navios_destruidos
)

def desenhar_texto(tela, texto, tamanho, x, y, cor=PRETO):
    fonte = pygame.font.SysFont(None, tamanho)
    superficie = fonte.render(texto, True, cor)
    tela.blit(superficie, (x, y))


def main():
    pygame.init()

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Batalha Naval")

    tabuleiro_jogador1 = criar_tabuleiro()
    tabuleiro_jogador2 = criar_tabuleiro()

    jogador_atual = 1
    fase = "posicionamento"

    # Tela intermediaria => esconde o tabuleiro do outro jogador na troca de turno.
    mostrar_transicao = False
    tempo_transicao = 0
    proximo_jogador = 1

    mensagem = ""

    vencedor = None

    relogio = pygame.time.Clock()
    rodando = True

    while rodando:
        relogio.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if not mostrar_transicao and fase == "posicionamento":
                    celula = obter_celula_mouse(evento.pos)

                    if celula is not None:
                        linha, coluna = celula

                        if jogador_atual == 1:
                            tabuleiro_atual = tabuleiro_jogador1
                        else:
                            tabuleiro_atual = tabuleiro_jogador2

                        if pode_posicionar_navio(tabuleiro_atual, linha, coluna, TAMANHO_NAVIO):
                            posicionar_navio(tabuleiro_atual, linha, coluna, TAMANHO_NAVIO)

                            quantidade = contar_navios(tabuleiro_atual)

                            if quantidade == TOTAL_NAVIOS:
                                if jogador_atual == 1:
                                    mostrar_transicao = True
                                    tempo_transicao = pygame.time.get_ticks()
                                    proximo_jogador = 2
                                    mensagem = "Passe a vez para o Jogador 2"
                                else:
                                    fase = "combate"
                                    jogador_atual = 1
                                    mostrar_transicao = True
                                    tempo_transicao = pygame.time.get_ticks()
                                    proximo_jogador = 1
                                    mensagem = "Fim do posicionamento. Jogador 1 começa atacando."

                elif not mostrar_transicao and fase == "combate":
                    celula = obter_celula_mouse(evento.pos)

                    if celula is not None:
                        linha, coluna = celula

                        if jogador_atual == 1:
                            tabuleiro_inimigo = tabuleiro_jogador2
                        else:
                            tabuleiro_inimigo = tabuleiro_jogador1

                        # A funcao já altera o tabuleiro e informa se houve acerto, água ou ataque repetido.
                        resultado = atacar_celula(tabuleiro_inimigo, linha, coluna)

                        if resultado == "repetido":
                            mensagem = "Essa casa ja foi atacada. Escolha outra."
                        elif resultado == "acerto":
                            mensagem = f"Jogador {jogador_atual} acertou um navio e joga novamente!"

                            if todos_navios_destruidos(tabuleiro_inimigo):
                                vencedor = jogador_atual
                                fase = "fim"
                        elif resultado == "agua":
                            mensagem = f"Jogador {jogador_atual} acertou a agua."

                            if jogador_atual == 1:
                                proximo_jogador = 2
                            else:
                                proximo_jogador = 1

                            mostrar_transicao = True
                            tempo_transicao = pygame.time.get_ticks()
                            mensagem = f"Jogador {jogador_atual} acertou a agua. Passe a vez para o Jogador {proximo_jogador}."

        # O jogador so muda de fato depois de 3 segundos mostrando a mensagem de transicao.
        if mostrar_transicao and pygame.time.get_ticks() - tempo_transicao > 3000:
            mostrar_transicao = False
            jogador_atual = proximo_jogador

        tela.fill(BRANCO)

        if mostrar_transicao:
            desenhar_texto(tela, mensagem, 40, 90, 300)
            desenhar_texto(tela, "Aguarde 3 segundos...", 32, 300, 360)

        elif fase == "posicionamento":
            if jogador_atual == 1:
                tabuleiro_atual = tabuleiro_jogador1
            else:
                tabuleiro_atual = tabuleiro_jogador2

            desenhar_texto(tela, f"Posicionamento - Jogador {jogador_atual}", 42, 220, 25)
            desenhar_texto(tela, "Clique para posicionar um navio horizontal de 3 casas", 30, 120, 75)

            quantidade_navios = contar_navios(tabuleiro_atual)
            desenhar_texto(tela, f"Navios colocados: {quantidade_navios}/{TOTAL_NAVIOS}", 32, 285, 640)

            desenhar_tabuleiro(tela, tabuleiro_atual, mostrar_navios=True)

        elif fase == "combate":
            if jogador_atual == 1:
                tabuleiro_inimigo = tabuleiro_jogador2
            else:
                tabuleiro_inimigo = tabuleiro_jogador1

            desenhar_texto(tela, f"Combate - Jogador {jogador_atual}", 42, 260, 20)
            desenhar_texto(tela, "Clique no tabuleiro do adversario para atacar", 30, 165, 70)

            desenhar_tabuleiro(tela, tabuleiro_inimigo, mostrar_navios=False)

            destruidos = contar_navios_destruidos(tabuleiro_inimigo)
            desenhar_texto(tela, f"Navios destruidos do adversario: {destruidos}/{TOTAL_NAVIOS}", 30, 220, 640)

            if mensagem != "":
                desenhar_texto(tela, mensagem, 28, 120, 600, AMARELO)

        elif fase == "fim":
            desenhar_texto(tela, f"Jogador {vencedor} venceu!", 60, 250, 250)
            desenhar_texto(tela, "Feche a janela para encerrar o jogo.", 35, 210, 330)

            if vencedor == 1:
                desenhar_tabuleiro(tela, tabuleiro_jogador2, mostrar_navios=True)
            else:
                desenhar_tabuleiro(tela, tabuleiro_jogador1, mostrar_navios=True)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
