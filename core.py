import logging
from abc import abstractmethod
from itertools import count

ecs_logger = logging.Logger("ECCLES_LOGGER", level=logging.DEBUG)
created_entity_counter = count(0)


#########################################################################
# ECS Exceptions
# todo -> Write more comprehensive exception messages,
#  but will do this once the module is more fleshed
#  out and I have a better idea of the things that can go wrong
#########################################################################


class EcclesComponentException(Exception):
    def __init__(self, component, message):
        """
        :param component: component that raised the error
        :param message: what error occurred
        """
        self.component = component
        self.message = message
        super().__init__(f"{self.component}: {self.message}")


class EcclesSystemException(Exception):
    def __init__(self, system, message):
        """

        :param system: system that raised the error
        :param message: what error occurred
        """
        self.system = system
        self.message = message
        super().__init__(f"{self.system}: {self.message}")


class EcclesFoundryException(Exception):
    def __init__(self, foundry, message):
        """
        :param system: system that raised the error
        :param message: what error occurred
        """
        self.foundry = foundry
        self.message = message
        super().__init__(f"{self.foundry}: {self.message}")


class ECS:
    components = {}
    entities = {}
    systems = []


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
            if isinstance(component, type):
                component = component()
            if issubclass(component.__class__, Component):
                component.attach(self.entity_id)
                self.__dict__.update({component.__class__.__name__: component})
                log += f"{component.__class__.__name__}""\n\r"
            else:
                raise EcclesComponentException(component,
                                               "This object is not a Component Object, please check your code")
            ecs_logger.log(logging.DEBUG, log)

        ECS.entities[self.entity_id] = self
        return self

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

    def __str__(self):
        out = f"{self.__class__.__name__}({[v for v in self.__dict__.values() if issubclass(v.__class__, Component)]})"
        return out

    @classmethod
    def from_archetype(cls, blueprint: list[Component], name=None, class_dict=None):
        cd = class_dict if class_dict else {}
        if name:
            e = type(name, (Entity,), cd)(*blueprint)
        else:
            e = Entity(*blueprint)
            e.__dict__.update(cd)
        return e


class System:
    def __init__(self, *managed):
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