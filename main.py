import common
import core
import events
import prefabs
from core import Entity, Component, System, CoreException

__doc__ = "\n\r" f"""### {common.__PROJECT_NAME__}: {common.__VERSION_STR__} ###

 {common.__PROJECT_NAME__} is the Entity Component System Module of this project
 it provides a compositional system for creating entities that
 can be dynamically modified during runtime by adding and removing 
 Components that are automatically handled by Systems, this helps 
 decouple data from functions, and allows for new modules to be 
 introduced with ease 
 
"""

__all__ = ['common', 'events', 'prefabs', 'Entity', 'Component', 'System', 'CoreException', "docs"]

__todo__ = """
## TODO ###

 The general idea of this module is to provide a fast, easy to use ECS
 that allows the dynamic creation, modification and cleanup of entities
 and _components, the initial build will be geared towards games, but I
 will later include a UI app ECS as I feel it could be of use there too

* ### Core ###
   * JIT capabilities 
   * write core thread manager
   * write core event manager


* ### Math ### 
   * various curves, waves and linear functions
   * geometry for shape, vert, model, path etc
   * interpolations    


* ### Strings ###
   * string builders
   * string parser
   * string randomizer


* ### Render ###
   * OpenGL or Vulkan? - answer appears to be moderngl?
   * particle engine
   * shader engine


* ### Mesh Management ###
   * OBJ loading and manipulation - pywavefront
   * procedural mesh generation


* ### Input Capture ###
   * mappings keyboard, mouse, controller


* ### Animation System ###
   * skeleton controller
   * kinematics


* ### Physics ###
   * colliders
   * interactions
"""


def docs():
    return __doc__ + core.core_objects.__doc__ + common.__doc__


if __name__ == "__main__":
    print(docs())
