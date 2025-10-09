from dataclasses import dataclass
import numpy as np
import typing


# =============================================================================
#   Fake DiffableNdarray and its typing support for demonstration purposes
# =============================================================================
class DiffableNdarrayFake(np.ndarray):
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
        return DiffableNdarrayTyping(cls, params)


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


class DiffableNdarrayTyping:
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


###############################################################################
#   Example usage
#
if __name__ == "__main__":
    Shape = DiffableNdarrayShape
    Dtype = DiffableNdarrayDtype

    arr: DiffableNdarrayFake[Shape(2, 2), int] = DiffableNdarrayFake(np.zeros((2, 2), dtype=float))

    assert isinstance(arr, DiffableNdarrayFake[Shape(2, 2), float]), "Expected instance of DiffableNdarray[Shape(2, 2), float]"

    # test wrong shape
    arr_bad_shape = DiffableNdarrayFake(np.zeros((3, 2), dtype=float))
    assert isinstance(arr_bad_shape, DiffableNdarrayFake[Shape(2, 2), float]), "Expected instance of DiffableNdarray[Shape(2, 2), float]"

    # test wrong dtype
    arr_bad_dtype = DiffableNdarrayFake(np.zeros((2, 2), dtype=int))
    assert isinstance(arr_bad_dtype, DiffableNdarrayFake[Shape(2, 2), float]), "Expected instance of DiffableNdarray[Shape(2, 2), float]"

    print("All checks passed.")
