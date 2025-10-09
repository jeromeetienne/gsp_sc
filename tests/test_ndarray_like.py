# stdlib imports
import typing

# pip imports
import numpy as np

# local imports
from gsp_sc.transform.links.link_immediate import TransformLinkImmediate
from gsp_sc.types import NdarrayLikeType
from gsp_sc.types import NdarrayLikeUtils
from gsp_sc.types import DiffableNdarray, DiffableNdarrayDb


# =============================================================================
# Basic from/to_json tests on all three types : TransformLinkBase, DiffableNdarray, np.ndarray
# =============================================================================
def test_ndarray_like_to_from_json_transform() -> None:
    # define the two databases for serialization and deserialization
    diffable_ndarray_db_to_json = DiffableNdarrayDb()
    diffable_ndarray_db_from_json = DiffableNdarrayDb()

    arr_original = np.array([10, 20, 30])
    transform: NdarrayLikeType = TransformLinkImmediate(arr_original)
    serialized = NdarrayLikeUtils.to_json(transform, diffable_ndarray_db_to_json)
    deserialized_transform = typing.cast(TransformLinkImmediate, NdarrayLikeUtils.from_json(serialized, diffable_ndarray_db_from_json))
    arr_from_deserialized = deserialized_transform.run()
    assert np.array_equal(arr_from_deserialized, arr_original), "Deserialized array should match the original"


def test_ndarray_like_to_from_json_diffable_ndarray() -> None:
    # define the two databases for serialization and deserialization
    diffable_ndarray_db_to_json = DiffableNdarrayDb()
    diffable_ndarray_db_from_json = DiffableNdarrayDb()

    arr: NdarrayLikeType = DiffableNdarray(np.arange(9).reshape(3, 3))
    serialized = NdarrayLikeUtils.to_json(arr, diffable_ndarray_db_to_json)
    deserialized_arr = typing.cast(DiffableNdarray, NdarrayLikeUtils.from_json(serialized, diffable_ndarray_db_from_json))
    assert np.array_equal(deserialized_arr, arr), "Deserialized array should match the original"


def test_ndarray_like_to_from_json_plain_ndarray() -> None:
    # define the two databases for serialization and deserialization
    diffable_ndarray_db_to_json = DiffableNdarrayDb()
    diffable_ndarray_db_from_json = DiffableNdarrayDb()

    arr: NdarrayLikeType = np.arange(9).reshape(3, 3)
    serialized = NdarrayLikeUtils.to_json(arr, diffable_ndarray_db_to_json)
    deserialized_arr = typing.cast(np.ndarray, NdarrayLikeUtils.from_json(serialized, diffable_ndarray_db_from_json))
    assert np.array_equal(deserialized_arr, arr), "Deserialized array should match the original"


# =============================================================================
# DiffableNdarray specific tests
# =============================================================================


def test_ndarray_like_diffable_ndarray_to_from_json_zero_modification() -> None:
    # define the two databases for serialization and deserialization
    diffable_ndarray_db_to_json = DiffableNdarrayDb()
    diffable_ndarray_db_from_json = DiffableNdarrayDb()

    arr: NdarrayLikeType = DiffableNdarray(np.arange(9).reshape(3, 3))
    arr[2, 2] = 100

    # Serialize the original array
    serialized1 = NdarrayLikeUtils.to_json(arr, diffable_ndarray_db_to_json)

    # Deserialize the original array
    deserialized1 = typing.cast(DiffableNdarray, NdarrayLikeUtils.from_json(serialized1, diffable_ndarray_db_from_json))
    assert deserialized1.get_uuid() != arr.get_uuid(), "UUIDs should not match after deserialization"
    assert deserialized1.is_modified() == False, "Deserialized array should not be marked as modified"
    assert np.array_equal(deserialized1, arr), "Deserialized array should match the original"

    # Dont modify the original array
    assert arr.is_modified() == False, "Array should not be marked as modified"

    # Serialize the modified array
    serialized2 = NdarrayLikeUtils.to_json(arr, diffable_ndarray_db_to_json)
    assert arr.is_modified() == False, "Array should be unmodified after serialization"

    # Deserialize the modified array
    deserialized_arr_2 = typing.cast(DiffableNdarray, NdarrayLikeUtils.from_json(serialized2, diffable_ndarray_db_from_json))
    assert np.array_equal(deserialized_arr_2, arr), "Deserialized array should match the modified original"
    assert deserialized_arr_2.get_uuid() != arr.get_uuid(), "UUIDs should not match after deserialization"
    assert deserialized_arr_2.get_uuid() == deserialized1.get_uuid(), "UUIDs should match the first deserialized array"


def test_ndarray_like_diffable_ndarray_to_from_json_one_modification() -> None:
    # define the two databases for serialization and deserialization
    diffable_ndarray_db_to_json = DiffableNdarrayDb()
    diffable_ndarray_db_from_json = DiffableNdarrayDb()

    arr: NdarrayLikeType = DiffableNdarray(np.arange(9).reshape(3, 3))
    arr[2, 2] = 100

    # Serialize the original array
    serialized1 = NdarrayLikeUtils.to_json(arr, diffable_ndarray_db_to_json)

    # Deserialize the original array
    deserialized1 = typing.cast(DiffableNdarray, NdarrayLikeUtils.from_json(serialized1, diffable_ndarray_db_from_json))
    assert deserialized1.get_uuid() != arr.get_uuid(), "UUIDs should not match after deserialization"
    assert deserialized1.is_modified() == False, "Deserialized array should not be marked as modified"
    assert np.array_equal(deserialized1, arr), "Deserialized array should match the original"

    # Modify the original array to create a diff
    arr[1, 1] = -10  # Modify the array to create a diff
    assert arr.is_modified() == True, "Array should be marked as modified"

    # Serialize the modified array
    serialized2 = NdarrayLikeUtils.to_json(arr, diffable_ndarray_db_to_json)
    assert arr.is_modified() == False, "Array should be unmodified after serialization"

    # Deserialize the modified array
    deserialized_arr_2 = typing.cast(DiffableNdarray, NdarrayLikeUtils.from_json(serialized2, diffable_ndarray_db_from_json))
    assert np.array_equal(deserialized_arr_2, arr), "Deserialized array should match the modified original"
    assert deserialized_arr_2.get_uuid() != arr.get_uuid(), "UUIDs should not match after deserialization"
    assert deserialized_arr_2.get_uuid() == deserialized1.get_uuid(), "UUIDs should match the first deserialized array"


def test_ndarray_like_diffable_ndarray_to_from_json_full_modification() -> None:
    # define the two databases for serialization and deserialization
    diffable_ndarray_db_to_json = DiffableNdarrayDb()
    diffable_ndarray_db_from_json = DiffableNdarrayDb()

    arr: NdarrayLikeType = DiffableNdarray(np.arange(9).reshape(3, 3))
    arr[2, 2] = 100

    # Serialize the original array
    serialized1 = NdarrayLikeUtils.to_json(arr, diffable_ndarray_db_to_json)

    # Deserialize the original array
    deserialized1 = typing.cast(DiffableNdarray, NdarrayLikeUtils.from_json(serialized1, diffable_ndarray_db_from_json))
    assert deserialized1.get_uuid() != arr.get_uuid(), "UUIDs should not match after deserialization"
    assert deserialized1.is_modified() == False, "Deserialized array should not be marked as modified"
    assert np.array_equal(deserialized1, arr), "Deserialized array should match the original"

    # Modify the original array completly
    arr[:] = np.arange(100, 109).reshape(3, 3)
    assert arr.is_modified() == True, "Array should be marked as modified"

    # Serialize the modified array
    serialized2 = NdarrayLikeUtils.to_json(arr, diffable_ndarray_db_to_json)
    assert arr.is_modified() == False, "Array should be unmodified after serialization"

    # Deserialize the modified array
    deserialized_arr_2 = typing.cast(DiffableNdarray, NdarrayLikeUtils.from_json(serialized2, diffable_ndarray_db_from_json))
    assert np.array_equal(deserialized_arr_2, arr), "Deserialized array should match the modified original"
    assert deserialized_arr_2.get_uuid() != arr.get_uuid(), "UUIDs should not match after deserialization"
    assert deserialized_arr_2.get_uuid() == deserialized1.get_uuid(), "UUIDs should match the first deserialized array"
