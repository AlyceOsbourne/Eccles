#########################################################################
# default args for dataclass Components
#########################################################################
__doc__ = """# common defaults #

    script for variables, methods and arguments that represent default values
    
"""
# unpacked as dataclass(**common.default_dataclass_args)
default_dataclass_args = {'slots': True, 'eq': True, 'unsafe_hash': True}

# unpacked as field(default or default_factory, **common.default_field_args)
default_field_args = {'init': True, 'hash': True, 'compare': True, "repr": True}
