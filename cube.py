# -*- coding: utf-8 -*-

import logging


import OpenGL.GL as oglgl

import color

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


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

    def inverse(self, x):
        if x == 0:
            return x
        return -x


    def len_side_and_dire(self, pos):
        change = (1,1,1)
        #if self.__dire == Cube.PLANE_FRONT:
        #    change = (1,1,1)
        #elif self.__dire == Cube.PLANE_BEHIND:
        #    change = (1,-1,-1)
        #elif self.__dire == Cube.PLANE_TOP:
        #    change = (1,1,-1)
        #elif self.__dire == Cube.PLANE_BOTTOM:
        #    change = (1,-1,1)
        #elif self.__dire == Cube.PLANE_LEFT:
        #    change = (-1,1,1)
        #elif self.__dire == Cube.PLANE_RIGHT:
        #    change = (1,1,1)

        return (self.__hs * pos[0] * change[0], self.__hs * pos[1] * change[1], self.__hs * pos[2] * change[2])

    def multipl_len_side(self, points):
        return tuple(self.len_side_and_dire(point) for point in points)

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

    def get_pos(self):
        return self.__x, self.__y, self.__z

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_z(self):
        return self.__z

    def get_real_x(self):
        return self.get_real_pos()[0]

    def get_real_y(self):
        return self.get_real_pos()[1]

    def get_real_z(self):
        return self.get_real_pos()[2]

    def get_real_pos(self):
        """
        获得真实坐标
        :return:
        """
        pos = self.__x, self.__y, self.__z

        if self.__x_rotate_angle == 90:
            pos = (pos[0], self.inverse(pos[2]), pos[1])
        elif self.__x_rotate_angle == 180:
            pos = (pos[0], self.inverse(pos[1]), self.inverse(pos[2]))
        elif self.__x_rotate_angle == 270:
            pos = (pos[0], pos[2], self.inverse(pos[1]))

        if self.__y_rotate_angle == 90:
            pos = (pos[2], pos[1], self.inverse(pos[0]))
        elif self.__y_rotate_angle == 180:
            pos = (self.inverse(pos[0]), pos[1], self.inverse(pos[2]))
        elif self.__y_rotate_angle == 270:
            pos = (self.inverse(pos[2]), pos[1], pos[0])


        if self.__z_rotate_angle == 90:
            pos = (pos[1], self.inverse(pos[0]), pos[2])

        elif self.__z_rotate_angle == 180:
            pos = (self.inverse(pos[0]), self.inverse(pos[1]), pos[2])
        elif self.__z_rotate_angle == 270:
            pos = (self.inverse(pos[1]), pos[0], pos[2])

        return pos


    def is_plane(self, plane):
        if plane == "A":
            return self.is_A()
        if plane == "B":
            return self.is_B()
        if plane == "C":
            return self.is_C()
        if plane == "D":
            return self.is_D()
        if plane == "E":
            return self.is_E()
        if plane == "F":
            return self.is_F()
        if plane == "G":
            return self.is_G()
        if plane == "H":
            return self.is_H()
        if plane == "I":
            return self.is_I()

    def is_A(self):
        return self.get_real_x() == -1
    def is_B(self):
        return self.get_real_x() == 0
    def is_C(self):
        return self.get_real_x() == 1

    def is_D(self):
        return self.get_real_y() == 1
    def is_E(self):
        return self.get_real_y() == 0
    def is_F(self):
        return self.get_real_y() == -1

    def is_G(self):
        return self.get_real_z() == 1
    def is_I(self):
        return self.get_real_z() == 0
    def is_H(self):
        return self.get_real_z() == -1

    def __str__(self):
        return  str((self.__name, self.__x, self.__y, self.__z, self.__x_rotate_angle, self.__y_rotate_angle, self.__z_rotate_angle))

    def __init__(self, name, x, y, z, x_rotate_angle, y_rotate_angle, z_rotate_angle):
        self.__name = name
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

        # 边长
        self.__hs = Cube.LEN_OF_HALF_SIDE

        # 自转角度
        self.__dire = Cube.PLANE_FRONT

    def re_trans(self):
        """
        平等转换
        :return:
        """
        if self.__x_rotate_angle >= 360:
            self.__x_rotate_angle = self.__x_rotate_angle - 360
        elif self.__x_rotate_angle < 0:
            self.__x_rotate_angle = self.__x_rotate_angle + 360


        if self.__y_rotate_angle >= 360:
            self.__y_rotate_angle = self.__y_rotate_angle - 360
        elif self.__y_rotate_angle < 0:
            self.__y_rotate_angle = self.__y_rotate_angle + 360


        if self.__z_rotate_angle >= 360:
            self.__z_rotate_angle = self.__z_rotate_angle - 360
        elif  self.__z_rotate_angle < 0:
            self.__z_rotate_angle = self.__z_rotate_angle + 360


        if self.__x_rotate_angle == 90:
            return (self.__x, self.__y, self.inverse(self.__z))
        elif self.__x_rotate_angle == 180:
            return (self.__x, self.inverse(self.__y), self.inverse(self.__z))
        elif self.__x_rotate_angle == 270:
            return (self.__x, self.inverse(self.__y), self.__z)

        if self.__y_rotate_angle == 90:
            return (self.inverse(self.__x), self.__y, self.__z)
        elif self.__y_rotate_angle == 180:
            return (self.inverse(self.__x), self.__y, self.inverse(self.__z))
        elif self.__y_rotate_angle == 270:
            return (self.__x, self.inverse(self.__y), self.inverse(self.__z))


        if self.__z_rotate_angle == 90:
            return (self.inverse(self.__x), self.__y, self.__z)
        elif self.__z_rotate_angle == 180:
            return (self.inverse(self.__x), self.inverse(self.__y), self.__z)
        elif self.__z_rotate_angle == 270:
            return (self.__x, self.inverse(self.__y), self.inverse(self.__z))

        return (self.__x, self.__y, self.__z)

    def can_rotate(self, r):
        """
        是否可以下旋转
        :return:
        """
        if r == "x":
            if self.__y_rotate_angle  in (0, 90, 180, 270) and self.__z_rotate_angle  in (0, 90, 180, 270):
                return True
        elif r == "y":
            if self.__x_rotate_angle  in (0, 90, 180, 270) and self.__z_rotate_angle  in (0, 90, 180, 270):
                return True
        elif r == "z":
            if self.__x_rotate_angle  in (0, 90, 180, 270) and self.__y_rotate_angle  in (0, 90, 180, 270):
                return True
        return False


    def rotatex_axis(self, x):
        self.__x_rotate_angle = self.__x_rotate_angle + x
        self.re_trans()

    def rotatey_axis(self, y):
        self.__y_rotate_angle = self.__y_rotate_angle + y
        self.re_trans()

    def rotatez_axis(self, z):
        self.__z_rotate_angle = self.__z_rotate_angle + z
        self.re_trans()


    def revolution(self):
        """
        绕中心轴公转
        :return:
        """
        oglgl.glTranslatef(self.inverse(self.__x), self.inverse(self.__y), self.inverse(self.__z))
        oglgl.glRotatef(self.__x_rotate_angle, 1, 0, 0)
        oglgl.glRotatef(self.__y_rotate_angle, 0, 1, 0)
        oglgl.glRotatef(self.__z_rotate_angle, 0, 0, 1)

        oglgl.glTranslatef(self.__x, self.__y, self.__z)

    def draw_plane(self, color, a, b, c, d):
        oglgl.glColor3f(*color)
        oglgl.glVertex3f(*a)
        oglgl.glVertex3f(*b)
        oglgl.glVertex3f(*c)
        oglgl.glVertex3f(*d)

    def draw_cube(self):
        self.draw_plane(color.WHITE, *self.get_plane_front())
        self.draw_plane(color.RED, *self.get_plane_behind())
        self.draw_plane(color.GREEN, *self.get_plane_top())
        self.draw_plane(color.BLUE, *self.get_plane_bottom())
        self.draw_plane(color.YELLOW, *self.get_plane_left())
        self.draw_plane(color.ORANGE, *self.get_plane_right())

    def draw(self):
        oglgl.glPushMatrix()
        oglgl.glTranslatef(self.__x, self.__y, self.__z)

        self.revolution()

        oglgl.glBegin(oglgl.GL_QUADS)
        self.draw_cube()
        oglgl.glEnd()
        oglgl.glPopMatrix()