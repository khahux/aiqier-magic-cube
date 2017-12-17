# -*- coding: utf-8 -*-

import sys
import logging

import math

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import color
from cube import Cube
from magiccube import MagicCube

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

window =0

class Camera:
    origin = [0.0,0.0,0.0]
    length = 1.
    yangle = 0.
    zangle = 0.
    __bthree = False
    def __init__(this):
        this.mouselocation = [0.0,0.0]
        this.offest = 0.01
        this.zangle = 0. if not this.__bthree else math.pi
    def setthree(this,value):
        this.__bthree = value
        this.zangle = this.zangle + math.pi
        this.yangle = -this.yangle
    def eye(this):
        return this.origin if not this.__bthree else this.direction()
    def target(this):
        return this.origin if this.__bthree else this.direction()
    def direction(this):
        if this.zangle > math.pi * 2.0 :
            this.zangle < - this.zangle - math.pi * 2.0
        elif this.zangle < 0. :
            this.zangle < - this.zangle + math.pi * 2.0
        len = 1. if not this.__bthree else this.length if 0. else 1.
        xy = math.cos(this.yangle) * len
        x = this.origin[0] + xy * math.sin(this.zangle)
        y = this.origin[1] + len * math.sin(this.yangle)
        z = this.origin[2] + xy * math.cos(this.zangle)
        return [x,y,z]
    def move(this,x,y,z):
        sinz,cosz = math.sin(this.zangle),math.cos(this.zangle)
        xstep,zstep = x * cosz + z * sinz,z * cosz - x * sinz
        if this.__bthree :
            xstep = -xstep
            zstep = -zstep
        this.origin = [this.origin[0] + xstep,this.origin[1] + y,this.origin[2] + zstep]
    def rotate(this,z,y):
        this.zangle,this.yangle = this.zangle - z,this.yangle + y if not this.__bthree else -y
    def setLookat(this):
        ve,vt = this.eye(),this.target()
        #print ve,vt
        glLoadIdentity()
        gluLookAt(ve[0],ve[1],ve[2],vt[0],vt[1],vt[2],0.0,1.0,0.0)
    def keypress(this,key, x, y):
        if key in ('e', 'E'):
            this.move(0.,0.,1 * this.offest)
        if key in ('f', 'F'):
            this.move(1 * this.offest,0.,0.)
        if key in ('s', 'S'):
            this.move(-1 * this.offest,0.,0.)
        if key in ('d', 'D'):
            this.move(0.,0.,-1 * this.offest)
        if key in ('w', 'W'):
            this.move(0.,1 * this.offest,0.)
        if key in ('r', 'R'):
            this.move(0.,-1 * this.offest,0.)
        if key in ('v', 'V'):
            #this.__bthree = not this.__bthree
            this.setthree(not this.__bthree)
        if key == GLUT_KEY_UP:
            this.offest = this.offest + 0.1
        if key == GLUT_KEY_DOWN:
            this.offest = this.offest - 0.1
    def mouse(this,x,y):
        rx = (x - this.mouselocation[0]) * this.offest * 0.1
        ry = (y - this.mouselocation[1]) * this.offest * -0.1
        this.rotate(rx,ry)
        print x,y
        this.mouselocation = [x,y]

class Window(object):
    DIMENSION_ROTATE = 5
    DIMENSION_TRANSLATE = 1
    DIMENSION_EYE = 10

    def __init__(self):
        global window
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_SINGLE)
        glutInitWindowSize(640,400)
        glutInitWindowPosition(400,400)
        window = glutCreateWindow("opengl")
        glutDisplayFunc(self.drawGLScene)
        glutIdleFunc(self.drawGLScene)
        glutReshapeFunc(self.reSizeGLScene, 640, 400)

        glutKeyboardFunc(self.keylistener)
        glutSpecialFunc(self.keylistener)

        self.camera = Camera()
        self.magicCube = MagicCube()

        #self._cubes = []
        #self._cubes.append(Cube(-1.0, 0.0, 0.0, 0.0, 0.0, 0.0))
        #self._cubes.append(Cube(0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
        #self._cubes.append(Cube(1.0, 0.0, 0.0, 0.0, 0.0, 0.0))

        self.initGL(640, 400)
        glutMainLoop()


    def reSizeGLScene(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def drawGLScene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        #self.camera.setLookat()
        #for cube in self._cubes:
        #    cube.draw()
        #self.camera.setLookat()
        #glTranslatef(0.0,0.0,0.0)
        #glBegin(GL_QUADS)
        #glVertex3f(-1.0, 1.0, 0.0)
        #glVertex3f(1.0, 1.0, 0.0)
        #glVertex3f(1.0, -1.0, 0.0)
        #glVertex3f(-1.0, -1.0, 0.0)
        #glEnd()
        self.camera.setLookat()
        self.magicCube.draw()
        #for cube in self._cubes:
        #    cube.draw()

        glFlush()



    def initGL(self, width,height):
        glClearColor(0.1,0.1,0.5,0.1)
        glClearDepth(1.0)
        #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0,float(width)/float(height),0.1,100.0)
        self.camera.move(0.0, 0.0, -15)


    def keylistener(self, key, x, y):
#        logger.info("symbol: %s, ord: %#x, modifiers: %s" % (symbol,  symbol, modifiers))
        #if key == GLUT_KEY_UP:
        #    for cube in self._cubes:
        #        cube.rotatex_axis(-Window.DIMENSION_ROTATE)
        #elif key == GLUT_KEY_DOWN:
        #    for cube in self._cubes:
        #        cube.rotatex_axis(Window.DIMENSION_ROTATE)

        if key in 'a,b,c,d,e,f,g,h,i,A,B,C,D,E,F,G,H,I':
            self.magicCube.totate(key.upper(), 0)



        #if key == GLUT_KEY_LEFT:
        #    self.magicCube.totate_z_clockwise()
        #elif key == GLUT_KEY_RIGHT:
        #    self.magicCube.totate_z_anticlockwise()

        #elif key in ('n', 'N'):
        #    for cube in self._cubes:
        #        cube.rotatez_axis(-Window.DIMENSION_ROTATE)
        #elif key in ('m', 'M'):
        #    for cube in self._cubes:
        #        cube.rotatez_axis(Window.DIMENSION_ROTATE)
        #elif key in ('a', 'A'):
        #    for cube in self._cubes:
        #        cube.translatex(-Window.DIMENSION_TRANSLATE)
        #elif key in ('d', 'D'):
        #    for cube in self._cubes:
        #        cube.translatey(Window.DIMENSION_TRANSLATE)
        elif key in ('w', 'W'):
            self.camera.move(0.,0., 1 * Window.DIMENSION_EYE)
        elif key in ('s', 'S'):
            self.camera.move(0.,0.,-1 * Window.DIMENSION_EYE)

#        elif symbol == key.E:
#            for cube in self._cubes:
#                cube.translatez(-Window.DIMENSION_TRANSLATE)
#        elif symbol == key.Z:
#            self.eyez = self.eyez + Window.DIMENSION_EYE
#        elif symbol == key.X:
#            self.eyez = self.eyez - Window.DIMENSION_EYE
#        elif symbol == key.ESCAPE:
#            logger.info("exit..")
#            sys.exit()


if __name__ == '__main__':
    w = Window()
