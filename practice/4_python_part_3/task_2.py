"""
Write function which executes custom operation from math module
for given arguments.
Restrition: math function could take 1 or 2 arguments
If given operation does not exists, raise OperationNotFoundException
Examples:
     >>> math_calculate('log', 1024, 2)
     10.0
     >>> math_calculate('ceil', 10.7)
     11
"""
import math

class OperationNotFoundException(Exception):
    pass

class NoAttributeException(Exception):
    pass

def math_calculate(function: str, *args):
    try:
        math_function = getattr(math, function)
    except AttributeError:
        raise OperationNotFoundException("Operation not found")
    try:
        if len(args) == 1:
            return math_function(args[0])
        elif len(args) == 2:
            return math_function(args[0], args[1])
        else:
            raise TypeError("Incorrect number of arguments provided")
    except TypeError:
        raise NoAttributeException("Operation raised a TypeError due to invalid arguments")
    return None 



"""
Write tests for math_calculate function
"""
