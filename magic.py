# -*- coding: utf-8 -*-

import pprint

import math
import random

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import OpenGL.GL as OGLGL

def rotate(pos, loc, ran):
    u, v, w = pos
    x, y, z = loc
    vx = u * math.cos(math.radians(ran)) + (y*w - z*v) * math.sin(math.radians(ran)) + x * (x*u + y*v + z*w) * ( 1- math.cos(math.radians(ran)))
    vy = v * math.cos(math.radians(ran)) + (z*u - x*w) * math.sin(math.radians(ran)) + y * (x*u + y*v + z*w) * ( 1- math.cos(math.radians(ran)))
    vz = w * math.cos(math.radians(ran)) + (x*v - y*u) * math.sin(math.radians(ran)) + z * (x*u + y*v + z*w) * ( 1- math.cos(math.radians(ran)))
    return vx, vy, vz

class Camera(object):
    """
    照相机对象
    此照相机只按照中心轴公转,长度固定,且只看最中心的位置,方向向上
    """
    # 默认半径
    RADIUS = 10
    # 默认旋转角度
    ROVE_ANGLE = 1

    def __init__(self):
        self._r = Camera.RADIUS

        self._x = self._r * math.cos(math.radians(self.mod_angle(45)))
        self._y = self._r * math.cos(math.radians(self.mod_angle(45)))
        self._z = self._r * math.cos(math.radians(self.mod_angle(45)))


        self._up_xyz = (0, 1, 0)

    def rove(self):
        self.revolution_y()

    def revolution_y(self):
        """
        绕y轴公转
        :return:
        """
        self._x, self._y, self._z = rotate((self._x, self._y, self._z), (0, 1, 0), Camera.ROVE_ANGLE)
        self._x, self._y, self._z = -0.523359562429, 7.07106781187, 9.98629534755
        #print self._x, self._y, self._z


    def reset_angle(self, angle):
        """
        角度不能大于360
        :param angle:
        :return:
        """
        return angle % 360

    def get_sign_by_angle(self, angle):
        """
        获得一个角度的正负号
        :param angle:
        :return:
        """
        if 0 <= angle < 90 or 270 < angle < 360:
            return 1
        elif angle == 90 or angle == 270:
            return 0
        elif 90 < angle < 270:
            return -1


    def mod_angle(self, angle):
        return angle % 90

    def eye(self):
        """
        获得摄像头的坐标
        :return:
        """
        return self._x, self._y, self._z

    def direction(self):
        return -self._x, -self._y, -self._z
        # if this.zangle > math.pi * 2.0 :
        #     this.zangle < - this.zangle - math.pi * 2.0
        # elif this.zangle < 0. :
        #     this.zangle < - this.zangle + math.pi * 2.0
        # len = 1. if not this.__bthree else this.length if 0. else 1.
        # xy = math.cos(this.yangle) * len
        # x = this.origin[0] + xy * math.sin(this.zangle)
        # y = this.origin[1] + len * math.sin(this.yangle)
        # z = this.origin[2] + xy * math.cos(this.zangle)
        # return [x,y,z]

    def toup(self):
        return self._up_xyz

    # def move(this,x,y,z):
    #     sinz,cosz = math.sin(this.zangle),math.cos(this.zangle)
    #     xstep,zstep = x * cosz + z * sinz,z * cosz - x * sinz
    #     if this.__bthree :
    #         xstep = -xstep
    #         zstep = -zstep
    #     this.origin = [this.origin[0] + xstep,this.origin[1] + y,this.origin[2] + zstep]
    # def rotate(this,z,y):
    #     this.zangle,this.yangle = this.zangle - z,this.yangle + y if not this.__bthree else -y
    def setLookat(self):
        ve,vt = self.eye(), self.direction()
        upxyz = self.toup()
        #print ve,vt
        glLoadIdentity()
        gluLookAt(ve[0],ve[1],ve[2],vt[0],vt[1],vt[2], upxyz[0],upxyz[1],upxyz[2])
        ##gluLookAt(20, 20, 20 ,0, 0, 0,  0.0,1.0,0.0)
    #def keypress(this,key, x, y):
    #    if key in ('e', 'E'):
    #        this.move(0.,0.,1 * this.offest)
    #    if key in ('f', 'F'):
    #        this.move(1 * this.offest,0.,0.)
    #    if key in ('s', 'S'):
    #        this.move(-1 * this.offest,0.,0.)
    #    if key in ('d', 'D'):
    #        this.move(0.,0.,-1 * this.offest)
    #    if key in ('w', 'W'):
    #        this.move(0.,1 * this.offest,0.)
    #    if key in ('r', 'R'):
    #        this.move(0.,-1 * this.offest,0.)
    #    if key in ('v', 'V'):
    #        #this.__bthree = not this.__bthree
    #        this.setthree(not this.__bthree)
    #    if key == GLUT_KEY_UP:
    #        this.offest = this.offest + 0.1
    #    if key == GLUT_KEY_DOWN:
    #        this.offest = this.offest - 0.1
    #def mouse(this,x,y):
    #    rx = (x - this.mouselocation[0]) * this.offest * 0.1
    #    ry = (y - this.mouselocation[1]) * this.offest * -0.1
    #    this.rotate(rx,ry)
    #    print x,y
    #    this.mouselocation = [x,y]

class Window(object):
    """
    绘图窗口
    """
    DIMENSION_ROTATE = 5
    DIMENSION_TRANSLATE = 1
    DIMENSION_EYE = 10
    window = None # 全局窗口对象

    def __init__(self):
        self._rangle = 0
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_SINGLE)
        glutInitWindowSize(640,400)
        glutInitWindowPosition(400,400)
        Window.window = glutCreateWindow("opengl")
        glutDisplayFunc(self.drawGLScene)
        glutIdleFunc(self.drawGLScene)
        glutReshapeFunc(self.reSizeGLScene, 640, 400)

        glutKeyboardFunc(self.key_listener)
        glutSpecialFunc(self.key_listener)

        self.camera = Camera() # 照相机对象
        self.magicCube = MagicCube() # 魔方对象

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)

        draw_plane_infos = self.magicCube.get_draw_planes()

        #for draw_plane_info in draw_plane_infos:
        #    print draw_plane_info


        self._ran = 0
        #self.magicCube.rotate("F")
        # self.magicCube.rotate("F")
        self.magicCube.show()

        # self._cubes = []
        # self._cubes.append(Cube(-1.0, 0.0, 0.0, 0.0, 0.0, 0.0))
        # self._cubes.append(Cube(0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
        # self._cubes.append(Cube(1.0, 0.0, 0.0, 0.0, 0.0, 0.0))

        self.initGL(640, 400)
        glutMainLoop()



    def reSizeGLScene(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def drawGLScene(self):
        """
        逻辑
        :return:
        """
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
        self.camera.rove()
        self.camera.setLookat()

        DrawUtil.draw_line_x(OGLGL)
        DrawUtil.draw_line_y(OGLGL)
        DrawUtil.draw_line_z(OGLGL)

        draw_plane_infos = self.magicCube.get_draw_planes()
        # draw_plane_infos = self.magicCube.get_draw_plane_info_test(self._ran)
        for draw_plane_info in draw_plane_infos:
            DrawUtil.draw_plane_by_pos_rpos_rangle_side_color(OGLGL, draw_plane_info[0], draw_plane_info[1], draw_plane_info[2], draw_plane_info[3], draw_plane_info[4], draw_plane_info[5])
        # DrawUtil.draw_cube(oglgl, (2, 2, -2), (0, 1, 0), self._rangle, 2)
        #for cube in self._cubes:
        #    cube.draw()
        glFlush()



    def initGL(self, width, height):
        x, y, z = MagicCube.COLOR_BLACK
        # 设置背景颜色
        glClearColor(x, y, z, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearDepth(1.0)
        #glDisable(GL_BLEND)
        #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0,float(width)/float(height),0.1,200.0)
        #self.camera.move(0.0, 0.0, -15)
        #glDepthFunc(GL_BLEND)


    def key_listener(self, key, x, y):
        """
        键盘事件监听
        :param key:
        :param x:
        :param y:
        :return:
        """

#        logger.info("symbol: %s, ord: %#x, modifiers: %s" % (symbol,  symbol, modifiers))
        #if key == GLUT_KEY_UP:
        #    for cube in self._cubes:
        #        cube.rotatex_axis(-Window.DIMENSION_ROTATE)
        #elif key == GLUT_KEY_DOWN:
        #    for cube in self._cubes:
        #        cube.rotatex_axis(Window.DIMENSION_ROTATE)

        #if key in 'a,b,c,d,e,f,g,h,i,A,B,C,D,E,F,G,H,I':
        #    self.magicCube.totate(key.upper(), 0)



        if key == GLUT_KEY_LEFT:
            self._ran -= 10
            #self.camera.rotate(30, 0)
        elif key == GLUT_KEY_RIGHT:
            self._ran += 10
            #self.camera.rotate(0, 30)

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
            # 镜头拉近距离
            self.camera.move(0.,0., 1 * Window.DIMENSION_EYE)
        elif key in ('s', 'S'):
            # 镜头拉远距离
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


class ErrorSideTagException(Exception):
    def __init__(self, tag):
        self.tag = tag

    def __str__(self):
        return self.tag

    def __repr__(self):
        return self.tag

class ErrorSideIndexException(Exception):
    def __init__(self, index):
        self.index = index

    def __str__(self):
        return self.index

    def __repr__(self):
        return self.index

class CountSideIndexException(Exception):
    def __init__(self, count):
        self.count = count

    def __str__(self):
        return self.count

    def __repr__(self):
        return self.count


class DrawUtil(object):
    """
    绘图工具
    """
    @staticmethod
    def len_side_and_dire(pos, half_side):
        return (half_side * pos[0], half_side * pos[1], half_side * pos[2])

    @staticmethod
    def multipl_len_side(points, half_side):
        return tuple(DrawUtil.len_side_and_dire(point, half_side) for point in points)

    @staticmethod
    def get_sign(i):
        if i > 0:
            return 1
        else:
            return -1

    @staticmethod
    def draw_plan_info(side, pos, size):
        if side == "F" or side == "B":
            return ((pos[0] + DrawUtil.get_sign(pos[0]) * size/2.0, pos[1] + DrawUtil.get_sign(pos[1]) * size/2.0, pos[2] + DrawUtil.get_sign(pos[2]) * size/2.0),
                    (pos[0] - DrawUtil.get_sign(pos[0]) * size/2.0, pos[1] + DrawUtil.get_sign(pos[1]) * size/2.0, pos[2] + DrawUtil.get_sign(pos[2]) * size/2.0),
                    (pos[0] - DrawUtil.get_sign(pos[0]) * size/2.0, pos[1] - DrawUtil.get_sign(pos[1]) * size/2.0, pos[2] + DrawUtil.get_sign(pos[2]) * size/2.0),
                    (pos[0] + DrawUtil.get_sign(pos[0]) * size/2.0, pos[1] - DrawUtil.get_sign(pos[1]) * size/2.0, pos[2] + DrawUtil.get_sign(pos[2]) * size/2.0))
        elif side == "L" or side == "R":
            return ((pos[0] + DrawUtil.get_sign(pos[0]) * size/2.0, pos[1] + DrawUtil.get_sign(pos[1]) * size/2.0, pos[2] + DrawUtil.get_sign(pos[2]) * size/2.0),
                    (pos[0] + DrawUtil.get_sign(pos[0]) * size/2.0, pos[1] + DrawUtil.get_sign(pos[1]) * size/2.0, pos[2] - DrawUtil.get_sign(pos[2]) * size/2.0),
                    (pos[0] + DrawUtil.get_sign(pos[0]) * size/2.0, pos[1] - DrawUtil.get_sign(pos[1]) * size/2.0, pos[2] - DrawUtil.get_sign(pos[2]) * size/2.0),
                    (pos[0] + DrawUtil.get_sign(pos[0]) * size/2.0, pos[1] - DrawUtil.get_sign(pos[1]) * size/2.0, pos[2] + DrawUtil.get_sign(pos[2]) * size/2.0))
        elif side == "U" or side == "D":
            return ((pos[0] + DrawUtil.get_sign(pos[0]) * size/2.0, pos[1] + DrawUtil.get_sign(pos[1]) * size/2.0, pos[2] + DrawUtil.get_sign(pos[2]) * size/2.0),
                    (pos[0] - DrawUtil.get_sign(pos[0]) * size/2.0, pos[1] + DrawUtil.get_sign(pos[1]) * size/2.0, pos[2] + DrawUtil.get_sign(pos[2]) * size/2.0),
                    (pos[0] - DrawUtil.get_sign(pos[0]) * size/2.0, pos[1] + DrawUtil.get_sign(pos[1]) * size/2.0, pos[2] - DrawUtil.get_sign(pos[2]) * size/2.0),
                    (pos[0] + DrawUtil.get_sign(pos[0]) * size/2.0, pos[1] + DrawUtil.get_sign(pos[1]) * size/2.0, pos[2] - DrawUtil.get_sign(pos[2]) * size/2.0))

    @staticmethod
    def get_plane_front(half_side):
        return DrawUtil.multipl_len_side((MagicCube.POINT_D, MagicCube.POINT_A, MagicCube.POINT_E, MagicCube.POINT_H), half_side)

    @staticmethod
    def get_plane_behind(half_side):
        return DrawUtil.multipl_len_side((MagicCube.POINT_C, MagicCube.POINT_B, MagicCube.POINT_F, MagicCube.POINT_G), half_side)

    @staticmethod
    def get_plane_up(half_side):
        return DrawUtil.multipl_len_side((MagicCube.POINT_C, MagicCube.POINT_B, MagicCube.POINT_A, MagicCube.POINT_D), half_side)

    @staticmethod
    def get_plane_down(half_side):
        return DrawUtil.multipl_len_side((MagicCube.POINT_G, MagicCube.POINT_F, MagicCube.POINT_E, MagicCube.POINT_H), half_side)

    @staticmethod
    def get_plane_left(half_side):
        return DrawUtil.multipl_len_side((MagicCube.POINT_D, MagicCube.POINT_C, MagicCube.POINT_G, MagicCube.POINT_H), half_side)

    @staticmethod
    def get_plane_right(half_side):
        return DrawUtil.multipl_len_side((MagicCube.POINT_A, MagicCube.POINT_B, MagicCube.POINT_F, MagicCube.POINT_E), half_side)

    @staticmethod
    def draw_plane(oglgl, color, a, b, c, d):
        """
        绘制一个平面
        :param oglgl:
        :param color:
        :param a:
        :param b:
        :param c:
        :param d:
        :return:
        """
        oglgl.glColor3f(*color)
        oglgl.glVertex3f(*a)
        oglgl.glVertex3f(*b)
        oglgl.glVertex3f(*c)
        oglgl.glVertex3f(*d)

    @staticmethod
    def draw_cube(oglgl, rpos, side_size):
        """
        绘制一个立方体
        :param oglgl:
        :param rpos:
        :param side_size:
        :return:
        """
        DrawUtil.draw_plane(oglgl, MagicCube.COLOR_WHITE, *DrawUtil.get_plane_front(side_size / 2.0))
        DrawUtil.draw_plane(oglgl, MagicCube.COLOR_RED, *DrawUtil.get_plane_behind(side_size / 2.0))
        DrawUtil.draw_plane(oglgl, MagicCube.COLOR_GREEN, *DrawUtil.get_plane_up(side_size / 2.0))
        DrawUtil.draw_plane(oglgl, MagicCube.COLOR_BLUE, *DrawUtil.get_plane_down(side_size / 2.0))
        DrawUtil.draw_plane(oglgl, MagicCube.COLOR_YELLOW, *DrawUtil.get_plane_left(side_size / 2.0))
        DrawUtil.draw_plane(oglgl, MagicCube.COLOR_ORANGE, *DrawUtil.get_plane_right(side_size / 2.0))

    @staticmethod
    def inverse(x):
        """
        取反
        :param x:
        :return:
        """
        if x == 0:
            return x
        return -x

    @staticmethod
    def revolution(oglgl, pos, rpos, rangle):
        """
        绕中心轴公转
        :return:
        """
        oglgl.glTranslatef(DrawUtil.inverse(pos[0]), DrawUtil.inverse(pos[1]), DrawUtil.inverse(pos[2]))
        oglgl.glRotatef(rangle, rpos[0],rpos[1], rpos[2])
        oglgl.glTranslatef(pos[0], pos[1], pos[2])


    @staticmethod
    def draw_cube(oglgl, pos, rpos, rangle, side_size):
        """
        绘制
        :param oglgl:
        :param pos: 立方体坐标
        :param rpos: 旋转轴坐标
        :param rangle: 旋转角度
        :param side_size: 边长
        :return:
        """
        oglgl.glPushMatrix()
        oglgl.glTranslatef(*pos)
        DrawUtil.revolution(oglgl, pos, rpos, rangle)
        oglgl.glBegin(oglgl.GL_QUADS)
        DrawUtil.draw_cube(oglgl, side_size / 2.0)
        oglgl.glEnd()
        oglgl.glPopMatrix()

    @staticmethod
    def draw_line(oglgl, xyz1, xyz2, color):
        oglgl.glPushMatrix()
        glLineWidth(1)
        oglgl.glBegin(oglgl.GL_LINES)
        glColor3f(*color)
        glVertex3f(*xyz1)
        glVertex3f(*xyz2)
        oglgl.glEnd()
        oglgl.glPopMatrix()

    @staticmethod
    def draw_line_x(oglgl):
        DrawUtil.draw_line(oglgl, (-30, 0, 0), (30, 0, 0), MagicCube.COLOR_YELLOW)

    @staticmethod
    def draw_line_y(oglgl):
        DrawUtil.draw_line(oglgl, (0, -30, 0), (0, 30, 0), MagicCube.COLOR_GREEN)

    @staticmethod
    def draw_line_z(oglgl):
        DrawUtil.draw_line(oglgl, ( 0, 0, -30), (0, 0, 30), MagicCube.COLOR_RED)

    @staticmethod
    def draw_plane_by_pos_rpos_rangle_side_color(oglgl, side, pos, rpos, rangle, size, color):
        """
        绘制一个平面
        :param oglgl: 绘板上下文
        :param pos: 坐标 (x, y, z)
        :param rpos: 绕轴坐标 (x, y, z)
        :param rangle: 绕轴旋转角度
        :param side_size: 边长
        :param color: 绘制颜色
        :return:
        """
        oglgl.glPushMatrix()
        #oglgl.glTranslatef(*pos)
        #DrawUtil.revolution(oglgl, pos, rpos, rangle)
        oglgl.glBegin(oglgl.GL_QUADS)
        DrawUtil.draw_plane(oglgl, color, *DrawUtil.draw_plan_info(side, pos, size))
        oglgl.glEnd()
        oglgl.glPopMatrix()


class MagicCube(object):
    COLOR_YELLOW = (1, 1 , 0)
    COLOR_WHITE = (1, 1, 1)
    COLOR_BLUE = (0, 0, 1)
    COLOR_RED = (1, 0, 0)
    COLOR_GREEN = (0, 0.6, 0)
    COLOR_ORANGE = (1, 0.49, 0.14)
    COLOR_BLACK = (0, 0, 0)

    STATUS_ROTATE = "ROTATE"
    STATUS_PAUSE = "PAUSE"

    POINT_A = (1.0, 1.0, 1.0)
    POINT_B = (1.0, 1.0, -1.0)
    POINT_C = (-1.0, 1.0, -1.0)
    POINT_D = (-1.0, 1.0, 1.0)

    POINT_E = (1.0, -1.0, 1.0)
    POINT_F = (1.0, -1.0, -1.0)
    POINT_G = (-1.0, -1.0, -1.0)
    POINT_H = (-1.0, -1.0, 1.0)

    # 边长
    LEN_OF_SIDE = 1
    LEN_OF_HALF_SIDE = LEN_OF_SIDE / 2.0


    def __init__(self):
        """
        每个数字面,十位数确定颜色.个位数确定位置.
        1, 2, 3
        4, 5, 6
        7, 8, 9
        而每个数字面所在的面位(F,R,L,B,U,D)将确定此面所绕的旋转轴和旋转角度(顺时针,大拇指左旋).
        :return:
        """
        self._s = {
        "F": {"square":[1,2,3,    4,5,6,    7,8,9],   "side": "URDL"}, # Front
        "R": {"square":[11,12,13, 14,15,16, 17,18,19],"side": "UBDF"}, # Right
        "L": {"square":[21,22,23, 24,25,26, 27,28,29],"side": "UFDB"}, # Left
        "B": {"square":[31,32,33, 34,35,36, 37,38,39],"side": "ULDR"}, # Behind
        "U": {"square":[41,42,43, 44,45,46, 47,48,49],"side": "BRFL"}, # Up
        "D": {"square":[51,52,53, 54,55,56, 57,58,59],"side": "FRBL"}, # Down
        }

        # 魔方状态
        self._status = MagicCube.STATUS_PAUSE

    def get_color_by_num(self, num):
        """
        根据传入的面,判断出此面的颜色
        前蓝－后绿
        左橙－右红
        上黄－下白
        :return:
        """
        if  0 < num < 10:
            return MagicCube.COLOR_BLUE
        elif 30 < num < 40:
            return MagicCube.COLOR_GREEN
        elif 20 < num < 30:
            return MagicCube.COLOR_ORANGE
        elif 10 < num < 20:
            return MagicCube.COLOR_RED
        elif 40 < num < 50:
            return MagicCube.COLOR_YELLOW
        elif 50 < num < 60:
            return MagicCube.COLOR_WHITE
        else:
            raise CountSideIndexException(num)

    def get_pos_w_h_by_num(self, num):
        """
        根据各位数获得每个面的x坐标和y坐标
        :param num:
        :return:
        """
        n = num % 10
        if n == 1:
            return (1, 1)
        elif n == 2:
            return (0, 1)
        elif n == 3:
            return (-1, 1)
        elif n == 4:
            return (1, 0)
        elif n == 5:
            return (0, 0)
        elif n == 6:
            return (-1, 0)
        elif n == 7:
            return (1, -1)
        elif n == 8:
            return (0, -1)
        elif n == 9:
            return (-1, -1)

    def get_pos_high_by_side_tag(self, side):
        if "F" == side:
            return -1
        elif "R" == side:
            return -1
        elif "L" == side:
            return 1
        elif "B" == side:
            return 1
        elif "U" == side:
            return 1
        elif "D" == side:
            return -1
        else:
            raise ErrorSideTagException(side)

    def get_pos_high_by_wh_high(self, side, wh, high):
        if "F" == side or "B" == side:
            return wh[0], wh[1], high
        elif "L" == side or "R" == side:
            return high, wh[0], wh[1]
        elif "U" == side or "D" == side:
            return wh[0], high, wh[1]
        else:
            raise ErrorSideTagException(side)


    def get_rpos_by_side_tag(self, side):
        if "F" == side:
            return (0, 0, 0)
        elif "R" == side:
            return (1, 0, 0)
        elif "L" == side:
            return (1, 0, 0)
        elif "B" == side:
            return (0, 0, 0)
        elif "U" == side:
            return (0, 1, 0)
        elif "D" == side:
            return (0, 1, 0)
        else:
            raise ErrorSideTagException(side)

    def get_rangle_by_side_tag(self, side):
        if "F" == side:
            return 0
        elif "R" == side:
            return 180
        elif "L" == side:
            return 0
        elif "B" == side:
            return 0
        elif "U" == side:
            return 0
        elif "D" == side:
            return 180
        else:
            raise ErrorSideTagException(side)


    def get_draw_planes(self):
        planes = []
        for side, side_item in self._s.iteritems():
            #if side != "F":
            if side != "F" and side != "B":
            #if side != "F" and side != "B" and side != "L":
                continue
            for side_num in side_item["square"]:
                wh = self.get_pos_w_h_by_num(side_num)
                z = self.get_pos_high_by_side_tag(side)
                pos = self.get_pos_high_by_wh_high(side, wh, z)
                rpos = self.get_rpos_by_side_tag(side)
                rangle = self.get_rangle_by_side_tag(side)
                side_size = MagicCube.LEN_OF_SIDE
                color = self.get_color_by_num(side_num)
                item = (side, pos, rpos, rangle, side_size, color)
                #print item
                planes.append(item)
        return planes


    def get_draw_plane_info_test(self, range):
        """
        绘制边框,用于测试的接口
        :param side:
        :return:
        """
        return [
            ((1 ,  1, 3),  (1,0,0), range, 1, MagicCube.COLOR_YELLOW),
            ((0 ,  1, 3),  (1,0,0), range, 1, MagicCube.COLOR_WHITE),
            ((-1,  1, 3),  (1,0,0), range, 1, MagicCube.COLOR_RED),
            ((1 ,  0, 3),  (1,0,0), range, 1, MagicCube.COLOR_YELLOW),
            ((0 ,  0, 3),  (1,0,0), range, 1, MagicCube.COLOR_WHITE),
            ((-1,  0, 3),  (1,0,0), range, 1, MagicCube.COLOR_RED),
            ((1 , -1, 3), (1,0,0), range, 1, MagicCube.COLOR_YELLOW),
            ((0 , -1, 3), (1,0,0), range, 1, MagicCube.COLOR_WHITE),
            ((-1, -1, 3), (1,0,0), range, 1, MagicCube.COLOR_RED),
        ]


    def get_color_by_count(self, count):
        if count < 10:
            return MagicCube.COLOR_YELLOW
        elif 10 < count < 20:
            return MagicCube.COLOR_WHITE
        elif 20 < count < 30:
            return MagicCube.COLOR_BLUE
        elif 30 < count < 40:
            return MagicCube.COLOR_RED
        elif 40 < count < 50:
            return MagicCube.COLOR_GREEN
        elif 50 < count < 60:
            return MagicCube.COLOR_ORANGE
        else:
            raise CountSideIndexException(count)

    def show(self):
        pprint.pprint(self._s)

    def get_first_row_coordinate(self):
        """
        第1行
        :return:
        """
        return 0, 1, 2

    def get_third_col_coordinate(self):
        """
        第3列
        :return:
        """
        return 2, 5, 8

    def get_third_row_coordinate(self):
        """
        第3行
        :return:
        """
        return 6, 7, 8

    def get_first_col_coordinate(self):
        """
        第1列
        :return:
        """
        return 0, 3, 6

    def get_coordinate_by_index(self, i):
        if i == 0:
            return self.get_first_row_coordinate()
        elif i == 1:
            return self.get_third_col_coordinate()
        elif i == 2:
            return self.get_third_row_coordinate()
        elif i == 3:
            return self.get_first_col_coordinate()
        else:
            raise ErrorSideIndexException(i)

    def get_value_by_coordinate(self, side, coordinate):
        return self._s[side]["square"][coordinate[0]], self._s[side]["square"][coordinate[1]], self._s[side]["square"][coordinate[2]]

    def set_value_by_coordinate(self, side, coordinate, values):
         self._s[side]["square"][coordinate[0]] = values[0]
         self._s[side]["square"][coordinate[1]] = values[1]
         self._s[side]["square"][coordinate[2]] = values[2]


    def move_tail_to_head(self, li):
        return li[len(li)-1:] + li[0:len(li)-1]



    def rotate_self_side(self, side):
        s = self._s[side]["square"]
        s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8] = s[6], s[3], s[0], s[7], s[4], s[1], s[8], s[5], s[2]

    def rotate(self, side):
        sides = self._s[side]["side"]
        temp = None
        sc = []
        v = []

        self.rotate_self_side(side)
        for s in sides:
            index = self._s[s]["side"].index(side)
            coordinate = self.get_coordinate_by_index(index)
            values = self.get_value_by_coordinate(s, coordinate)
            sc.append((s, coordinate))
            v.append(values)
        v = self.move_tail_to_head(v)
        for index, s in enumerate(sc):
            self.set_value_by_coordinate(s[0], s[1], v[index])


def main():
    w = Window()

if __name__ == "__main__":
    main()