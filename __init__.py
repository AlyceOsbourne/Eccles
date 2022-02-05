import common
import core
import events
import prefabs
from core import Entity, Component, System, CoreException

__doc__ = "\n\r" f"""{common.__PROJECT_NAME__}: {common.__VERSION_STR__}

 {common.__PROJECT_NAME__} is the Entity Component System Module of this project
 it provides a compositional system for creating entities that
 can be dynamically modified during runtime by adding and removing 
 Components that are automatically handled by Systems, this helps 
 decouple data from functions, and allows for new modules to be 
 introduced with ease 
"""

__all__ = ['common', 'events', 'prefabs', 'Entity', 'Component', 'System', 'CoreException']


#########################################################################
# The general idea of this module is to provide a fast, easy to use ECS
# that allows the dynamic creation, modification and cleanup of entities
# and _components, the initial build will be geared towards games, but I
# will later include a UI app ECS as I feel it could be of use there too
#
# todo study into LLVMLite for JIT capabilities, candidates for jit:
#   -> write core thread manager
#   -> write core event manager
#   -> core system functions
#       -> collect
#           collect needs to disregard components that are not shared along all lists
#       -> process
#           should be a generic method tto be implemented byy subclasses
#
# todo create common math functions
#   -> various curves, waves and linear functions
#   -> geometry for shape, vert, model, path etc
#
# todo create common string functions
#   -> string builders
#   -> string parser
#   -> string randomizer
#
# todo render system
#   -> OpenGL or Vulkan? - answer appears to be moderngl?
#   -> *.OBJ loading and manipulation - pywavefront
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


def docs():
    return __doc__ + core.core_objects.__doc__ + common.__doc__


def to_wiki():
    with open("C:\\Users\\Alyce\\PycharmProjects\\Eccles.wiki\\" + "ECS.md", 'w') as f:
        f.write(docs())


if __name__ == "__main__":
    print(docs())
    to_wiki()
