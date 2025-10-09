import numpy as np
from gsp.types.diffable_ndarray.diffable_ndarray import DiffableNdarray


def test_diffable_ndarray_setitem_and_diff_tracking() -> None:
    # Create a 4x4 DiffableNdarray initialized with zeros
    arr = DiffableNdarray(np.zeros((4, 4), dtype=int))
    # The array should not be marked as modified initially
    assert arr.is_modified() is False

    # Modify two elements in the array
    arr[1, 2] = 7
    arr[2, 1] = 8

    # The array should now be marked as modified
    assert arr.is_modified() is True

    # Get the slices covering the modified region
    slices = arr.get_diff_slices()
    assert slices == (slice(1, 3), slice(1, 3))

    # Get the data corresponding to the modified region
    diff = arr.get_diff_data()
    assert np.array_equal(diff, arr[1:3, 1:3])


def test_diffable_ndarray_clear_diff() -> None:
    # Create a 3x3 DiffableNdarray initialized with zeros
    arr = DiffableNdarray(np.zeros((3, 3), dtype=int))
    # Modify one element in the array
    arr[0, 0] = 1
    # The array should now be marked as modified
    assert arr.is_modified() is True
    # The diff slices should cover only the modified element
    assert arr.get_diff_slices() == (slice(0, 1), slice(0, 1))
    # Clear the diff tracking
    arr.clear_diff()
    # The array should no longer be marked as modified
    assert arr.is_modified() is False


def test_diffable_ndarray_apply_patch() -> None:
    # Create a 3x3 DiffableNdarray initialized with zeros
    arr = DiffableNdarray(np.zeros((3, 3), dtype=int))
    # Define the patch slices and patch data to apply
    patch_slices = (slice(0, 2), slice(0, 2))
    patch_data = np.array([[1, 2], [3, 4]])
    # Apply the patch to the array
    arr.apply_patch(patch_slices, patch_data)
    # Check that the array has been updated correctly
    assert np.array_equal(arr, np.array([[1, 2, 0], [3, 4, 0], [0, 0, 0]]))
    # The array should be marked as modified
    assert arr.is_modified() is True
    # The diff slices should match the patch slices
    assert arr.get_diff_slices() == patch_slices
    # The diff data should match the patch data
    assert np.array_equal(arr.get_diff_data(), patch_data)


def test_diffable_ndarray_no_modifications() -> None:
    arr = DiffableNdarray(np.zeros((2, 2), dtype=int))

    # Initially, the array should not be marked as modified
    assert arr.is_modified() is False

    # Attempting to get diff slices or data should raise an assertion error
    try:
        arr.get_diff_slices()
    except AssertionError as e:
        assert str(e) == "No modifications to get diff slices from (use is_modified() to check)"
    else:
        assert False, "Expected an AssertionError when getting diff data from unmodified array"

    # Attempting to get diff data should raise an assertion error
    try:
        arr.get_diff_data()
    except AssertionError as e:
        assert str(e) == "No modifications to get diff data from (use is_modified() to check)"
    else:
        assert False, "Expected an AssertionError when getting diff data from unmodified array"


def test_diffable_ndarray_copy() -> None:
    # Create a DiffableNdarray
    arr = DiffableNdarray(np.zeros((2, 2), dtype=int))

    # Modify the array
    arr[0, 0] = 1
    arr[1, 1] = 2
    # Check if the original array is marked as modified
    assert arr.is_modified() is True
    # Create a copy of the array
    arr_copy = arr.copy()

    # Clear the diff tracking in the original array
    arr.clear_diff()

    # Check if the copied array is equal to the original and also marked as modified
    assert np.array_equal(arr_copy, arr) is True, "Copied array should be equal to the original"
    assert arr_copy.is_modified() is True, "Copied array should be marked as modified"

    # Modify the copied array and check it is different from the original
    arr_copy[0, 1] = 3
    assert arr.is_modified() is False, "Original array should not be marked as modified after modifying the copy"
    assert np.array_equal(arr, np.array([[1, 0], [0, 2]])) is True, "Original array should remain unchanged"
    assert np.array_equal(arr_copy, np.array([[1, 3], [0, 2]])) is True, "Copied array should reflect its own modifications"
