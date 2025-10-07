from os import link
import numpy as np
import typing
from typing import Any

from gsp_sc.src.transform import TransformSerialisation
# from .transform_chain import TransformLinkBase
from .transform_link_base import TransformLinkBase

class TransformOrNdarray:
    """
    Utility class to handle inputs that can be either a numpy ndarray or a TransformLinkBase.

    Used a lot in the visuals
    """

    @staticmethod
    def to_json(data: np.ndarray | TransformLinkBase) -> list[dict[str, Any]] | list:
        """
        Convert the input data to a JSON-serializable format.
        """
        if(isinstance(data, TransformLinkBase)):
            link_head = typing.cast(TransformLinkBase, data)
            link_head_json = TransformSerialisation.to_json(link_head)
            return link_head_json
        elif(isinstance(data, np.ndarray)):
            array_np = typing.cast(np.ndarray, data)
            return array_np.tolist()
        else:
            raise TypeError("Input must be either a numpy ndarray or a TransformLinkBase instance.")
        
    @staticmethod
    def from_json(data: list[dict[str, Any]] | list) -> TransformLinkBase | np.ndarray:
        """
        Convert a JSON-serializable format to either a TransformLinkBase or a numpy ndarray.
        """

        if(isinstance(data[0], dict)):
            json_array = typing.cast(list[dict[str, Any]], data)
            link_head = TransformSerialisation.from_json(json_array)
            return link_head
        elif(isinstance(data[0], (int, float, list))):
            array_np = np.array(data)
            return array_np
        else:
            raise TypeError("Input list elements must be either dicts or numeric types.")
        
    @staticmethod
    def to_ndarray(data: np.ndarray | TransformLinkBase) -> np.ndarray:
        """
        Convert the input data to a numpy ndarray.
        """

        if(isinstance(data, TransformLinkBase)):
            link_head = typing.cast(TransformLinkBase, data)
            array_np = link_head.run()
            return array_np
        elif(isinstance(data, np.ndarray)):
            array_np = typing.cast(np.ndarray, data)
            return array_np
        else:
            raise TypeError("Input must be either a numpy ndarray or a TransformLinkBase instance.")