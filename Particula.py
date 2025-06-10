import math
import random
from Ponto import Ponto

class Particula:
    def __init__(self, origem: Ponto):
        self.origem = origem
        self.posicao = Ponto(origem.x, origem.y, origem.z)

        # Velocidade inicial para a queda
        self.vy = 0
        self.vx = random.uniform(-0.01, 0.01)
        self.vz = random.uniform(-0.01, 0.01)

        # Gravitacional simples
        self.gravidade = -0.001

        # Guarda o tempo do primeiro quique
        self.tempo_quique = None

        # Propriedades para fase de funil
        self.frame_inicio_funil = 700  # constante para controle
        self.fase_angular = random.uniform(0, 2 * math.pi)
        self.velocidade_angular = random.uniform(0.05, 0.12)
        self.velocidade_vertical = random.uniform(0.03, 0.06)
        self.raio_espiral = math.sqrt(origem.x**2 + origem.z**2) + random.uniform(-0.2, 0.2)
        self.altura_inicial = self.posicao.y

    def atualizar(self, frame):
        if frame < self.frame_inicio_funil:
            # Queda e quique
            self.vy += self.gravidade
            self.posicao.x += self.vx
            self.posicao.y += self.vy
            self.posicao.z += self.vz

            # Colisão com o chão
            if self.posicao.y < 0:
                self.posicao.y = 0
                self.vy *= -0.5  # perde energia no quique
                if abs(self.vy) < 0.001:
                    self.vy = 0

    def atualizar_fase_funil(self, frame):
        t = frame - self.frame_inicio_funil
        if t < 0:
            return

        tempo_normalizado = t / 200.0  # controle de tempo para ajustar afunilamento
        tempo_normalizado = min(tempo_normalizado, 1.0)

        angulo = self.fase_angular + self.velocidade_angular * t

        # Raio diminui conforme o tempo avança (funil afunila)
        raio = self.raio_espiral * (1.0 - tempo_normalizado)
        raio = max(raio, 0.05)  # evita colapso total

        self.posicao.x = raio * math.cos(angulo)
        self.posicao.z = raio * math.sin(angulo)

        # Altura sobe proporcional ao tempo
        self.posicao.y = self.altura_inicial + (tempo_normalizado * 5.0)

    def resetar_para_origem(self):
        self.posicao = Ponto(self.origem.x, self.origem.y, self.origem.z)

    def desenhar(self):
        from OpenGL.GL import glVertex3f
        glVertex3f(self.posicao.x, self.posicao.y, self.posicao.z)