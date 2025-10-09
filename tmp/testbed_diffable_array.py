from gsp.types.diffable_ndarray import DiffableNdarray
from gsp.types.diffable_ndarray_serialisation import DiffableNdarraySerialisation
import numpy as np


def test_apply_patch() -> None:
    arr = DiffableNdarray(np.arange(16).reshape(4, 4))
    arr[1, 2] = -7
    arr[2, 1] = -8

    arr2 = DiffableNdarray(np.arange(16).reshape(4, 4))
    arr2.apply_patch(arr.get_diff_slices(), arr.get_diff_data())

    assert np.array_equal(arr, arr2)


def test_workflow() -> None:
    arr = DiffableNdarray(np.arange(16).reshape(4, 4))
    arr[1, 2] = -7
    arr[2, 1] = -8

    arr_dict = DiffableNdarraySerialisation.to_json(arr)

    reconstructed_arr = None
    arr2 = DiffableNdarraySerialisation.from_json(arr_dict, previous_arr=reconstructed_arr, in_place=True)

    assert np.array_equal(arr, arr2)


if __name__ == "__main__":
    # test_apply_patch()
    # print("test_apply_patch passed")

    arr = DiffableNdarray(np.arange(16).reshape(4, 4))
    print("Initial array:\n", arr)
