from objloader import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from pygame.constants import *
from SARCExtract import SARCExtract
from bntx_extract import bntx_extract
from tkinter.filedialog import askopenfilename
import subprocess
import pygame
import ntpath
import time
import os

pygame.init()
viewport = (800,600)
hx = viewport[0]/2
hy = viewport[1]/2
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)
glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)
filepath = askopenfilename()
bfres_path = ""
if filepath.endswith(".szs"):
    SARCExtract.extract_szs(filepath)
    bfres_path = os.path.join(filepath[:-4], ntpath.basename(filepath)[:-3] + "bfres")
elif filepath.endswith(".bfres"):
    bfres_path = filepath
p = subprocess.Popen(os.path.join("BFRES2OBJ", "BFRES2OBJ.exe") + " " + bfres_path + " " + bfres_path[:-5] + "obj").wait()
obj_path = bfres_path[:-5] + "obj"
new_text = open(obj_path, "r").read().replace(",", ".")
with open(obj_path, "w") as f:
    f.truncate(0)
    f.write(new_text)
obj = OBJ(obj_path, swapyz=False)
clock = pygame.time.Clock()
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = viewport
gluPerspective(90.0, width/float(height), 1, 1000000.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)
rx, ry = (0,0)
tx, ty = (0,0)
zpos = 5
rotate = move = False
running = True
while running:
    clock.tick(30)
    for e in pygame.event.get():
        if e.type == QUIT:
            running = False
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            running = False
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 4: zpos -= 10
            elif e.button == 5: zpos += 10
            elif e.button == 1: rotate = True
            elif e.button == 3: move = True
        elif e.type == MOUSEBUTTONUP:
            if e.button == 1: rotate = False
            elif e.button == 3: move = False
        elif e.type == MOUSEMOTION:
            i, j = e.rel
            if rotate:
                rx += i/2
                ry += j/2
            if move:
                tx += i*5
                ty -= j*5
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslate(tx/20., ty/20., - zpos)
    glRotate(ry, 1, 0, 0)
    glRotate(rx, 0, 1, 0)
    glCallList(obj.gl_list)
    pygame.display.flip()
pygame.quit()
