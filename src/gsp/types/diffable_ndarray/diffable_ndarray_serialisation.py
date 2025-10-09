# stdlib imports
from typing import Any, Literal
from dataclasses import dataclass, field

# pip imports
import numpy as np

# local imports
from .diffable_ndarray import DiffableNdarray


@dataclass
class DiffableNdarrayDb:
    to_json_db: dict[str, DiffableNdarray] = field(default_factory=dict)
    """A simple in-memory database to store DiffableNdarray instances by their UUIDs during serialization."""
    from_json_db: dict[str, DiffableNdarray] = field(default_factory=dict)
    """A simple in-memory database to store DiffableNdarray instances by their UUIDs during deserialization."""


class DiffableNdarraySerialisationError(Exception):
    """Custom exception for DiffableNdarray serialization errors."""

    pass


class DiffableNdarraySerialisation:

    @staticmethod
    def reset_db(diffable_db: DiffableNdarrayDb) -> None:
        """
        Clear both the to_json and from_json databases.
        """
        diffable_db.to_json_db.clear()
        diffable_db.from_json_db.clear()

    # =============================================================================
    # JSON serialisation
    # =============================================================================
    @staticmethod
    def to_json(
        diff_ndarray: DiffableNdarray, diff_db: DiffableNdarrayDb
    ) -> dict[str, Any]:
        """
        Serialize the DiffableNdarray to a JSON-serializable dictionary.
        """

        is_in_db = diff_ndarray.get_uuid() in diff_db.to_json_db

        # =============================================================================
        # if not in the database, we need to serialize the full array
        # =============================================================================

        # If not in the database, serialize the whole array
        if not is_in_db:
            # Add to the database to track it
            diff_db.to_json_db[diff_ndarray.get_uuid()] = diff_ndarray
            # clear the modified flag since we are serializing the full array
            diff_ndarray.clear_diff()
            # Serialize the entire array
            json_dict = {
                "uuid": diff_ndarray.get_uuid(),
                "slices": None,
                "data": diff_ndarray.tolist(),
            }
            return json_dict

        # =============================================================================
        # Here diff_ndarray is in the database, if no modifications, we return a minimal json
        # =============================================================================

        if diff_ndarray.is_modified() is False:
            json_dict = {
                "uuid": diff_ndarray.get_uuid(),
                "slices": None,
                "data": None,
            }
            return json_dict

        # =============================================================================
        # Here there are modifications to serialize
        # =============================================================================

        assert (
            diff_ndarray.is_modified() is True
        ), "There should be modifications to serialize"

        # There are modifications, serialize only the delta region
        diff_slices = DiffableNdarray.get_diff_slices(diff_ndarray)
        diff_data = DiffableNdarray.get_diff_data(diff_ndarray)

        # clear the modified flag since we are serializing the diff
        diff_ndarray.clear_diff()

        # Ensure the delta_region is valid
        assert (
            diff_data is not None
        ), "diff region should not be None if delta slices exists"

        # Serialize the slices and the delta region
        json_dict = {
            "uuid": diff_ndarray.get_uuid(),
            "slices": DiffableNdarraySerialisation._slices_to_json(diff_slices),
            "data": diff_data.tolist(),
        }
        return json_dict

    # =============================================================================
    # JSON deserialisation
    # =============================================================================

    @staticmethod
    def from_json(
        json_dict: dict[str, Any], diffable_db: DiffableNdarrayDb
    ) -> "DiffableNdarray":
        """
        Deserialize a JSON-serializable dictionary back to a DiffableNdarray.
        """

        # Check if the array is already in the database
        is_in_db = json_dict["uuid"] in diffable_db.from_json_db

        # Determine the type of patch
        is_patch_full_data = (
            json_dict["slices"] is None and json_dict["data"] is not None
        )
        is_patch_diff_data = (
            json_dict["slices"] is not None and json_dict["data"] is not None
        )
        is_patch_empty = json_dict["slices"] is None and json_dict["data"] is None

        # Sanity check - only one of the above should be true
        assert (
            sum([is_patch_full_data, is_patch_empty, is_patch_diff_data]) == 1
        ), "PANIC is_patch_* logic error"

        # If it is a full data patch
        if is_patch_full_data:
            if is_in_db:
                # update the existing array in place
                recv_arr = diffable_db.from_json_db[json_dict["uuid"]]
                recv_arr[:] = np.array(json_dict["data"])
                # clear the modifications since we received the full data
                recv_arr.clear_diff()
                # return it
                return recv_arr
            else:
                # create a new array
                new_arr = DiffableNdarray(np.array(json_dict["data"]))
                # add to the database
                diffable_db.from_json_db[json_dict["uuid"]] = new_arr
                # return it
                return new_arr

        # if it is an empty patch ?
        if is_patch_empty:
            if not is_in_db:
                raise DiffableNdarraySerialisationError(
                    "DiffableNdarray not found in database, cannot apply empty patch"
                )
            else:
                # get the existing array as from the database
                existing_arr = diffable_db.from_json_db[json_dict["uuid"]]
                # return it
                return existing_arr

        # if it is a diff patch ?
        if is_patch_diff_data:
            if not is_in_db:
                raise DiffableNdarraySerialisationError(
                    "DiffableNdarray not found in database, cannot apply diff patch"
                )
            else:
                # get the existing array as from the database
                existing_arr = diffable_db.from_json_db[json_dict["uuid"]]
                # deserialize the slices and the delta region
                diff_slices = DiffableNdarraySerialisation._slices_from_json(
                    json_dict["slices"]
                )
                diff_data = np.array(json_dict["data"])
                # apply the diff patch to the existing array
                existing_arr.apply_patch(diff_slices, diff_data)
                # return it
                return existing_arr

        raise DiffableNdarraySerialisationError(
            "DiffableNdarray - Invalid patch format"
        )

    @staticmethod
    def get_patch_type(
        json_dict: dict[str, Any],
    ) -> Literal["full_data", "diff_data", "empty"]:
        """
        Analyse the type of patch represented by the JSON dictionary.

        Returns:
            "full_data" if the patch contains full data,
            "diff_data" if the patch contains a diff,
            "empty" if the patch is empty (no data, no slices).
        """

        # Determine the type of patch
        is_patch_full_data = (
            json_dict["slices"] is None and json_dict["data"] is not None
        )
        is_patch_diff_data = (
            json_dict["slices"] is not None and json_dict["data"] is not None
        )
        is_patch_empty = json_dict["slices"] is None and json_dict["data"] is None

        # Sanity check - only one of the above should be true
        assert (
            sum([is_patch_full_data, is_patch_empty, is_patch_diff_data]) == 1
        ), "PANIC is_patch_* logic error"

        if is_patch_full_data:
            return "full_data"
        if is_patch_empty:
            return "empty"
        if is_patch_diff_data:
            return "diff_data"

        raise DiffableNdarraySerialisationError("Invalid patch format")

    ###############################################################################
    #   Slice to/from JSON
    #
    @staticmethod
    def _slices_to_json(slices: tuple[slice, ...]) -> dict[str, Any]:
        """
        Convert a tuple of slices to a JSON-serializable dictionary.
        """
        slice_dict = {"slices": []}
        for _slice in slices:
            assert _slice.step in (
                None,
                1,
            ), "Only slices with step=1 or step=None are supported"
            slice_dict["slices"].append(
                {
                    "start": _slice.start,
                    "stop": _slice.stop,
                }
            )
        return slice_dict

    @staticmethod
    def _slices_from_json(slice_dict: dict[str, Any]) -> tuple[slice, ...]:
        """
        Convert a JSON-serializable dictionary back to a tuple of slices.
        """
        slices_arr = [
            slice(_slice["start"], _slice["stop"], None)
            for _slice in slice_dict["slices"]
        ]
        slices_tuple = tuple(slices_arr)
        return slices_tuple


###############################################################################
#   Example usage
#
if __name__ == "__main__":
    diffable_ndarray_db = DiffableNdarrayDb()

    # Example 1: Using a numpy ndarray
    arr = DiffableNdarray(np.array([[1, 2, 3], [4, 5, 6]]))
    arr[0, 0] = 10  # Modify an element

    # Serialize to JSON
    serialized_arr = DiffableNdarraySerialisation.to_json(arr, diffable_ndarray_db)
    print("Serialized DiffableNdarray 1")
    print(serialized_arr)

    # Deserialize back to DiffableNdarray
    deserialized_arr1 = DiffableNdarraySerialisation.from_json(
        serialized_arr, diffable_ndarray_db
    )
    print("Deserialized DiffableNdarray 1")
    print(deserialized_arr1)

    arr[0, 1] = 20  # Further modify an element
    # arr[1, 2] = 30  # Further modify an element

    # Serialize to JSON again
    serialized_arr2 = DiffableNdarraySerialisation.to_json(arr, diffable_ndarray_db)
    print("Serialized DiffableNdarray 2")
    print(serialized_arr2)

    # Deserialize back to DiffableNdarray
    deserialized_arr2 = DiffableNdarraySerialisation.from_json(
        serialized_arr2, diffable_ndarray_db
    )
    print("Deserialized DiffableNdarray 2")
    print(deserialized_arr2)
