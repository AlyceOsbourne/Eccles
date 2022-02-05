import importlib
import inspect


def get_class_docs(_name_: str = __name__, just_names: bool = False):
    return {(cls.__doc__ + "\n\r"
             if cls.__doc__
             else ''
    if not just_names
    else name + "\n\r")
            for name, cls
            in inspect.getmembers(importlib.import_module(_name_), inspect.isclass)
            if cls.__module__ == _name_}


def get_method_docs(obj):
    return {method.__doc__ for name, method in inspect.getmembers(obj, predicate=inspect.ismethod)}
