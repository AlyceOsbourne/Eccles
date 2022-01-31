import logging
import sys
from abc import abstractmethod
from functools import lru_cache
from itertools import count

ecs_logger = logging.Logger("ECCLES_LOGGER", level=logging.DEBUG)
created_entity_counter = count(0)


#########################################################################
# ECS Exceptions
# todo -> Write more comprehensive exception messages,
#  but will do this once the module is more fleshed
#  out and I have a better idea of the things that can go wrong
#########################################################################

class CoreException(Exception):
    obj: object

    def __init__(self, obj, message):
        """
        :param obj: input that raised the error
        :param message: what error occurred
        """
        self.obj = obj
        self.frame = sys._getframe(1).f_code.co_name
        self.message = message
        out = "\n\r" f"> Object: {self.obj}" "\n\r->" f" Method: {self.frame}:" "\n\r-->" f" {self.message}"
        super().__init__(out)


class ECS:
    components = {}
    entities = {}
    systems = []


class Component:
    __doc__ = """
    ### Component ###
    One of the three main parts of the ECS: the Component
    The Component acts as a data container, it holds nothing but values, get/set functions and a paired entity id
    it is suggested to decorate components with @dataclass and unpack the dicts in common.common_defaults as their args 
    for consistency and access to dataclass methods methods such as repr, hash, eq
    
    Examples of components can be found in prefabs
    """

    entity_id = None

    @classmethod
    def name(cls):
        return cls.__name__

    @abstractmethod
    def get_value(self):
        raise CoreException(self, "not implemented, please check your code")

    @abstractmethod
    def set_value(self, *args, **kwargs):
        raise CoreException(self, "not implemented, please check your code")

    def attach(self, entity_id):
        """
        attaches component to entity, generally used internally when applying components to entity object
        :param entity_id:
        """
        if self.__class__.__name__ not in ECS.components.keys():
            ECS.components[self.__class__.__name__] = {}
        ECS.components[self.__class__.__name__].update({entity_id: self})
        self.entity_id = entity_id

    def detach(self):
        if self.__class__.__name__ not in ECS.components.keys():
            return
        ECS.components[self.__class__.__name__].pop(self.entity_id)

    def is_attached(self):
        """
        :return: is attached to an entity
        """
        return self.entity_id is not None


class Entity:
    __doc__ = """
    ### Entity ###
    One of the three main parts of the ECS: the Entity
    It has a entity_id, and components
    
    An Entity can be instantiated in on of several ways.
    
        Entity base: Entity()
        
    It's uses *components so takes any number of Components
        
        Entity object with component objects: Entity(Position((1, 10, 0)), Rotation(), Velocity())

        Entity with component types: Entity(Mesh, Lifetime, Transform)

        Entity instantiated from archetype: Entity.from_archetype(*DefaultLivingCreatures.Player.value)
        
    components can be access like thus
        player.Position
    """

    def __init__(self, *components):
        self.entity_id = created_entity_counter.__next__()
        self.attach(*components)
        ecs_logger.log(logging.DEBUG, f"Entity#{self.entity_id} created")

    def attach(self, *components):
        """
        :param components: can be type extending Component or Component
        :return: self
        """
        self.entity_id = created_entity_counter.__next__()
        log = "Attached: \n\r"
        for component in components:
            if isinstance(component, type):
                component = component()
            if issubclass(component.__class__, Component):
                component.attach(self.entity_id)
                self.__dict__.update({component.__class__.__name__: component})
                log += f"{component.__class__.__name__}""\n\r"
            else:
                raise CoreException(component, "This object is not a Component Object, please check your code")
            ecs_logger.log(logging.DEBUG, log)

        ECS.entities[self.entity_id] = self
        return self

    def detach(self, component):
        """
        detaches the component and destroys it
        :param component:
        :return:
        """
        if isinstance(component, str):
            ecs_logger.log(logging.DEBUG, f"detached {component} from Entity#{self.entity_id}")
            self.__dict__.pop(component).detach()
        elif isinstance(component, Component):
            ecs_logger.log(logging.DEBUG, f"detached {component.__class__.__name__} from Entity#{self.entity_id}")
            self.__dict__.pop(component.__class__.__name__).detach()
        elif isinstance(component, type):
            ecs_logger.log(logging.DEBUG, f"detached {component.__name__} from Entity#{self.entity_id}")
            self.__dict__.pop(component.__name__).detach()
        else:
            raise CoreException(component, f" component not attached to {type(self)}#{self.entity_id}")

    def __str__(self):
        return f"{self.__class__.__name__}({[v for v in self.__dict__.values() if issubclass(v.__class__, Component)]})"

    @classmethod
    @lru_cache(30)  # caching for speed
    def from_archetype(cls, blueprint: list[Component], name=None, class_dict=None):
        """
        :param: class_dict:
        :param: name: name of the resulting type
        :param: blueprint: list of components to attach
        :param: class_dict dict to update class __dict__
        :return: entity with archetype
        """
        cd = class_dict if class_dict else {}
        if name:
            e = type(name, (Entity,), cd)(*blueprint)
        else:
            e = Entity(*blueprint)
            e.__dict__.update(cd)
        return e


class System:
    # todo finish core system

    __doc__ = """
    ### System ###
    One of the three main parts of the ECS: the System.
    The System takes a list of components that it acts upon, 
    this is for for the collector that then collects the 
    relevant lists from the core ECS, this is because its 
    faster to multiprocess a list of component than it is to 
    iterate through each Entity and then check if they have 
    component then get from the Entities __dict__
    """

    def __init__(self, *managed):
        """
        :param managed: components this system checks for from component pools
        """
        self.managed_components = managed
        ECS.systems.append(self)

    def collect(self):
        return [ECS.components[key.__class__.__name__] for key in self.managed_components]

    @abstractmethod
    def update(self, c):
        print(f"{self.__class__.__name__}"
              " does not seem to implement the update function OR said implementation of update calls super")

    def __call__(self, *args, **kwargs):  # we call up on the system to collect the data and process via the update
        # function
        self.update(self.collect())
