# -*- coding: utf-8 -*-

import sys
import logging

import pyglet
from pyglet.gl import *
from pyglet.window import key


from cube import Cube

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
)

class Window(pyglet.window.Window):
    DIMENSION_ROTATE = 5
    DIMENSION_TRANSLATE = 1
    DIMENSION_EYE = 0.1

    def __init__(self, width, height, title=''):
        super(Window, self).__init__(width, height, title)

        self._cubes = [Cube(-1.0, 0.0, -10.0, 0.0, 0.0, 0.0), Cube(0.0, 0.0, -10.0, 0.0, 0.0, 0.0), Cube(1.0, 0.0, -10.0, 0.0, 0.0, 0.0)]

        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

        self.fovy = 35
        self.znear = 1
        self.zfar = 1000

        self.eyex = 0.0
        self.eyey = 0.0
        self.eyez = 0.0

        # 背景
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)

    def on_draw(self):
        self.clear()
        self.camera(self.width, self.height)
        for cube in self._cubes:
            cube.draw()


    def camera(self, width, height):
        # using Projection mode
        # 对投影矩阵操作
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluLookAt(self.eyex, self.eyey, self.eyez, 0, 0,-1, 0, 1, 0)

        aspectRatio = width / height
        # 指定了观察的视景体在世界坐标系中的具体大小
        gluPerspective(self.fovy, aspectRatio, self.znear, self.zfar)

    def on_resize(self, width, height):
        # set the Viewport
        glViewport(0, 0, width, height)

        self.camera(width, height)

        #glMatrixMode(GL_MODELVIEW)


    def on_key_press(self, symbol, modifiers):
        logger.info("symbol: %s, ord: %#x, modifiers: %s" % (symbol,  symbol, modifiers))
        if symbol == key.UP:
            for cube in self._cubes:
                cube.rotatex_axis(-Window.DIMENSION_ROTATE)
        elif symbol == key.DOWN:
            for cube in self._cubes:
                cube.rotatex_axis(Window.DIMENSION_ROTATE)
        elif symbol == key.LEFT:
            for cube in self._cubes:
                cube.rotatey_axis(-Window.DIMENSION_ROTATE)
        elif symbol == key.RIGHT:
            for cube in self._cubes:
                cube.rotatey_axis(Window.DIMENSION_ROTATE)
        elif symbol == key.F1:
            for cube in self._cubes:
                cube.rotatez_axis(-Window.DIMENSION_ROTATE)
        elif symbol == key.F2:
            for cube in self._cubes:
                cube.rotatez_axis(Window.DIMENSION_ROTATE)
        elif symbol == key.A:
            for cube in self._cubes:
                cube.translatex(-Window.DIMENSION_TRANSLATE)
        elif symbol == key.D:
            for cube in self._cubes:
                cube.translatex(Window.DIMENSION_TRANSLATE)
        elif symbol == key.W:
            for cube in self._cubes:
                cube.translatey(Window.DIMENSION_TRANSLATE)
        elif symbol == key.S:
            for cube in self._cubes:
                cube.translatey(-Window.DIMENSION_TRANSLATE)
        elif symbol == key.Q:
            for cube in self._cubes:
                cube.translatez(Window.DIMENSION_TRANSLATE)
        elif symbol == key.E:
            for cube in self._cubes:
                cube.translatez(-Window.DIMENSION_TRANSLATE)
        elif symbol == key.Z:
            self.eyex = self.eyex + Window.DIMENSION_EYE
        elif symbol == key.X:
            self.eyex = self.eyex - Window.DIMENSION_EYE
        elif symbol == key.ESCAPE:
            logger.info("exit..")
            sys.exit()


if __name__ == '__main__':
    Window(600, 600, 'Pyglet Colored Cube')
    pyglet.app.run()