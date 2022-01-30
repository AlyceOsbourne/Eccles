from core import Entity, ECS
from ecs_prefabs.prefabs import *

__VERSION__ = {'MAJOR': 0, 'MINOR': 0, 'DEBUG': 0, 'DEVELOPMENT': 1}
__PROJECT_NAME__ = "Eccles"
__VERSION_STR__ = "v{}.{}.{}.{}".format(*__VERSION__.values())
print(f"{__PROJECT_NAME__}.{__VERSION_STR__} loaded")


#########################################################################
# The general idea of this module is to provide a fast, easy to use ECS
# that allows the dynamic creation, modification and cleanup of entities
# and components, the initial build will be geared towards games, but I
# will later include a UI app ECS as I feel it could be of use there too
#
# todo study into LLVMLite for JIT capabilities, candidates for jit:
#   -> system update functions
#   -> entity archetype instantiation
#   -> Components? As we will always know their core values?
#
# todo create common math functions
#   -> vector math, unit vector conversions
#   -> various curves, waves and linear functions
#   -> geometry for shape, vert, model, path etc
#
# todo create common string functions
#   -> string builders
#   -> string parser
#   -> string randomizer
#
# todo render system
#   -> OpenGL or Vulkan?
#   -> *.OBJ loading and manipulation
#   -> procedural mesh generation
#   -> particle engine
#   -> shader engine
#
# todo input capture
#   -> mappings keyboard, mouse, controller
#
# todo animation system
#   -> skeleton controller
#   -> kinematics
#
# todo pysics
#   -> colliders
#   -> interactions
#########################################################################
# Init
#########################################################################

def init():
    print("Starting init")
    # -> load definitions from file

    print("Loading definitions")
    # -> create components from definitions

    print("running component factory")
    # -> create entity archetypes from definitions and components

    print("Running entity factory")
    # -> load systems from definitions and link to relevant lists and dicts


if __name__ == "__main__":
    # just an example of how this code works
    # firstly you can create entities in the following ways

    # the basic Entity object
    default_entity = Entity()
    print(default_entity)
    print("\n\r")

    # Entity object with component objects
    default_obj_entity = Entity(Position((1, 10, 0)), Rotation(), Velocity())
    print(default_obj_entity)
    print("\n\r")

    # Entity with component types
    default_type_entity = Entity(Mesh, Lifetime, Transform)
    print(default_type_entity)
    print("\n\r")

    # creates a Player entity with all Components instantiated from archetype
    player = Entity.from_archetype(*DefaultLivingCreatures.Player.value)
    print(player)
    print("\n\r")

    # components can be access like thus
    print(player.Position)
    print("\n\r")

    # components can be accessed by their class name
    # this is for systems to iterate through quickly
    print(list(ECS.components['Rotation'].values()))
    print("\n\r")
