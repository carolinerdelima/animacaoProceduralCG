import math
import random
from Ponto import Ponto

class Particula:
    def __init__(self, posicao: Ponto):
        self.pos = Ponto(posicao.x, posicao.y, posicao.z)       # posição atual
        self.vel = Ponto(random.uniform(-0.02, 0.02),            # velocidade inicial aleatória
                         random.uniform(0.05, 0.15),
                         random.uniform(-0.02, 0.02))
        self.original = Ponto(posicao.x, posicao.y, posicao.z)  # usada para reconstrução
        self.target = Ponto(posicao.x, posicao.y, posicao.z)    # posição final esperada
        self.cor = (0.0, 0.0, 0.0)
        self.rebotes = 0

    def atualizar(self, frame):
        if frame < 400:
            # Fase 2: partículas caindo e quicando
            self.pos.x += self.vel.x
            self.pos.y += self.vel.y
            self.pos.z += self.vel.z

            self.vel.y -= 0.01  # gravidade

            if self.pos.y <= 0:
                self.pos.y = 0
                if self.rebotes < 3:
                    self.vel.y *= -0.5  # quique
                    self.rebotes += 1
                else:
                    self.vel.y = 0
                    self.vel.x *= 0.98
                    self.vel.z *= 0.98

        elif 400 <= frame < 600:
            # Fase 3: formar espiral e subir como vento
            dx = -self.pos.x
            dz = -self.pos.z
            dist = math.sqrt(dx * dx + dz * dz) + 0.001

            angle = math.atan2(self.pos.z, self.pos.x) + 0.1
            raio = max(dist * 0.96, 0.05)

            self.pos.x = raio * math.cos(angle)
            self.pos.z = raio * math.sin(angle)
            self.pos.y += 0.05  # subida vertical

        elif 600 <= frame < 700:
            # Fase 4: reconstrução da cabeça
            t = (frame - 600) / 100.0
            self.pos.x = self.pos.x * (1 - t) + self.target.x * t
            self.pos.y = self.pos.y * (1 - t) + self.target.y * t
            self.pos.z = self.pos.z * (1 - t) + self.target.z * t

    def desenhar(self):
        from OpenGL.GL import glVertex3f
        glVertex3f(self.pos.x, self.pos.y, self.pos.z)
