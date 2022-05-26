from unittest import TestCase, mock

from jogador import Jogador
from jogo import (
    Jogo,
    _obtem_comportamento_mais_vitorias,
    _obtem_media_rodadas,
    _obtem_percentual_vitoria_comportamentos,
    _obtem_quantidade_jogos_timeout
)
from propriedade import Propriedade


class TestJogo(TestCase):

    def setUp(self):
        self.jogo = Jogo(tabuleiro=[], jogadores=[])

    def test_define_vencedor_jogo(self):
        self.jogo.jogadores = [
            Jogador(identificador='1', tipo='', saldo=170),
            Jogador(identificador='2', tipo='', saldo=170),
            Jogador(identificador='3', tipo='', saldo=150),
        ]
        self.jogo.define_vencedor()
        self.assertEqual(self.jogo.vencedor, Jogador(identificador='1', tipo='', saldo=170))

    def test_atualiza_posicao_jogador_sem_finalizar_tabuleiro(self):
        jogador = Jogador(identificador='1', tipo='', saldo=50, posicao_atual=5)
        posicoes = 5
        self.jogo.atualiza_posicao_jogador(jogador, posicoes)
        self.assertEqual(jogador.posicao_atual, 10)

    def test_atualiza_posicao_jogador_finaliza_tabuleiro(self):
        jogador = Jogador(identificador='1', tipo='', saldo=50, posicao_atual=17)
        posicoes = 5
        self.jogo.atualiza_posicao_jogador(jogador, posicoes)
        self.assertEqual(jogador.posicao_atual, 2)
        self.assertEqual(jogador.saldo, 150)

    def test_jogo_falha_comprar_propriedade_jogador_saldo_isuficiente(self):
        jogador = Jogador(identificador='1', tipo='', saldo=15, posicao_atual=5)
        propriedade = Propriedade(identificador='1', aluguel=60, valor=100)
        self.jogo.acao(propriedade, jogador)
        self.assertEqual(propriedade.proprietario, None)
        self.assertEqual(jogador.saldo, 15)
        
    def test_jogo_comprar_propriedade_jogador_exigente(self):
        jogador = Jogador(identificador='1', tipo='exigente', saldo=150, posicao_atual=5)
        propriedade = Propriedade(identificador='1', aluguel=60, valor=100)
        self.jogo.acao(propriedade, jogador)
        self.assertEqual(propriedade.proprietario, jogador)
        self.assertEqual(jogador.saldo, 50)

    def test_jogo_nao_comprar_propriedade_jogador_exigente(self):
        jogador = Jogador(identificador='1', tipo='exigente', saldo=150, posicao_atual=5)
        propriedade = Propriedade(identificador='1', aluguel=40, valor=100)
        self.jogo.acao(propriedade, jogador)
        self.assertEqual(propriedade.proprietario, None)
        self.assertEqual(jogador.saldo, 150)

    def test_jogo_comprar_propriedade_jogador_cauteloso(self):
        jogador = Jogador(identificador='1', tipo='cauteloso', saldo=150, posicao_atual=5)
        propriedade = Propriedade(identificador='1', aluguel=40, valor=70)
        self.jogo.acao(propriedade, jogador)
        self.assertEqual(propriedade.proprietario, jogador)
        self.assertEqual(jogador.saldo, 80)

    def test_jogo_nao_comprar_propriedade_jogador_cauteloso(self):
        jogador = Jogador(identificador='1', tipo='cauteloso', saldo=150, posicao_atual=5)
        propriedade = Propriedade(identificador='1', aluguel=40, valor=71)
        self.jogo.acao(propriedade, jogador)
        self.assertEqual(propriedade.proprietario, None)
        self.assertEqual(jogador.saldo, 150)

    def test_jogo_comprar_propriedade_jogador_aleatorio(self):
        jogador = Jogador(identificador='1', tipo='aleatorio', saldo=150, posicao_atual=5)
        propriedade = Propriedade(identificador='1', aluguel=40, valor=120)
        with mock.patch("jogador.randint", return_value=1):
            self.jogo.acao(propriedade, jogador)
            self.assertEqual(propriedade.proprietario, jogador)
            self.assertEqual(jogador.saldo, 30)

    def test_jogo_nao_comprar_propriedade_jogador_aleatorio(self):
        jogador = Jogador(identificador='1', tipo='aleatorio', saldo=150, posicao_atual=5)
        propriedade = Propriedade(identificador='1', aluguel=40, valor=120)
        with mock.patch("jogador.randint", return_value=2):
            self.jogo.acao(propriedade, jogador)
            self.assertEqual(propriedade.proprietario, None)
            self.assertEqual(jogador.saldo, 150)

    def test_jogo_falha_comprar_propriedade_jogador_aleatorio_sem_saldo(self):
        jogador = Jogador(identificador='1', tipo='aleatorio', saldo=50, posicao_atual=5)
        propriedade = Propriedade(identificador='1', aluguel=40, valor=120)
        with mock.patch("jogador.randint", return_value=1):
            self.jogo.acao(propriedade, jogador)
            self.assertEqual(propriedade.proprietario, None)
            self.assertEqual(jogador.saldo, 50)

    def test_jogo_pagar_aluguel_propriedade(self):
        jogador_recebe = Jogador(identificador='1', tipo='aleatorio', saldo=50, posicao_atual=5)
        jogador_paga = Jogador(identificador='2', tipo='cauteloso', saldo=100, posicao_atual=5)
        propriedade = Propriedade(identificador='1', valor=150, aluguel=15, proprietario=jogador_recebe)
        self.jogo.acao(propriedade, jogador_paga)
        self.assertEqual(jogador_paga.saldo, 85)
        self.assertEqual(jogador_recebe.saldo, 65)
        self.assertEqual(propriedade.proprietario, jogador_recebe)

    def test_remove_jogador_jogo_corretamente(self):
        jogador1 = Jogador(identificador='1', tipo='aleatorio', saldo=-1, posicao_atual=5)
        jogador2 = Jogador(identificador='2', tipo='cauteloso', saldo=100, posicao_atual=5)
        jogador3 = Jogador(identificador='3', tipo='exigente', saldo=100, posicao_atual=5)
        self.jogo.jogadores = [jogador1, jogador2, jogador3]
        self.jogo.tabuleiro = [
            Propriedade(identificador='1', aluguel=15, valor=100, proprietario=jogador1),
            Propriedade(identificador='2', aluguel=25, valor=150, proprietario=jogador1),
            Propriedade(identificador='3', aluguel=25, valor=150, proprietario=jogador2),
            Propriedade(identificador='4', aluguel=50, valor=250, proprietario=jogador3),
        ]
        self.jogo.remove_jogador(jogador1, posicao=0)
        proprietarios = [propriedade.proprietario for propriedade in self.jogo.tabuleiro if propriedade != None]
        self.assertNotIn(jogador1, proprietarios)


class TestJogoEstatisticas(TestCase):

    def setUp(self):
        pass

    def test_percentual_vitorias_por_comportamento(self):
        jogos = [
            Jogo(
                vencedor=Jogador(identificador='1', tipo='cauteloso'),
                rodadas=5,
                jogadores=[],
                tabuleiro=[],
            ),
            Jogo(
                vencedor=Jogador(identificador='2', tipo='exigente'),
                rodadas=5,
                jogadores=[],
                tabuleiro=[],
            ),
            Jogo(
                vencedor=Jogador(identificador='3', tipo='aleatorio'),
                rodadas=5,
                jogadores=[],
                tabuleiro=[],
            ),
        ]
        resultado = _obtem_percentual_vitoria_comportamentos(jogos)
        self.assertEqual(resultado['aleatorio'], 33.33)
        self.assertEqual(resultado['exigente'], 33.33)
        self.assertEqual(resultado['cauteloso'], 33.33)
        self.assertEqual(resultado['impulsivo'], 0.00)

    def test_obtem_media_rodadas_por_jogo(self):
        jogos = [
            Jogo(
                rodadas=100,
                jogadores=[],
                tabuleiro=[],
            ),
            Jogo(
                rodadas=1000,
                jogadores=[],
                tabuleiro=[],
            ),
            Jogo(
                rodadas=12,
                jogadores=[],
                tabuleiro=[],
            ),
        ]
        resultado = _obtem_media_rodadas(jogos)
        self.assertEqual(resultado, 370.67)

    def test_obtem_quantidade_jogos_timeout(self):
        jogos = [
            Jogo(
                rodadas=100,
                jogadores=[],
                tabuleiro=[],
            ),
            Jogo(
                rodadas=1000,
                jogadores=[],
                tabuleiro=[],
            ),
            Jogo(
                rodadas=12,
                jogadores=[],
                tabuleiro=[],
            ),
            Jogo(
                rodadas=12,
                jogadores=[],
                tabuleiro=[],
            ),
            Jogo(
                rodadas=1000,
                jogadores=[],
                tabuleiro=[],
            ),
        ]
        resultado = _obtem_quantidade_jogos_timeout(jogos)
        self.assertEqual(resultado, 2)

    def test_obtem_comportamento_mais_vencedor(self):
        jogos = [
            Jogo(
                vencedor=Jogador(identificador='1', tipo='cauteloso'),
                rodadas=5,
                jogadores=[],
                tabuleiro=[],
            ),
            Jogo(
                vencedor=Jogador(identificador='2', tipo='exigente'),
                rodadas=5,
                jogadores=[],
                tabuleiro=[],
            ),
            Jogo(
                vencedor=Jogador(identificador='3', tipo='aleatorio'),
                rodadas=5,
                jogadores=[],
                tabuleiro=[],
            ),
            Jogo(
                vencedor=Jogador(identificador='3', tipo='aleatorio'),
                rodadas=5,
                jogadores=[],
                tabuleiro=[],
            ),
        ]
        resultado = _obtem_comportamento_mais_vitorias(jogos)
        self.assertEqual(resultado, 'aleatorio')
