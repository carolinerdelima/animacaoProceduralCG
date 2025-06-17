from Ponto import Ponto
import math

def gerarPontosCoracao(qtdePontos):
    pontos = []
    for i in range(qtdePontos):
        t = math.pi * 2 * i / qtdePontos
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
        x /= 20  # Escala para caber na tela
        y = y / 20 + 2.0
        pontos.append(Ponto(x, y, 0))
    return pontos
