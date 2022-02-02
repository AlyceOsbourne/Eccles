import math


#########################################################################
# Math Functions
#########################################################################


#########################################################################
# Math Objects
#########################################################################
from typing import Iterable


class Vector:

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def get(self):
        return self.x, self.y, self.z

    @property
    def __len__(self):
        """ :return"""
        return math.sqrt(sum((v ** 2 for v in self.get())))

    @__len__.setter
    def __len__(self, magnitude):
        """
        :param magnitude: magnitude to scale vector too
        :param normalize: whether or not to convert to unit before scale
        """
        if 0 > self.__len__ > 1:
            self.normalize()
        self.x *= magnitude
        self.y *= magnitude
        self.z *= magnitude

    def __add__(self, other):
        if isinstance(other, Vector):
            self.x += other if isinstance(other, int) or isinstance(other, float) \
                else other[0] if isinstance(other, Iterable) \
                else other.x

            self.y += other if isinstance(other, int) or isinstance(other, float) \
                else other[1] if isinstance(other, Iterable) \
                else other.y

            self.x += other if isinstance(other, int) or isinstance(other, float) \
                else other[2] if isinstance(other, Iterable) \
                else other.y

    def __mul__(self, other):

        self.x *= other if isinstance(other, int) or isinstance(other, float) \
            else other[0] if isinstance(other, Iterable) \
            else other.x

        self.y *= other if isinstance(other, int) or isinstance(other, float) \
            else other[1] if isinstance(other, Iterable) \
            else other.y

        self.x *= other if isinstance(other, int) or isinstance(other, float) \
            else other[2] if isinstance(other, Iterable) \
            else other.y

    def __str__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y}, z={self.z})[magnitude={self.__len__}, angle={self.angle_degrees}]"

    @property
    def angle_radians(self):
        ax = math.atan2(math.sqrt(self.y ** 2 + self.z ** 2), self.x)
        ay = math.atan2(math.sqrt(self.z ** 2 + self.x ** 2), self.y)
        az = math.atan2(math.sqrt(self.x ** 2 + self.y ** 2), self.z)
        return ax, ay, az

    @property
    def angle_degrees(self):
        return tuple(math.degrees(n) for n in self.angle_radians)

    @classmethod
    def as_unit(cls, vector):
        vec_mag = vector.magnitude
        x = vector.x / vec_mag
        y = vector.y / vec_mag
        z = vector.z / vec_mag
        return cls(x, y, z)

    @classmethod
    def from_degrees(cls, ax, ay, mag):
        return cls.from_radians(math.radians(ax), math.radians(ay), mag)

    @classmethod
    def from_radians(cls, ax, ay, magnitude):
        x = (math.sin(ax) * math.cos(ay))
        y = math.cos(ax) * magnitude
        z = (math.sin(ax) * math.sin(ay))
        return x, y, z

    def normalize(self):
        # using a while because sometimes this method yields 0.999... or 1.000...1. a second run fixes this,
        # this is important because the normalized vector us often scaled and while the difference is small
        # this change has an effect equal to the 0.000...1 to the scale, which overall becomes harder to fix
        while self.__len__ != 1:
            mag = self.__len__
            self.x /= mag
            self.y /= mag
            self.z /= mag

    def dot_product(self):
        pass


class Matrix:
    pass


class Geometry:
    pass


class Tri(Geometry):
    pass


class Quad(Geometry):
    pass
