from typing import Any
import numpy as np
from .transform_link_base import TransformLinkBase

from .transform_registry import TransformRegistry


class TransformSerialisation:

    @staticmethod
    def to_json(transformBase: TransformLinkBase) -> list[dict[str, Any]]:
        """
        Convert the transformation chain to a JSON-serializable array.
        """

        # Find the first transform in the chain
        first_transform = transformBase
        while first_transform.previous_transform is not None:
            first_transform = first_transform.previous_transform

        # Traverse the chain and build the JSON array
        json_array = []
        current_transform = first_transform
        while current_transform is not None:
            # Convert this transform to JSON
            json_array.append(current_transform._to_json())
            # Move to the next transform
            current_transform = current_transform.next_transform

        return json_array

    @staticmethod
    def from_json(json_array: list[dict[str, Any]]) -> "TransformLinkBase":
        """
        Convert a JSON-serializable array to a transformation chain.
        """

        if not json_array:
            raise ValueError("JSON array MUST NOT be empty")

        # Create the first transform
        current_transform = TransformSerialisation.__get_link_instance(json_array[0])

        # Create and chain the remaining transforms
        for json_dict in json_array[1:]:
            next_transform = TransformSerialisation.__get_link_instance(json_dict)
            current_transform = current_transform.chain(next_transform)

        # Find the first transform in the chain
        first_transform = current_transform
        while first_transform.previous_transform is not None:
            first_transform = first_transform.previous_transform

        return first_transform

    @staticmethod
    def __get_link_instance(json_dict: dict[str, Any]) -> TransformLinkBase:
        """
        Get an instance of a TransformBase subclass from a JSON dictionary and TransformLinkDB
        """

        class_name = json_dict.get("type")
        if class_name is None:
            raise ValueError("JSON dictionary MUST contain a 'type' field")

        # Get the class from the TransformLinkDB
        link_class = TransformRegistry.get_link(class_name)
        if link_class is None:
            raise ValueError(f"Unknown transform type: {class_name}")

        # call the static method _from_json of the link_class
        link_instance = link_class._from_json(json_dict)

        return link_instance
