from dataclasses import dataclass, field
from enum import Enum

import common
from core import Component, System


@dataclass(**common.default_dataclass_args)
class Vectored(Component):
    # currently, represents an x, y, z, will be swapped for a vector class
    x: float = field(default=0, **common.default_field_args)
    y: float = field(default=0, **common.default_field_args)
    z: float = field(default=0, **common.default_field_args)

    def get_value(self):
        return self.x, self.y, self.z

    def set_value(self, vector):
        self.x, self.y, self.x = vector


@dataclass(**common.default_dataclass_args)
class Position(Vectored):
    pass

@dataclass(**common.default_dataclass_args)
class Rotation(Vectored):
    pass

@dataclass(**common.default_dataclass_args)
class Velocity(Vectored):
    pass

@dataclass
class Transform(Vectored):
    pass


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
class WeightedInventory(Inventory):
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
    Player = (Position, Rotation, Velocity, Mesh, Scale((1, 2, 1)), Inventory), 'Player'
    """# DefaultLivingCreatures #
    an enumerator of of archetype blueprints for the Entity.from_archetype command
    >>> Entity.from_archetype(**DefaultLivingCreatures.|name|.value) 
        where |name| is is the name of the archetype  
    """

############################################################################
#                                SYSTEMS
############################################################################


class MotionSystem(System):
    def __init__(self):
        super().__init__(Position, Rotation, Velocity)


class AudioSystem(System):
    pass


class TransformSystem(System):
    pass


class RenderSystem(System):
    pass


__doc__ = """ ### Prefabs ###
    Module that provides a bunch of prebuilt _components, archetypes and systems
"""

for c in common.get_class_docs(__name__):
    __doc__ += str(c)
