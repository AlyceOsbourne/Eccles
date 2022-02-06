from common.common_defaults import *
from common.common_math import *
from common.common_string_functions import *

__VERSION__ = {'MAJOR': 0, 'MINOR': 0, 'DEBUG': 0, 'DEVELOPMENT': 3}
__PROJECT_NAME__ = "Eccles"  # subject to change
__VERSION_STR__ = "v{}.{}.{}.{}".format(*__VERSION__.values())

__doc__ = """### Common ###

 Module to help cut down on code repetition, 
 if you find yourself repeating lines over and over 
 you may find a default for it here, this module also 
 includes common math functions, string functions etc   
 
"""

__doc__ += common_defaults.__doc__ + common_math.__doc__ + common_string_functions.__doc__
