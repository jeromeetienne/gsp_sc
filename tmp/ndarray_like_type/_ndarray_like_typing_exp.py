from dataclasses import dataclass
from typing import TYPE_CHECKING
import typing

# from gsp_sc.types import NdarrayLikeVariableType
from gsp.types import DiffableNdarray
from gsp.transform import TransformLinkImmediate, TransformLinkBase
import numpy as np


class MyTypeMeta(type):

    def __getitem__(cls, params):
        # Define a classmethod for __class_getitem__ without using a lambda
        @classmethod
        def class_getitem(inner_cls, x):
            return inner_cls[x]

        # Return a parameterized type object with the params stored
        my_type = type(
            f"Parameterized{cls.__name__}",
            (cls,),
            {
                "_params": params,
                "__class_getitem__": class_getitem,
                "__metaclass__": cls,
            },
        )
        return my_type

    def __instancecheck__(self, obj):
        # Custom logic for isinstance(obj, MyType[...])
        params = getattr(self, "_params", None)
        print(f"Checking {obj=} against MyType with params {params=}")
        # Example: accept any object, just for demonstration
        return True


@dataclass
class NdarrayLikeShape:
    def __init__(self, *dims: int):
        self.shape = dims


@dataclass
class NdarrayLikeDtype:
    def __init__(self, dtype: type):
        self.dtype = dtype


class NdarrayLikeTyping(metaclass=MyTypeMeta):
    Shape = NdarrayLikeShape
    Dtype = NdarrayLikeDtype

    def __class_getitem__(cls, params):
        """Expose a class-level __class_getitem__ so static type checkers
        (pyright/mypy) recognize subscription like ``NdarrayLikeTyping[... ]``.

        Delegate to the metaclass implementation to preserve runtime
        behaviour provided by MyTypeMeta.__getitem__.
        """
        return MyTypeMeta.__getitem__(cls, params)


NdarrayLikeVar = TransformLinkBase | DiffableNdarray | np.ndarray

# =============================================================================
#
# =============================================================================
if __name__ == "__main__":
    Shape = NdarrayLikeTyping.Shape
    Dtype = NdarrayLikeTyping.Dtype

    var_np_array: NdarrayLikeVar = np.array([[1, 2], [3, 4]])
    var_diffable_array: NdarrayLikeVar = DiffableNdarray(np.array([[1, 2], [3, 4]]))
    var_transform_link: NdarrayLikeVar = TransformLinkImmediate(np.array([[1, 2], [3, 4]]))

    # var_other: NdarrayLikeType = "Hello"

    arr = np.array([[1, 2], [3, 4]])
    assert isinstance(arr, NdarrayLikeTyping[int, Shape(2, 2)]), "np.ndarray should be a valid NdarrayLikeVariableType"

    def myFunction(x: NdarrayLikeTyping[int, Shape(2, 2)], y: str) -> NdarrayLikeTyping[int]:
        print("In myFunction:", x, y)
        return x

    myFunction(arr, "Hello")
