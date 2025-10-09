from dataclasses import dataclass
import numpy as np
import typing


# =============================================================================
#   Fake DiffableNdarray and its typing support for demonstration purposes
# =============================================================================
class DiffableNdarray(np.ndarray):
    """
    Fake diffable ndarray subclass for demonstration purposes.
    """

    def __new__(cls, input_array, *args, **kwargs):
        obj = np.asarray(input_array).view(cls)
        # custom stuff here
        return obj

    @classmethod
    def __class_getitem__(cls, params):
        # params might be (shape, dtype) tuple, e.g., DiffableNdarray[(Shape["2,2"], int)]
        return DiffableNdarrayType(cls, params)


# =============================================================================
#   Typing support for DiffableNdarray
# =============================================================================


@dataclass
class DiffableNdarrayShape:
    def __init__(self, *dims: int):
        self.shape = dims


class DiffableNdarrayDtype:
    def __init__(self, dtype: type):
        self.dtype = dtype


class DiffableNdarrayType:
    def __init__(self, base, params):
        self.base = base
        self.params = params

    def __instancecheck__(self, inst, /, throw_exception=True, exception_prefix=""):
        # Check type
        if not isinstance(inst, self.base):
            return False
        # Check
        for param in self.params:
            if isinstance(param, DiffableNdarrayShape):
                if inst.shape != param.shape:
                    if throw_exception:
                        raise TypeError(f"{exception_prefix}DiffableNdarray shape mismatch: expected {param.shape}, got {inst.shape}")
                    return False
            elif isinstance(param, DiffableNdarrayDtype):
                if not np.issubdtype(inst.dtype, param.dtype):
                    if throw_exception:
                        raise TypeError(f"{exception_prefix}DiffableNdarray dtype mismatch: expected {param.dtype}, got {inst.dtype}")
                    return False
            elif isinstance(param, type):
                if not np.issubdtype(inst.dtype, param):
                    if throw_exception:
                        raise TypeError(f"{exception_prefix}DiffableNdarray dtype mismatch: expected {param}, got {inst.dtype}")
                    return False
            else:
                raise TypeError("Parameters must be either DiffableNdarrayShape or a dtype type.")

        # Write custom logic here (shape/dtype? Only basic for MVP)
        return True


# =============================================================================
#  Decorator to check function arguments and return types against DiffableNdarrayType annotations
# =============================================================================
def diffable_ndarray_checker(func) -> typing.Callable[..., typing.Any]:
    """
    A decorator to check function arguments and return types against DiffableNdarrayType annotations.
    If a mismatch is found, a TypeError is raised with a descriptive message.
    """

    def _get_argument_value(func, args, kwargs, argument_name):
        # Find argument value by name
        if argument_name in kwargs:
            return kwargs[argument_name]
        else:
            # Get position of argument
            arg_names = func.__code__.co_varnames
            idx = arg_names.index(argument_name)
            if idx < len(args):
                return args[idx]
            else:
                return None  # Argument not provided

    def func_wrapper(*args, **kwargs):
        annotations = func.__annotations__

        # =============================================================================
        # Check argument types
        # =============================================================================
        for annotated_name, annotation in annotations.items():
            # Skip return annotation now, do it after the function call
            if annotated_name == "return":
                continue

            # check only DiffableNdarrayType annotations
            if isinstance(annotation, DiffableNdarrayType) is False:
                continue

            # get the argument name and value
            argument_name = annotated_name
            argument_value = _get_argument_value(func, args, kwargs, argument_name)

            # perform the instance check
            is_instance = annotation.__instancecheck__(argument_value, throw_exception=True, exception_prefix=f"Argument '{argument_name}': ")

            # sanity check
            assert is_instance == True, f"PANIC: should never be reached, as __instancecheck__ should have thrown an exception if False"

        # =============================================================================
        # Call the original function
        # =============================================================================
        returned_value = func(*args, **kwargs)

        # =============================================================================
        # Check return type
        # =============================================================================
        # TODO check the return type too
        if "return" in annotations:
            annotation = annotations["return"]

            # check only DiffableNdarrayType annotations
            if isinstance(annotation, DiffableNdarrayType) is True:
                # perform the instance check
                is_instance = annotation.__instancecheck__(returned_value, throw_exception=True, exception_prefix="Return value: ")
                # sanity check
                assert is_instance == True, f"PANIC: should never be reached, as __instancecheck__ should have thrown an exception if False"

        # return the original function's return value
        return returned_value

    return func_wrapper


###############################################################################
#   Example usage
#
if __name__ == "__main__":
    Shape = DiffableNdarrayShape
    Dtype = DiffableNdarrayDtype

    arr: DiffableNdarray[Shape(2, 2), int] = DiffableNdarray(np.zeros((2, 2), dtype=float))

    assert isinstance(arr, DiffableNdarray[Shape(2, 2), float]), "Expected instance of DiffableNdarray[Shape(2, 2), float]"

    # print(isinstance(arr, DiffableNdarray[Shape(2, 3), float]))

    @diffable_ndarray_checker
    def foo(my_str: str, arr: DiffableNdarray[Shape(2, 4), int]) -> DiffableNdarray[Shape(4, 2), float]:

        print("In foo:", arr)
        return DiffableNdarray(np.zeros((4, 2), dtype=float))

    foo(my_str="Hello", arr=DiffableNdarray(np.zeros((2, 4), dtype=float)))
