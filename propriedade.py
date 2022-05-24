from dataclasses import dataclass
from random import randint


@dataclass
class Propriedade:

    identificador: int
    aluguel: int
    valor: int
    proprietario: str = ''


def cria_propriedades(quantidade: int = 20) -> list:
    propriedades = []
    for index in range(quantidade):
        propriedade = Propriedade(
            identificador=index,
            aluguel=randint(1, 300//2),
            valor=randint(1, 300)
        )
        propriedades.append(propriedade)
    return propriedades
