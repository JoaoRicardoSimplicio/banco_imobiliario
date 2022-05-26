from dataclasses import dataclass
from typing import Any
from random import randint


@dataclass
class Propriedade:

    identificador: int
    aluguel: int
    valor: int
    proprietario: Any = None

    def disponivel_para_venda(self) -> bool:
        return self.proprietario is None


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
