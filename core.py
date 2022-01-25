import logging
from abc import abstractmethod
from threading import Thread
from itertools import count

from numba import jit
logging.basicConfig(level=logging.DEBUG)
created_entity_counter = count(0)

#########################################################################
# object storage
#########################################################################
_components = {}
_entities = {}
_systems = []


#########################################################################
# ECS Exceptions
# todo -> Write more comprehensive exception messages,
#  but will do this once the module is more fleshed
#  out and I have a better idea of the things that can go wrong
#########################################################################


class ComponentException(Exception):
    def __init__(self, component, message):
        """
        :param component: component that raised the error
        :param message: what error occurred
        """
        self.component = component
        self.message = message
        super().__init__(f"{self.component}: {self.message}")


class ComponentSystemException(Exception):
    def __init__(self, system, message):
        """

        :param system: system that raised the error
        :param message: what error occurred
        """
        self.system = system
        self.message = message
        super().__init__(f"{self.system}: {self.message}")


class ComponentSystemManagerException(Exception):
    def __init__(self, message):
        """
        param message: what error occurred
        """
        self.message = message
        super().__init__(f"{self.message}")


#########################################################################
# Core Objects
# todo -> write the core system class, it should extend thread as this
#  will be running as its own thing, will probably have to implement a lock
#  for when components are being modified.
#  - should contain refs to entities components, maybe
#########################################################################
class Component:
    default_field_args = {'init': True, 'hash': True, 'compare': True}

    @abstractmethod
    def get_value(self):
        pass

    @abstractmethod
    def set_value(self, *args, **kwargs):
        pass

    def attach(self, entity_id):
        if self.__class__.__name__ not in _components.keys():
            _components[self.__class__.__name__] = {}
        _components[self.__class__.__name__].update({entity_id: self})




class Entity:
    def __init__(self, *components):
        self.entity_id = created_entity_counter.__next__()
        self.attach(*components)

    def attach(self, *components):
        self.entity_id = created_entity_counter.__next__()
        for component in components:
            if issubclass(component.__class__, Component):
                component.attach(self.entity_id)
                self.__dict__.update({component.__class__.__name__: component})
            else:
                raise ComponentException(component, "This object is not a Component Object, please check your code")
        _entities[self.entity_id] = self

    def detach(self, component):
        self.__dict__.pop(component.__class__.__name__)

    def __repr__(self):
        out = f"{self.__class__.__name__}"
        out += f"#{self.entity_id}"'\n\r'
        for v in self.__dict__.values():
            if issubclass(v.__class__, Component):
                out += '\n\r'f"-> {v.__class__.__name__}:({v.get_value()})"
        return out


class System(Thread):
    def __init__(self):
        _systems.append(self)
