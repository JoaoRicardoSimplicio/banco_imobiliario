from random import randint

from jogador import Jogador, cria_jogadores
from jogo import Jogo
from propriedade import cria_propriedades


MAX_RODADAS = 1000


def _jogar_dado() -> int:
    return randint(1, 6)


def jogar() -> Jogo:
    jogo = Jogo(
        tabuleiro=cria_propriedades(),
        jogadores=cria_jogadores(),
        rodadas=0
    )
    while jogo.rodadas < MAX_RODADAS and len(jogo.jogadores) > 1:
        print("Rodada Atual ", jogo.rodadas)
        qtd_jogadores = len(jogo.jogadores)
        index_jogador = 0
        while index_jogador < qtd_jogadores:
            jogador = jogo.jogadores[index_jogador]
            posicoes = _jogar_dado()
            jogo.atualiza_posicao_jogador(jogador, posicoes)
            propriedade = jogo.tabuleiro[jogador.posicao_atual]
            jogo.acao(propriedade, jogador)
            if not jogador.eh_valido():
                jogo.remove_jogador(jogador, index_jogador)
                qtd_jogadores -= 1
                index_jogador -= 1
            index_jogador += 1
        jogo.rodadas += 1
    jogo.define_vencedor()
    return jogo


if __name__ == '__main__':
    jogar()
