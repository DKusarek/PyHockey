from __future__ import division

import math
import operator


# TODO: Provide unittests
class Vector(object):
    __slots__ = ['x', 'y']

    def __init__(self, x_or_pair, y=None):
        if y is None:
            self.x = x_or_pair[0]
            self.y = x_or_pair[1]
        else:
            self.x = x_or_pair
            self.y = y

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("Invalid subscript " + str(key) + " to Vector")

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("Invalid subscript " + str(key) + " to Vector")

    # String representation (for debugging)
    def __repr__(self):
        return 'Vector(%s, %s)' % (self.x, self.y)

    # Comparison
    def __eq__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        else:
            return False

    def __ne__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x != other[0] or self.y != other[1]
        else:
            return True

    def __nonzero__(self):
        return bool(self.x or self.y)

    # Generic operator handlers
    def _o2(self, other, f):
        "Any two-operator operation where the left operand is a Vector"
        if isinstance(other, Vector):
            return Vector(f(self.x, other.x),
                          f(self.y, other.y))
        elif hasattr(other, "__getitem__"):
            return Vector(f(self.x, other[0]),
                          f(self.y, other[1]))
        else:
            return Vector(f(self.x, other),
                          f(self.y, other))

    def _r_o2(self, other, f):
        "Any two-operator operation where the right operand is a Vector"
        if hasattr(other, "__getitem__"):
            return Vector(f(other[0], self.x),
                          f(other[1], self.y))
        else:
            return Vector(f(other, self.x),
                          f(other, self.y))

    def _io(self, other, f):
        "inplace operator"
        if hasattr(other, "__getitem__"):
            self.x = f(self.x, other[0])
            self.y = f(self.y, other[1])
        else:
            self.x = f(self.x, other)
            self.y = f(self.y, other)
        return self

    # Addition
    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        elif hasattr(other, "__getitem__"):
            return Vector(self.x + other[0], self.y + other[1])
        else:
            return Vector(self.x + other, self.y + other)

    __radd__ = __add__

    def __iadd__(self, other):
        if isinstance(other, Vector):
            self.x += other.x
            self.y += other.y
        elif hasattr(other, "__getitem__"):
            self.x += other[0]
            self.y += other[1]
        else:
            self.x += other
            self.y += other
        return self

    # Subtraction
    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        elif hasattr(other, "__getitem__"):
            return Vector(self.x - other[0], self.y - other[1])
        else:
            return Vector(self.x - other, self.y - other)

    def __rsub__(self, other):
        if isinstance(other, Vector):
            return Vector(other.x - self.x, other.y - self.y)
        if hasattr(other, "__getitem__"):
            return Vector(other[0] - self.x, other[1] - self.y)
        else:
            return Vector(other - self.x, other - self.y)

    def __isub__(self, other):
        if isinstance(other, Vector):
            self.x -= other.x
            self.y -= other.y
        elif hasattr(other, "__getitem__"):
            self.x -= other[0]
            self.y -= other[1]
        else:
            self.x -= other
            self.y -= other
        return self

    # Multiplication
    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y)
        if hasattr(other, "__getitem__"):
            return Vector(self.x * other[0], self.y * other[1])
        else:
            return Vector(self.x * other, self.y * other)

    __rmul__ = __mul__

    def __imul__(self, other):
        if isinstance(other, Vector):
            self.x *= other.x
            self.y *= other.y
        elif hasattr(other, "__getitem__"):
            self.x *= other[0]
            self.y *= other[1]
        else:
            self.x *= other
            self.y *= other
        return self

    # Division
    def __div__(self, other):
        return self._o2(other, operator.div)

    def __rdiv__(self, other):
        return self._r_o2(other, operator.div)

    def __idiv__(self, other):
        return self._io(other, operator.div)

    def __truediv__(self, other):
        return self._o2(other, operator.truediv)

    def __rtruediv__(self, other):
        return self._r_o2(other, operator.truediv)

    def __itruediv__(self, other):
        return self._io(other, operator.floordiv)

    # Unary operations
    def __neg__(self):
        return Vector(operator.neg(self.x), operator.neg(self.y))

    def __pos__(self):
        return Vector(operator.pos(self.x), operator.pos(self.y))

    # vector functions
    @property
    def length_sqrd(self):
        return self.x ** 2 + self.y ** 2

    @property
    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    @length.setter
    def length(self, value):
        length = self.length
        if length:
            self.x *= value / length
            self.y *= value / length
        else:
            self.x = self.y = 0

    def rotated(self, radians):
        # radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x * cos - self.y * sin
        y = self.x * sin + self.y * cos
        return Vector(x, y)

    def rotate(self, radians):
        rotated_vec = self.rotated(radians)
        self.x = rotated_vec.x
        self.y = rotated_vec.y

    @property
    def angle(self):
        if self.length_sqrd == 0:
            return 0
        return math.degrees(math.atan2(self.y, self.x))

    @angle.setter
    def angle(self, angle_degrees):
        self.x = self.length
        self.y = 0
        self.rotate(angle_degrees)

    def get_angle_between(self, other):
        return math.degrees(math.atan2(self.cross(other), self.dot(other)))

    def normalized(self):
        length = self.length
        if length != 0:
            return self / length
        return Vector(self)

    def perpendicular(self):
        return Vector(-self.y, self.x)

    def dot(self, other):
        return float(self.x * other[0] + self.y * other[1])

    def get_distance(self, other):
        return math.sqrt((self.x - other[0]) ** 2 + (self.y - other[1]) ** 2)

    def projection(self, other):
        return other * (self.dot(other) / other.length_sqrd) if other.length_sqrd else 0

    def cross(self, other):
        return self.x * other[1] - self.y * other[0]

    @property
    def state(self):
        return self.x, self.y

    @state.setter
    def state(self, tup):
        self.x, self.y = tup

    def change_state(self, tup):
        self.x += tup[0]
        self.y += tup[1]
