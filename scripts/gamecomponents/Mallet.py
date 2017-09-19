import pygame

from scripts.Logger import Logger
from scripts.gamecomponents.DrawableInterface import Drawable
from scripts.gamecomponents.Kinematics import PhysicsObject
from scripts.gamecomponents.MalletInterface import MalletInterface


class Mallet(MalletInterface, PhysicsObject, Drawable):
    def __init__(self, radius, pos_x, pos_y, mass, player, borders):
        """
        Initialize Mallet object
        :param radius: int/float radius of Mallet
        :param pos_x: int/float - x position of Mallet
        :param pos_y: int/float - x position of Mallet
        :param mass: mass of Mallet
        :param player: Player - Mallet owner
        :param borders: list of tuples - borders in which mallet can move
        :return:
        """

        MalletInterface.__init__(self)
        PhysicsObject.__init__(self, pos_x, pos_y, mass, radius, borders)
        self._player = player
        # old line of load image self.load_image()

    @property
    def image(self):
        return self._image

    @property
    def direction(self):
        return self._direction

    @property
    def radius(self):
        return self._radius

    @property
    def pos(self):
        return self._pos

    @property
    def vel(self):
        return self._vel

    @vel.setter
    def vel(self, v):
        self._vel = v

    @direction.setter
    def direction(self, d):
        self.vel.angle = d

    def move_to(self, x, y):
        from scripts.gamecomponents.Kinematics import Vector
        Logger.debug("MALLET: move_to(%s,%s) pos before =%s", str(x), str(y), str(self._pos))
        move_vector = Vector(x, y) - self._pos
        if move_vector.length > PhysicsObject.MAX_MALLET_VELOCITY:
            move_vector.length = PhysicsObject.MAX_MALLET_VELOCITY
        self.pos.state = (self._pos.x + move_vector.x, self._pos.y + move_vector.y)
        Logger.debug("MALLET: move_to(%s,%s) pos after =%s", str(x), str(y), str(self._pos))

        self.correct_position_in_borders()
        Logger.debug("MALLET: move_to(%s,%s) pos after position correction=%s", str(x), str(y), str(self._pos))

    def load_image(self, image1, image2):
        """
        Method used to load sprite for Mallet according to Player.
        :return: None
        """
        from Player import Player
        if self._player.playerColor == Player.PLAYER_BLUE:
            Logger.debug("MALLET: load_image playerColor = PLAYER_BLUE")
            image = image1
        elif self._player.playerColor == Player.PLAYER_RED:
            Logger.debug("MALLET: load_image playerColor = PLAYER_RED")
            image = image2
        else:
            Logger.error("MALLET: Invalid value for player (" + self._player.playerColor + ")")
            raise ValueError('Invalid value for player (' + self._player.playerColor + ')')
        self._image = pygame.transform.scale(pygame.image.load(image), (int(2 * self.radius), int(2 * self.radius)))

    def print_properties(self):
        print self.velocity
        print self.direction
        print self.pos
        print self.radius
