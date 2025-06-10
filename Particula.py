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
        self.gravidade = -0.001

        # Fase inicial: queda
        self.frame_inicio_funil = 700
        self.fase_angular = random.uniform(0, 2 * math.pi)
        self.velocidade_angular = random.uniform(0.05, 0.12)
        self.velocidade_vertical = random.uniform(0.01, 0.03)
        self.raio_espiral = math.sqrt(origem.x**2 + origem.z**2) + random.uniform(-0.2, 0.2)
        self.altura_inicial = 0
        self.escala_raio = 1.0 + random.uniform(0.5, 1.5)
        self.frame_ativacao = self.frame_inicio_funil + random.randint(0, 100)

        # Parâmetros de reconstrução
        self.frame_inicio_reconstrucao = 1000 + random.randint(0, 100)

    def atualizar(self, frame):
        if frame < self.frame_inicio_funil:
            self.vy += self.gravidade
            self.posicao.x += self.vx
            self.posicao.y += self.vy
            self.posicao.z += self.vz

            if self.posicao.y < 0:
                self.posicao.y = 0
                self.vy *= -0.5
                if abs(self.vy) < 0.001:
                    self.vy = 0

    def atualizar_fase_funil(self, frame):
        if frame < self.frame_ativacao:
            return

        t = frame - self.frame_ativacao
        tempo_normalizado = t / 200.0
        tempo_normalizado = min(tempo_normalizado, 1.0)

        angulo = self.fase_angular + self.velocidade_angular * t
        raio = self.raio_espiral * (1.0 - tempo_normalizado)
        raio *= self.escala_raio
        raio = max(raio, 0.02)

        self.posicao.x = raio * math.cos(angulo)
        self.posicao.z = raio * math.sin(angulo)
        self.posicao.y = 0 + tempo_normalizado * 5.0

    def atualizar_descida_reconstrucao(self, frame):
        if frame < self.frame_inicio_reconstrucao:
            return

        t = frame - self.frame_inicio_reconstrucao
        tempo_normalizado = t / 200.0
        tempo_normalizado = min(tempo_normalizado, 1.0)

        angulo = self.fase_angular + self.velocidade_angular * t
        raio = self.raio_espiral * tempo_normalizado
        raio *= self.escala_raio

        self.posicao.x = raio * math.cos(angulo)
        self.posicao.z = raio * math.sin(angulo)
        self.posicao.y = 5.0 - tempo_normalizado * 5.0  # descendo

    def resetar_para_origem(self):
        self.posicao = Ponto(self.origem.x, self.origem.y, self.origem.z)

    def desenhar(self):
        from OpenGL.GL import glVertex3f
        glVertex3f(self.posicao.x, self.posicao.y, self.posicao.z)
