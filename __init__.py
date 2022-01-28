from core import ECSClock

__VERSION__ = {'MAJOR': 0, 'MINOR': 0, 'DEBUG': 0, 'DEVELOPMENT': 1}
PROJECT_NAME = "Eccles"
VERSION = "v{}.{}.{}.{}".format(*__VERSION__.values())
print(f"{PROJECT_NAME}.{VERSION} loaded")


#########################################################################
# The general idea of this module is to provide a fast, easy to use ECS
# that allows the dynamic creation, modification and cleanup of entities
# and components, the initial build will be geared towards games, but I
# will later include a UI app ECS as I feel it could be of use there too
#########################################################################
# Init
#########################################################################
def init():
    print("Starting init")
    # -> load definitions from file

    print("Loading definitions")
    # -> create components from definitions

    print("running component factory")
    # -> create entity archetypes from definitions and components

    print("Running entity factory")
    # -> load systems from definitions and link to relevant lists and dicts

    clock = ECSClock()


init()
