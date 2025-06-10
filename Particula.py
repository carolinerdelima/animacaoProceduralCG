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
        self.posicao_final_funil = None  # ← novo atributo

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

        # Armazena a posição final no topo do funil, uma única vez
        if tempo_normalizado >= 1.0 and self.posicao_final_funil is None:
            self.posicao_final_funil = Ponto(self.posicao.x, self.posicao.y, self.posicao.z)

    def atualizar_descida_reconstrucao(self, frame):
        if self.posicao_final_funil is None:
            return  # ainda não terminou a subida

        t = frame - 1000
        duracao = 200
        progresso = min(t / duracao, 1.0)

        # Interpola suavemente da posição final do funil até a posição original
        self.posicao.x = (1 - progresso) * self.posicao_final_funil.x + progresso * self.origem.x
        self.posicao.y = (1 - progresso) * self.posicao_final_funil.y + progresso * self.origem.y
        self.posicao.z = (1 - progresso) * self.posicao_final_funil.z + progresso * self.origem.z

    def resetar_para_origem(self):
        self.posicao = Ponto(self.origem.x, self.origem.y, self.origem.z)

    def desenhar(self):
        from OpenGL.GL import glVertex3f
        glVertex3f(self.posicao.x, self.posicao.y, self.posicao.z)
