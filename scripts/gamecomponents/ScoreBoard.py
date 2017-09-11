from __future__ import division

from datetime import datetime

import pygame as pg

from scripts.gamecomponents.DrawableInterface import Drawable
from scripts.gamecomponents.Player import Player
from scripts.gamecomponents.Text import Text


class GameTime:
    # TODO: Decide value of max time in sth like game rules, probably implemented in another class
    MAX_TIME = 1  # [minutes]

    startTime = datetime.now()

    def __init__(self):
        pass

    @staticmethod
    def startMeasuring():
        """This method should be called at start of game so that it starts measuring time"""
        GameTime.startTime = datetime.now()

    @staticmethod
    def getCurrentGameTime():
        game_time = (datetime.now() - GameTime.startTime).total_seconds()
        minutes = int(game_time) // 60
        seconds = int(game_time) % 60
        if minutes >= GameTime.MAX_TIME:
            raise OutOfGameTimeException
        return minutes, seconds


class OutOfGameTimeException(Exception):
    """Raised when time of game is over."""
    pass


class ScoreBoard(Drawable):
    """Represents the board on which scores and time are displayed."""

    def __init__(self, player1, player2):
        Drawable.__init__(self, None, None, None)
        self._player1 = player1
        self._player2 = player2

    @property
    def player1(self):
        return self._player1

    @property
    def player2(self):
        return self._player2

    def displayScore(self, screen):
        if self._player1.points == Player.MAX_POINTS:
            scores = [Text(color=pg.Color("red"), position=(25, 25), text="Player 1 won. Game over!", size=50)]
        elif self._player2.points == Player.MAX_POINTS:
            scores = [Text(color=pg.Color("blue"), position=(25, 25), text="Player 2 won. Game over!", size=50)]
        else:
            scores = [Text(color=pg.Color("red"), position=(25, 25), text=str(self._player1.points), size=50),
                      Text(color=pg.Color("blue"), position=(750, 25), text=str(self._player2.points), size=50)]
        for s in scores:
            s.draw(screen)

    # TODO: graphic version
    def displayTime(self, screen):
        """Text version displaying game time"""
        h, m = GameTime.getCurrentGameTime()
        text = Text(color=pg.Color("black"), position=(362, 100), text=str(h).zfill(2) + ":" + str(m).zfill(2), size=25)
        text.draw(screen)

    def displayTimeExceptionally(self, screen):
        text = [
            Text(color=pg.Color("black"), position=(362, 100), text=str(GameTime.MAX_TIME).zfill(2) + ":00", size=25),
            Text(color=pg.Color("black"), position=(280, 75), text="Game time is over!", size=25)]
        for t in text:
            t.draw(screen)

    def draw(self, screen):
        try:
            self.displayTime(screen)
        except OutOfGameTimeException:
            self.displayTimeExceptionally(screen)
        self.displayScore(screen)
