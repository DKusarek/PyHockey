from scripts.controls.AbstractGameControls import AbstractGameControls


class CameraGameControls(AbstractGameControls):
    def __init__(self, videoCapture, markerTracker):
        self._videoCapture = videoCapture
        self._markerTracker = markerTracker

    def get_players_positions(self):
        frame = self._videoCapture.get_frame()
        return self._markerTracker.get_markers_positions(frame)
