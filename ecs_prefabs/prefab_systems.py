from core import System
from prefab_components import *


class MotionSystem(System):
    def __init__(self):
        super().__init__(Position, Rotation, Velocity)

    def update(self, c):
        pass


class AudioSystem(System):
    pass


class TransformSystem(System):
    pass


class RenderSystem(System):
    pass
