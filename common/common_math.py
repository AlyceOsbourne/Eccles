#########################################################################
# Math Functions
#########################################################################


#########################################################################
# Math Objects
#########################################################################
import math


class Vector:

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def get(self):
        return self.x, self.y, self.z

    @property
    def magnitude(self):
        return math.sqrt(sum((v ** 2 for v in self.get())))

    @magnitude.setter
    def magnitude(self, magnitude, normalize=True):
        """
        :param magnitude: magnitude to scale vector too
        :param normalize: whether or not to convert to unit before scale
        """
        if self.magnitude > 1 and normalize:
            self.normalize()
        self.x *= magnitude
        self.y *= magnitude
        self.z *= magnitude

    @property
    def angle_radians(self):
        pass

    @property
    def angle_degrees(self):
        pass

    @classmethod
    def as_unit(cls, vector):
        vec_mag = vector.magnitude
        x = vector.x / vec_mag
        y = vector.y / vec_mag
        z = vector.z / vec_mag
        return cls(x, y, z)

    @classmethod
    def from_radians(cls):
        pass

    @classmethod
    def from_degrees(cls):
        pass

    def normalize(self):
        while self.magnitude != 1:
            mag = self.magnitude
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
