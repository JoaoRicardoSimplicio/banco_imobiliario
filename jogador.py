from dataclasses import dataclass
from random import shuffle, randint

from propriedade import Propriedade


@dataclass
class Jogador:

    identificador: str
    tipo: str
    saldo: int = 300
    posicao_atual: int = 0

    def eh_valido(self) -> bool:
        return self.saldo >= 0

    def deve_comprar_propriedade(self, propriedade: Propriedade) -> bool:
        if (self.saldo - propriedade.valor) < 0:
            return False
        if self.tipo == "exigente":
            if propriedade.aluguel <= 50:
                return False
        elif self.tipo == "cauteloso":
            if (self.saldo - propriedade.valor) < 80:
                return False
        elif self.tipo == "aleatorio":
            if randint(1, 2) % 2 == 0:
                return False
        return True


def cria_jogadores() -> list:
    tipos = ['impulsivo', 'exigente', 'cauteloso', 'aleatorio']
    jogadores = [
        Jogador(identificador=f'{index}', tipo=tipo)
        for index, tipo in enumerate(tipos)
    ]
    shuffle(jogadores)
    return jogadores
