from __future__ import absolute_import

import math
import unittest

from scripts.gamecomponents.Vector import Vector
from scripts.gamecomponents.tests import DummyDisc


class TestDisc(unittest.TestCase):
    expected_points = (((100, 100), (11, 20), (111, 120)),
                       ((100, 100), (11, -20), (111, 80)),
                       ((101, 99), (10, 21), (111, 120)),
                       ((95, 103), (-25, -15), (70, 88)))

    expected_points_to = (((100, 100), (111, 120), (111, 120)),
                          ((100, 100), (111, 80), (111, 80)),
                          ((100, 90), (111, 120), (111, 120)),
                          ((70, 130), (70, 88), (70, 88)))

    expected_velocity_value = (((0, 0), 0),
                               ((1, -1), math.sqrt(2)),
                               ((1, 2), math.sqrt(5)),
                               ((100, 80), math.sqrt(16400)))

    # we don't need to check whether disc is on pitch. It's a task of border_colision
    def test_move_to(self):
        for tup in self.expected_points_to:
            t_disc = DummyDisc(tup[0][0], tup[0][1], 1, 26, [(0, 800), (0, 600)])
            t_disc.move_to(tup[1][0], tup[1][1])
            result = t_disc.pos.x, t_disc.pos.y
            self.assertEqual(tup[2], result)

    def test_move(self):
        for tup in self.expected_points:
            t_disc = DummyDisc(tup[0][0], tup[0][1], 1, 26, [(0, 800), (0, 600)])
            t_disc.move(tup[1][0], tup[1][1])
            result = t_disc.pos.x, t_disc.pos.y
            self.assertEqual(tup[2], result)

    def test_velocity_set(self):
        for tup in self.expected_points_to:
            t_disc = DummyDisc(100, 100, 1, 26, [(0, 800), (0, 600)])
            t_disc.vel = Vector(tup[0][0], tup[0][1])
            t_disc.vel = Vector(tup[1][0], tup[1][1])
            result = t_disc.vel.x, t_disc.vel.y
            self.assertEqual(tup[2], result)

    def test_accelerate(self):
        for tup in self.expected_points:
            t_disc = DummyDisc(100, 100, 1, 26, [(0, 800), (0, 600)])
            t_disc.vel = Vector(tup[0][0], tup[0][1])
            t_disc.accelerate(tup[1][0], tup[1][1])
            result = t_disc.vel.x, t_disc.vel.y
            self.assertEqual(tup[2], result)


if __name__ == '__main__':
    unittest.main()
