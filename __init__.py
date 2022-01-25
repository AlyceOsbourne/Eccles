#########################################################################
# The general idea of this module is to provide a fast, easy to use ECS
# that allows the dynamic creation, modification and cleanup of entities
# and components, the initial build will be geared towards games, but I
# will later include a UI app ECS as I feel it could be of use there too
#########################################################################
from core import Component, Entity, System, ComponentException, ComponentSystemException, ComponentSystemManagerException, _systems, _components, _entities
from ecs_prfabs.prefab_components import *
from ecs_prfabs.prefab_systems import *

if __name__ == "__main__":

    e = Entity(Position((1., 1., 1.)), Rotation(), Velocity(), Mesh(), Scale())
    e.attach(Glow())
    e.detach(e.Velocity)
    s = MotionSystem()
