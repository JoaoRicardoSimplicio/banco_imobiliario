from unittest import TestCase

from jogador import Jogador, cria_jogadores
from propriedade import Propriedade


class TestJogador(TestCase):

    def setUp(self):
        self.jogador = Jogador(identificador='0', tipo='')
        self.propriedade = Propriedade(identificador=0, aluguel=100, valor=200)

    def test_jogador_eh_valido_com_saldo_positivo(self):
        self.assertTrue(self.jogador.eh_valido())
        
    def test_jogador_eh_valido_com_saldo_negativo(self):
        self.jogador.saldo = -100
        self.assertFalse(self.jogador.eh_valido())

    def test_jogodor_impulsivo_deve_comprar_propriedade(self):
        self.jogador.tipo = 'impulsivo'
        self.assertTrue(self.jogador.deve_comprar(self.propriedade))

    def test_jogador_exigente_deve_comprar_propriedade_aluguel_maior_50(self):
        self.jogador.tipo = 'exigente'
        self.propriedade.aluguel = 80
        self.assertTrue(self.jogador.deve_comprar(self.propriedade))

    def test_jogador_exigente_deve_comprar_propriedade_aluguel_menor_50(self):
        self.jogador.tipo = 'exigente'
        self.propriedade.aluguel = 30
        self.assertFalse(self.jogador.deve_comprar(self.propriedade))

    def test_jogador_exigente_deve_comprar_propriedade_aluguel_igual_50(self):
        self.jogador.tipo = 'exigente'
        self.propriedade.aluguel = 50
        self.assertFalse(self.jogador.deve_comprar(self.propriedade))

    def test_jogador_cauteloso_deve_comprar_propriedade_saldo_restante_maior_80(self):
        self.jogador.tipo = 'cauteloso'
        self.propriedade.valor = 100
        self.assertTrue(self.jogador.deve_comprar(self.propriedade))
        self.assertTrue((self.jogador.saldo - self.propriedade.valor) >= 80)

    def test_jogador_cauteloso_deve_comprar_propriedade_saldo_restante_menor_80(self):
        self.jogador.tipo = 'cauteloso'
        self.propriedade.valor = 250
        self.assertFalse(self.jogador.deve_comprar(self.propriedade))
        self.assertTrue((self.jogador.saldo - self.propriedade.valor) < 80)

    def test_jogador_cauteloso_deve_comprar_propriedade_saldo_restante_igual_80(self):
        self.jogador.tipo = 'cauteloso'
        self.propriedade.valor = 220
        self.assertTrue(self.jogador.deve_comprar(self.propriedade))
        self.assertEqual((self.jogador.saldo - self.propriedade.valor), 80)

    def test_jogador_falha_comprar_propriedade_com_saldo_insuficiente(self):
        self.propriedade.valor = 350
        self.jogador.comprar(self.propriedade)
        self.assertEqual(self.propriedade.proprietario, '')

    def test_jogador_compra_propriedade_com_saldo_suficiente_maior(self):
        self.jogador.comprar(self.propriedade)
        self.assertEqual(self.propriedade.proprietario, self.jogador.identificador)

    def test_jogador_compra_propriedade_com_saldo_suficiente_igual(self):
        self.propriedade.valor = 300
        self.jogador.comprar(self.propriedade)
        self.assertEqual(self.propriedade.proprietario, self.jogador.identificador)

    def test_jogador_recebe_aluguel_propriedade(self):
        self.propriedade.aluguel = 50
        self.jogador.receber_alguel(self.propriedade)
        self.assertEqual(self.jogador.saldo, 350)

    def test_cria_jogadores(self):
        jogadores = cria_jogadores()
        self.assertEqual(len(jogadores), 4)
        self.assertEqual(type(jogadores[0]), Jogador)
