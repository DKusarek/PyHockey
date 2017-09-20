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
        red_frame = cv2.extractChannel(frame, 2)
        green_frame = cv2.extractChannel(frame, 1)
        blue_frame = cv2.extractChannel(frame, 0)

        red_green_components = cv2.addWeighted(red_frame, 0.5, green_frame, 0.5, 0)
        uniform_blue_frame = cv2.subtract(blue_frame, red_green_components)

        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(uniform_blue_frame)

        return maxLoc

    def __get_the_most_red_position(self, frame):
        # OpenCV uses BGR not RGB !!!
        red_frame = cv2.extractChannel(frame, 2)
        green_frame = cv2.extractChannel(frame, 1)
        blue_frame = cv2.extractChannel(frame, 0)

        blue_green_components = cv2.addWeighted(blue_frame, 0.5, green_frame, 0.5, 0)
        uniform_red_frame = cv2.subtract(red_frame, blue_green_components)

        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(uniform_red_frame)

        return maxLoc
