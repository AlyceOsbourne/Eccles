import logging
import sys
from abc import abstractmethod
from itertools import count
from threading import Thread

import common

ecs_logger = logging.Logger("ECCLES_LOGGER", level=logging.DEBUG)
entity_count = count()
systems = []
components = {}
entities = {}

class CoreException(Exception):
    """### CoreException ###

  Core exception for the ECS module, called by Entity, Component and System
  will tell you what object and function failed, what the parameters were (if supplied)
  and a message of what went wrong
 
    >>> CoreException(object, message, *args, **kwargs
        object = the object that has errored
        message = the message to be printed
        *args/**kwargs = the args passed to the errored object

        """

    obj: object

    def __init__(self, obj, message, *args, **kwargs):
        self.obj = obj
        self.frame = sys._getframe(1).f_code.co_name  # lets us get the name of the failed code
        self.message = message
        out = "\n\r" + \
              f"{common.__PROJECT_NAME__} {common.__VERSION_STR__}" + \
              "\n\r" + \
              f" Object: {self.obj.__class__.__name__}" + \
              "\n\r->" + \
              f" Variables: {vars(obj)}" + \
              "\n\r->" + \
              f" Method: {self.frame}(args = {args},  kwargs = {kwargs}):" + \
              "\n\r->" + \
              f" {self.message} "

        super().__init__(out)


class Component:
    """### Component ###
    
This is the core data holder within the system, systems will enact upon the data stored in components,
and generally, except for special cases, should contain no methods besides getters/setters

during thair init they add themselves to lists of their component type, this is so Systems can operate on them faster
rather than having to do lossy lookups on entities aka if Entity has such and such do thing
this way our systems only ever operate on the components used in said systems

has abstract methods:

    >>> get_value()
    >>> set_value(*args, **kwargs)
        *arg/**kwargs are for the user to implement
    >>> is_attached()
        check to see if component is attached to an entity

    """

    entity_id = None

    @abstractmethod
    def get_value(self):
        """gets the value of the component"""
        raise CoreException(self, "not implemented, please check your code")

    @abstractmethod
    def set_value(self, *args, **kwargs):
        """gets the value of the component"""
        raise CoreException(self, "not implemented, please check your code")

    def __attach__(self, entity_id):
        """
        attaches component to entity, generally used internally when applying _components to entity object
        :param entity_id:
        """
        if self.__class__.__name__ not in components.keys():
            components[self.__class__.__name__] = {}
        components[self.__class__.__name__].update({entity_id: self})
        self.entity_id = entity_id

    def __detach__(self):
        """detaches component from entity"""

        if self.__class__.__name__ not in components.keys():
            return
        components[self.__class__.__name__].pop(self.entity_id)

    def is_attached(self):
        """
        :return: is attached to an entity
        """
        return self.entity_id is not None


class Entity:
    """### Entity ###

  entity of the ECS system, this class is an intermediary object that links Components with Systems, in a fashion
  allows the user to perform operations easily on an entity by entity basis.

  class shouldn't have to be expanded upon as they are composed with components and managed by systems and
  attached components become members of the Entity by default

    >>> Entity(*_components)
        *_components = any number of components to be attached to the entity

     >>> attach(*_components)
        *_componets = a list of component to attach to the entity

    >>> detach(*_components)
        detaches components from the entity

    >>> from_archetype(bluprint, name, class_dict)
        bluprint = a list of component to assign to the entity
        name = the name of the resulting type
        class_dict = a dict of objects to add as members of the class

    """

    def __init__(self, *_components):
        self.entity_id = entity_count.__next__()
        self.attach(*_components)

    def attach(self, *_components):
        """
        :param _components: can be type extending Component or Component
        :return: self
        """
        log = "Attached: \n\r"
        for component in _components:
            if isinstance(component, type):
                component = component()
            if issubclass(component.__class__, Component):
                component.__attach__(self.entity_id)
                self.__dict__.update({component.__class__.__name__: component})
                log += f"{component.__class__.__name__}""\n\r"
            else:
                raise CoreException(component, "This object is not a Component Object, please check your code",
                                    *_components)
            ecs_logger.log(logging.DEBUG, log)
        entities[self.entity_id] = self
        return self

    def detach(self, _components):
        """
        detaches the component and destroys it
        :param _components:
        :return:
        """
        if len(_components) == 1:
            _components = _components[0]

        if isinstance(component, str):
            ecs_logger.log(logging.DEBUG, f"detached {component} from Entity#{self.entity_id}")
            self.__dict__.pop(component).__detach__()

        elif isinstance(component, Component):
            ecs_logger.log(logging.DEBUG, f"detached {component.__class__.__name__} from Entity#{self.entity_id}")
            self.__dict__.pop(component.__class__.__name__).__detach__()

        elif isinstance(component, type):
            ecs_logger.log(logging.DEBUG, f"detached {component.__name__} from Entity#{self.entity_id}")
            self.__dict__.pop(component.__name__).__detach__()

        elif isinstance(_components, list) or isinstance(_components, tuple) or isinstance(_components, set):
            for c in _components:
                self.detach(c)
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

    def __del__(self):
        for i in self.__dict__.values():
            if issubclass(i.__class__, Component):
                i.__detach__()


class System(Thread):
    """### System ###

  Core System object for the ECS system,
  this deals in data management and manipulation and only ever operates on a predefined set of components
  this helps keep data organized, allows for modularization and ease of updating

    >>> collect()
        method used to collect components from lists and organize the data for processing

    >>> update(*component_list)
        if provided a list of components (in the correct structure for said system)
        will perform systems update operations on them, if not provided args will
        process in the default fashion by using the collect method

    >>> start()
        starts the processing thread, small amount of init

    >>> run()
        triggered by start method and runs the update cycle

    """

    def __init__(self, *managed):
        """
        :param managed: _components this system checks for from component pools
        """
        super().__init__(name=self.__class__.__name__, daemon=True)
        self.managed_components = [_c for _c in managed if issubclass(_c, Component)]
        for _c in self.managed_components:
            if _c.__name__ not in components.keys():
                components[_c.__name__] = []
        systems.append(self)
        self.running = False

    def collect(self):
        # components[key] yields a dict with [entity_id: Component]
        # collected contains an indeterminate number of dicts, I want to compare the lists of keys
        # and return a named tuple of lists of values in those dicts for each key that is in all dicts
        # this way we can iterate through each one and apply data
        return tuple(components[key.__name__] for key in self.managed_components)

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
        return f"{self.__class__.__name__}: {[_c.__name__ for _c in self.managed_components]}"


__doc__ = """## Core ##

 Core module that contains the core objects that makes up the ECS system, contains:

"""

for c in common.get_class_docs(__name__):
    __doc__ += " " + str(c)
