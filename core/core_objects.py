import logging
import sys
from abc import abstractmethod
from itertools import count
from threading import Thread

ecs_logger = logging.Logger("ECCLES_LOGGER", level=logging.DEBUG)
entity_count = count()
systems = []
components = {}
entities = {}


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


class Component:
    __doc__ = """
    ### Component ###
    One of the three main parts of the ECS: the Component
    The Component acts as a data container, it holds nothing but values, get/set functions and a paired entity id
    it is suggested to decorate _components with @dataclass and unpack the dicts in common.common_defaults as their args 
    for consistency and access to dataclass methods methods such as repr, hash, eq
    
    Examples of _components can be found in prefabs
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
        attaches component to entity, generally used internally when applying _components to entity object
        :param entity_id:
        """
        if self.__class__.__name__ not in components.keys():
            components[self.__class__.__name__] = {}
        components[self.__class__.__name__].update({entity_id: self})
        self.entity_id = entity_id

    def detach(self):
        if self.__class__.__name__ not in components.keys():
            return
        components[self.__class__.__name__].pop(self.entity_id)

    def is_attached(self):
        """
        :return: is attached to an entity
        """
        return self.entity_id is not None


class Entity:
    __doc__ = """
    ### Entity ###
    One of the three main parts of the ECS: the Entity
    It has a entity_id, and _components
    
    An Entity can be instantiated in on of several ways.
    
        Entity base: Entity()
        
    It's uses *_components so takes any number of Components
        
        Entity object with component objects: Entity(Position((1, 10, 0)), Rotation(), Velocity())

        Entity with component types: Entity(Mesh, Lifetime, Transform)

        Entity instantiated from archetype: Entity.from_archetype(*DefaultLivingCreatures.Player.value)
        
    _components can be access like thus
        player.Position
    """

    def __init__(self, *_components):
        self.entity_id = entity_count.__next__()
        self.attach(*_components)
        print(logging.DEBUG, f"Entity#{self.entity_id} created")

    def attach(self, *_components):
        """
        :param components: can be type extending Component or Component
        :return: self
        """
        log = "Attached: \n\r"
        for component in _components:
            if isinstance(component, type):
                component = component()
            if issubclass(component.__class__, Component):
                component.attach(self.entity_id)
                self.__dict__.update({component.__class__.__name__: component})
                log += f"{component.__class__.__name__}""\n\r"
            else:
                raise CoreException(component, "This object is not a Component Object, please check your code")
            ecs_logger.log(logging.DEBUG, log)
        entities[self.entity_id] = self
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
    def from_archetype(cls, blueprint: list[Component], name=None, class_dict=None):
        """
        :param: class_dict:
        :param: name: name of the resulting type
        :param: blueprint: list of _components to attach
        :param: class_dict dict to update class __dict__
        :return: entity with archetype
        """
        if name:
            e = type(name, (Entity,), class_dict if class_dict else {})(*blueprint)
        else:
            e = Entity(*blueprint)
            if class_dict:
                e.__dict__.update(class_dict)
        return e


class System(Thread):
    # todo finish core system

    __doc__ = """
    ### System ###
    One of the three main parts of the ECS: the System.
    The System takes a list of _components that it acts upon, 
    this is for for the collector that then collects the 
    relevant lists from the core ECS, this is because its 
    faster to multiprocess a list of component than it is to 
    iterate through each Entity and then check if they have 
    component then get from the Entities __dict__
    """

    def __init__(self, *managed):
        """
        :param managed: _components this system checks for from component pools
        """
        super().__init__(name=self.__class__.__name__, daemon=True)
        self.managed_components = [c for c in managed if issubclass(c, Component)]
        for c in self.managed_components:
            if c.__name__ not in components.keys():
                components[c.__name__] = []
        systems.append(self)
        self.running = False

    def collect(self):
        collected = tuple(components[key.__name__] for key in self.managed_components)
        # now we need to reduce these by making sure that entityID is in all so we are not , this should be as simple as
        # adding all of the values of the keys and converting to a set and then collecting those
        keys = []
        for d in collected:
            for k in list(d.keys()):
                keys.append(k)

        keys = set(keys)
        return tuple(
            [{key: components[component.__name__][key]} for key in keys] for component in self.managed_components)

    def update(self, *component_list):
        self.process(component_list if component_list else self.collect())

    @abstractmethod
    def process(self, *args, **kwargs):
        """
        method to be overloaded y user, here you will receive a tuple of dicts
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def start(self):
        super().start()

    def run(self):
        self.running = True
        while self.running:
            self.update()

    def __str__(self):
        return f"{self.__class__.__name__}: {[c.__name__ for c in self.managed_components]}"
