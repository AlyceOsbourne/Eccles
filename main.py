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
        - this is so that solid functions (functions with little variability besides its vars)
            can be compiled to machine code for faster calls, things like vector math would be good 
            candidates for JIT
        
   * write core thread manager
        - I think this would work best as an async context manager, 
            we can send the list of systems to manage as an arg, 
            and then we can cleanly shut down those systems on exit
        
   * write core event manager
        - I feel this also need to be an threaded process, but more study needs to be done
        
   * core clock
        - should be able to supply any tick rate requested, supply time since last tick etc
            I think there should be a global clock, and this ticks the other clocks at requested 
            intervals this way we can have different things support different tick rates while 
            maintaining synchronicity


* ### Math ### 
   * various curves, waves and linear functions
   * interpolations
   * Vector math
   * distance calculations
   * coordinate systems
        - planar, 3D, spherical
   * statistical math
        - may include a testing module including matplotlib for this
            this is for things like balance tools, performance analysis etc    
   * geometry for shape, vert, model, path etc


* ### Strings ###
   * string builders
        - for things like text outputs for logs, message/ ui builders
            npc chat/text etc etc
   * string parser
        - to convert data to human readable
        - to convert human readable to data
        - to take data to create execs
   * string randomizer
        - think borderlands weapon naming or any city builders citizens
            creates random names from pools etc


* ### Render ###
   * ModernGL seems to be the core of choice for now
        - uses OPENGL as backend, simplifies the process etc etc
            I am likely to make graphics a seperate module with an intermediary 
            so we can support multiple backends (and potentially other engines,
            like ursina or pygame)
   * shader engine
        - I'd like to try my hand at a light weight shader system, much study needs to 
            go into this though
   * particle engine
        - same as the above really, but for particles


* ### Mesh Management ###
   * OBJ loading and manipulation
        - I think I am going to use pywavefront
            as the object loader as its fully featured and working
   * procedural mesh generation
        - So I wish to include things like dynamic mesh stitching 
            (Think no mans sky's procedural mobs, metal gear risings mesh slicing
            or red factions destructible environments)

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
