from __future__ import annotations

import typing

import numpy as np

from gsp.transform.transform_link_base import TransformLinkBase
from gsp.types.diffable_ndarray.diffable_ndarray import DiffableNdarray


class Shape:
    """Simple value object capturing an ndarray shape."""

    __slots__ = ("dims",)

    def __init__(self, *dims: int) -> None:
        if not dims:
            raise ValueError("Shape requires at least one dimension")
        if any(not isinstance(dim, int) or dim < 0 for dim in dims):
            raise ValueError("Shape dimensions must be non-negative integers")
        self.dims: tuple[int, ...] = tuple(dims)

    def __iter__(self) -> typing.Iterator[int]:
        return iter(self.dims)

    def __len__(self) -> int:
        return len(self.dims)

    def __repr__(self) -> str:
        dims = ", ".join(str(dim) for dim in self.dims)
        return f"Shape({dims})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Shape):
            return False
        return self.dims == other.dims

    def __hash__(self) -> int:
        return hash(self.dims)


class _SuperTypeMeta(type):
    """Metaclass implementing ``isinstance(obj, SuperType)`` as a runtime union with optional shape checks."""

    _allowed_types = (np.ndarray, DiffableNdarray, TransformLinkBase)

    def __instancecheck__(cls, instance: object) -> bool:  # type: ignore[override]
        if not isinstance(instance, cls._allowed_types):
            return False

        shape_constraint = getattr(cls, "_shape", None)
        if shape_constraint is None:
            return True

        if isinstance(instance, (np.ndarray, DiffableNdarray)):
            return tuple(instance.shape) == shape_constraint

        if isinstance(instance, TransformLinkBase):
            inferred_shape = getattr(instance, "shape", None)
            if inferred_shape is None:
                return False
            if isinstance(inferred_shape, tuple):
                return tuple(inferred_shape) == shape_constraint
        return False

    def __getitem__(cls, params: Shape | tuple[int, ...]) -> type:
        shape = cls._normalize_shape_param(params)

        cache = getattr(cls, "_shape_cache", {})
        if shape in cache:
            return cache[shape]

        name = f"{cls.__name__}[{', '.join(str(dim) for dim in shape)}]"
        parametrised = type(cls)(name, (cls,), {"_shape": shape})
        cache = dict(cache)
        cache[shape] = parametrised
        setattr(cls, "_shape_cache", cache)
        return parametrised

    @staticmethod
    def _normalize_shape_param(params: Shape | tuple[int, ...]) -> tuple[int, ...]:
        if isinstance(params, Shape):
            return params.dims
        if isinstance(params, tuple) and all(isinstance(dim, int) for dim in params):
            return params
        raise TypeError("SuperType[...] expects a Shape or a tuple of integers")


if typing.TYPE_CHECKING:

    @typing.runtime_checkable
    class SuperType(typing.Protocol):
        @classmethod
        def __class_getitem__(cls, params: Shape | tuple[int, ...]) -> type["SuperType"]: ...

else:

    class SuperType(metaclass=_SuperTypeMeta):
        """Runtime type that behaves like ``np.ndarray | DiffableNdarray | TransformLinkBase`` with optional shape."""

        _shape: tuple[int, ...] | None = None
        _shape_cache: dict[tuple[int, ...], type] = {}


if __name__ == "__main__":
    diffable: SuperType[Shape(2, 3)] = DiffableNdarray(np.arange(4).reshape(2, 2))
    ndarray: SuperType[Shape(2, 3)] = np.arange(3)
    transform: SuperType[Shape(2, 3)] = TransformLinkBase()

    shaped_diffable: SuperType[Shape(2, 3)] = DiffableNdarray(np.arange(6).reshape(2, 3))

    assert isinstance(diffable, SuperType)
    assert isinstance(ndarray, SuperType)
    assert isinstance(transform, SuperType)
    assert not isinstance(object(), SuperType)

    # assert isinstance(shaped_diffable, SuperType[Shape(2, 3)])
    # assert isinstance(shaped_diffable, SuperType[(2, 3)])
    assert not isinstance(shaped_diffable, SuperType[Shape(3, 2)])
    # assert not isinstance(transform, SuperType[Shape(2, 3)])

    print("All SuperType isinstance checks passed.")

    def foo(arr: SuperType[(2, 3)]) -> SuperType[Shape(2, 3)]:
        print("in foo arr=", arr)
        return arr

    foo_result = foo(shaped_diffable)
    assert isinstance(foo_result, SuperType[Shape(2, 3)])
