from scripts.Logger import Logger


class Drawable:
    def __init__(self, image, imagerect, position):
        """
        :param image: shape or image to be drawn
        :param position: position on screen (of type Point)
        :param imagerect: rectangle of image to be displayed
        """
        Logger.debug("DRAWABLE: init(position=(%s)", str(position))
        self._image = image
        self._pos = position

    def draw(self, screen):
        """
        Override if in need

        :param screen: pygame screen instance
        """
        # http://stackoverflow.com/questions/8873219/what-is-a-good-way-to-draw-images-using-pygame
        # if object has radius - set origin to object's center
        if hasattr(self, 'radius'):
            pos = self._pos.state[0] - self.radius, self._pos.state[1] - self.radius
            screen.blit(self._image, pos)
        else:
            screen.blit(self._image, self._pos.state)
