from __future__ import division

import cv2

from scripts.videocapture.AbstractVideoCapture import AbstractVideoCapture


class VideoCapture(AbstractVideoCapture):
    def __init__(self):
        self.VIDEO_SIZE = (400, 300)
        self.cap = cv2.VideoCapture(0)  # 0 for camera
        self.failedFramesLimit = 10

    def get_frame(self):
        failed_frames = 0
        while True:
            ret, frame = self.cap.read()
            if ret == true:
                break

            failed_frames = failed_frames + 1
            if failed_frames > self.failedFramesLimit:
                raise Exception(
                    "VideoCapture cannot receive stable video stream. Possible reason is camera driver issue."
                )

        frame = cv2.resize(cv2.flip(frame, 1), self.VIDEO_SIZE)  # vertical flip+ resize
        return frame
