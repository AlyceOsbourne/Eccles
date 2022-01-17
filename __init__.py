from abc import abstractmethod

loaded_entities, loaded_systems = {}, {}


class ComponentError(Exception):

    def __init__(self, component, message):
        """
        :param component: component that raised the error
        :param message: what error occurred
        """
        self.component = component
        self.message = message
        super().__init__(f"{self.component}: {self.message}")


class Component:

    @abstractmethod
    def get(self):
        ...

    @abstractmethod
    def set(self, *args):
        ...

    def __str__(self):
        return f"{self.__class__.__name__}:{self.__dict__}"


class Entity:
    def __init__(self, *components):
        self.__dict__.update({k.__class__.__name__: k for (k) in components if isinstance(k, Component)})
        if self.__class__.__name__ not in loaded_entities.keys():
            loaded_entities[self.__class__.__name__] = {}
        loaded_entities[self.__class__.__name__].update({self.__hash__(): self})

    def attach_component(self, component):
        if isinstance(component, Component):
            self.__dict__[component.__class__.__name__] = component

    def detach_component(self, component_class):
        if component_class in self.__dict__.keys():
            c = self.__dict__[component_class]
            c.__del__()
            self.__dict__.pop(component_class)

    def get_attached_component(self, component_id):
        if component_id in self.__dict__.keys():
            return self.__dict__[component_id]

    def get_attached_component_by_type(self, component_type):
        return {k: v for (k, v) in self.__dict__ if isinstance(v, component_type)}

    def __str__(self):
        return f"{self.__class__.__name__}.{self.__hash__()}: " \
               f"{str({var_name: str(var_data) for (var_name, var_data) in self.__dict__.items()})}"


class System:
    __slots__ = ('system_id', 'managed_components')
    managed_components: list[Component]

    def __init__(self):
        loaded_systems[self.__class__.__name__] = self

    def update(self):
        pass


class Rotation(Component):
    def set(self, rotation: tuple[int, int, int] or None = None, rot_x=0, rot_y=0, rot_z=0):
        self.rotation_x, self.rotation_y, self.rotation_z = rotation if rotation else rot_x, rot_y, rot_z

    __slots__ = ('rotation_x', 'rotation_y', 'rotation_z')

    def __init__(self, rotation: tuple[int, int, int] or None = None, rot_x=0, rot_y=0, rot_z=0):
        self.rotation_x, self.rotation_y, self.rotation_z = rotation if rotation else rot_x, rot_y, rot_z

    def get(self):
        return self.rotation_x, self.rotation_y, self.rotation_z

    def __str__(self):
        return f"{self.rotation_x},{self.rotation_y},{self.rotation_z}"


class Position(Component):
    __slots__ = ('x', 'y', 'z')

    def __init__(self, position: tuple[int, int, int] or None = None, pos_x=0, pos_y=0, pos_z=0):
        super().__init__()
        self.x, self.y, self.z = position if position else pos_x, pos_y, pos_z

    def get(self):
        return self.x, self.y, self.z

    def set(self, position: tuple[int, int, int] or None = None, pos_x=0, pos_y=0, pos_z=0):
        self.x, self.y, self.z = position if position else pos_x, pos_y, pos_z

    def __str__(self):
        return f"{self.x},{self.y},{self.z}"


class Velocity(Component):
    __slots__ = ('velocity_x', 'velocity_y', 'velocity_z')

    def __init__(self, velocity: tuple[int, int, int] or None = None, velocity_x=0, velocity_y=0, velocity_z=0):
        super().__init__()
        self.velocity_x, self.velocity_y, self.velocity_z = velocity if velocity else velocity_x, velocity_y, velocity_z

    def set(self, id_, velocity: tuple[int, int, int] or None = None, velocity_x=0, velocity_y=0, velocity_z=0):
        self.velocity_x, self.velocity_y, self.velocity_z = velocity if velocity else velocity_x, velocity_y, velocity_z

    def get(self):
        return self.velocity_x, self.velocity_y, self.velocity_z

    def __str__(self):
        return f"{self.velocity_x}, {self.velocity_y}, {self.velocity_z}"


class Mass(Component):
    __slots__ = ('mass',)

    def __init__(self, mass):
        self.mass = mass

    def get(self):
        return self.mass

    def set(self, mass):
        self.mass = mass

    def __str__(self):
        return str(self.mass)


class MotionSystem(System):
    managed_components = Position, Rotation, Velocity
