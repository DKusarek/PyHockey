import pygame

from scripts.gamecomponents.DrawableInterface import Drawable
from scripts.gamecomponents.Kinematics import *


class Disc(PhysicsObject, Drawable):
    PICTURE_PATH = "resources/graphics/disc.png"

    def __init__(self, init_x, init_y, mass, radius, borders):
        """
        Initialize Disc object
        :param init_x: int/float - x position of Disc
        :param init_y: int/float - y position of Disc
        :param mass: mass of Disc
        :param radius: radius of Disc
        :param borders: pitch's borders - list [(pitch x_min, pitch x_max), (pitch y_min, pitch y_max)]
        :return:
        """
        PhysicsObject.__init__(self, init_x, init_y, mass, radius, borders)
        self._init_x = init_x
        self._init_y = init_y
        image = self.load_image(radius)
        Drawable.__init__(self, image, None, Vector(init_x, init_y))

    @property
    def image(self):
        """
        returns image of Disc
        """
        return self._image

    @property
    def pos(self):
        """
        return position of Disc
        :return: Vector
        """
        return self._pos

    @property
    def vel(self):
        """
        return velocity of Disc
        :return: Vector
        """
        return self._vel

    @property
    def radius(self):
        """
        return radius of Disc
        :return: integer/float
        """
        return self._radius

    @property
    def init_x(self):
        """
        Initial x coord
        :return:integer/float
        """
        return self._init_x

    @property
    def init_y(self):
        """
        Initial y coord
        :return:integer/float
        """
        return self._init_y

    def move_to(self, x, y):
        """
        Move Disc to (x, y) position
        :param x: int/float
        :param y: int/float
        :return: None
        """
        Logger.debug('DISC: radius accessed, returned %s', str(self._radius))
        self._pos.state = (x, y)

    def move(self, x_move, y_move):
        """
        Move Disc by (x_move, y_move)
        (x, y) = (x_0 + x_move, y_0 + y_move)
        :param x_move: int/float
        :param y_move: int/float
        :return: None
        """
        Logger.debug('DISC: move (%s, %s), position before = %s', str(x_move), str(y_move), str(self._pos))
        self._pos.change_state((x_move, y_move))
        Logger.debug('DISC: move (%s, %s), position after = %s', str(x_move), str(y_move), str(self._pos))

    def accelerate(self, v_x_diff, v_y_diff):
        """
        Change Disc's velocity by (v_x_diff, v_y_diff)
        :param v_x_diff: int/float
        :param v_y_diff: int/float
        :return: None
        """
        Logger.debug('DISC: accelerate (%s, %s), velocity before = %s', str(v_x_diff), str(v_y_diff), str(self._vel))
        self._vel.change_state((v_x_diff, v_y_diff))
        Logger.debug('DISC: accelerate (%s, %s), velocity after = %s', str(v_x_diff), str(v_y_diff), str(self._vel))

    def load_image(self, radius):
        Logger.debug('DISC: loading image (radius=%s), PICTURE_PATH = %s', str(radius), str(Disc.PICTURE_PATH))
        return pygame.transform.scale(pygame.image.load(Disc.PICTURE_PATH), (int(2 * radius), int(2 * radius)))

    @vel.setter
    def vel(self, vel):
        """
        Set velocity of Disc to vel
        :param vel: Vector
        :return: None
        """
        self._vel.state = vel

    def printStatus(self):
        print("Position: " + self._pos.x + ", " + self._pos.y)
        print("Velocity: " + self._vel.x + ", " + self._vel.y)
        print("Velocity value: " + self._vel.length)
