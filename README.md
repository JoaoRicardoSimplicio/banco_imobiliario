# Banco Imobiliário (Resumido)

Este jogo é uma versão resumida do célebre jogo Banco Imobiliário.
Segue regras do jogo:
-  Os jogadores jogam de modo alternado em rodadas, sendo a ordem de quem joga
definida aleatoriamente no início do jogo.
- Todos os jogadores iniciam com saldo de 300.
- São disponibilizadas 20 propriedades, cada uma possui custo de venda, aluguel
    e um proprietário (caso já tenha sido comprada). Não é permitido construção de
    novas propriedades.
- Em sua vez, o jogador joga um dado de 6 faces que determina quantas posições ele
    irá avançar. Ao cair em uma propriedade o jogador possui as seguintes opções:
   - Pode escolher entre comprar ou não, caso a propriedade não possua proprietário
   - Ao cair em uma propriedade com proprietário o jogador deverá pagar o valor do
     aluguel para o proprietário
   - Ao completar uma volta no tabuleiro o jogador ganha +100 em seu saldo

- Jogadores só podem comprar uma propriedade caso ela não possua proprietário e ele
    possua o valor para compra.
- Cada jogador possui um tipo diferente que irá determinar o comportamente que ele
    adotará ao longo do jogo. As seguintes regras descrevem o comportamento de cada
    tipo de jogador:
    - Impulsivo: Compra qualquer propriedade que ele parar.
    - Exigente: Compra qualquer propriedade, desde que o valor de seu aluguel seja maior que 80.
    - Cauteloso: Compra qualquer propriedade, desde que reste pelo menos 80 em saldo após a compra.
    - Aleatório: Compra qualquer propriedade que ele para com probabilidade 50%.
- Um jogador que ficar com saldo negativo será imediatamente eliminado do jogo,
    ficando suas propriedades disponíveis para que outros jogadores possam comprá-las.
- O jogo termina quando restar apenas um jogador com saldo positivo ou o que possuir
    maior saldo ao final de 1000 rodadas.

A execução do programa deverá rodar 300 simulações, imprimindo no console dados referentes às execuções.
Deverá estar contido nessas informações:
- Quantas jogos terminam com 1000 rodadas (Timeout).
- Quantas rodadas em média demora um jogo.
- Qual o percentual de vitórias por tipo de jogador.
- Qual tipo de jogador mais vence.
___________

### Índice

[Requirements](#requirements)
[Executar](#executando)
[Testes](#testes)


### Requirements

- Python 3.8.*


#### Executando o projeto 

```bash
$ python3 jogar.py
```


### Testes

Crie um ambiente virtual
```bash
$ python3.8 -m venv env
```

Ative o ambiente virtual
```bash
$ source env/bin/activate
```

Instale as dependências:
```bash
$ pip install -r core/requirements/base.txt
```

Rode os testes:
```bash
$ pytest
```
