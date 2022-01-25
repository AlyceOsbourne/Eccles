#########################################################################
# The general idea of this module is to provide a fast, easy to use ECS
# that allows the dynamic creation, modification and cleanup of entities
# and components, the initial build will be geared towards games, but I
# will later include a UI app ECS as I fell it could be of use there too
#########################################################################
from core import Component, Entity, System, ComponentException, ComponentSystemException, ComponentSystemManagerException
from ecs_prfabs.prefab_components import *
from ecs_prfabs.prefab_systems import *

if __name__ == "__main__":

    e = Entity(Position((1., 1., 1.)), Rotation(), Velocity(),Scale(), Mesh())
    print(e.__repr__())

    s = MotionSystem()
