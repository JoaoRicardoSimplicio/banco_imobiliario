from collections import Counter

from dataclasses import dataclass

from jogador import Jogador
from propriedade import Propriedade


MAIOR_POSICAO = 19


def obtem_comportamento_mais_vitorias(jogos: list) -> str:
    tipo_vencedor = ''
    quantidade_vitorias_tipo = 0
    vitorias_por_tipo = Counter([jogo.vencedor.tipo for jogo in jogos])
    for key, value in vitorias_por_tipo.items():
        if value > quantidade_vitorias_tipo:
            quantidade_vitorias_tipo = value
            tipo_vencedor = key
    return tipo_vencedor


def obtem_percentual_vitoria_comportamentos(jogos: list) -> dict:
    quantidade_jogos = len(jogos)
    vitorias_por_tipo = Counter([jogo.vencedor.tipo for jogo in jogos])
    return {
        'impulsivo': round((vitorias_por_tipo['impulsivo'] / quantidade_jogos) * 100, 2),
        'exigente': round((vitorias_por_tipo['exigente'] / quantidade_jogos) * 100, 2),
        'cauteloso': round((vitorias_por_tipo['cauteloso'] / quantidade_jogos) * 100, 2),
        'aleatorio': round((vitorias_por_tipo['aleatorio'] / quantidade_jogos) * 100, 2)
    }


def obtem_media_rodadas(jogos: list) -> float:
    total_rodadas = sum([jogo.rodadas for jogo in jogos])
    return round((total_rodadas / len(jogos)), 2)


def obtem_quantidade_jogos_timeout(jogos: list) -> int:
    jogos_timeout = [jogo for jogo in jogos if jogo.rodadas == 1000]
    return len(jogos_timeout)


def obtem_estatisticas_jogos(jogos: list) -> dict:
    return {
        'quantidade_jogos_timeout': obtem_quantidade_jogos_timeout(jogos),
        'media_rodada_por_jogos': obtem_media_rodadas(jogos),
        'percentual_vitorias_por_tipo_jogador': obtem_percentual_vitoria_comportamentos(jogos),
        'tipo_jogador_mais_vitorioso': obtem_comportamento_mais_vitorias(jogos)
    }


@dataclass
class Jogo:

    tabuleiro: list
    jogadores: list
    rodadas: int = 0
    vencedor: Jogador = None

    def define_vencedor(self) -> None:
        self.jogadores.sort(reverse=True, key=self._obtem_saldo_jogador)
        self.vencedor = self.jogadores[0]

    def atualiza_posicao_jogador(self, jogador: Jogador, posicoes) -> None:
        if (jogador.posicao_atual + posicoes) > MAIOR_POSICAO:
            jogador.posicao_atual = ((jogador.posicao_atual + posicoes) - MAIOR_POSICAO) - 1
            jogador.saldo += 100
        else:
            jogador.posicao_atual += posicoes

    def acao(self, propriedade: Propriedade, jogador: Jogador) -> None:
        if propriedade.disponivel_para_venda():
            if jogador.deve_comprar_propriedade(propriedade):
                self._comprar_propriedade(propriedade, jogador)
        else:
            self._pagar_aluguel(propriedade, jogador)

    def remove_jogador(self, jogador: Jogador, posicao: int) -> None:
        for propriedade in self.tabuleiro:
            if propriedade.proprietario == jogador:
                propriedade.proprietario = None
        self.jogadores.pop(posicao)

    def _comprar_propriedade(self, propriedade: Propriedade, jogador: Jogador) -> None:
        propriedade.proprietario = jogador
        jogador.saldo -= propriedade.valor

    def _pagar_aluguel(self, propriedade: Propriedade, jogador: Jogador) -> None:
        if propriedade.proprietario is not jogador:
            propriedade.proprietario.saldo += propriedade.aluguel
            jogador.saldo -= propriedade.aluguel

    def _obtem_saldo_jogador(self, jogador: Jogador) -> int:
        return jogador.saldo
