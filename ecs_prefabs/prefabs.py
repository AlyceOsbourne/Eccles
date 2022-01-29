from dataclasses import dataclass, field

import common
from core import Component, System


#############################################################################
#                                    COMPONENTS
#############################################################################

# Components categorized by recommended system, this is a guide but not a rule
# It's recommended to create new components that subclass Component rather than
# subclass existing ones, again, this is structural advice and not a rule.

#############################################################################
#                                   Locomotion
#############################################################################

@dataclass(**common.default_dataclass_args)
class Position(Component):
    position: tuple[float, float, float] = field(default=(0, 0, 0), **common.default_field_args)

    def get_value(self):
        return self.position

    def set_value(self, pos, lock=None):
        self.position = pos


@dataclass(**common.default_dataclass_args)
class Rotation(Component):
    rotation: tuple[float, float, float] = field(default=(0., 0., 0.), **common.default_field_args)

    def get_value(self):
        return self.rotation

    def set_value(self, rotation):
        self.rotation = rotation


@dataclass(**common.default_dataclass_args)
class Velocity(Component):
    velocity: tuple[float, float, float] = field(default=(0., 0., 0.), **common.default_field_args)

    def get_value(self):
        return self.velocity

    def set_value(self, velocity):
        self.velocity = velocity


@dataclass(**common.default_dataclass_args)
class Mass(Component):
    mass: float = field(default=1., **common.default_field_args)

    def get_value(self):
        return self.mass

    def set_value(self, mass):
        self.mass = mass


#############################################################################
#                                   Model
#############################################################################
@dataclass(**common.default_dataclass_args)
class Mesh(Component):
    model: str = field(default='cube', **common.default_field_args)

    def get_value(self):
        return self.model

    def set_value(self, model):
        self.model = model


@dataclass(**common.default_dataclass_args)
class Scale(Component):
    scale: tuple[float, float, float] = field(default=(1., 1., 1.), **common.default_field_args)

    def get_value(self):
        return self.scale

    def set_value(self, scale):
        self.scale = scale


############################################################################
#                                   Render
############################################################################

@dataclass(**common.default_dataclass_args)
class Light(Component):  # to emit light in range
    colour: tuple[int, int, int] = field(default=(255, 255, 255), **common.default_field_args)
    intensity: float = field(default=1, **common.default_field_args)
    radius: float = field(default=1, **common.default_field_args)

    def get_value(self):
        return self.colour, self.intensity, self.radius

    def set_value(self, colour, intensity, radius):
        self.colour, self.intensity, self.radius = colour, intensity, radius


@dataclass(**common.default_dataclass_args)
class Glow(Component):  # to emit glow on particular region of object
    colour: tuple[int, int, int] = field(default=(255, 255, 255), **common.default_field_args)
    intensity: float = field(default=1, **common.default_field_args)
    radius: float = field(default=1, **common.default_field_args)

    def get_value(self):
        return self.colour, self.intensity, self.radius

    def set_value(self, colour, intensity, radius):
        self.colour, self.intensity, self.radius = colour, intensity, radius


@dataclass(**common.default_dataclass_args)
class Opacity(Component):
    opacity: float = field(default=1.0, **common.default_field_args)

    def get_value(self):
        return self.opacity

    def set_value(self, opacity):
        self.opacity = opacity


@dataclass(kw_only=True, **common.default_dataclass_args)
class Colour(Component):
    colour: tuple[int, int, int] = field(default=(255, 255, 255), **common.default_field_args)

    def get_value(self):
        return self.colour

    def set_value(self, colour):
        self.colour = colour


############################################################################
#                             Game Components
############################################################################

@dataclass(**common.default_dataclass_args)
class Name(Component):
    name: str = field(default="No Name", **common.default_field_args)
    short_name: str = field(default="No Name", **common.default_field_args)


@dataclass(**common.default_dataclass_args)
class Value(Component):
    value: float = field(default=1, **common.default_field_args)


@dataclass(**common.default_dataclass_args)
class Tradable(Component):
    tradable: bool = field(default=True, **common.default_field_args)
    sellable: bool = field(default=True, **common.default_field_args)


@dataclass(**common.default_dataclass_args)
class Inventory(Component):
    max_size: int = field(default=10, **common.default_field_args)
    inventory: list = field(default_factory=dict, **common.default_field_args)


############################################################################
#                             UI Components
############################################################################

@dataclass(**common.default_dataclass_args)
class Pane(Component):
    width: int = field(default=100, **common.default_field_args)
    height: int = field(default=100, **common.default_field_args)
    transparency: int = field(default=100, **common.default_field_args)


@dataclass(**common.default_dataclass_args)
class Label(Component):
    text: str = field(default='', **common.default_field_args)


############################################################################
#                          Temporal Components
############################################################################

@dataclass(++common.default_dataclass_args)
class Lifetime(Component):
    time: float = field(default=100, **common.default_field_args)


############################################################################
#                          Sound Components
############################################################################

@dataclass(++common.default_dataclass_args)
class AudioClip(Component):
    sound: str = field(default='', **common.default_field_args)
    volume: float = field(default=1, **common.default_field_args)
    duration: float = field(default=100, **common.default_field_args)
    range: int = field(default=10, **common.default_field_args)


@dataclass(++common.default_dataclass_args)
class AudioLoop(Component):
    sound: str = field(default='', **common.default_field_args)
    volume: float = field(default=1, **common.default_field_args)
    range: int = field(default=10, **common.default_field_args)


############################################################################
#                               ARCHETYPES
############################################################################
class ArchetypeFactory:
    pass
    # ok, so, I think this class is going to construct archetypes from dicts,
    # this way the user can provide new dicts to the factory to create new archetypes
    # I think it should yield a completed Entity rather than a particular Type,
    # as I feel this wil overall be more consistent with the overall design of
    # little inheritance

    # design ideas ->
    # I wish to create a callable object that serves as a container fo sorts
    #


############################################################################
#                                SYSTEMS
############################################################################


class MotionSystem(System):
    def __init__(self):
        super().__init__(Position, Rotation, Velocity)

    def update(self, c):
        pass


class AudioSystem(System):
    pass


class TransformSystem(System):
    pass


class RenderSystem(System):
    pass
