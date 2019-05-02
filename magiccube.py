# -*- coding: utf-8 -*-

import logging

from cube import Cube

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

class MagicCube(object):
    # 旋转
    STATUS_ROTATE = 0
    # 静止
    STATUS_STOP = 1

    def __init__(self):
        # 初始化每一个方块和其位置
        self_a1 = Cube("a1", -1.0, 1.0, 1.0, 0.0, 0.0, 0.0)
        self_b1 = Cube("b1", 0.0, 1.0, 1.0, 0.0, 0.0, 0.0)
        self_c1 = Cube("c1", 1.0, 1.0, 1.0, 0.0, 0.0, 0.0)

        self_d1 = Cube("d1", -1.0, 1.0, 0.0, 0.0, 0.0, 0.0)
        self_e1 = Cube("e1", 0.0, 1.0, 0.0, 0.0, 0.0, 0.0)
        self_f1 = Cube("f1", 1.0, 1.0, 0.0, 0.0, 0.0, 0.0)

        self_g1 = Cube("g1", -1.0, 1.0, -1.0, 0.0, 0.0, 0.0)
        self_h1 = Cube("h1", 0.0, 1.0, -1.0, 0.0, 0.0, 0.0)
        self_i1 = Cube("i1", 1.0, 1.0, -1.0, 0.0, 0.0, 0.0)

        self_a2 = Cube("a2", -1.0, 0.0, 1.0, 0.0, 0.0, 0.0)
        self_b2 = Cube("b2", 0.0, 0.0, 1.0, 0.0, 0.0, 0.0)
        self_c2 = Cube("c2", 1.0, 0.0, 1.0, 0.0, 0.0, 0.0)

        self_d2 = Cube("d2", -1.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        self_e2 = Cube("e2", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        self_f2 = Cube("f2", 1.0, 0.0, 0.0, 0.0, 0.0, 0.0)

        self_g2 = Cube("g2", -1.0, 0.0, -1.0, 0.0, 0.0, 0.0)
        self_h2 = Cube("h2", 0.0, 0.0, -1.0, 0.0, 0.0, 0.0)
        self_i2 = Cube("i2", 1.0, 0.0, -1.0, 0.0, 0.0, 0.0)

        self_a3 = Cube("a3", -1.0, -1.0, 1.0, 0.0, 0.0, 0.0)
        self_b3 = Cube("b3", 0.0, -1.0, 1.0, 0.0, 0.0, 0.0)
        self_c3 = Cube("c3", 1.0, -1.0, 1.0, 0.0, 0.0, 0.0)

        self_d3 = Cube("d3", -1.0, -1.0, 0.0, 0.0, 0.0, 0.0)
        self_e3 = Cube("e3", 0.0, -1.0, 0.0, 0.0, 0.0, 0.0)
        self_f3 = Cube("f3", 1.0, -1.0, 0.0, 0.0, 0.0, 0.0)

        self_g3 = Cube("g3", -1.0, -1.0, -1.0, 0.0, 0.0, 0.0)
        self_h3 = Cube("h3", 0.0, -1.0, -1.0, 0.0, 0.0, 0.0)
        self_i3 = Cube("i3", 1.0, -1.0, -1.0, 0.0, 0.0, 0.0)

        # self._A = [self_a1, self_d1, self_g1, self_a2, self_d2, self_g2, self_a3, self_d3, self_g3]
        # self._B = [self_b1, self_e1, self_h1, self_b2, self_e2, self_h2, self_b3, self_e3, self_h3]
        # self._C = [self_c1, self_f1, self_i1, self_c2, self_f2, self_i2, self_c3, self_f3, self_i3]
        #
        # self._D = []
        # self._E = []
        # self._F = []
        #
        # self._G = []
        # self._H = []
        # self._I = []


        self._cubes = [
            self_a1,
            self_b1,
            self_c1,
            self_d1,
            self_e1,
            self_f1,
            self_g1,
            self_h1,
            self_i1,
            self_a2,
            self_b2,
            self_c2,
            self_d2,
            self_e2,
            self_f2,
            self_g2,
            self_h2,
            self_i2,
            self_a3,
            self_b3,
            self_c3,
            self_d3,
            self_e3,
            self_f3,
            self_g3,
            self_h3,
            self_i3
        ]

    def all_cube_can_trans(self, cubes, r):
        for cube in cubes:
            if not cube.can_rotate(r):
                logging.warning(cube)
                return False
        return True

    def totate(self, plane, clock):
        """
        旋转
        :param plane: 平面
        :param axis: 轴
        :param clock: 顺,逆时 0 : 顺, 1 : 逆时针
        :return:
        """
        cubes =  self.get_plane(plane)

        if plane in ("A", "B", "C"):
            if not self.all_cube_can_trans(cubes, "x"):
                logger.warning("cant rotate x")
                return
        elif plane in ("D", "E", "F"):
            if not self.all_cube_can_trans(cubes, "y"):
                logger.warning("cant rotate y")
                return
        elif plane in ("G", "H", "I"):
            if not self.all_cube_can_trans(cubes, "z"):
                logger.warning("cant rotate z")
                return

        for cube in cubes:
            if plane in ("A", "B", "C"):
                if clock == 1:
                    cube.rotatex_axis(-10)
                else:
                    cube.rotatex_axis(10)
            elif plane in ("D", "E", "F"):
                if clock == 1:
                    cube.rotatey_axis(-10)
                else:
                    cube.rotatey_axis(10)
            elif plane in ("G", "H", "I"):
                if clock == 1:
                    cube.rotatez_axis(-10)
                else:
                    cube.rotatez_axis(10)

            logger.info(cube)

    def get_plane(self, p):
        return tuple(cube for cube in self._cubes if cube.is_plane(p))

    def draw(self):
        for cube in self._cubes:
            cube.draw()