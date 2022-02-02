import prefabs
from core import Entity, Component, System

__doc__ = "\n\r" f"""{prefabs.common.__PROJECT_NAME__}: {prefabs.common.__VERSION_STR__}

{prefabs.common.__PROJECT_NAME__} is the Entity Component System Module of this project
it provides a compositional system for creating entities that
can be dynamically modified during runtime by adding and removing 
Components that are automatically handled by Systems, this helps 
decouple data from functions, and allows for new modules to be 
introduced with ease 
"""


#########################################################################
# The general idea of this module is to provide a fast, easy to use ECS
# that allows the dynamic creation, modification and cleanup of entities
# and _components, the initial build will be geared towards games, but I
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
# todo obj capture
#   -> mappings keyboard, mouse, controller
#
# todo animation system
#   -> skeleton controller
#   -> kinematics
#
# todo physics
#   -> colliders
#   -> interactions
#
#########################################################################
# Init
#########################################################################

def init():
    print("Starting init")
    # -> load definitions from file

    print("Loading definitions")
    # -> create _components from definitions

    print("running component factory")
    # -> create entity archetypes from definitions and _components

    print("Running entity factory")
    # -> load systems from definitions and link to relevant lists and dicts


def print_docs():
    print(__doc__, Component.__doc__, Entity.__doc__, System.__doc__, prefabs.__doc__)


if __name__ == "__main__":
    print_docs()
