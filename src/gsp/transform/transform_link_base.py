from typing import Any
import numpy as np

class TransformLinkBase:
    def __init__(self):
        """
        Base class for data transformations.
        Each transformation can be chained to another transformation.
        """
        self.next_transform: TransformLinkBase | None = None
        self.previous_transform: TransformLinkBase | None = None


    def chain(self, other_transform: 'TransformLinkBase') -> 'TransformLinkBase':
        """
        Chain another transformation to this one.
        """
        other_transform.previous_transform = self
        self.next_transform = other_transform

        return self.next_transform
    
    ###########################################################################

    def _run(self, np_array: np.ndarray) -> np.ndarray:
        raise NotImplementedError("_run method must be implemented by subclasses")
    
    def _to_json(self) -> dict[str, Any]:
        raise NotImplementedError("_to_json method must be implemented by subclasses")
    
    @staticmethod
    def _from_json( json_dict: dict[str, Any]) -> 'TransformLinkBase':
        raise NotImplementedError("_from_json method must be implemented by subclasses")

    ###########################################################################

    def run(self) -> np.ndarray:
        """
        Run the chain of transformations and return the resulting numpy array.
        """

        # Find the first transform in the chain
        first_transform = self
        while first_transform.previous_transform is not None:
            first_transform = first_transform.previous_transform

        # Run the chain of transforms
        np_array = np.array([])  # Start with an empty array
        current_transform = first_transform
        while current_transform is not None:
            # Run this transform
            np_array = current_transform._run(np_array)
            # Move to the next transform
            current_transform = current_transform.next_transform

        return np_array
        
