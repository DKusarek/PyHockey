import random
import unittest

from mock import Mock

from scripts.gamecomponents.Kinematics import PhysicsObject
from scripts.gamecomponents.Vector import Vector


class TestPhysicsObject(unittest.TestCase):
    MAX_RANDOM_VELOCITY = 25
    MIN_RANDOM_POSITION = 0
    MAX_RANDOM_POSITION = 100
    MIN_RANDOM_RADIUS = 5
    MAX_RANDOM_RADIUS = 5

    def test_friction(self):
        po = PhysicsObject(50, 50, 1, 50, [(25, 75), (25, 75)])
        for i in range(0, 1000):
            po._vel = Vector(random.randint(0, self.MAX_RANDOM_VELOCITY), random.randint(0, self.MAX_RANDOM_VELOCITY))
            expected_velocity = po._vel * PhysicsObject.COEFFICIENT_OF_FRICTION \
                if po._vel > PhysicsObject.STOPPING_VELOCITY else 0
            po.friction()
            self.assertTrue(abs(po._vel.x - expected_velocity.x) < 0.1 and abs(po._vel.y - expected_velocity.y) < 0.1)

    def test_collision_effect(self):
        po = PhysicsObject(50, 50, 1, 50, [(25, 75), (25, 75)])
        for i in range(0, 1000):
            po._vel = Vector(random.randint(0, self.MAX_RANDOM_VELOCITY), random.randint(0, self.MAX_RANDOM_VELOCITY))
            expected_velocity = po._vel * PhysicsObject.COEFFICIENT_OF_BORDER_COLLISION
            po.collision_effect()
            self.assertTrue(abs(po._vel.x - expected_velocity.x) < 0.1 and abs(po._vel.y - expected_velocity.y) < 0.1)

    def test_correct_position_in_border(self):
        for i in range(0, 1000):
            from scripts.gamecomponents.Disc import Disc
            Disc.load_image = Mock()
            po = Disc(random.randint(self.MIN_RANDOM_POSITION, self.MAX_RANDOM_POSITION),
                      random.randint(self.MIN_RANDOM_POSITION, self.MAX_RANDOM_POSITION), 1,
                      random.randint(self.MIN_RANDOM_RADIUS, self.MAX_RANDOM_RADIUS),
                      [(25, 50), (25, 50)])
            xmin, xmax = po._borders[0]
            ymin, ymax = po._borders[1]
            po.correct_position_in_borders()
            self.assertTrue(po._pos.x - po._radius >= xmin
                            and po._pos.x + po._radius <= xmax
                            and po._pos.y - po._radius >= ymin
                            and po._pos.y + po._radius <= ymax)

    def test_correct_position_post_collision(self):
        from scripts.gamecomponents.Mallet import Mallet
        from scripts.gamecomponents.Disc import Disc

        mock = Mock()
        mock.playerColor = 1
        Mallet.load_image = Mock()
        Disc.load_image = Mock()

        m = Mallet(10, 35, 35, 1, mock, [(0, 100), (0, 100)])
        d = Disc(37, 37, 1, 10, [(0, 100), (0, 100)])

        m.correct_position_post_collision(d)
        distance_vector = m.pos - d.pos
        self.assertTrue(distance_vector.length >= m.radius + d.radius)

        m = Mallet(10, 35, 35, 1, mock, [(0, 100), (0, 100)])
        d = Disc(37, 37, 1, 10, [(0, 100), (0, 100)])

        d.correct_position_post_collision(m)
        distance_vector = m.pos - d.pos
        self.assertTrue(distance_vector.length >= m.radius + d.radius)

    # TODO
    def test_apply_speed_limit(self):
        pass

    # TODO
    def test_border_collision(self):
        pass

    # TODO
    def test_circle_collision(self):
        pass


if __name__ == '__main__':
    unittest.main()
