import math
import random
from Ponto import Ponto

class Particula:
    def __init__(self, origem: Ponto):
        self.origem = origem
        self.posicao = Ponto(origem.x, origem.y, origem.z)

        # Trepidação, atribuindo valores aleatórios em x e y
        self.vx = random.uniform(-0.01, 0.01)
        self.vz = random.uniform(-0.01, 0.01)

        # Parte responsável pela queda (gravidade + velocidade vertical)
        self.vy = 0
        self.gravidade = -0.001

        # Movimento de subida em espiral
        self.frameInicioFunil = 700
        self.faseAngular = random.uniform(0, 2 * math.pi) # define o ângulo inicial da partícula na espiral
        self.velocidadeAngular = random.uniform(0.05, 0.12) # faz girar em círculo
        self.velocidadeVertical = random.uniform(0.01, 0.03) # velocidade de subida
        self.raioEspiral = math.sqrt(origem.x**2 + origem.z**2) + random.uniform(-0.2, 0.2) # distância radial inicial da partícula em relação ao eixo central
        self.alturaInicial = 0
        self.escalaRaio = 1.0 + random.uniform(0.5, 1.5)
        self.frameAtivacao = self.frameInicioFunil + random.randint(0, 100) # faz com que as partículas não comecem todas juntas

        # Parâmetros de reconstrução
        self.frameInicioReconstrucao = 1000 + random.randint(0, 100)
        self.posicaoFinalFunil = None

        self.destino = None
        self.frameInicioTransformacao = 1200

    def atualizar(self, frame):
        if frame < self.frameInicioFunil:
            self.vy += self.gravidade # queda vertical (eixo Y)

            # Trepidação horizontal
            self.posicao.x += self.vx
            self.posicao.y += self.vy
            self.posicao.z += self.vz

            # se a partícula passar da altura y = 0 (o chão da cena), ela bate no chão
            if self.posicao.y < 0:
                self.posicao.y = 0

                # rebote para cima
                self.vy *= -0.5
                if abs(self.vy) < 0.001:
                    self.vy = 0

    def atualizarFaseFunil(self, frame):
        if frame < self.frameAtivacao:
            return

        t = frame - self.frameAtivacao

        # isso garante que o movimento dure cerca de 200 frames, e depois pare
        tempoNormalizado = t / 200.0
        tempoNormalizado = min(tempoNormalizado, 1.0)

        # Enquanto o tempo avança:
        # O raio vai diminuindo, fazendo as partículas irem para o centro do funil
        # O ângulo aumenta, então elas giram
        # A posição y sobe gradualmente
        angulo = self.faseAngular + self.velocidadeAngular * t
        raio = self.raioEspiral * (1.0 - tempoNormalizado)
        raio *= self.escalaRaio
        raio = max(raio, 0.02)

        self.posicao.x = raio * math.cos(angulo)
        self.posicao.z = raio * math.sin(angulo)
        self.posicao.y = 0 + tempoNormalizado * 5.0

        # Armazena a posição final no topo do funil, uma única vez
        if tempoNormalizado >= 1.0 and self.posicaoFinalFunil is None:
            self.posicaoFinalFunil = Ponto(self.posicao.x, self.posicao.y, self.posicao.z)

    def atualizarDescidaReconstrucao(self, frame):
        if self.posicaoFinalFunil is None:
            return  # ainda não terminou a subida

        t = frame - 1000
        duracao = 200
        progresso = min(t / duracao, 1.0)

        # Interpola suavemente da posição final do funil até a posição original
        self.posicao.x = (1 - progresso) * self.posicaoFinalFunil.x + progresso * self.origem.x
        self.posicao.y = (1 - progresso) * self.posicaoFinalFunil.y + progresso * self.origem.y
        self.posicao.z = (1 - progresso) * self.posicaoFinalFunil.z + progresso * self.origem.z

    def resetarParaOrigem(self):
        self.posicao = Ponto(self.origem.x, self.origem.y, self.origem.z)

    def desenhar(self):
        from OpenGL.GL import glVertex3f
        glVertex3f(self.posicao.x, self.posicao.y, self.posicao.z)

    def atualizarTransformacaoParaDestino(self, frame):
        if self.destino is None:
            return
        t = frame - self.frameInicioTransformacao
        duracao = 200
        progresso = min(t / duracao, 1.0)

        self.posicao.x = (1 - progresso) * self.origem.x + progresso * self.destino.x
        self.posicao.y = (1 - progresso) * self.origem.y + progresso * self.destino.y
        self.posicao.z = (1 - progresso) * self.origem.z + progresso * self.destino.z

