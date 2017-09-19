from __future__ import division

import os

import pygame as pg
from pygame.locals import *

from Logger import Logger
from scripts.controls.CameraGameControls import CameraGameControls
from scripts.controls.KeyboardGameControls import KeyboardGameControls
from scripts.gamecomponents.Disc import Disc
from scripts.gamecomponents.Pitch import Pitch
from scripts.gamecomponents.Player import Player
from scripts.gamecomponents.Player import TooManyPointsException
from scripts.gamecomponents.ScoreBoard import GameTime
from scripts.gamecomponents.ScoreBoard import OutOfGameTimeException
from scripts.gamecomponents.ScoreBoard import ScoreBoard
from scripts.tracking.NaiveMarkerTracker import NaiveMarkerTracker
from scripts.videocapture.VideoCapture import VideoCapture
from scripts.gamecomponents.Kinematics import PhysicsObject


class Game(object):
    DISC_RADIUS = 16.5
    INIT_DISC1_X = 402
    INIT_DISC1_Y = 310
    INIT_DISC2_X = 402
    INIT_DISC2_Y = 400

    def __init__(self, size):
        Logger.info("GAME INIT: Initializing PyGame...")
        pg.init()

        Logger.info("GAME INIT: Initializing Game Control Options Display")
        self.screensize = (850, 300)
        self.screen = pg.display.set_mode(self.screensize)
        pg.display.set_caption("PyHockey")
        self.screen.fill((0, 0, 0))
        myfont = pg.font.Font(None, 25)
        label = myfont.render(
            "Press ENTER to play game with keyboard, or press V to use video control", 1, (255, 255, 0)
        )
        self.screen.blit(label, (100, 100))
        pg.display.flip()
        self.gamecontrol = 0
        while self.gamecontrol == 0:
            for event in pg.event.get():
                if event.type == KEYDOWN and event.key == K_RETURN:
                    self.gamecontrol = 1
                if event.type == KEYDOWN and event.key == K_v:
                    self.gamecontrol = 2
                if event.type == QUIT:
                    exit()

        # choose kind of Pitch
        self.screensize = (850, 300)
        self.screen = pg.display.set_mode(self.screensize)
        pg.display.set_caption("PyHockey")
        self.screen.fill((0, 0, 0))
        myfont = pg.font.Font(None, 25)
        label = myfont.render(
            "Press 1 to play hockey, press 2 to play football", 1, (255, 255, 0)
        )

        self.screen.blit(label, (100, 100))
        pg.display.flip()
        stop = 0
        while stop == 0:
            for event in pg.event.get():
                if event.type == KEYDOWN and event.key == K_1:
                    Logger.debug("Pitch: load_image Hockey Pitch")
                    self.pitch = Pitch("resources/graphics/pitch.png")


                    pitch_borders = [(self.pitch.i_min, self.pitch.i_max), (self.pitch.j_min, self.pitch.j_max)]
                    self.players = [Player(Player.PLAYER_RED, self.pitch, False),
                                    Player(Player.PLAYER_BLUE, self.pitch, False)]
                    self.mallets = [self.players[0].mallet, self.players[1].mallet]
                    self.players[0].mallet.load_image("resources/graphics/redmallet.png", "resources/graphics/bluemallet.png")
                    self.players[1].mallet.load_image("resources/graphics/redmallet.png", "resources/graphics/bluemallet.png")
                    self.discs = [Disc(Game.INIT_DISC1_X, Game.INIT_DISC1_Y, 1, Game.DISC_RADIUS, pitch_borders),
                                  Disc(Game.INIT_DISC2_X, Game.INIT_DISC2_Y, 1, Game.DISC_RADIUS, pitch_borders)]


                    self.objects = self.discs + self.mallets
                    self.scoreboard = ScoreBoard(self.players[0], self.players[1])
                    stop = 1
                if event.type == KEYDOWN and event.key == K_2:
                    Logger.debug("Pitch: load_image Football Pitch")
                    self.pitch = Pitch("resources/graphics/football_board.png")
                    self.players = [Player(Player.PLAYER_RED, self.pitch,True),
                                    Player(Player.PLAYER_BLUE, self.pitch,True)]

                    pitch_borders = [(self.pitch.i_min, self.pitch.i_max), (self.pitch.j_min, self.pitch.j_max)]
                    self.mallets = [self.players[0].mallet, self.players[1].mallet]
                    self.players[0].mallet.load_image("resources/graphics/messi_face.png", "resources/graphics/ronaldo_face.png")

                    self.players[1].mallet.load_image("resources/graphics/messi_face.png", "resources/graphics/ronaldo_face.png")

                    Disc.PICTURE_PATH = "resources/graphics/ball.png"
                    disc_initX = 402
                    disc_initY = 355
                    self.discs = [Disc(disc_initX, disc_initY, 1, Game.DISC_RADIUS, pitch_borders)]
                    self.objects = self.discs + self.mallets
                    self.scoreboard = ScoreBoard(self.players[0], self.players[1])
                    PhysicsObject.COEFFICIENT_OF_FRICTION = 0.93

                    stop = 1
                if event.type == QUIT:
                    exit()






        Logger.info("GAME INIT: Initializing  Game Display (%s)", str(size))
        os.environ["SDL_VIDEO_CENTERED"] = "True"
        self.screensize = (int(size[0]), int(size[1]))
        self.screen = pg.display.set_mode(self.screensize)
        self.screen_rect = self.screen.get_rect()
        Logger.info("GAME INIT: Initializing clock and fps rate...")

        self.clock = pg.time.Clock()
        self.fps = 60
        self.keys = pg.key.get_pressed()
        self.done = False
        self.playing = True

        Logger.info("GAME INIT: Initializing Model...")
        # model part
        # here was an old place of Pitch definition


        Logger.info("GAME INIT: Initializing Drawables...")
        # everything that will be drawn
        self.drawables = [self.pitch]
        self.drawables.extend(self.mallets)
        self.drawables.extend(self.discs)
        self.drawables.append(self.scoreboard)

        Logger.info("GAME INIT: Initializing Video Capture...")
        self.video = VideoCapture()
        self.markerTracker = NaiveMarkerTracker()

        Logger.info("GAME INIT: Initializing Game Controls...")
        if self.gamecontrol == 1:
            self.controls = KeyboardGameControls(self.players[0], self.players[1])
        if self.gamecontrol == 2:
            self.controls = CameraGameControls(self.video, self.markerTracker)

        Logger.info("GAME INIT: Starting game loop...")
        GameTime.startMeasuring()
        self.loop()
        Logger.info("GAME INIT: Game loop ended")
        Logger.info("GAME INIT: Exiting")

    def loop(self):
        background = (255, 255, 255)
        Logger.info("GAME LOOP: In Game Loop")
        while not self.done:
            self.clock.tick(self.fps)
            for event in pg.event.get():
                if event.type == QUIT:
                    Logger.info("Quit event registered")
                    self.done = True

            if not self.playing:
                continue

            try:
                GameTime.getCurrentGameTime()
            except OutOfGameTimeException:
                # self.done = True
                self.playing = False

            pos = self.controls.get_players_positions()

            # calculate velocities, it should not be here
            self.players[0].mallet.vel.state, self.players[1].mallet.vel.state = (pos[0][0] - self.players[
                0].mallet.pos.x, pos[0][1] - self.players[0].mallet.pos.y), (pos[1][0] - self.players[1].mallet.pos.x,
                                                                             pos[1][1] - self.players[1].mallet.pos.y)

            self.players[0].mallet.move_to(pos[0][0], pos[0][1])
            self.players[1].mallet.move_to(pos[1][0], pos[1][1])

            # reset screen
            self.screen.fill(background)

            # check if the goal was scored
            for pl in self.players:
                for d in self.discs:
                    if pl.goal_to_score.in_goal(d.pos.x, d.pos.y, Game.DISC_RADIUS):
                        try:
                            pl.addPoint()
                            d.move_to(d.init_x, d.init_y)
                            d.vel.x = d.vel.y = 0.
                        except TooManyPointsException:
                            self.playing = False

            for o in self.objects:
                o.friction()
                axis = self.pitch.is_border_collision(o)
                if axis:
                    o.border_collision(axis)

            # Detect and react on collisions between discs
            for i in range(len(self.objects) - 1):
                for j in range(i, len(self.objects)):
                    self.objects[i].circle_collision(self.objects[j])

            for disc in self.discs:
                disc.move(disc.vel.x, disc.vel.y)

            # draw everything
            for drawable in self.drawables:
                drawable.draw(self.screen)

            # update display
            pg.display.flip()
