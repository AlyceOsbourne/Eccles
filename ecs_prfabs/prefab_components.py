from dataclasses import dataclass, field
from core import Component


#############################################################################
#                                    Prefabs
#############################################################################

# Components categorized by recommended system, this is a guideline but not a rule
# It's recommended to create new components that subclass Component rather than
# subclass existing ones, again, this is structural advice and not a rule

#############################################################################
#                                   Locomotion
#############################################################################

@dataclass(slots=True, eq=True)
class Position(Component):
    position: tuple[float, float, float] = field(default=(0, 0, 0), **Component.default_field_args)

    def get_value(self):
        return self.position

    def set_value(self, pos, lock=None):
        self.position = pos


@dataclass(slots=True, eq=True)
class Rotation(Component):
    rotation: tuple[float, float, float] = field(default=(0., 0., 0.), **Component.default_field_args)

    def get_value(self):
        return self.rotation

    def set_value(self, rotation):
        self.rotation = rotation


@dataclass(slots=True, eq=True)
class Velocity(Component):
    velocity: tuple[float, float, float] = field(default=(0., 0., 0.), **Component.default_field_args)

    def get_value(self):
        return self.velocity

    def set_value(self, velocity):
        self.velocity = velocity


@dataclass(slots=True, eq=True)
class Mass(Component):
    mass: float = field(default=1., **Component.default_field_args)

    def get_value(self):
        return self.mass

    def set_value(self, mass):
        self.mass = mass


#############################################################################
#                                   Model
#############################################################################
@dataclass(slots=True, eq=True)
class Mesh(Component):
    model: str = field(default='cube', **Component.default_field_args)

    def get_value(self):
        return self.model

    def set_value(self, model):
        self.model = model


@dataclass(slots=True, eq=True)
class Scale(Component):
    scale: tuple[float, float, float] = field(default=(1., 1., 1.), **Component.default_field_args)

    def get_value(self):
        return self.scale

    def set_value(self, scale):
        self.scale = scale


############################################################################
#                                   Render
############################################################################

@dataclass(slots=True, eq=True)
class Light(Component):  # to emit light in range
    colour: tuple[int, int, int] = field(default=(255, 255, 255), **Component.default_field_args)
    intensity: float = field(default=1, **Component.default_field_args)
    radius: float = field(default=1, **Component.default_field_args)

    def get_value(self):
        return self.colour, self.intensity, self.radius

    def set_value(self, colour, intensity, radius):
        self.colour, self.intensity, self.radius = colour, intensity, radius


@dataclass(slots=True, eq=True)
class Glow(Component):  # to emit glow on particular region of object
    colour: tuple[int, int, int] = field(default=(255, 255, 255), **Component.default_field_args)
    intensity: float = field(default=1, **Component.default_field_args)
    radius: float = field(default=1, **Component.default_field_args)

    def get_value(self):
        return self.colour, self.intensity, self.radius

    def set_value(self, colour, intensity, radius):
        self.colour, self.intensity, self.radius = colour, intensity, radius


@dataclass(kw_only=True, slots=True, eq=True)
class Opacity(Component):
    opacity: float = field(default=1.0, **Component.default_field_args)

    def get_value(self):
        return self.opacity

    def set_value(self, opacity):
        self.opacity = opacity


@dataclass(kw_only=True, slots=True, eq=True)
class Colour(Component):
    colour: tuple[int, int, int] = field(default=(255, 255, 255), **Component.default_field_args)

    def get_value(self):
        return self.colour

    def set_value(self, colour):
        self.colour = colour
