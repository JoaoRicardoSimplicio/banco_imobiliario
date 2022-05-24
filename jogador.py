from dataclasses import dataclass
from random import shuffle, randint

from propriedade import Propriedade


@dataclass
class Jogador:

    identificador: int
    tipo: str
    saldo: int = 300

    def eh_valido(self) -> bool:
        return self.saldo >= 0

    def deve_comprar(self, propriedade: Propriedade) -> bool:
        if self.tipo == "exigente":
            if propriedade.aluguel <= 50:
                return False
        elif self.tipo == "cauteloso":
            if propriedade.valor - self.saldo < 80:
                return False
        elif self.tipo == "aleatorio":
            if randint(1, 2) % 2 == 0:
                return False
        return True


def cria_jogadores() -> list:
    tipos = ['impulsivo', 'exigente', 'cauteloso', 'aleatorio']
    shuffle(tipos)
    return [
        Jogador(identificador=index, tipo=tipo)
        for index, tipo in enumerate(tipos)
    ]
