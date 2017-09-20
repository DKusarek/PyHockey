import pygame

from scripts.gamecomponents.DrawableInterface import Drawable
from scripts.gamecomponents.Goal import Goal
from scripts.gamecomponents.Disc import Disc
from scripts.gamecomponents.Mallet import Mallet
from scripts.gamecomponents.Kinematics import Vector
from scripts.Logger import Logger


class WrongTypeException(Exception):
    """
    raised when the parameter is wrong type
    """
    pass


class OutOfRangeException(Exception):
    """
    raised when the disk is out of the pitch
    """
    pass


class Pitch(Drawable):
    """
    class represent a pitch on which the game will take a place
    """

    def __init__(self,pitch_name):
        """
        define constructor of class Pitch.
        """
        Logger.info("PITCH: Initializing pitch")
        self.i_min = 42
        self.i_max = 762
        self.j_min = 154
        self.j_max = 562
        self.i_border = 50

        Logger.debug("PITCH: init i_min=%s i_max=%s j_min=%s j_max=%s i_border=%s", str(self.i_min), str(self.i_max),
                     str(self.j_min), str(self.j_max), str(self.i_border))

        goal_width = 150
        j_middle = 0.5 * (self.j_min + self.j_max)
        self.goals = [Goal(self.i_min, j_middle, goal_width),
                      Goal(self.i_max, j_middle, goal_width)]

        # drawable part
        # TODO better pitch image
        Logger.info("PITCH: loading image")
        # self._image = pygame.image.load("resources/graphics/pitch.png")
        self._image = pygame.image.load(pitch_name)
        self._pos = Vector(0, 0)

    # TODO: add unittests
    def is_border_collision(self, object):
        """
        check a collision between disk and a border of the pitch
        :param object: object with x,y,radius parameters
        :return: 'x' or 'y' if the collision between a disk/mallet and the border of pitch have taken place, false - if it haven't
        :raise: WrongTypeException if object is not type of disc/mallet
        """
        # TODO: Is there a way to do it better ?

        if not isinstance(object, Disc) and not isinstance(object, Mallet):
            Logger.error("PITCH: is_border_collision raised WrongTypeException")
            raise WrongTypeException
        if object.pos.x - object.radius < self.i_min or object.pos.x + object.radius > self.i_max:
            Logger.debug("PITCH: is_border_collision return x")
            return 'x'
        if object.pos.y - object.radius < self.j_min or object.pos.y + object.radius > self.j_max:
            Logger.debug("PITCH: is_border_collision return y")
            return 'y'
        Logger.debug("PITCH: is_border_collision return False")
        return False

    def left_half(self, ii, r):
        """
        check in which half of the pitch the disk is situated
        :param ii: x coordinates of disk
        :return: true if the disk is on left player half of pitch, false if it is not
        :raise: WrongTypeException if ii or r is not type of int, OutOfRangeException if disk is out of pitch
        """
        if not type(ii) == int or not type(r) == int:
            raise WrongTypeException
        if ii + r > self.i_max or ii - r < self.i_min:
            raise OutOfRangeException
        if ii < self.i_border:
            return True
        else:
            return False

    def right_half(self, ii, r):
        """
        check on which half of the pitch the disk is situated
        :param ii: x coordinates of disk
        :return: true if the disk is on right player half of pitch, false if it is not
        :raise: WrongTypeException if ii or r is not type of int, OutOfRangeException if disk is out of pitch
        """
        if not type(ii) == int or not type(r) == int:
            raise WrongTypeException
        if ii + r > self.i_max or ii - r < self.i_min:
            raise OutOfRangeException
        if ii > self.i_border:
            return True
        else:
            return False

    def get_left_goal(self):
        return self.goals[0]

    def get_right_goal(self):
        return self.goals[1]
