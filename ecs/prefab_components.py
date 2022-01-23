from dataclasses import dataclass, field
from core import Component
from game_math import Vector


#############################################################################
# Prefabs
#############################################################################

# Components categorized by recommended system, this is a guideline but not a rule
# It's recommended to create new components that subclass Component rather than
# subclass existing ones, again, this is structural advice and not a rule

#################
# Locomotion
#################
@dataclass(slots=True, eq=True)
class Position(Component):
    position: Vector


@dataclass(slots=True, eq=True)
class Rotation(Component):
    rotation: Vector


@dataclass(slots=True, eq=True)
class Velocity(Component):
    velocity: Vector


@dataclass(slots=True, eq=True)
class Mass(Component):
    mass: float = field(default=1.)

    @property
    def mass(self):
        return self.mass

    @mass.setter
    def mass(self, mass):
        self.mass = mass


#################
# Model
#################
@dataclass(slots=True, eq=True)
class Mesh(Component):
    model: str = field(default='cube')


@dataclass(slots=True, eq=True)
class Scale(Component):
    scale: tuple[float, float, float] = field(default=(1, 1, 1))

    @property
    def scale(self):
        return self.scale

    @scale.setter
    def scale(self, scale: tuple[float, float, float]):
        self.scale = scale


#################
# Render
#################
@dataclass(slots=True, eq=True)
class Light(Component):  # to emit light in range
    colour: tuple[int, int, int] = field(default=(255, 255, 255))
    intensity: float = field(default=1)
    radius: float = field(default=1)


@dataclass(slots=True, eq=True)
class Glow(Component):  # to emit glow on particular region of object
    colour: tuple[int, int, int] = field(default=(255, 255, 255))
    intensity: float = field(default=1)
    radius: float = field(default=1)


@dataclass(kw_only=True, slots=True, eq=True)
class Opacity(Component):
    opacity: float = field(default=1.0, metadata="Entity Opacity")


@dataclass(kw_only=True, slots=True, eq=True)
class Colour(Component):
    colour: tuple[int, int, int] = field(default=(255, 255, 255), metadata="Entity Colour")
