from dataclasses import dataclass
import numpy as np
import typing
from tmp.ndarray_like_type.diffable_ndarray_typing import DiffableNdarrayFake, DiffableNdarrayShape, DiffableNdarrayDtype, DiffableNdarrayTyping


# =============================================================================
#  Decorator to check function arguments and return types against DiffableNdarrayTyping annotations
# =============================================================================
def diffable_ndarray_checker(func) -> typing.Callable[..., typing.Any]:
    """
    A decorator to check function arguments and return types against DiffableNdarrayTyping annotations.
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

    def diffable_ndarray_checker_wrapper(*args, **kwargs):
        annotations = func.__annotations__

        # =============================================================================
        # Check argument types
        # =============================================================================
        for annotated_name, annotation in annotations.items():
            # Skip return annotation now, do it after the function call
            if annotated_name == "return":
                continue

            # check only DiffableNdarrayTyping annotations
            if isinstance(annotation, DiffableNdarrayTyping) is False:
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

        if "return" in annotations:
            annotation = annotations["return"]

            # check only DiffableNdarrayTyping annotations
            if isinstance(annotation, DiffableNdarrayTyping) is True:
                # perform the instance check
                is_instance = annotation.__instancecheck__(returned_value, throw_exception=True, exception_prefix="Return value: ")
                # sanity check
                assert is_instance == True, f"PANIC: should never be reached, as __instancecheck__ should have thrown an exception if False"

        # return the original function's return value
        return returned_value

    return diffable_ndarray_checker_wrapper


###############################################################################
#   Example usage
#
if __name__ == "__main__":
    Shape = DiffableNdarrayShape
    Dtype = DiffableNdarrayDtype

    @diffable_ndarray_checker
    def foo_typed_args(my_str: str, arr: DiffableNdarrayFake[Shape(2, 4), int]) -> None:

        print("In foo:", arr)
        return None

    @diffable_ndarray_checker
    def foo_typed_return(my_str: str, arr) -> DiffableNdarrayFake[Shape(4, 2), float]:
        print("In foo_with_return")
        return arr

    # =============================================================================
    # Test various correct usages for @diffable_ndarray_checker decorator
    # =============================================================================

    # correct usage - typed args
    foo_typed_args(my_str="Hello", arr=DiffableNdarrayFake(np.zeros((2, 4), dtype=int)))

    # correct usage - typed return
    returned = foo_typed_return(my_str="Hello", arr=DiffableNdarrayFake(np.zeros((4, 2), dtype=float)))
    assert isinstance(returned, DiffableNdarrayFake[Shape(4, 2), float])

    # =============================================================================
    # Test various incorrect usages for @diffable_ndarray_checker decorator
    # =============================================================================
    try:
        # wrong argument shape
        foo_typed_args(my_str="Hello", arr=DiffableNdarrayFake(np.zeros((3, 4), dtype=float)))
        assert False, "Expected TypeError for wrong shape"
    except TypeError as e:
        print("Caught expected TypeError for wrong shape:", e)

    try:
        # wrong argument dtype
        foo_typed_args(my_str="Hello", arr=DiffableNdarrayFake(np.zeros((2, 4), dtype=float)))
        assert False, "Expected TypeError for wrong dtype"
    except TypeError as e:
        print("Caught expected TypeError for wrong dtype:", e)

    try:
        # wrong return shape
        foo_typed_return(my_str="Hello", arr=DiffableNdarrayFake(np.zeros((2, 4), dtype=int)))
        assert False, "Expected TypeError for wrong return shape"
    except TypeError as e:
        print("Caught expected TypeError for wrong return shape:", e)

    try:
        # wrong return dtype
        foo_typed_return(my_str="Hello", arr=DiffableNdarrayFake(np.zeros((2, 4), dtype=int)))
        assert False, "Expected TypeError for wrong return dtype"
    except TypeError as e:
        print("Caught expected TypeError for wrong return dtype:", e)
