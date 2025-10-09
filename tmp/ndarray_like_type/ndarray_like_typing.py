from __future__ import annotations

import typing

import numpy as np

from gsp.transform.transform_link_base import TransformLinkBase
from gsp.types.diffable_ndarray.diffable_ndarray import DiffableNdarray


class NdarrayLikeShape:
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
        if not isinstance(other, NdarrayLikeShape):
            return False
        return self.dims == other.dims

    def __hash__(self) -> int:
        return hash(self.dims)


class NdarrayLikeDType:
    """Value object representing an ndarray dtype constraint."""

    __slots__ = ("dtype",)

    def __init__(self, dtype: typing.Any) -> None:
        try:
            self.dtype = np.dtype(dtype)
        except TypeError as exc:  # pragma: no cover - defensive
            raise ValueError(f"Unsupported dtype parameter: {dtype!r}") from exc

    def __repr__(self) -> str:
        return f"DType({self.dtype.name})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NdarrayLikeDType):
            return False
        return self.dtype == other.dtype

    def __hash__(self) -> int:
        return hash(self.dtype)


class _NdarrayLikeTypingMeta(type):
    """Metaclass implementing ``isinstance(obj, SuperType)`` as a runtime union with optional shape/dtype checks."""

    _allowed_types = (np.ndarray, DiffableNdarray, TransformLinkBase)

    def __instancecheck__(cls, instance: object) -> bool:  # type: ignore[override]
        if not isinstance(instance, cls._allowed_types):
            return False

        shape_constraint = getattr(cls, "_shape", None)
        dtype_constraint = getattr(cls, "_dtype", None)

        if shape_constraint is not None:
            if isinstance(instance, (np.ndarray, DiffableNdarray)):
                if tuple(instance.shape) != shape_constraint:
                    return False
            elif isinstance(instance, TransformLinkBase):
                inferred_shape = getattr(instance, "shape", None)
                if inferred_shape is None or not isinstance(inferred_shape, tuple) or tuple(inferred_shape) != shape_constraint:
                    return False
            else:  # pragma: no cover - defensive
                return False

        if dtype_constraint is not None:
            instance_dtype: np.dtype | None = None
            if isinstance(instance, (np.ndarray, DiffableNdarray)):
                try:
                    instance_dtype = np.dtype(getattr(instance, "dtype", None))
                except TypeError:
                    instance_dtype = None
            elif isinstance(instance, TransformLinkBase):
                inferred_dtype = getattr(instance, "dtype", None)
                try:
                    instance_dtype = np.dtype(inferred_dtype) if inferred_dtype is not None else None
                except TypeError:
                    instance_dtype = None

            if instance_dtype is None or not np.issubdtype(instance_dtype, dtype_constraint):
                return False

        return True

    def __getitem__(cls, params: typing.Any) -> type:
        shape, dtype = cls._normalize_params(params)

        cache = getattr(cls, "_param_cache", {})
        key = (shape, dtype)
        if key in cache:
            return cache[key]

        descriptor = []
        if shape is not None:
            descriptor.append(f"Shape({', '.join(str(dim) for dim in shape)})")
        if dtype is not None:
            descriptor.append(f"DType({dtype.name})")
        descriptor_str = ", ".join(descriptor) if descriptor else "Any"
        name = f"{cls.__name__}[{descriptor_str}]"

        parametrised = type(cls)(name, (cls,), {"_shape": shape, "_dtype": dtype})
        cache = dict(cache)
        cache[key] = parametrised
        setattr(cls, "_param_cache", cache)
        return parametrised

    @staticmethod
    def _is_shape_tuple(candidate: object) -> bool:
        return isinstance(candidate, tuple) and candidate != () and all(isinstance(dim, int) for dim in candidate)

    @classmethod
    def _normalize_params(cls, params: typing.Any) -> tuple[tuple[int, ...] | None, np.dtype | None]:
        # Allow passing a single parameter (shape or dtype) or a tuple of parameters
        if isinstance(params, tuple) and not cls._is_shape_tuple(params):
            param_seq = params
        else:
            param_seq = (params,)

        shape: tuple[int, ...] | None = None
        dtype: np.dtype | None = None

        for param in param_seq:
            if isinstance(param, NdarrayLikeShape):
                shape = param.dims
            elif cls._is_shape_tuple(param):
                shape = typing.cast(tuple[int, ...], param)
            elif isinstance(param, NdarrayLikeDType):
                dtype = param.dtype
            elif isinstance(param, np.dtype):
                dtype = param
            elif isinstance(param, type):
                try:
                    dtype = np.dtype(param)
                except TypeError as exc:  # pragma: no cover - defensive
                    raise TypeError(f"Unsupported dtype parameter: {param!r}") from exc
            elif param is None:
                continue
            else:
                raise TypeError("SuperType[...] expects Shape, tuple[int, ...], DType, numpy dtype or type")

        return shape, dtype


class NdarrayLikeTyping_(metaclass=_NdarrayLikeTypingMeta):
    """Runtime type that behaves like ``np.ndarray | DiffableNdarray | TransformLinkBase`` with optional shape."""

    _shape: tuple[int, ...] | None = None
    _dtype: np.dtype | None = None
    _param_cache: dict[tuple[tuple[int, ...] | None, np.dtype | None], type] = {}


# =============================================================================
# Typing support for NdarrayLikeTyping
# =============================================================================
if typing.TYPE_CHECKING:

    @typing.runtime_checkable
    class NdarrayLikeTyping(typing.Protocol):
        @classmethod
        def __class_getitem__(cls, params: typing.Any) -> type["NdarrayLikeTyping"]: ...

else:
    NdarrayLikeTyping = NdarrayLikeTyping_

# =============================================================================
# Example usage and tests
# =============================================================================
if __name__ == "__main__":
    DType = NdarrayLikeDType
    Shape = NdarrayLikeShape

    # =============================================================================
    # Create some example instances
    # =============================================================================

    diffable_any: NdarrayLikeTyping = DiffableNdarray(np.arange(4).reshape(2, 2))
    ndarray_any: NdarrayLikeTyping = np.arange(3)
    transform_any: NdarrayLikeTyping = TransformLinkBase()

    # =============================================================================
    # Check isinstance with various parametrizations
    # =============================================================================

    shaped_diffable = DiffableNdarray(np.arange(6, dtype=float).reshape(2, 3))
    shaped_diffable_f32 = DiffableNdarray(np.arange(6, dtype=np.float32).reshape(2, 3))

    assert isinstance(diffable_any, NdarrayLikeTyping)
    assert isinstance(ndarray_any, NdarrayLikeTyping)
    assert isinstance(transform_any, NdarrayLikeTyping)
    assert not isinstance(object(), NdarrayLikeTyping)

    assert isinstance(shaped_diffable, NdarrayLikeTyping[Shape(2, 3)])
    assert isinstance(shaped_diffable, NdarrayLikeTyping[(2, 3)])
    assert isinstance(shaped_diffable, NdarrayLikeTyping[DType(float)])
    assert isinstance(shaped_diffable, NdarrayLikeTyping[Shape(2, 3), float])
    assert isinstance(shaped_diffable_f32, NdarrayLikeTyping[Shape(2, 3), DType(np.float32)])
    assert not isinstance(shaped_diffable_f32, NdarrayLikeTyping[Shape(3, 2)])
    assert not isinstance(shaped_diffable_f32, NdarrayLikeTyping[DType(np.float64)])

    print("All SuperType isinstance checks passed.")

    # =============================================================================
    # Additional checks with functions
    # =============================================================================

    def accepts_shaped_float(arr: NdarrayLikeTyping[Shape(2, 3), float]) -> NdarrayLikeTyping[Shape(2, 3)]:
        print("accepts_shaped_float:", arr)
        return arr

    def accepts_any(arr: NdarrayLikeTyping) -> NdarrayLikeTyping:
        print("accepts_any:", arr)
        return arr

    def accepts_transform(arr: NdarrayLikeTyping[TransformLinkBase]) -> NdarrayLikeTyping[TransformLinkBase]:
        print("accepts_transform:", arr)
        return arr

    def returns_shaped_float() -> NdarrayLikeTyping[Shape(2, 3), float]:
        result = DiffableNdarray(np.arange(6, dtype=float).reshape(2, 3))
        print("returns_shaped_float:", result)
        return result

    foo_result = accepts_shaped_float(shaped_diffable)
    assert isinstance(foo_result, NdarrayLikeTyping[Shape(2, 3)])

    accepts_any(shaped_diffable)
    accepts_any(transform_any)

    accepts_transform(transform_any)

    returned = returns_shaped_float()
    assert isinstance(returned, NdarrayLikeTyping[Shape(2, 3), float])
