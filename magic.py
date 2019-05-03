# -*- coding: utf-8 -*-

import pprint

import math
import random
import time

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import OpenGL.GL as OGLGL

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

def rotate(pos, loc, ran):
    u, v, w = pos
    x, y, z = loc
    vx = u * math.cos(math.radians(ran)) + (y*w - z*v) * math.sin(math.radians(ran)) + x * (x*u + y*v + z*w) * ( 1- math.cos(math.radians(ran)))
    vy = v * math.cos(math.radians(ran)) + (z*u - x*w) * math.sin(math.radians(ran)) + y * (x*u + y*v + z*w) * ( 1- math.cos(math.radians(ran)))
    vz = w * math.cos(math.radians(ran)) + (x*v - y*u) * math.sin(math.radians(ran)) + z * (x*u + y*v + z*w) * ( 1- math.cos(math.radians(ran)))
    return vx, vy, vz

class Boy(object):
    """
    一个类,像一双手一样,拧魔方
    """

    REFLEX_ARC = 100
    ROTATE_SIDE = "FBUDLR"
    MEMORY_SIZE = 50

    PLAY_STATUS_GO = 0
    PLAY_STATUS_BACK = 1

    PLAY_COUNT = 1

    def __init__(self):
        self._rotate_side = None
        self._last_timestamp = self.get_current_time_ms()
        self._memory = []
        self._play_status = Boy.PLAY_STATUS_GO
        self._memory_stack_temp = []
        self._play_count = Boy.PLAY_COUNT

    def pop_memory(self):
        if  len(self._memory_stack_temp) > 0:
            return self._memory_stack_temp.pop()
        else:
            first, count = self.pop_same_list(self._memory)
            if first is None:
                return None
            else:
                temp = self.get_inverse_operation(first, count)
                if temp is None:
                    return None
                else:
                    self._memory_stack_temp = list(temp)
                    return self._memory_stack_temp.pop()


    def pop_same_list(self, li):
        if li is None or li == []:
            return (None,0)
        first = li.pop()
        count = 1
        for i in li[: : -1]:
            if i != first:
                break
            else:
                count += 1
        for i in range(count-1):
            li.pop()

        return (first, count)

    def get_inverse_operation(self, side, count):
        if count == 1:
            return side*3
        elif count == 2:
            return side*2
        elif count == 3:
            return side
        else:
            return None

    def play_go(self, magicCube):
        """
        正着玩
        :param magicCube:
        :return:
        """
        if self._rotate_side is None:
            self._rotate_side = self.random_side()

        isOk = magicCube.rotate_side(self._rotate_side)
        if not isOk:
            self._rotate_side = None
        else:
            # 说明成功的完成了一次旋转
            if magicCube.is_pause():
                self._memory.append(self._rotate_side)
                self._rotate_side = None

    def play_back(self, magicCube):
        """
        反着玩
        :param magicCube:
        :return:
        """
        if self._rotate_side is None:
            temp = self.pop_memory()
            if temp is not None:
                logger.info("calcute inverse operation: %s" %(temp,))
                self._rotate_side = temp
            else:
                return

        isOk = magicCube.rotate_side(self._rotate_side)
        if not isOk:
            self._rotate_side = None
        else:
            # 说明成功的完成了一次旋转
            if magicCube.is_pause():
                self._rotate_side = None


    def play(self, magicCube):
        if self._last_timestamp is None or self.get_current_time_ms() - self._last_timestamp < Boy.REFLEX_ARC:
            return

        if len(self._memory) > Boy.MEMORY_SIZE and self._rotate_side is None:
            self._play_status = Boy.PLAY_STATUS_BACK
        elif len(self._memory) == 0 and len(self._memory_stack_temp) == 0 and self._rotate_side is None:
            if self._play_status == Boy.PLAY_STATUS_BACK:
                print self._memory_stack_temp
                print self._rotate_side
                self._play_count -= 1

            self._play_status = Boy.PLAY_STATUS_GO

        if self._play_count == 0:
            logger.info("FINISH")
            return

        if self._play_status == Boy.PLAY_STATUS_GO:
            self.play_go(magicCube)
        else:
            self.play_back(magicCube)





    def random_side(self):
        return random.choice(Boy.ROTATE_SIDE)

    def get_current_time_ms(self):
        """
        获得当前毫秒时间戳
        :return:
        """
        return int(time.time()*1000)



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


    def revolution_y_right(self):
        """
        绕y轴公转
        :return:
        """
        self._x, self._y, self._z = rotate((self._x, self._y, self._z), (0, 1, 0), Camera.ROVE_ANGLE)

    def revolution_y_left(self):
        """
        绕y轴公转
        :return:
        """
        self._x, self._y, self._z = rotate((self._x, self._y, self._z), (0, -1, 0), Camera.ROVE_ANGLE)

    def revolution_x_right(self):
        """
        绕x轴公转
        :return:
        """
        self._x, self._y, self._z = rotate((self._x, self._y, self._z), (1, 0, 0), Camera.ROVE_ANGLE)

    def revolution_x_left(self):
        """
        绕x轴公转
        :return:
        """
        self._x, self._y, self._z = rotate((self._x, self._y, self._z), (-1, 0, 0), Camera.ROVE_ANGLE)
    def revolution_z_right(self):
        """
        绕y轴公转
        :return:
        """
        self._x, self._y, self._z = rotate((self._x, self._y, self._z), (0, 0, 1), Camera.ROVE_ANGLE)

    def revolution_z_left(self):
        """
        绕y轴公转
        :return:
        """
        self._x, self._y, self._z = rotate((self._x, self._y, self._z), (0, 0, -1), Camera.ROVE_ANGLE)


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


    def toup(self):
        return self._up_xyz

    def setLookat(self):
        ve,vt = self.eye(), self.direction()
        upxyz = self.toup()
        #print ve,vt
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        gluLookAt(ve[0],ve[1],ve[2],vt[0],vt[1],vt[2], upxyz[0],upxyz[1],upxyz[2])


class Window(object):
    """
    绘图窗口
    """
    DIMENSION_ROTATE = 5
    DIMENSION_TRANSLATE = 1
    DIMENSION_EYE = 10
    window = None # 全局窗口对象
    W_H = (1000, 800)

    def __init__(self):
        self._rangle = 0
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE | GLUT_DEPTH)
        glutInitWindowSize(*Window.W_H)
        glutInitWindowPosition(400,400)
        Window.window = glutCreateWindow("MagicCube")
        glutDisplayFunc(self.drawGLScene)
        glutIdleFunc(self.drawGLScene)
        glutReshapeFunc(self.reSizeGLScene, 800, 600)

        glutKeyboardFunc(self.key_listener)
        glutSpecialFunc(self.key_listener)

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)

        #启用0号光源
        glEnable(GL_LIGHT0)

        x, y, z = MagicCube.COLOR_BLACK
        # 设置背景颜色
        glClearColor(x, y, z, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearDepth(1.0)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0,float(Window.W_H[0])/float(Window.W_H[1]),0.1,200.0)


        self.camera = Camera() # 照相机对象
        self.magicCube = MagicCube() # 魔方对象
        self.cube = Cube(Cube.PLANE_FRONT, 1, 1, 1, 1, 0,1,0, 0)
        self.boy = Boy()
        self._ran = 0

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
        self.camera.revolution_y_right()
        self.camera.setLookat()

        self.boy.play(self.magicCube)
        # 绘制罪坐标线
        #DrawUtil.draw_coordinate_axis(OGLGL)

        draw_plane_infos = self.magicCube.get_draw_planes()
        for draw_plane_info in draw_plane_infos:
            DrawUtil.draw_plane_by_pos_rpos_rangle_side_color(OGLGL, draw_plane_info[0], draw_plane_info[1], draw_plane_info[2], draw_plane_info[3], draw_plane_info[4], draw_plane_info[5])
        glFlush()





    def key_listener(self, key, x, y):
        """
        键盘事件监听
        :param key:
        :param x:
        :param y:
        :return:
        """
        if key == "1":
            self.magicCube.rotate_side("F")
        elif key == "2":
            self.magicCube.rotate_side("B")
        elif key == "3":
            self.magicCube.rotate_side("U")
        elif key == "4":
            self.magicCube.rotate_side("D")
        elif key == "5":
            self.magicCube.rotate_side("L")
        elif key == "6":
            self.magicCube.rotate_side("R")
        elif key in ('a', 'A'):
            # 镜头拉近距离
            self.camera.revolution_y_left()
        elif key in ('d', 'D'):
            # 镜头拉远距离
            self.camera.revolution_y_right()
        elif key in ('w', 'W'):
            # 镜头拉近距离
            self.camera.revolution_x_left()
        elif key in ('s', 'S'):
            # 镜头拉远距离
            self.camera.revolution_x_right()
        elif key in ('z', 'Z'):
            # 镜头拉近距离
            self.camera.revolution_z_left()
        elif key in ('x', 'X'):
            # 镜头拉远距离
            self.camera.revolution_z_left()
        #elif key == key.ESCAPE:
        #    logger.info("exit..")
        #    sys.exit()


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

class Cube(object):
    """
    立方体
    """
    # 面
    # 前
    PLANE_FRONT = 1
    # 后
    PLANE_BEHIND = 2
    # 上
    PLANE_TOP = 3
    # 下
    PLANE_BOTTOM = 4
    # 左
    PLANE_LEFT = 5
    # 右
    PLANE_RIGHT = 6
    # 正方体有六个面
    PLANE_COUNT = 6

    POINT_A = (1.0, 1.0, 1.0)
    POINT_B = (1.0, 1.0, -1.0)
    POINT_C = (-1.0, 1.0, -1.0)
    POINT_D = (-1.0, 1.0, 1.0)

    POINT_E = (1.0, -1.0, 1.0)
    POINT_F = (1.0, -1.0, -1.0)
    POINT_G = (-1.0, -1.0, -1.0)
    POINT_H = (-1.0, -1.0, 1.0)


    def __init__(self, dir, x, y, z, side_len, x_rotate_angle, y_rotate_angle, z_rotate_angle, rotate_angle):
        self.__dir = dir
        # 坐标
        self.__x = x
        self.__y = y
        self.__z = z

        self.__x_rotate_angle = x_rotate_angle
        self.__y_rotate_angle = y_rotate_angle
        self.__z_rotate_angle = z_rotate_angle
        # 旋转角度
        self._rotate_angle = rotate_angle

        self.__hs = side_len

    def rotate_up(self):
        self._rotate_angle += 10

    def rotate_down(self):
        self._rotate_angle -= 10

    def get_plane_front(self):
        return self.multipl_len_side((Cube.POINT_D, Cube.POINT_A, Cube.POINT_E, Cube.POINT_H))

    def get_plane_behind(self):
        return self.multipl_len_side((Cube.POINT_C, Cube.POINT_B, Cube.POINT_F, Cube.POINT_G))

    def get_plane_top(self):
        return self.multipl_len_side((Cube.POINT_C, Cube.POINT_B, Cube.POINT_A, Cube.POINT_D))

    def get_plane_bottom(self):
        return self.multipl_len_side((Cube.POINT_G, Cube.POINT_F, Cube.POINT_E, Cube.POINT_H))

    def get_plane_left(self):
        return self.multipl_len_side((Cube.POINT_D, Cube.POINT_C, Cube.POINT_G, Cube.POINT_H))

    def get_plane_right(self):
        return self.multipl_len_side((Cube.POINT_A, Cube.POINT_B, Cube.POINT_F, Cube.POINT_E))

    def multipl_len_side(self, points):
        return tuple(self.len_side_and_dire(point) for point in points)

    def len_side_and_dire(self, pos):
        change = (1,1,1)

        return (self.__hs /2.0 * pos[0] * change[0], self.__hs /2.0  * pos[1] * change[1], self.__hs /2.0  * pos[2] * change[2])

    def get_pos(self):
        return self.__x, self.__y, self.__z

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_z(self):
        return self.__z

    def get_xyz_rotate(self):
        return self.__x_rotate_angle, self.__y_rotate_angle, self.__z_rotate_angle

    def get_rotate_angle(self):
        return self._rotate_angle

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
            sign = 1
            if side == "F":
                sign = -1
            elif side == "B":
                sign = 1
            return ((pos[0] + DrawUtil.get_sign(pos[0]) * size/2.0, pos[1] + DrawUtil.get_sign(pos[1]) * size/2.0, pos[2] + sign * size/2.0),
                    (pos[0] - DrawUtil.get_sign(pos[0]) * size/2.0, pos[1] + DrawUtil.get_sign(pos[1]) * size/2.0, pos[2] + sign * size/2.0),
                    (pos[0] - DrawUtil.get_sign(pos[0]) * size/2.0, pos[1] - DrawUtil.get_sign(pos[1]) * size/2.0, pos[2] + sign * size/2.0),
                    (pos[0] + DrawUtil.get_sign(pos[0]) * size/2.0, pos[1] - DrawUtil.get_sign(pos[1]) * size/2.0, pos[2] + sign * size/2.0))
        elif side == "L" or side == "R":
            sign = 1
            if side == "R":
                sign = -1
            elif side == "L":
                sign = 1
            return ((pos[0] + sign * size/2.0, pos[1] + DrawUtil.get_sign(pos[1]) * size/2.0, pos[2] + DrawUtil.get_sign(pos[2]) * size/2.0),
                    (pos[0] + sign * size/2.0, pos[1] + DrawUtil.get_sign(pos[1]) * size/2.0, pos[2] - DrawUtil.get_sign(pos[2]) * size/2.0),
                    (pos[0] + sign * size/2.0, pos[1] - DrawUtil.get_sign(pos[1]) * size/2.0, pos[2] - DrawUtil.get_sign(pos[2]) * size/2.0),
                    (pos[0] + sign * size/2.0, pos[1] - DrawUtil.get_sign(pos[1]) * size/2.0, pos[2] + DrawUtil.get_sign(pos[2]) * size/2.0))
        elif side == "U" or side == "D":
            sign = 1
            if side == "D":
                sign = -1
            elif side == "U":
                sign = 1
            return ((pos[0] + DrawUtil.get_sign(pos[0]) * size/2.0, pos[1] + sign * size/2.0, pos[2] + DrawUtil.get_sign(pos[2]) * size/2.0),
                    (pos[0] - DrawUtil.get_sign(pos[0]) * size/2.0, pos[1] + sign * size/2.0, pos[2] + DrawUtil.get_sign(pos[2]) * size/2.0),
                    (pos[0] - DrawUtil.get_sign(pos[0]) * size/2.0, pos[1] + sign * size/2.0, pos[2] - DrawUtil.get_sign(pos[2]) * size/2.0),
                    (pos[0] + DrawUtil.get_sign(pos[0]) * size/2.0, pos[1] + sign * size/2.0, pos[2] - DrawUtil.get_sign(pos[2]) * size/2.0))


    @staticmethod
    def draw_cube_by_cube(oglgl, cube):
        oglgl.glPushMatrix()

        oglgl.glTranslatef(*cube.get_pos())

        oglgl.glTranslatef(DrawUtil.inverse(cube.get_x()), DrawUtil.inverse(cube.get_y()), DrawUtil.inverse(cube.get_z()))
        x, y, z = cube.get_xyz_rotate()
        oglgl.glRotatef(cube.get_rotate_angle(), x, y, z)
        oglgl.glTranslatef(*cube.get_pos())

        oglgl.glBegin(oglgl.GL_QUADS)
        DrawUtil.draw_plane(oglgl, MagicCube.COLOR_WHITE, *cube.get_plane_front())
        DrawUtil.draw_plane(oglgl, MagicCube.COLOR_RED, *cube.get_plane_behind())
        DrawUtil.draw_plane(oglgl, MagicCube.COLOR_GREEN, *cube.get_plane_top())
        DrawUtil.draw_plane(oglgl, MagicCube.COLOR_BLUE, *cube.get_plane_bottom())
        DrawUtil.draw_plane(oglgl, MagicCube.COLOR_YELLOW, *cube.get_plane_left())
        DrawUtil.draw_plane(oglgl, MagicCube.COLOR_ORANGE, *cube.get_plane_right())
        oglgl.glEnd()


        oglgl.glPopMatrix()


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
        绕rpos
        :return:
        """
        oglgl.glTranslatef(DrawUtil.inverse(pos[0]), DrawUtil.inverse(pos[1]), DrawUtil.inverse(pos[2]))
        oglgl.glRotatef(rangle, rpos[0],0, 0)
        oglgl.glRotatef(rangle, 0,rpos[1], 0)
        oglgl.glRotatef(rangle, 0, 0, rpos[2])

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
        glLineStipple (1, 1000100010001000)
        oglgl.glBegin(oglgl.GL_LINES)
        glColor3f(*color)
        glVertex3f(*xyz1)
        glVertex3f(*xyz2)
        oglgl.glEnd()
        oglgl.glPopMatrix()

    @staticmethod
    def draw_coordinate_axis(oglgl):
        DrawUtil.draw_line_x(oglgl)
        DrawUtil.draw_line_y(oglgl)
        DrawUtil.draw_line_z(oglgl)
    @staticmethod
    def draw_line_x(oglgl):
        DrawUtil.draw_line(oglgl, (-30, 0, 0), (30, 0, 0), MagicCube.COLOR_PURPLE)

    @staticmethod
    def draw_line_y(oglgl):
        DrawUtil.draw_line(oglgl, (0, -30, 0), (0, 30, 0), MagicCube.COLOR_PURPLE)

    @staticmethod
    def draw_line_z(oglgl):
        DrawUtil.draw_line(oglgl, ( 0, 0, -30), (0, 0, 30), MagicCube.COLOR_PURPLE)

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

        oglgl.glRotatef(rangle, rpos[0],rpos[1], rpos[2])

        oglgl.glBegin(oglgl.GL_QUADS)
        a, b, c, d = DrawUtil.draw_plan_info(side, pos, size)
        DrawUtil.draw_plane(oglgl, color, a, b, c, d)
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
    COLOR_CYAN = (0,255,255)
    COLOR_PURPLE = (255,0,255)

    STATUS_ROTATE_SIDE = "ROTATE"
    STATUS_PAUSE = "PAUSE"

    TRANS_TYPE_SIDE_F = "F"
    TRANS_TYPE_SIDE_B = "B"
    TRANS_TYPE_SIDE_U = "U"
    TRANS_TYPE_SIDE_D = "D"
    TRANS_TYPE_SIDE_L = "L"
    TRANS_TYPE_SIDE_R = "R"

    # 边长
    LEN_OF_SIDE = 1
    LEN_OF_HALF_SIDE = LEN_OF_SIDE / 2.0
    # 旋转速率 = 10
    ROTATE_ANGLE_RATE = 10

    def is_pause(self):
        return self._status == MagicCube.STATUS_PAUSE

    def __init__(self):
        """
        每个数字面,十位数确定颜色.个位数确定位置.
        1, 2, 3
        4, 5, 6
        7, 8, 9
        而每个数字面所在的面位(F,R,L,B,U,D)将确定此面所绕的旋转轴和旋转角度(顺时针,大拇指左旋).
        :return:
        F: 蓝
        B: 绿
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
        self._trans = None
        self._rang = 0

    def rotate_side(self, side):
        if not self.can_trans_side(side):
            logger.warning("cant rotate side %s because now is :%s status and transtype is %s" %(side, self._status, self._trans))
            return False

        self.rotate(side)
        return True

    def rotate(self, side_type):
        new_rang = self._rang + MagicCube.ROTATE_ANGLE_RATE
        if new_rang >= 90:
            # 旋转角度设置为零,状态切换
            self._rang = 0
            self.rotate_side_change_status(side_type)
            self._status = MagicCube.STATUS_PAUSE
            self._trans = None
            #self.show()
        else:
            if self._status == MagicCube.STATUS_PAUSE:
                self._status = MagicCube.STATUS_ROTATE_SIDE
                # 这里应该有个转换才对
                self._trans = side_type
            self._rang = new_rang


    def can_trans_side(self, trans_side):
        """
        判断状态是否可以旋转
        :param trans_side:
        :return:
        """
        if self._status == MagicCube.STATUS_PAUSE:
            return True

        # 同一时刻只能旋转一条边
        if self._status == MagicCube.STATUS_ROTATE_SIDE and self._trans == trans_side:
            return True
        return False


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

    def get_rpos_default(self):
        return (0, 0, 0)

    def get_rpos_by_side_tag(self, num):
        if not self.judge_num_is_in_side(num, self._trans):
            return self.get_rpos_default()

        if "F" == self._trans:
            return (0, 0, 1)
        elif "R" == self._trans:
            return (1, 0, 0)
        elif "L" == self._trans:
            return (-1, 0, 0)
        elif "B" == self._trans:
            return (0, 0, -1)
        elif "U" == self._trans:
            return (0, -1, 0)
        elif "D" == self._trans:
            return (0, 1, 0)
        else:
            raise ErrorSideTagException(self._trans)

    def get_rangle_default(self):
        return 0

    def get_rangle_by_side_tag(self, num):
        if not self.judge_num_is_in_side(num, self._trans):
            return self.get_rangle_default()
        else:
            return self._rang

    def get_pos_num_F(self, num):
        """
        根据各位数获得每个面的x坐标和y坐标
        :param num:
        :return:
        """
        n = num + 1
        if n == 1:
            return (1, 1, -1)
        elif n == 2:
            return (0, 1, -1)
        elif n == 3:
            return (-1, 1, -1)
        elif n == 4:
            return (1, 0, -1)
        elif n == 5:
            return (0, 0, -1)
        elif n == 6:
            return (-1, 0, -1)
        elif n == 7:
            return (1, -1, -1)
        elif n == 8:
            return (0, -1, -1)
        elif n == 9:
            return (-1, -1, -1)

    def get_pos_num_B(self, num):
        """
        根据各位数获得每个面的x坐标和y坐标
        :param num:
        :return:
        """
        n = num + 1
        if n == 1:
            return (-1, 1, 1)
        elif n == 2:
            return (0, 1, 1)
        elif n == 3:
            return (1, 1, 1)
        elif n == 4:
            return (-1, 0, 1)
        elif n == 5:
            return (0, 0, 1)
        elif n == 6:
            return (1, 0, 1)
        elif n == 7:
            return (-1, -1, 1)
        elif n == 8:
            return (0, -1, 1)
        elif n == 9:
            return (1, -1, 1)

    def get_pos_num_L(self, num):
        """
        根据各位数获得每个面的x坐标和y坐标
        :param num:
        :return:
        """
        n = num + 1
        if n == 1:
            return (1, 1, 1)
        elif n == 2:
            return (1, 1, 0)
        elif n == 3:
            return (1, 1, -1)
        elif n == 4:
            return (1, 0, 1)
        elif n == 5:
            return (1, 0, 0)
        elif n == 6:
            return (1, 0, -1)
        elif n == 7:
            return (1, -1, 1)
        elif n == 8:
            return (1, -1, 0)
        elif n == 9:
            return (1, -1, -1)

    def get_pos_num_R(self, num):
        """
        根据各位数获得每个面的x坐标和y坐标
        :param num:
        :return:
        """
        n = num + 1
        if n == 1:
            return (-1, 1, -1)
        elif n == 2:
            return (-1, 1, 0)
        elif n == 3:
            return (-1, 1, 1)
        elif n == 4:
            return (-1, 0, -1)
        elif n == 5:
            return (-1, 0, 0)
        elif n == 6:
            return (-1, 0, 1)
        elif n == 7:
            return (-1, -1, -1)
        elif n == 8:
            return (-1, -1, 0)
        elif n == 9:
            return (-1, -1, 1)

    def get_pos_num_U(self, num):
        """
        根据各位数获得每个面的x坐标和y坐标
        :param num:
        :return:
        """
        n = num + 1
        if n == 1:
            return (1, 1, 1)
        elif n == 2:
            return (0, 1, 1)
        elif n == 3:
            return (-1, 1, 1)
        elif n == 4:
            return (1, 1, 0)
        elif n == 5:
            return (0, 1, 0)
        elif n == 6:
            return (-1, 1, 0)
        elif n == 7:
            return (1, 1, -1)
        elif n == 8:
            return (0, 1, -1)
        elif n == 9:
            return (-1, 1, -1)

    def get_pos_num_D(self, num):
        """
        根据各位数获得每个面的x坐标和y坐标
        :param num:
        :return:
        """

        n = num + 1
        if n == 1:
            return (1, -1, -1)
        elif n == 2:
            return (0, -1, -1)
        elif n == 3:
            return (-1, -1, -1)
        elif n == 4:
            return (1, -1, 0)
        elif n == 5:
            return (0, -1, 0)
        elif n == 6:
            return (-1, -1, 0)
        elif n == 7:
            return (1, -1, 1)
        elif n == 8:
            return (0, -1, 1)
        elif n == 9:
            return (-1, -1, 1)

    def get_pos_by_side_and_index(self, side, index):
        if "F" == side:
            return self.get_pos_num_F(index)
        elif "R" == side:
            return self.get_pos_num_R(index)
        elif "L" == side:
            return self.get_pos_num_L(index)
        elif "B" == side:
            return self.get_pos_num_B(index)
        elif "U" == side:
            return self.get_pos_num_U(index)
        elif "D" == side:
            return self.get_pos_num_D(index)
        else:
            raise ErrorSideTagException(side)

    def judge_num_is_in_side(self, num, side):
        """
        判断一个数字是否与此面相关
        :param num:
        :param side:
        :return:
        """
        if side is None:
            return False
        if num in self._s[side]["square"]:
            return True
        for s in self._s[side]["side"]:
            index = self._s[s]["side"].index(side)
            coordinate = self.get_coordinate_by_index(index)
            values = self.get_value_by_coordinate(s, coordinate)
            if num in values:
                return True
        return False


    def get_draw_planes(self):
        planes = []
        for side in "FRLBUD":
            side_item = self._s.get(side)

            for index, side_num in enumerate(side_item["square"]):
                pos = self.get_pos_by_side_and_index(side, index)
                rpos = self.get_rpos_by_side_tag(side_num)
                rangle = self.get_rangle_by_side_tag(side_num)
                side_size = MagicCube.LEN_OF_SIDE
                color = self.get_color_by_num(side_num)
                item = (side, pos, rpos, rangle, side_size, color)
                planes.append(item)


                # 每一个旋转边的会在加2个黑色的内边
                # 一个旋转,一个不旋转
                if self._trans == side:
                    pos = self.fix_black_axle(self.get_pos_by_side_and_index(side, index), side)
                    color = MagicCube.COLOR_BLACK
                    item = (side, pos, rpos, rangle, side_size, color)
                    planes.append(item)
                    #一个不旋转
                    rpos = self.get_rpos_default()
                    rangle = self.get_rangle_default()
                    item = (side, pos, rpos, rangle, side_size, color)
                    planes.append(item)

        return planes

    def fix_black_axle(self, pos, side):
        """
        获取黑色面的轴
        :return:
        """
        if side in "FB":
            return (pos[0], pos[1], 0)
        elif side in "UD":
            return (pos[0], 0, pos[2])
        elif side in "LR":
            return (0, pos[1], pos[2])


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

    def reft_trans_seq(self, s, o, t):
        """
        左旋顺序:
        1 正序
        1 逆序
        :return:
        """
        d = {
            "F":{
                "UR": 1,
                "RD": -1,
                "DL": 1,
                "LU": -1
            },
            "B":{
                "UL": -1,
                "LD": 1,
                "DR": -1,
                "RU": 1
            },
            "L":{
                "UF": 1,
                "FD": 1,
                "DB": -1,
                "BU": -1
            },
            "R":{
                "UB": -1,
                "BD": -1,
                "DF": 1,
                "FU": 1
            },
            "U":{
                "BR": 1,
                "RF": 1,
                "FL": 1,
                "LB": 1
            },
            "D":{
                "FR": 1,
                "RB": 1,
                "BL": 1,
                "LF": 1
            }
        }
        return d[s][o+t]

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

    def get_next_side(self, s, side):
        index = self._s[s]["side"].index(side)
        if index == len(self._s[s]["side"]) - 1:
            return self._s[s]["side"][0]
        else:
            return self._s[s]["side"][index + 1]


    def rotate_side_change_status(self, side):
        """
        旋转一个边
        :param side:
        :return:
        """
        logger.info("rotate change side: %s" %(side,))
        sides = self._s[side]["side"]

        di = {

        }

        # 自我变换
        self.rotate_self_side(side)
        for s in sides:
            index = self._s[s]["side"].index(side)
            coordinate = self.get_coordinate_by_index(index)
            values = self.get_value_by_coordinate(s, coordinate)
            trans_side = self.get_next_side(side, s)
            trans_side_index = self._s[trans_side]["side"].index(side)
            trans_side_coordinate = self.get_coordinate_by_index(trans_side_index)
            isrev = self.reft_trans_seq(side, s, trans_side)
            if isrev == -1:
                trans_side_coordinate = trans_side_coordinate[::-1]

            di[trans_side] = (trans_side_coordinate, values)
        for k,v in di.iteritems():
            self.set_value_by_coordinate(k, v[0], v[1])


def main():
    w = Window()

if __name__ == "__main__":
    main()