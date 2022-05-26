from random import randint

from jogador import cria_jogadores
from jogo import Jogo, obtem_estatisticas_jogos
from propriedade import cria_propriedades


QUANTIDADE_JOGOS = 300
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


def executar_jogos() -> dict:
    jogos = []
    for i in range(QUANTIDADE_JOGOS):
        novo_jogo = jogar()
        jogos.append(novo_jogo)
    return obtem_estatisticas_jogos(jogos)


if __name__ == '__main__':
    estatisticas = executar_jogos()
    print(
        'Quantidade jogos com 1000 rodadas (Timeout): {quantidade_jogos_timeout}\n'
        'Média de rodadas por jogo: {media_rodada_por_jogos}\n'
        'Percentual de vitórias por tipo de jogador: {percentual_vitorias_por_tipo_jogador}\n'
        'Tipo de jogador mais vitorioso: {tipo_jogador_mais_vitorioso}'
        .format(**estatisticas)
    )
