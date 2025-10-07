from typing import Any
import numpy as np

from ..transform_link_base import TransformLinkBase
from ..transform_link_db import TransformLinkDB

class TransformLinkAssertShape(TransformLinkBase):

    def __init__(self, expected_shape: tuple[int, ...]):
        """
        Ensure the input array has the specified shape.
        """

        super().__init__()

        self.__expected_shape = expected_shape
        """The desired shape of the array"""

    def _run(self, np_array: np.ndarray) -> np.ndarray:
        if np_array.shape != self.__expected_shape:
            raise ValueError(f"Input array shape {np_array.shape} does not match the expected shape {self.__expected_shape}")
        
        return np_array 
    
    def _to_json(self) -> dict[str, Any]:
        return {
            "type": "TransformAssertShape",
            "expected_shape": self.__expected_shape
        }
    
    @staticmethod
    def _from_json(json_dict: dict[str, Any]) -> TransformLinkBase:
        expected_shape = tuple(json_dict["expected_shape"])
        return TransformLinkAssertShape(expected_shape)

# Register the TransformAssertShape class in the TransformLinkDB
TransformLinkDB.add_link("TransformAssertShape", TransformLinkAssertShape)