from Ponto import Ponto
import math

def gerarPontosCoracao(qtdePontos):
    pontos = []

    # vai gerar exatamente o mesmo número de pontos que o número de partículas que temos na animação 
    for i in range(qtdePontos):
        # distribui os pontos ao longo de um ângulo de 0 a 2π (faz um loop completo em círculo)
        t = math.pi * 2 * i / qtdePontos

        # equações matemáticas de um coração, onde o x e o y geram o contorno do coração
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)

        x /= 20  # Escala para caber na tela
        y = y / 20 + 2.0
        pontos.append(Ponto(x, y, 0))
    return pontos
