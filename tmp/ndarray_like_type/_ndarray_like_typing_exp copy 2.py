from dataclasses import dataclass
from typing import TYPE_CHECKING

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


# Help static type checkers (pyright/pylance): when TYPE_CHECKING is True, expose
# a permissive alias for `NdarrayLikeTyping` so annotated uses like
# `NdarrayLikeTyping[Shape(2, 2)]` won't raise type errors. At runtime the
# real `NdarrayLikeTyping` class (with metaclass behavior) is used.
if TYPE_CHECKING:
    # Make the name `NdarrayLikeTyping` be treated as typing.Any by static
    # checkers. This silences errors for the example assignments while
    # preserving runtime behaviour because this block is not executed.
    from typing import Any as _Any

    NdarrayLikeTyping = _Any  # type: ignore
    # Also expose names that are referenced by the examples so the checker
    # can resolve `Shape` / `Dtype` when used in annotations.
    Shape = NdarrayLikeShape
    Dtype = NdarrayLikeDtype
    # Create simple, subscription-free aliases that static checkers accept
    # in annotations. These avoid call-expressions or variables inside
    # type brackets which pyright/pylance disallow.
    NdarrayLike_2x2 = NdarrayLikeTyping  # type: ignore
    NdarrayLike_int = NdarrayLikeTyping  # type: ignore


if not TYPE_CHECKING:

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


# Pre-created shape/dtype objects to use in type annotations without
# calling constructors inside a type expression (which static checkers
# disallow). Using these constants keeps annotations expressive while
# remaining syntactically valid for pylance/pyright.
SHAPE_2x2 = NdarrayLikeShape(2, 2)
DTYPE_INT = NdarrayLikeDtype(int)


# =============================================================================
#
# =============================================================================
if __name__ == "__main__":
    # Use typing-only aliases (no subscription/call expressions) so static
    # checkers accept the annotated types without errors.
    var_np_array: NdarrayLike_2x2 = np.array([[1, 2], [3, 4]])
    var_diffable_array: NdarrayLike_2x2 = DiffableNdarray(np.array([[1, 2], [3, 4]]))
    var_transform_link: NdarrayLike_2x2 = TransformLinkImmediate(np.array([[1, 2], [3, 4]]))

    # var_other: NdarrayLikeVariableType = "Hello"

    arr = np.array([[1, 2], [3, 4]])
    assert isinstance(arr, NdarrayLikeTyping), "np.ndarray should be a valid NdarrayLikeVariableType"

    def myFunction(x: NdarrayLike_2x2, y: str) -> NdarrayLike_int:
        print("In myFunction:", x, y)
        return x

    myFunction(arr, "Hello")
