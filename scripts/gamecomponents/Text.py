import pygame

from scripts.gamecomponents.DrawableInterface import Drawable


class Text(Drawable):
    def __init__(self, size=15, fontname="monospace",
                 text="", color=pygame.Color("black"), position=(0, 0)):
        Drawable.__init__(self, None, None, position)
        self._size = size
        self._fontname = fontname
        self._text = text
        self._color = color
        self._position = position

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, f):
        self._font = f

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, s):
        self._size = s

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, t):
        self._text = t

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, c):
        self._color = c

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, p):
        self._position = p

    def draw(self, screen):
        self._font = pygame.font.SysFont(self._fontname, self._size)
        self._image = self._font.render(self._text, 1, self._color)
        screen.blit(self._image, (self._position[0], self._position[1]))
