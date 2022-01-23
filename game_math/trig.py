# module for common math functions
import math
from dataclasses import dataclass, field
from math import sqrt, hypot, atan2, degrees


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
        return hypot(self.x, self.y, self.z)

    @magnitude.setter
    def magnitude(self, magnitude):
        self.convert_to_unit()
        self.x *= magnitude
        self.y *= magnitude
        self.z *= magnitude

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
            return self.y / self.magnitude
        else:
            ax = atan2(sqrt((self.y ** 2) + (self.z ** 2)), self.x)
            ay = atan2(sqrt((self.z ** 2) + (self.x ** 2)), self.y)
            az = atan2(sqrt((self.x ** 2) + (self.y ** 2)), self.z)
            return ax, ay, az

    def angle_in_degrees(self):
        return math.degrees(self.angle) if self.z == 0 else tuple((math.degrees(rad) for rad in self.angle))

    def convert_to_unit(self):
        m = self.magnitude
        self.x /= m
        self.y /= m
        self.z /= m
        return self

    def __add__(self, other):
        x = other.x + self.x
        y = other.y + self.y
        z = other.z + self.z
        return self.__create__(x, y, z)

    def __repr__(self):
        return f'{self.__class__.__name__}(x={self.x}, y={self.y}, z={self.z})'

    def __str__(self):
        out = f'{self.__class__.__name__} ' \
              f'{2 if self.z == 0 else 3}D ' \
              f'{str("Unit") if self.magnitude == 1 else str("")}'\
              '\n\r'\
              f'  -> x = {self.x}'\
              '\n\r'\
              f'  -> y = {self.y}'
        if self.z > 0:
            out += '\n\r'\
                   f'  -> z = {self.z}'
        angle = self.angle_in_degrees()

        out += '\n\r  -> angle {}'.format(angle)\
            if isinstance(angle, float) or isinstance(angle, int) \
            else '\n\r' f'  -> angle x:{angle[0]},y:{angle[1]},z:{angle[2]}'

        out += '\n\r'f'  -> magnitude {self.magnitude}'
        out += '\n\r'
        return out

    @classmethod
    def __create__(cls, x, y, z):
        return cls(x, y, z)


if __name__ == "__main__":
    v1 = Vector(10., 15)
    print("v1\n\r", v1.__repr__(), "\n\r", v1)

    v2 = Vector(10., 20)
    print("v2\n\r", v2.__repr__(), "\n\r", v2)

    v3 = Vector(10., -70., 30)
    print("v3\n\r", v3.__repr__(), "\n\r", v3)

    print("Adding Vectors v1, v2, v3 \n\r")
    v4 = (v1 + v2 + v3)
    print("v4\n\r", v4.__repr__(), "\n\r", v4)

    print(f"Converting v4 into Unit Vector \n\r")
    v5 = v4.convert_to_unit()
    print("v5\n\r", v5.__repr__(), "\n\r", v5)

    print("Increasing v5's magnitude to a factor of 10\n\r")
    v5.magnitude = 10
    print("v5 * 10\n\r", v5.__repr__(), "\n\r", v5)
