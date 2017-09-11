import abc


class AbstractMarkerTracker(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_markers_positions(self, frame):
        pass
