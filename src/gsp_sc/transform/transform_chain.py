# stdlib imports
from typing import Literal
import typing

# pip imports
import numpy as np

# local imports
from .links import (
    TransformLinkAssertShape,
    TransformLinkImmediate,
    TransformLinkLambda,
    TransformLinkLoad,
    TransformLinkMathOp,
)
from .transform_link_base import TransformLinkBase

class TransformChain:
    """
    Helper class to build and manage a chain of transformations on numpy arrays.

    Only eye-candy to make it easier for the user to build a chain of transformations.
    
    MUST NOT be used in the library
    """
    def __init__(self, np_array: np.ndarray | list| None = None) -> None:
        """
        Initialize the TransformHelper with an optional initial numpy array.
        """
        self._link_head: TransformLinkBase | None = None

        if isinstance(np_array, list):
            self.immediate(np.array(np_array))
        elif isinstance(np_array, np.ndarray):
            self.immediate(np_array)

    def get_link_head(self) -> TransformLinkBase:
        """
        Get the current transformation chain.
        """
        if self._link_head is None:
            raise ValueError("No transformation chain defined.")
        return self._link_head
    
    def complete(self) -> TransformLinkBase:
        """
        Complete the transformation chain and return the head link.
        """
        if self._link_head is None:
            raise ValueError("No transformation chain defined.")
        return self._link_head

    def is_empty(self) -> bool:
        """
        Check if a transformation chain is defined.
        """
        return self._link_head is None

    def run(self) -> np.ndarray:
        """
        Run the transformation chain and return the resulting numpy array.
        """

        if self._link_head is None:
            # If no transforms, return empty array
            np_array = np.array([])
        else:
            # Run the chain of transforms
            np_array = self._link_head.run()

        # return the re
        return np_array
    
    def __chain(self, new_link: TransformLinkBase) -> "TransformChain":
        """
        Chain a new transformation to the existing transformation chain.
        """

        if self._link_head is None:
            self._link_head = new_link
        else:
            # get the last link
            last_link = self._link_head
            while last_link.next_transform is not None:
                last_link = last_link.next_transform
            # chain the new link to the last link
            last_link.chain(new_link)

        return self

	#####################################################################################
    # Transformation methods
    # FIXME those hardcoded strings are error-prone and should be avoided - have that to be dynamic - similar in transform_helper.py
    #

    def assert_shape(self, expected_shape: tuple[int, ...]) -> "TransformChain":
        """
        Ensure the input array has the specified shape.
        """
        new_transform = TransformLinkAssertShape(expected_shape)
        
        return self.__chain(new_transform)

    def immediate(self, np_array: np.ndarray) -> "TransformChain":
        """
        Use the provided numpy array as the initial data.
        """
        new_transform = TransformLinkImmediate(np_array)

        return self.__chain(new_transform)
    
    def lambdaFunc(self, lambda_func: typing.Callable[[np.ndarray], np.ndarray] | str) -> "TransformChain":
        """
        Define a lambda function to apply to the numpy array

        **NOTE**: some black magic is used to serialize the lambda function passed as arguement to a string.
        don't use it more than once per lines of code, as it will not work.
        If you hit issues, just pass the lambda function as a string.
        e.g. 'lambda x: x + 1'
        """
        new_transform = TransformLinkLambda(lambda_func)

        return self.__chain(new_transform)

    def load(self, data_url: str) -> "TransformChain":
        """
        Load a numpy array from the specified .npy file URL.
        """
        new_transform = TransformLinkLoad(data_url)
        
        return self.__chain(new_transform)

    def math_op(
        self, operation: Literal["add", "sub", "mul", "div"], operand: float
    ) -> "TransformChain":
        """
        Perform a math operation on the data.
        """
        new_transform = TransformLinkMathOp(operation, operand)

        return self.__chain(new_transform)

