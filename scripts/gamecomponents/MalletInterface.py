from abc import abstractmethod, abstractproperty

from scripts.gamecomponents.DrawableInterface import Drawable


class MalletInterface(Drawable):
    def __init__(self):
        self._player = None

    @abstractproperty
    def pos(self):
        pass

    @abstractproperty
    def image(self):
        pass

    @abstractproperty
    def radius(self):
        pass

    @abstractproperty
    def vel(self):
        pass

    @abstractproperty
    def direction(self):
        pass

    @abstractmethod
    def move_to(self, x, y):
        pass

    @abstractmethod
    def move_by(self, x, y):
        pass

    @abstractmethod
    def load_image(self):
        pass
