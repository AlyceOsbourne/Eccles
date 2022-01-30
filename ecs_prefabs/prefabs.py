from dataclasses import dataclass, field
from enum import Enum

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


@dataclass
class Transform(Component):
    pass


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
    scale: tuple[float, float, float] = field(default_factory=tuple, **common.default_field_args)

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
#                     Item and Creature Components
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
    inventory: list = field(default_factory=dict, **common.default_field_args)


@dataclass(**common.default_dataclass_args)
class WieghtedInventory(Inventory):
    max_weight: float = field(default=100., **common.default_field_args)
    current_weight: float = field(default=0., **common.default_field_args)
    inventory: list = field(default_factory=dict, **common.default_field_args)


@dataclass(**common.default_dataclass_args)
class SlottedInventory(Inventory):
    number_of_slots: int = field(default=100, **common.default_field_args)
    occupied_slots: int = field(default=0, **common.default_field_args)
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
class Label(Pane):
    text: str = field(default='', **common.default_field_args)


############################################################################
#                          Temporal Components
############################################################################

@dataclass(**common.default_dataclass_args)
class Lifetime(Component):
    time: float = field(default=100, **common.default_field_args)


############################################################################
#                          Sound Components
############################################################################

class Audio(Component):
    sound: str = field(default='', **common.default_field_args)
    volume: float = field(default=1, **common.default_field_args)
    range: int = field(default=10, **common.default_field_args)


@dataclass(**common.default_dataclass_args)
class AudioClip(Audio):
    duration: float = field(default=100, **common.default_field_args)


@dataclass(**common.default_dataclass_args)
class AudioLoop(Audio):
    pass


@dataclass(**common.default_dataclass_args)
class AudioInterval(Audio):
    pass


############################################################################
#                             AI Components
############################################################################

@dataclass(**common.default_dataclass_args)
class FollowAI(Component):
    pass


@dataclass(**common.default_dataclass_args)
class FleeAI(Component):
    pass


@dataclass(**common.default_dataclass_args)
class HostileAI(Component):
    pass


@dataclass(**common.default_dataclass_args)
class AmbientAI(Component):
    pass


############################################################################
#                               ARCHETYPES
############################################################################

class DefaultLivingCreatures(Enum):
    Player = (Position, Rotation, Velocity, Mesh, Scale((1, 2, 1)), Inventory), "Player"



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
