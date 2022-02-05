import importlib
import inspect

__doc__ = """# common string functions #

    script for string functions that will see regular use

"""

def get_class_docs(_name_: str = __name__, just_names: bool = False):
    return [(cls.__doc__ + "\n\r"
             if cls.__doc__
             else ''
    if not just_names
    else name + "\n\r")
            for name, cls
            in inspect.getmembers(importlib.import_module(_name_), inspect.isclass)
            if cls.__module__ == _name_]


def get_method_docs(obj):
    return {method for name, method in inspect.getmembers(obj, predicate=inspect.ismethod)}
