from __future__ import division

import cv2
import numpy as np

from scripts.tracking.AbstractMarkerTracker import AbstractMarkerTracker


class MarkerTracker(AbstractMarkerTracker):
    def __init__(self):
        self.hsv = None
        self.player_red = []
        self.player_blue = []
        self.VIDEO_SIZE = (400, 300)
        self.GAME_SIZE = (800, 600)
        self.data = {'player_red': self.player_red, 'player_blue': self.player_blue}
        self.p1 = (0, 0)
        self.p2 = (0, 0)
        self.blue_x, self.blue_y = 0, 0
        self.red_x, self.red_y = 0, 0
        self.player_blue.append(np.array([90, 80, 80], dtype=np.uint8))  # low hsv limit
        self.player_blue.append(np.array([110, 255, 255], dtype=np.uint8))  # up hsv limit
        self.player_red.append(np.array([0,50,50], dtype=np.uint8))  # low hsv limit
        self.player_red.append(np.array([10,255,255], dtype=np.uint8))  # up hsv limit
        self.player_red.append(np.array([170,50,50], dtype=np.uint8))  # low hsv limit
        self.player_red.append(np.array([180,255,255], dtype=np.uint8))  # up hsv limit

    def get_markers_positions(self, frame):
        for player, limit in self.data.iteritems():
            cv2.imshow('frame', frame)
            cv2.waitKey(33) & 0xFF
            if player == 'player_blue':
                halfframe = frame[:, self.VIDEO_SIZE[0] // 2:]
                halfframe = cv2.blur(halfframe, (3, 3))
                self.hsv = cv2.cvtColor(halfframe, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(self.hsv, limit[0], limit[1])
            else:
                halfframe = frame[:, :self.VIDEO_SIZE[0] // 2]
                halfframe = cv2.blur(halfframe, (3, 3))
                self.hsv = cv2.cvtColor(halfframe, cv2.COLOR_BGR2HSV)
                mask0 = cv2.inRange(self.hsv, limit[0], limit[1])
                mask1 = cv2.inRange(self.hsv, limit[2], limit[3])
                mask = mask0+mask1
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
            mask = cv2.medianBlur(mask, 5)
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            maximum_area = 0
            best_contour = None
            for contour in contours:
                current_area = cv2.contourArea(contour)
                if current_area > maximum_area:
                    best_contour = contour
                    maximum_area = current_area

            if bestContour is not None:
                M = cv2.moments(best_contour)
                x, y = int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])
                if player == 'player_blue':
                    self.p2 = (int(x * self.GAME_SIZE[0] / self.VIDEO_SIZE[0] + self.GAME_SIZE[0] / 2),
                               int(y * self.GAME_SIZE[1] / self.VIDEO_SIZE[1]))
                    x += self.VIDEO_SIZE[0] // 2
                    self.blue_x, self.blue_y = x, y
                else:
                    self.p1 = (
                    int(x * self.GAME_SIZE[0] / self.VIDEO_SIZE[0]), int(y * self.GAME_SIZE[1] / self.VIDEO_SIZE[1]))
                    self.red_x, self.red_y = x, y
            cv2.circle(frame, (int(self.red_x), int(self.red_y)), 10, (0, 0, 255), 2)
            cv2.circle(frame, (int(self.blue_x), int(self.blue_y)), 10, (255, 0, 0), 2)
        return self.p1, self.p2
