# module for common math functions
from functools import cached_property
from dataclasses import dataclass, field
from math import sqrt, hypot, atan2, degrees

@dataclass(eq=True, init=True)
class Vector:
    x: float = field(default=0.)
    y: float = field(default=0.)
    z: float = field(default=0.)

    @property
    def vec(self):
        return self.x, self.y, self.z

    @vec.setter
    def vec(self, x=0., y=0., z=0):
        self.x, self.y, self.z = x, y, z

    @property
    def magnitude(self):
        return hypot(self.x, self.y, self.z)

    @magnitude.setter
    def magnitude(self, magnitude):
        self.normalize()
        self.x *= magnitude
        self.y *= magnitude
        self.z *= magnitude

    @cached_property
    def radians(self):
        if self.z == 0:
            return self.y / self.magnitude
        else:
            ax = atan2(sqrt((self.y ** 2) + (self.z ** 2)), self.x)
            ay = atan2(sqrt((self.z ** 2) + (self.x ** 2)), self.y)
            az = atan2(sqrt((self.x ** 2) + (self.y ** 2)), self.z)
            return ax, ay, az

    @cached_property
    def degrees(self):
        return degrees(self.radians) if self.z == 0 else tuple((degrees(rad) for rad in self.radians))


    def normalize(self):
        m = self.magnitude
        self.x, self.y, self.z = tuple(a/m for a in self.vec)
        return self

    @classmethod
    def normalized(cls, x, y, z):
        return cls(x, y, z).normalize()

    def __add__(self, other):
        if isinstance(other, Vector):
            x, y, z = tuple(a+b for (a, b) in zip(self.vec, other.vec))
        elif isinstance(other, int) or isinstance(other, float):
            x, y, z = tuple(a+other for a in self.vec)
        else:
            return self

        return self.__create__(x, y, z)

    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            x, y, z = tuple(a/b if a and b else 0 for (a, b) in zip(self.vec, other.vec))
        elif isinstance(other, float) or isinstance(other, int):
            x, y, z = tuple(a/other if a and other else 0  for a in self.vec)
        else:
            return self
        return self.__create__(x, y, z)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            x, y, z = tuple(a*b if a and b else 0 for (a, b) in zip(self.vec, other.vec))
        elif isinstance(other, float) or isinstance(other, int):
            x, y, z = tuple (a*other if a and other else 0 for a in self.vec)
        else:
            return self
        return self.__create__(x, y, z)

    def __repr__(self):
        return f'{self.__class__.__name__}(x={self.x}, y={self.y}, z={self.z})'

    def __str__(self):
        out = f'{self.__class__.__name__} ' \
              f'{2 if self.z == 0 else 3}D ' \
              f'{str("Unit") if self.magnitude == 1 else str("")}' \
              '\n\r' \
              f'  -> x = {self.x}' \
              '\n\r' \
              f'  -> y = {self.y}'
        if self.z > 0:
            out += '\n\r' \
                   f'  -> z = {self.z}'
        angle = self.degrees

        out += '\n\r  -> angle {}'.format(angle) \
            if isinstance(angle, float) or isinstance(angle, int) \
            else '\n\r' f'  -> angle x:{angle[0]},y:{angle[1]},z:{angle[2]}'

        out += '\n\r'f'  -> magnitude {self.magnitude}'
        out += '\n\r'
        return out

    @classmethod
    def __create__(cls, x=0, y=0, z=0):
        return cls(x, y, z)


if __name__ == "__main__":
    vector_1 = Vector(100, 100, 100)
    vector_2 = Vector(50, 50, 50)
    vector_3 = vector_1+vector_2
    vector_4 = vector_1*vector_2
    vector_5 = vector_1*vector_2

