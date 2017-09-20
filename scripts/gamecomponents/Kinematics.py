from __future__ import division

from scripts.Logger import Logger
from scripts.gamecomponents.Vector import Vector
import math


class PhysicsObject(object):
    COEFFICIENT_OF_FRICTION = 0.98
    COEFFICIENT_OF_BORDER_COLLISION = 0.8
    MAX_MALLET_VELOCITY = 15
    MAX_DISC_VELOCITY = 80
    STOPPING_VELOCITY = 0.1

    def __init__(self, x_init, y_init, mass, radius, borders):
        Logger.debug("KINEMATICS: PhysicsObject init(x_init=%s, y_init=%s, mass=%s, radius=%s, borders=%s)",
                     str(x_init), str(y_init), str(mass), str(radius), str(borders))
        self._pos = Vector(x_init, y_init)
        self._mass = mass
        self._radius = radius
        self._vel = Vector(0, 0)
        self._borders = borders

    # TODO: Add unittests
    def friction(self):
        Logger.debug("KINEMATICS: friction vel before = %s", str(self._vel))
        self._vel.length *= self.COEFFICIENT_OF_FRICTION
        self._vel.length = 0 if self._vel.length < self.STOPPING_VELOCITY else self._vel.length
        Logger.debug("KINEMATICS: friction vel after = %s", str(self._vel))

    def collision_effect(self):
        # TODO: a proper calculation of momentum and change in speed after collisions
        Logger.debug("KINEMATICS: collision_effect vel before = %s", str(self._vel))
        self._vel.length *= self.COEFFICIENT_OF_BORDER_COLLISION
        Logger.debug("KINEMATICS: collision_effect vel after = %s", str(self._vel))

    def correct_position_in_borders(self):
        """ Dislodges objects stuck in the pitch borders """
        x_min, x_max = self._borders[0]
        y_min, y_max = self._borders[1]
        log = False
        if self.pos.x - self.radius < x_min:
            self.pos.x = x_min + self.radius
            log = True
        if self.pos.x + self.radius > x_max:
            self.pos.x = x_max - self.radius
            log = True
        if self.pos.y - self.radius < y_min:
            self.pos.y = y_min + self.radius
            log = True
        if self.pos.y + self.radius > y_max:
            self.pos.y = y_max - self.radius
            log = True
        if log:
            Logger.debug("KINEMATICS: correct_position_in_borders pos.x=%s pos.y=%s", str(self.pos.x), str(self.pos.y))

    def correct_position_post_collision(self, obj):
        """ Dislodges objects stuck in each other. """
        distance_vector = self.pos - obj.pos
        if distance_vector.length < self.radius + obj.radius:
            distance_vector.length = self.radius + obj.radius
            self._pos = obj.pos + distance_vector
            self.correct_position_in_borders()
            Logger.debug("KINEMATICS: correct_position_post_collision distance_vector=%s self.radius=%s obj.radius=%s",
                         str(distance_vector), str(self.radius), str(obj.radius))
        distance_vector = obj.pos - self.pos

        if distance_vector.length < obj.pos - self.pos:
            distance_vector.length = self.radius + obj.radius
            obj._pos = self._pos + distance_vector
            obj.correct_position_in_borders()
        Logger.debug("KINEMATICS: correct_position_post_collision distance_vector=%s self.radius=%s obj.radius=%s",
                     str(distance_vector), str(self.radius), str(obj.radius))

    # TODO: Add common move_to and move methods for mallet and disc

    def apply_speed_limit(self):
        from scripts.gamecomponents.Disc import Disc
        from scripts.gamecomponents.Mallet import Mallet
        Logger.debug("KINEMATICS: apply_speed_limit MAX_DISC_VELOCITY=%s MAX_MALLET_VELOCITY=%s vel=%s",
                     str(self.MAX_DISC_VELOCITY), str(self.MAX_MALLET_VELOCITY), str(self._vel.length))
        if isinstance(self, Disc) and self._vel.length > self.MAX_DISC_VELOCITY:
            Logger.debug("KINEMATICS: apply_speed_limit is a Disc")
            self._vel.length = self.MAX_DISC_VELOCITY
        if isinstance(self, Mallet) and self._vel.length > self.MAX_MALLET_VELOCITY:
            Logger.debug("KINEMATICS: apply_speed_limit is a Mallet")
            self._vel.length = self.MAX_MALLET_VELOCITY

    # TODO: Add unittests
    def border_collision(self, axis):
        from scripts.gamecomponents.Disc import Disc
        COEFICIENT_OF_BOUNCE = 0.95
        Logger.debug("KINEMATICS: border_collision axis=%s _vel=%s", str(axis), str(self._vel))
        if isinstance(self, Disc):
            if axis == 'x':
                self._vel.x = -self._vel.x * COEFICIENT_OF_BOUNCE
                self.collision_effect()
                self.correct_position_in_borders()
            if axis == 'y':
                self._vel.y = -self._vel.y * COEFICIENT_OF_BOUNCE
                self.collision_effect()
                self.correct_position_in_borders()
        Logger.debug("KINEMATICS: _vel=%s", str(self._vel))

    # TODO: Add unittests
    def circle_collision(self, object):
        from scripts.gamecomponents.Disc import Disc
        if self._pos.get_distance(object.pos) <= self._radius + object.radius:  # impact
            Logger.debug("KINEMATICS: border_collision distance=%s self.radius=%s object.radius=%s",
                         str(self._pos.get_distance(object.pos)), str(self._radius), str(object.radius))
            vec_pos_diff = object.pos - self._pos
            vec_to = self._vel.projection(vec_pos_diff)
            obj_vec_to = object._vel.projection(vec_pos_diff)

            vec_side = self._vel - vec_to
            obj_vec_side = object._vel - obj_vec_to

            after_vec_to = (vec_to * (self._mass - object._mass) + (2 * object._mass * obj_vec_to)) / (
                self._mass + object._mass)
            after_obj_vec_to = (obj_vec_to * (object._mass - self._mass) + (2 * self._mass * vec_to)) / (
                self._mass + object._mass)

            dx = self._pos[0] - object._pos[0]
            dy = self._pos[1] - object._pos[1]
            distance = math.hypot(dx,dy)
            tangent = math.atan2(dy,dx)
            # self._radius = 2*tangent - self._radius
            # object._radius = 2*tangent - object._radius
            (self._vel, object._vel) = (object._vel, self._vel)
            angle = 0.5 * math.pi + tangent

            # Change velocity only if it is Disc
            if isinstance(self, Disc):
                self._vel = after_vec_to + vec_side
            if isinstance(object, Disc):
                object._vel = after_obj_vec_to + obj_vec_side

            self.apply_speed_limit()
            self.correct_position_post_collision(object)
            self._pos[0] += math.sin(angle)
            self._pos[1] -= math.cos(angle)
            object._pos[0] -= math.sin(angle)
            object._pos[1] += math.cos(angle)