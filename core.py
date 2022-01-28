import logging
from abc import abstractmethod
from itertools import count

ecs_logger = logging.Logger("ECCLES_LOGGER", level=logging.DEBUG)
created_entity_counter = count(0)


#########################################################################
# object storage
#########################################################################


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


class ECS:
    components = {}
    entities = {}
    systems = []


#########################################################################
# Core Objects
# todo -> write the core system class, it should extend thread as this
#  will be running as its own thing, will probably have to implement a lock
#  for when components are being modified.
#########################################################################
class Component:
    # used for components dataclass fields
    entity_id = None

    @abstractmethod
    def get_value(self):
        pass

    @abstractmethod
    def set_value(self, *args, **kwargs):
        pass

    def attach(self, entity_id):
        if self.__class__.__name__ not in ECS.components.keys():
            ECS.components[self.__class__.__name__] = {}
        ECS.components[self.__class__.__name__].update({entity_id: self})
        self.entity_id = entity_id

    def is_attached(self):
        return self.entity_id is not None


class Entity:

    def __init__(self, *components):
        self.entity_id = created_entity_counter.__next__()
        self.attach(*components)
        ecs_logger.log(logging.DEBUG, f"Entity#{self.entity_id} created")

    def attach(self, *components):
        self.entity_id = created_entity_counter.__next__()
        log = "Attached: \n\r"
        for component in components:
            if issubclass(component.__class__, Component):
                component.attach(self.entity_id)
                self.__dict__.update({component.__class__.__name__: component})
                log += f"{component.__class__.__name__}""\n\r"
            else:
                raise ComponentException(component, "This object is not a Component Object, please check your code")
            ecs_logger.log(logging.DEBUG, log)

        ECS.entities[self.entity_id] = self

    def detach(self, component):
        if isinstance(component, str):
            ecs_logger.log(logging.DEBUG, f"detached {component} from Entity#{self.entity_id}")
            self.__dict__.pop(component)
            return

        elif isinstance(component, Component):
            ecs_logger.log(logging.DEBUG, f"detached {component.__class__.__name__} from Entity#{self.entity_id}")
            self.__dict__.pop(component.__class__.__name__)
            return

        elif isinstance(component, type):
            ecs_logger.log(logging.DEBUG, f"detached {component.__name__} from Entity#{self.entity_id}")
            self.__dict__.pop(component.__name__)
            return


class System:

    def __init__(self, *managed):
        self.managed_components = managed
        ECS.systems.append(self)

    def collect(self):
        return [ECS.components[key.__class__.__name__] for key in self.managed_components]

    @abstractmethod
    def update(self, *args, **kwargs):
        print(self.__class__.__name__, "Update method for class has not been implemented")
