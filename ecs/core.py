import logging
from threading import Thread
from itertools import count

logging.basicConfig(level=logging.DEBUG)
created_entity_counter = count(0)

#########################################################################
# ECS Exceptions
#########################################################################
class ComponentError(Exception):
    def __init__(self, component, message):
        """
        :param component: component that raised the error
        :param message: what error occurred
        """
        self.component = component
        self.message = message
        super().__init__(f"{self.component}: {self.message}")


class ComponentSystemError(Exception):
    def __init__(self, system, message):
        """
        :param component: component that raised the error
        :param message: what error occurred
        """
        self.system = system
        self.message = message
        super().__init__(f"{self.system}: {self.message}")


class ComponentSystemManagerError(Exception):
    def __init__(self, message):
        """
        :param message: what error occurred
        """
        self.message = message
        super().__init__(f"{self.message}")


#########################################################################
# Core Objects
#########################################################################
class Component:
    entity_id: int
    pass


class Entity:
    def __init__(self, *components):
        self.entity_id = created_entity_counter.__next__()
        for component in components:
            if issubclass(component.__class__, Component):
                component.entity_id = self.entity_id
                self.__dict__.update({component.__class__.__name__: component})


class System(Thread):
    pass
