# module for common math functions
from abc import abstractmethod
from collections import namedtuple
from dataclasses import dataclass, field

import math
from functools import cached_property, cache
from math import atan2


class __V:
    @abstractmethod
    def magnitude(self):
        pass

    @abstractmethod
    def angle(self, other):
        pass

    @abstractmethod
    def convert_to_unit(self):
        pass

    @abstractmethod
    def __add__(self, other):
        pass


class __P:
    @abstractmethod
    def __add__(self, other):
        pass


@dataclass(eq=True, slots=True, init=True)
class Point2(__P):
    x: int = field(default=0)
    y: int = field(default=0)

    @property
    def pos(self):
        return self.x, self.y

    @pos.setter
    def pos(self, pos):
        self.x, self.y = pos

    def __add__(self, other):
        self.x += other.x
        self.y += other.y


@dataclass(eq=True, slots=True, init=True)
class Point3(__P):
    x: int = field(default=0)
    y: int = field(default=0)
    z: int = field(default=0)

    @property
    def pos(self):
        return self.x, self.y, self.z

    @pos.setter
    def pos(self, pos):
        self.x, self.y, self.z = pos

    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z


@dataclass(slots=True, eq=True, init=True)
class Vector2(__V):
    x: int or float
    y: int or float

    @property
    def vec(self):
        return self.x, self.y

    @vec.setter
    def vec(self, vec):
        self.x, self.y = vec

    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def convert_to_unit(self):
        mag = self.magnitude
        self.x /= mag
        self.y /= mag

    @cached_property
    def magnitude(self):
        return math.sqrt((self.x * self.x) + (self.y * self.y))

    def angle(self, other):
        return atan2(other.y - self.y, other.x - self.x) * (180 / math.pi)


@dataclass(slots=True, eq=True, init=True)
class Vector3(__V):
    x: int or float = field(default=0.)
    y: int or float = field(default=0.)
    z: int or float = field(default=0.)

    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    @cached_property
    def magnitude(self):
        return math.sqrt((self.x * self.x) + (self.y * self.y) + (self.z * self.z))

    @property
    def vec(self):
        return self.x, self.y, self.z

    @vec.setter
    def vec(self, vec):
        self.x, self.y, self.z = vec

    def angle(self, other):
        a = self.magnitude
        b = other.magnitude
        ab = a + b
        as2 = math.sqrt(a)
        bs2 = math.sqrt(b)
        return math.acos(ab / (as2 * bs2))

    def convert_to_unit(self):
        self.x /= self.magnitude
        self.y /= self.magnitude
        self.z /= self.magnitude


vec_a = Vector3(-5, 5, 2)
vec_b = Vector3(10, 10, 5)

print(vec_a + vec_b)
print(vec_a.angle(vec_b))