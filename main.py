from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import time

# ============ CONFIGURAÇÕES Iniciais =============== #
LARGURA = 1000
ALTURA = 700
GRAVIDADE = 9.8

# ============= Classe Canhão ======================== #
class Canhao:
    def __init__(self):
        self.x = 100
        self.y = 100

        self.angulo = 45
        self.forca = 40

    def desenhar(self):
        # Base
        glColor3f(0.3, 0.3, 0.3)
        
        # quadrado inferior
        glBegin(GL_QUADS)
        glVertex2f(self.x - 30, self.y - 50)
        glVertex2f(self.x + 30, self.y - 50)
        glVertex2f(self.x + 30, self.y + 20)
        glVertex2f(self.x - 30, self.y + 20)
        glEnd()

        # quadrado superior
        glBegin(GL_QUADS)
        glVertex2f(self.x - 20, self.y + 10)
        glVertex2f(self.x + 20, self.y + 10)
        glVertex2f(self.x + 20, self.y + 10)
        glVertex2f(self.x - 20, self.y + 10)
        glEnd()

        # centro (circulo)
        glColor3f(0.4, 0.4, 0.4)
        glBegin(GL_POLYGON)
        num_vertices = 40
        for i in range(num_vertices):
            angulo = 2 * math.pi * i / num_vertices
            glVertex2f(
                self.x + 30 * math.cos(angulo),
                self.y + 0 + 30 * math.sin(angulo)
            )
        glEnd()
        
        # Cano
        glPushMatrix()

        glTranslatef(self.x, self.y, 0)
        glRotatef(self.angulo, 0, 0, 1)

        glColor3f(0.1, 0.1, 0.1)

        glBegin(GL_QUADS)
        glVertex2f(0, -10)
        glVertex2f(60, -10)
        glVertex2f(60, 10)
        glVertex2f(0, 10)
        glEnd()

        glPopMatrix()

# ========= Classe do projetil ================= #
class Projetil:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = 0
        self.y = 0

        self.vx = 0
        self.vy = 0

        self.tempo = 0

        self.ativo = False

        self.trajetoria = []

    def disparar(self, canhao):
        if self.ativo:
            return

        angulo_rad = math.radians(canhao.angulo)

        self.x = canhao.x
        self.y = canhao.y

        self.vx = canhao.forca * math.cos(angulo_rad)
        self.vy = canhao.forca * math.sin(angulo_rad)

        self.tempo = 0

        self.ativo = True

        self.trajetoria = []

    def atualizar(self, dt):
        if not self.ativo:
            return

        self.tempo += dt

        self.x = canhao.x + self.vx * self.tempo * 5

        self.y = (
            canhao.y
            + self.vy * self.tempo * 5
            - 0.5 * GRAVIDADE * (self.tempo ** 2) * 20
        )

        self.trajetoria.append((self.x, self.y))

        if self.y <= 0:
            self.ativo = False

    def desenhar(self):
        if not self.ativo:
            return

        # trajetória
        glColor3f(1, 0, 0)

        glBegin(GL_LINE_STRIP)

        for px, py in self.trajetoria:
            glVertex2f(px, py)

        glEnd()

        # projétil
        glColor3f(1, 0, 0)

        glBegin(GL_POLYGON)

        raio = 8

        for i in range(30):
            ang = 2 * math.pi * i / 30
            glVertex2f(
                self.x + raio * math.cos(ang),
                self.y + raio * math.sin(ang)
            )
        glEnd()

# ============ CLASSE ALVO ================ #
class Alvo:
    def __init__(self):
        self.x = 850
        self.y = 100
        self.raio = 30

        self.acertado = False

    def verificar_colisao(self, projetil):
        if not projetil.ativo:
            return

        distancia = math.sqrt(
            (projetil.x - self.x) ** 2
            +
            (projetil.y - self.y) ** 2
        )

        if distancia < self.raio:

            self.acertado = True
            projetil.ativo = False

    def desenhar(self):
        if self.acertado:
            glColor3f(0, 1, 0)
        else:
            glColor3f(0, 0, 1)

        glBegin(GL_POLYGON)

        for i in range(50):

            ang = 2 * math.pi * i / 50

            glVertex2f(
                self.x + self.raio * math.cos(ang),
                self.y + self.raio * math.sin(ang)
            )

        glEnd()

# ============ Classes globais ============== #
canhao = Canhao()
projetil = Projetil()
alvo = Alvo()

ultimo_tempo = time.time()

# ============ Exibicao do texto  ==============
def desenhar_texto(x, y, texto):
    glRasterPos2f(x, y)

    for letra in texto: glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(letra))

# ============= Funcao do display ============== #
def display():

    glClear(GL_COLOR_BUFFER_BIT)

    # solo
    glColor3f(0.2, 0.8, 0.2)

    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(LARGURA, 0)
    glVertex2f(LARGURA, 50)
    glVertex2f(0, 50)
    glEnd()

    canhao.desenhar()
    projetil.desenhar()
    alvo.desenhar()

    glColor3f(0, 0, 0)

    desenhar_texto(
        10,
        ALTURA - 30,
        f"Angulo: {canhao.angulo}"
    )

    desenhar_texto(
        10,
        ALTURA - 60,
        f"Forca: {canhao.forca}"
    )

    if alvo.acertado:

        desenhar_texto(
            400,
            650,
            "ALVO ACERTADO!"
        )

    glutSwapBuffers()

# ========== Funcao de atualizacao ================
def atualizar(valor):
    global ultimo_tempo

    atual = time.time()

    dt = atual - ultimo_tempo

    ultimo_tempo = atual

    projetil.atualizar(dt)

    alvo.verificar_colisao(projetil)

    glutPostRedisplay()

    glutTimerFunc(16, atualizar, 0)

# ========= Leitura do teclado (manipulacao do canhao) ============= #
def teclado_especial(tecla, x, y):

    if tecla == GLUT_KEY_LEFT:
        canhao.angulo -= 2

    elif tecla == GLUT_KEY_RIGHT:
        canhao.angulo += 2

    elif tecla == GLUT_KEY_UP:
        canhao.forca += 2

    elif tecla == GLUT_KEY_DOWN:
        canhao.forca -= 2

    canhao.angulo = max(0, min(90, canhao.angulo))
    canhao.forca = max(5, min(100, canhao.forca))

# ========== Leitura teclado (Acoes do canhao) ================ #
def teclado(tecla, x, y):
    tecla = tecla.decode("utf-8")

    if tecla == ' ':
        projetil.disparar(canhao)
    elif tecla.lower() == 'r':
        projetil.reset()
        alvo.acertado = False
    elif ord(tecla) == 27:
        exit()

# ========== Definicao da funcao Init ================ #
def init():
    glClearColor(0.8, 0.9, 1.0, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, LARGURA, 0, ALTURA)
    glMatrixMode(GL_MODELVIEW)

# ============ Funcao Principal ============== #
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(LARGURA, ALTURA)
glutCreateWindow(b"Lancamento de Projetil com Fisica")
init()
glutDisplayFunc(display)
glutKeyboardFunc(teclado)
glutSpecialFunc(teclado_especial)
glutTimerFunc(16, atualizar, 0)
glutMainLoop()    