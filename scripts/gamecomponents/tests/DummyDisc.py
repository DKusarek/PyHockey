__author__ = 'michal'

from scripts.gamecomponents.Kinematics import *


class DummyDisc(PhysicsObject):
    # Actually, i'm not sure what whether it is sth wrong with loading image or
    # with my settings.
    """
    Disc class - version without image.
    """

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

    def move_to(self, x, y):
        """
        Move Disc to (x, y) position
        :param x: int/float
        :param y: int/float
        :return: None
        """
        self._pos.state = (x, y)

    def move(self, x_move, y_move):
        """
        Move Disc by (x_move, y_move)
        (x, y) = (x_0 + x_move, y_0 + y_move)
        :param x_move: int/float
        :param y_move: int/float
        :return: None
        """
        self._pos.change_state((x_move, y_move))

    def accelerate(self, v_x_diff, v_y_diff):
        """
        Change Disc's velocity by (v_x_diff, v_y_diff)
        :param v_x_diff: int/float
        :param v_y_diff: int/float
        :return: None
        """
        self._vel.change_state((v_x_diff, v_y_diff))

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
