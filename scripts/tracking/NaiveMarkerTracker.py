import cv2

from scripts.tracking.AbstractMarkerTracker import AbstractMarkerTracker


class NaiveMarkerTracker(AbstractMarkerTracker):
    def get_markers_positions(self, frame):
        p1 = self.__get_the_most_red_position(frame)
        p2 = self.__get_the_most_blue_position(frame)

        cv2.circle(frame, (int(p1[0]), int(p1[1])), 10, (0, 0, 255), 2)
        cv2.circle(frame, (int(p2[0]), int(p2[1])), 10, (255, 0, 0), 2)
        cv2.imshow('Frame preview', frame)
        cv2.waitKey(1) & 0xFF

        # transform to game coordinates
        p1 = (p1[0] * 2, p1[1] * 2)
        p2 = (p2[0] * 2, p2[1] * 2)

        return p1, p2

    def __get_the_most_blue_position(self, frame):
        # OpenCV uses BGR not RGB !!!
        redFrame = cv2.extractChannel(frame, 2)
        greenFrame = cv2.extractChannel(frame, 1)
        blueFrame = cv2.extractChannel(frame, 0)

        redGreenComponents = cv2.addWeighted(redFrame, 0.5, greenFrame, 0.5, 0)
        uniformBlueFrame = cv2.subtract(blueFrame, redGreenComponents)

        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(uniformBlueFrame)

        return maxLoc

    def __get_the_most_red_position(self, frame):
        # OpenCV uses BGR not RGB !!!
        redFrame = cv2.extractChannel(frame, 2)
        greenFrame = cv2.extractChannel(frame, 1)
        blueFrame = cv2.extractChannel(frame, 0)

        blueGreenComponents = cv2.addWeighted(blueFrame, 0.5, greenFrame, 0.5, 0)
        uniformRedFrame = cv2.subtract(redFrame, blueGreenComponents)

        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(uniformRedFrame)

        return maxLoc
