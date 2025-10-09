from typing import Any
import numpy as np

from ..transform_link_base import TransformLinkBase
from ..transform_registry import TransformRegistry


class TransformLinkImmediate(TransformLinkBase):

    def __init__(self, np_array: np.ndarray) -> None:
        """
        Load data from a .npy file.
        """
        super().__init__()

        self.__np_array = np_array

    def _run(self, np_array: np.ndarray) -> np.ndarray:
        # Do nothing and just return the data

        return self.__np_array

    # Serialization methods

    def _to_json(self) -> dict[str, Any]:
        return {"type": "TransformImmediate", "np_array": self.__np_array.tolist()}

    @staticmethod
    def _from_json(json_dict: dict[str, Any]) -> TransformLinkBase:
        np_array = np.array(json_dict["np_array"])
        return TransformLinkImmediate(np_array)


# Register the TransformImmediate class in the TransformLinkDB
TransformRegistry.register_link("TransformImmediate", TransformLinkImmediate)
