# stdlib imports
import typing

# pip imports
import numpy as np

# local imports
from gsp.types import DiffableNdarray
from gsp.types import DiffableNdarraySerialisation, DiffableNdarrayDb


def test_diffable_ndarray_to_from_json_zero_modification() -> None:
    diffable_ndarray_db = DiffableNdarrayDb()
    arr = DiffableNdarray(np.arange(9).reshape(3, 3))
    arr[2, 2] = 100

    # Serialize the original array
    serialized1 = DiffableNdarraySerialisation.to_json(arr, diffable_ndarray_db)

    # Deserialize the original array
    deserialized1 = typing.cast(DiffableNdarray, DiffableNdarraySerialisation.from_json(serialized1, diffable_ndarray_db))
    assert deserialized1.get_uuid() != arr.get_uuid(), "UUIDs should not match after deserialization"
    assert deserialized1.is_modified() == False, "Deserialized array should not be marked as modified"
    assert np.array_equal(deserialized1, arr), "Deserialized array should match the original"

    # Dont modify the original array
    assert arr.is_modified() == False, "Array should not be marked as modified"

    # Serialize the modified array
    serialized2 = DiffableNdarraySerialisation.to_json(arr, diffable_ndarray_db)
    assert arr.is_modified() == False, "Array should be unmodified after serialization"

    # Deserialize the modified array
    deserialized_arr_2 = typing.cast(DiffableNdarray, DiffableNdarraySerialisation.from_json(serialized2, diffable_ndarray_db))
    assert np.array_equal(deserialized_arr_2, arr), "Deserialized array should match the modified original"
    assert deserialized_arr_2.get_uuid() != arr.get_uuid(), "UUIDs should not match after deserialization"
    assert deserialized_arr_2.get_uuid() == deserialized1.get_uuid(), "UUIDs should match the first deserialized array"


def test_diffable_ndarray_to_from_json_one_modification() -> None:
    diffable_ndarray_db = DiffableNdarrayDb()
    arr = DiffableNdarray(np.arange(9).reshape(3, 3))
    arr[2, 2] = 100

    # Serialize the original array
    serialized1 = DiffableNdarraySerialisation.to_json(arr, diffable_ndarray_db)

    # Deserialize the original array
    deserialized1 = typing.cast(DiffableNdarray, DiffableNdarraySerialisation.from_json(serialized1, diffable_ndarray_db))
    assert deserialized1.get_uuid() != arr.get_uuid(), "UUIDs should not match after deserialization"
    assert deserialized1.is_modified() == False, "Deserialized array should not be marked as modified"
    assert np.array_equal(deserialized1, arr), "Deserialized array should match the original"

    # Modify the original array to create a diff
    arr[1, 1] = -10  # Modify the array to create a diff
    assert arr.is_modified() == True, "Array should be marked as modified"

    # Serialize the modified array
    serialized2 = DiffableNdarraySerialisation.to_json(arr, diffable_ndarray_db)
    assert arr.is_modified() == False, "Array should be unmodified after serialization"

    # Deserialize the modified array
    deserialized_arr_2 = typing.cast(DiffableNdarray, DiffableNdarraySerialisation.from_json(serialized2, diffable_ndarray_db))
    assert np.array_equal(deserialized_arr_2, arr), "Deserialized array should match the modified original"
    assert deserialized_arr_2.get_uuid() != arr.get_uuid(), "UUIDs should not match after deserialization"
    assert deserialized_arr_2.get_uuid() == deserialized1.get_uuid(), "UUIDs should match the first deserialized array"


def test_diffable_ndarray_to_from_json_full_modification() -> None:
    diffable_ndarray_db = DiffableNdarrayDb()
    arr = DiffableNdarray(np.arange(9).reshape(3, 3))
    arr[2, 2] = 100

    # Serialize the original array
    serialized1 = DiffableNdarraySerialisation.to_json(arr, diffable_ndarray_db)

    # Deserialize the original array
    deserialized1 = typing.cast(DiffableNdarray, DiffableNdarraySerialisation.from_json(serialized1, diffable_ndarray_db))
    assert deserialized1.get_uuid() != arr.get_uuid(), "UUIDs should not match after deserialization"
    assert deserialized1.is_modified() == False, "Deserialized array should not be marked as modified"
    assert np.array_equal(deserialized1, arr), "Deserialized array should match the original"

    # Modify the original array completly
    arr[:] = np.arange(100, 109).reshape(3, 3)
    assert arr.is_modified() == True, "Array should be marked as modified"

    # Serialize the modified array
    serialized2 = DiffableNdarraySerialisation.to_json(arr, diffable_ndarray_db)
    assert arr.is_modified() == False, "Array should be unmodified after serialization"

    # Deserialize the modified array
    deserialized_arr_2 = typing.cast(DiffableNdarray, DiffableNdarraySerialisation.from_json(serialized2, diffable_ndarray_db))
    assert np.array_equal(deserialized_arr_2, arr), "Deserialized array should match the modified original"
    assert deserialized_arr_2.get_uuid() != arr.get_uuid(), "UUIDs should not match after deserialization"
    assert deserialized_arr_2.get_uuid() == deserialized1.get_uuid(), "UUIDs should match the first deserialized array"
