from __future__ import division

import cv2

from scripts.videocapture.AbstractVideoCapture import AbstractVideoCapture


class VideoCapture(AbstractVideoCapture):
    def __init__(self):
        self.VIDEO_SIZE = (400, 300)
        self.cap = cv2.VideoCapture(0)  # 0 for camera
        self.failedFramesLimit = 10

    def get_frame(self):
        failedFrames = 0
        while True:
            ret, frame = self.cap.read()
            if ret == True:
                break

            failedFrames = failedFrames + 1
            if failedFrames > self.failedFramesLimit:
                raise Exception("VideoCapture cannot receive stable video stream. Possible reason is camera driver issue.")

        frame = cv2.resize(cv2.flip(frame, 1), self.VIDEO_SIZE)  # vertical flip+ resize
        return frame
