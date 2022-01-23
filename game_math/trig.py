# module for common math functions
import logging
from dataclasses import dataclass, field
import math

math_logger = logging.Logger(__name__)

@dataclass(eq=True, slots=True, init=True)
class Vector:
    _x: float = field(default=0.)
    _y: float = field(default=0.)
    _z: float = field(default=0.)

    @property
    def vec(self):
        return self.x, self.y, self.z

    @vec.setter
    def vec(self, vec):
        self.x, self.y, self.z = vec

    @vec.setter
    def vec(self, x=0., y=0., z=0):
        self.x = x
        self.y = y
        self.z = z

    @property
    def magnitude(self):
        return math.hypot(self.x, self.y, self.z)

    @magnitude.setter
    def magnitude(self, magnitude):
        self.convert_to_unit()
        self.vec = tuple((v * magnitude for v in self.vec))

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, z):
        self._z = z

    @property
    def angle(self):
        if self.z == 0:
            return self.y/self.magnitude
        else:
            return self.y/self.magnitude, self.z/self.magnitude

    def convert_to_unit(self):
        m = self.magnitude
        return self.__create__(*(v/m for v in self.vec))

    def __add__(self, other):
        x = other.x + self.x
        y = other.y + self.y
        z = other.z + self.z
        return self.__create__(x, y, z)

    def __repr__(self):
        return f'{self.__class__.__name__}(x={self.x}, y={self.y}, z={self.z})'

    def __str__(self):
        out = f'{self.__class__.__name__}{2 if self.z == 0 else 3}D''\n\r'f'-> x = {self.x}''\n\r'f'-> y = {self.y}'
        if self.z > 0:
            out += '\n\r'f'-> z = {self.z}'

        out += '\n\r'f'-> angle {self.angle}'
        out += '\n\r'f'-> magnitude {self.magnitude}'
        out += '\n\r'
        return out

    @classmethod
    def __create__(cls, x, y, z):
        return cls(x, y, z)


v1 = Vector(10., 15., 20)
v2 = Vector(10., 20.)
v3 = Vector(10. -70.)
v = (v1+v2+v3).convert_to_unit()

print(v1)
print(v2)
print(v3)
print(v)

