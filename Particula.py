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
        self.frame_inicio_funil = 700
        self.fase_angular = random.uniform(0, 2 * math.pi)
        self.velocidade_angular = random.uniform(0.05, 0.12)
        self.velocidade_vertical = random.uniform(0.01, 0.03)
        self.raio_espiral = math.sqrt(origem.x**2 + origem.z**2) + random.uniform(-0.2, 0.2)
        self.altura_inicial = self.posicao.y
        self.escala_raio = 1.0 + random.uniform(0.5, 1.5)

        # Tempo de ativação escalonado
        self.frame_ativacao = self.frame_inicio_funil + random.randint(0, 100)

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
            return  # ainda não ativou a subida

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

    def resetar_para_origem(self):
        self.posicao = Ponto(self.origem.x, self.origem.y, self.origem.z)

    def desenhar(self):
        from OpenGL.GL import glVertex3f
        glVertex3f(self.posicao.x, self.posicao.y, self.posicao.z)

    def atualizar_explosao(self, frame):
        t = frame - 1000
        if t > 100:
            t = 100
        tempo_normalizado = t / 100.0

        angulo = self.fase_angular + self.velocidade_angular * t
        raio = tempo_normalizado * self.raio_espiral * self.escala_raio

        self.posicao.x = raio * math.cos(angulo)
        self.posicao.z = raio * math.sin(angulo)
        self.posicao.y = tempo_normalizado * 5.0


    def atualizar_reconstrucao(self, frame):
        t = frame - 1100
        if t > 100:
            t = 100
        tempo_normalizado = t / 100.0

        # Interpolação linear do ponto atual até a origem
        self.posicao.x = self.posicao.x * (1 - tempo_normalizado) + self.origem.x * tempo_normalizado
        self.posicao.y = self.posicao.y * (1 - tempo_normalizado) + self.origem.y * tempo_normalizado
        self.posicao.z = self.posicao.z * (1 - tempo_normalizado) + self.origem.z * tempo_normalizado
