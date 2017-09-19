from __future__ import division

from scripts.Logger import Logger
from scripts.gamecomponents.Mallet import Mallet


class TooManyPointsException(Exception):
    """Raised when player has more points than he can according to rules."""
    pass


class Player:
    """
    Class for representing player
    """

    PLAYER_RED = 1
    PLAYER_BLUE = 2

    # TODO: Decide value of max points in sth like game rules, probably implemented in another class
    MAX_POINTS = 10  # temp

    def __init__(self, player_id, pitch, football ):
        """
        initializes Player object and creates underlying Mallet
        :param player_id: defines which player are you creating
        :param pitch: pitch is needed to calculate borders for mallet
        :return:
        """
        if football == False:
            if player_id == Player.PLAYER_RED:
                Logger.info("PLAYER: initializing PLAYER_RED")
                self.playerColor = Player.PLAYER_RED
                self._borders = ((pitch.i_min, (pitch.i_min + pitch.i_max) / 2), (pitch.j_min, pitch.j_max))
                self._center = (200, 355)
                self._goal_to_score = pitch.get_right_goal()  # opponent's goal
                print("hokej")
            else:
                Logger.info("PLAYER: initializing PLAYER_BLUE")
                self.playerColor = Player.PLAYER_BLUE
                self._borders = (((pitch.i_min + pitch.i_max) / 2, pitch.i_max), (pitch.j_min, pitch.j_max))
                self._center = (600, 355)
                self._goal_to_score = pitch.get_left_goal()

            self._points = 0
            self._name = ''
            self._player_id = player_id

            self._mallet = Mallet(20.5, self._center[0], self._center[1], 100, self, self._borders)
        if football == True:
            if player_id == Player.PLAYER_RED:
                Logger.info("PLAYER: initializing PLAYER_RED")
                self.playerColor = Player.PLAYER_RED
                self._borders = ((pitch.i_min, (pitch.i_min + pitch.i_max)), (pitch.j_min, pitch.j_max))
                self._center = (200, 355)
                self._goal_to_score = pitch.get_right_goal()  # opponent's goal
                print("football")
            else:
                Logger.info("PLAYER: initializing PLAYER_BLUE")
                self.playerColor = Player.PLAYER_BLUE
                self._borders = ((pitch.i_min, pitch.i_max), (pitch.j_min, pitch.j_max))
                self._center = (600, 355)
                self._goal_to_score = pitch.get_left_goal()

            self._points = 0
            self._name = ''
            self._player_id = player_id

            self._mallet = Mallet(20.5, self._center[0], self._center[1], 100, self, self._borders)


    @property
    def name(self):
        """
        Give Player's name
        :return: string - name
        """
        return self._name

    @property
    def player_id(self):
        """
        Give Player's ID
        :return:
        """
        return self._player_id

    @property
    def points(self):
        """
        Give Player's points
        :return: integer - points
        """
        return self._points

    @property
    def mallet(self):
        """
        Give Mallet object assigned to player
        :return: Mallet object
        """
        return self._mallet

    @property
    def goal_to_score(self):
        """
        Give goal of other player (opponent)
        :return: Goal object
        """
        return self._goal_to_score

    @name.setter
    def name(self, name):
        self._name = name

    def clearPoints(self):
        """When new round or set begins, player should have 0 points"""
        self._points = 0

    def addPoint(self):
        """Should be called when player scores a goal."""
        Logger.info("PLAYER: player %s scored a point", str(self.playerColor))
        self._points += 1
        if self._points >= self.MAX_POINTS:
            raise TooManyPointsException

    def printTooManyPointsInfo(self):
        print("Player " + self.name + " has won scoring " + str(self.MAX_POINTS) + " points.")




