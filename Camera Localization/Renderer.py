import sys
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import math as m
import numpy as np


class Renderer:

        def __init__(self):
                glutInit(sys.argv)
                glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)

        def __display(self):
                light_ambient = [0.0, 0.0, 0.0, 1.0]
                light_diffuse = [1.0, 1.0, 1.0, 1.0]
                light_specular = [1.0, 1.0, 1.0, 1.0]
                light_position = [1.0, 1.0, 1.0, 0.0]

                glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
                glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
                glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
                glLightfv(GL_LIGHT0, GL_POSITION, light_position)

                glEnable(GL_LIGHTING)
                glEnable(GL_LIGHT0)
                glEnable(GL_DEPTH_TEST)

                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()

                gluLookAt(3.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

                glPushMatrix()
                glTranslatef(self.px, self.pz, self.py)
                glRotatef(self.rx * 180 / m.pi, 1.0, 0.0, 0.0)
                glRotatef(self.ry * 180 / m.pi, 0.0, 1.0, 0.0)
                glRotatef(self.rz * 180 / m.pi, 0.0, 0.0, 1.0)
                glutSolidCone(0.5, 1.0, 15, 15)
                glPopMatrix()

                glPushMatrix()
                glTranslatef(0.0, -5.0, 0.0)
                glutSolidCube(10.0)
                glPopMatrix()

                glFlush()

        def __reshape(self, w, h):
                glViewport(0, 0, w, h)

                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()

                aspect_ratio = h / w if w <= h else w / h
                gluPerspective(90, aspect_ratio, .1, 100.0)

        def __keyboard(key, x, y, z):
                glutLeaveMainLoop()

        def render(self, title, rx, ry, rz, px, py, pz):
                self.rx = rx
                self.ry = ry
                self.rz = rz

                self.px = px
                self.py = py
                self.pz = pz

                glutInitWindowSize(500, 500)
                glutCreateWindow(title)
                glutReshapeFunc(self.__reshape)
                glutKeyboardFunc(self.__keyboard)
                glutDisplayFunc(self.__display)
                glutMainLoop()
