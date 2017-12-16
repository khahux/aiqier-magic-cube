# -*- coding: utf-8 -*-

import pyglet
from pyglet.gl import *

import color

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

    # 边长
    LEN_OF_HALF_SIDE = 0.5

    # X 轴
    X_AXIS = (1.0, 0.0, 0.0)
    # Y 轴
    Y_AXIS = (0.0, 1.0, 0.0)
    # Z轴
    Z_AXIS = (0.0, 0.0, 1.0)

    POINT_A = (1.0, 1.0, 1.0)
    POINT_B = (1.0, 1.0, -1.0)
    POINT_C = (-1.0, 1.0, -1.0)
    POINT_D = (-1.0, 1.0, 1.0)

    POINT_E = (1.0, -1.0, 1.0)
    POINT_F = (1.0, -1.0, -1.0)
    POINT_G = (-1.0, -1.0, -1.0)
    POINT_H = (-1.0, -1.0, 1.0)

    def multipl_len_side(self, points):
        return tuple(tuple(self.__hs * p  for p in point) for point in points)

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

    def __init__(self, x, y, z, x_rotate_angle, y_rotate_angle, z_rotate_angle):
        # 坐标
        self.__x = x
        self.__y = y
        self.__z = z
        # 绕X轴旋转角度
        self.__x_rotate_angle = x_rotate_angle
        # 绕Y轴旋转角度
        self.__y_rotate_angle = y_rotate_angle
        # 绕Z轴旋转角度
        self.__z_rotate_angle = z_rotate_angle

        self.__hs = Cube.LEN_OF_HALF_SIDE
        #self.reset_rotatexyz_self()
        self.set_rotatexyz(0,1,0)

    def set_rotatexyz(self, x, y, z):
        """
        设置旋转点x, y, z
        绕某个点旋转
        :param x:
        :param y:
        :param z:
        :return:
        """
        self.__rx, self.__ry, self.__rz = x, y, z

    def reset_rotatexyz_self(self):
        """
        将旋转点设为自身中点
        :return:
        """
        self.set_rotatexyz(self.__x, self.__y, self.__z)


    def translatexyz(self,  x, y ,z):
        self.translatex(x)
        self.translatex(y)
        self.translatex(z)

    def translatex(self, x):
        self.__x = self.__x + x

    def translatey(self, y):
        self.__y = self.__y + y

    def translatez(self, z):
        self.__z = self.__z + z

    def rotatexyz_axis(self, x, y ,z):
        """
        旋转
        :return:
        """
        self.rotatex_axis(x)
        self.rotatey_axis(y)
        self.rotatez_axis(z)

    def rotatex_axis(self, x, ):
        self.__x_rotate_angle = self.__x_rotate_angle + x

    def rotatey_axis(self, y):
        self.__y_rotate_angle = self.__y_rotate_angle + y

    def rotatez_axis(self, z):
        self.__z_rotate_angle = self.__z_rotate_angle + z


    def draw_plane(self, color, a, b, c, d):
        glColor3f(*color)
        glVertex3f(*a)
        glVertex3f(*b)
        glVertex3f(*c)
        glVertex3f(*d)

    def draw_cube(self):
        self.draw_plane(color.WHITE, *self.get_plane_front())
        self.draw_plane(color.RED, *self.get_plane_behind())
        self.draw_plane(color.GREEN, *self.get_plane_top())
        self.draw_plane(color.BLUE, *self.get_plane_bottom())
        self.draw_plane(color.YELLOW, *self.get_plane_left())
        self.draw_plane(color.ORANGE, *self.get_plane_right())

    def draw(self):
        #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #模型视景矩阵操作
        glMatrixMode(GL_MODELVIEW)
        # 重置当前指定的矩阵为单位矩阵
        glLoadIdentity()
        # 平移函数设置中心坐标
        glTranslatef(self.__x, self.__y, self.__z)

        # 旋转函数(绕自己的轴)
        glRotatef(self.__x_rotate_angle, self.__rx, self.__ry, self.__rz)
        #glRotatef(self.__y_rotate_angle, *Cube.Y_AXIS)
        #glRotatef(self.__z_rotate_angle, *Cube.Z_AXIS)

        # Draw Cube (multiple quads)
        glBegin(GL_QUADS)
        self.draw_cube()

        glEnd()