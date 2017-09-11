import abc


class AbstractVideoCapture(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_frame(self):
        pass