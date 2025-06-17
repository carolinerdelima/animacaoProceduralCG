from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from Objeto3D import *
from Particula import Particula
from HeartGenerator import gerarPontosCoracao

import math

o:Objeto3D

frame = 0
estado = 'PLAY'

particulas = []
explodiu = False

def init():
    global o
    glClearColor(0.85, 0.85, 0.85, 1.0)
    glClearDepth(1.0)

    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    o = Objeto3D()
    o.LoadFile('Human_Head.obj')

    DefineLuz()
    PosicUser()


def DefineLuz():
    # Define cores para um objeto dourado
    luz_ambiente = [0.4, 0.4, 0.4]
    luz_difusa = [0.7, 0.7, 0.7]
    luz_especular = [0.9, 0.9, 0.9]
    posicao_luz = [2.0, 3.0, 0.0]  # Posição da Luz
    especularidade = [1.0, 1.0, 1.0]

    # ****************  Fonte de Luz 0

    glEnable(GL_COLOR_MATERIAL)

    #Habilita o uso de iluminação
    glEnable(GL_LIGHTING)

    #Ativa o uso da luz ambiente
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, luz_ambiente)
    # Define os parametros da luz número Zero
    glLightfv(GL_LIGHT0, GL_AMBIENT, luz_ambiente)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, luz_difusa)
    glLightfv(GL_LIGHT0, GL_SPECULAR, luz_especular)
    glLightfv(GL_LIGHT0, GL_POSITION, posicao_luz)
    glEnable(GL_LIGHT0)

    # Ativa o "Color Tracking"
    glEnable(GL_COLOR_MATERIAL)

    # Define a reflectancia do material
    glMaterialfv(GL_FRONT, GL_SPECULAR, especularidade)

    # Define a concentração do brilho.
    # Quanto maior o valor do Segundo parametro, mais
    # concentrado será o brilho. (Valores válidos: de 0 a 128)
    glMateriali(GL_FRONT, GL_SHININESS, 51)

def PosicUser():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Configura a matriz da projeção perspectiva (FOV, proporção da tela, distância do mínimo antes do clipping, distância máxima antes do clipping
    # https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/gluPerspective.xml
    gluPerspective(60, 16/9, 0.01, 50)  # Projecao perspectiva
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    #Especifica a matriz de transformação da visualização
    # As três primeiras variáveis especificam a posição do observador nos eixos x, y e z
    # As três próximas especificam o ponto de foco nos eixos x, y e z
    # As três últimas especificam o vetor up
    # https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/gluLookAt.xml
    gluLookAt(0, 2, 6, 0, 2, 0, 0, 1, 0)

def DesenhaLadrilho():
    glColor3f(0.85, 0.85, 0.85)  # mesma cor do fundo
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glVertex3f(-0.5, 0.0, -0.5)
    glVertex3f(-0.5, 0.0, 0.5)
    glVertex3f(0.5, 0.0, 0.5)
    glVertex3f(0.5, 0.0, -0.5)
    glEnd()


def DesenhaPiso():
    glPushMatrix()
    glDisable(GL_LIGHTING)  # <--- desliga iluminação, pra desenhar o piso invisível	

    glTranslated(-20, -1, -10)
    for x in range(-20, 20):
        glPushMatrix()
        for z in range(-20, 20):
            DesenhaLadrilho()
            glTranslated(0, 0, 1)
        glPopMatrix()
        glTranslated(1, 0, 0)

    glEnable(GL_LIGHTING)   # <--- reativa iluminação, pra usar no resto da cena
    glPopMatrix()

def DesenhaCubo():
    glPushMatrix()
    glColor3f(1, 0, 0)
    glTranslated(0, 0.5, 0)
    glutSolidCube(1)

    glColor3f(0.5, 0.5, 0)
    glTranslated(0, 0.5, 0)
    glRotatef(90, -1, 0, 0)
    glRotatef(45, 0, 0, 1)
    glutSolidCone(1, 1, 4, 4)
    glPopMatrix()

def desenha():
    global frame, estado, particulas, explodiu

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)

    if estado == 'PLAY':
        frame += 1

    DesenhaPiso()

    if frame < 260:
        angulo_y = 30 * math.sin(frame * 0.025)
        angulo_x = 15 * math.cos(frame * 0.025)
        o.rotation = (angulo_x, angulo_y)
        o.DesenhaVertices()

    elif frame < 700:
        if not explodiu:
            particulas.clear()
            for v in o.vertices:
                particulas.append(Particula(v))
            explodiu = True

        glColor3f(0, 0, 0)
        glPointSize(5)
        glBegin(GL_POINTS)
        for p in particulas:
            p.atualizar(frame)
            p.desenhar()
        glEnd()

    elif frame < 1000:
        glColor3f(0, 0, 0)
        glPointSize(5)
        glBegin(GL_POINTS)
        for p in particulas:
            p.atualizarFaseFunil(frame)
            p.desenhar()
        glEnd()

    elif frame < 1200:
        glColor3f(0, 0, 0)
        glPointSize(5)
        glBegin(GL_POINTS)
        for p in particulas:
            p.atualizarDescidaReconstrucao(frame)
            p.desenhar()
        glEnd()

    else:
        # reconstrói a cabeça ou reinicia
        glColor3f(0, 0, 0)
        glPointSize(5)
        glBegin(GL_POINTS)
        for p in particulas:
            p.resetarParaOrigem()
            p.desenhar()
        glEnd()

    glutSwapBuffers()

def teclado(key, x, y):
    global estado, frame, explodiu, particulas, o

    if key == b' ': # Barra de espaço para pausar ou continuar
        if estado == 'PLAY':
            estado = 'PAUSE'
        else:
            estado = 'PLAY'
    elif key == b'r': # 'r' para REWIND
        frame = max(0, frame - 10) # Retrocede 10 frames, mas não abaixo de 0
        explodiu = False # Reseta o estado da explosão ao retroceder
    elif key == b'f': # 'f' para FORWARD
        frame = min(1200, frame + 10) # Avança 10 frames, mas não além do frame máximo
        if frame >= 700 and not explodiu: # Se avançar para a fase de explosão, reinicializa as partículas
            particulas.clear()
            for v in o.vertices:
                particulas.append(Particula(v))
            explodiu = True
    elif key == b'q': # 'q' para resetar
        frame = 0
        estado = 'PLAY' # Volta para o estado de play depos de resetar
        explodiu = False
        particulas.clear() # Limpa as partículas existentes
        o = Objeto3D() # Recarrega o objeto para resetar sua posição/rotação
        o.LoadFile('Human_Head.obj') # regarrega dnv o modelo

    glutPostRedisplay()
    pass

def main():

    glutInit(sys.argv)

    # Define o modelo de operacao da GLUT
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)

    # Especifica o tamnho inicial em pixels da janela GLUT
    glutInitWindowSize(400, 400)

    # Especifica a posição de início da janela
    glutInitWindowPosition(100, 100)

    # Cria a janela passando o título da mesma como argumento
    glutCreateWindow(b'T2 - CG')

    # Função responsável por fazer as inicializações
    init()

    # Registra a funcao callback de redesenho da janela de visualizacao
    glutDisplayFunc(desenha)

    # Registra a funcao callback para tratamento das teclas ASCII
    glutKeyboardFunc(teclado)

    glutIdleFunc(desenha)

    try:
        # Inicia o processamento e aguarda interacoes do usuario
        glutIdleFunc(glutPostRedisplay)  # chama redesenho automaticamente
        glutMainLoop()
    except SystemExit:
        pass

if __name__ == '__main__':
    main()