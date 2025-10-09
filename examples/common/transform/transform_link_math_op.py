import numpy as np
from typing import Literal, Any
from gsp.transform import TransformLinkBase, TransformRegistry


# =============================================================================
# Example of a user-defined TransformLink that performs a math operation
# =============================================================================
class TransformLinkMathOp(TransformLinkBase):
    def __init__(self, operation: Literal["add", "sub", "mul", "div"], operand: float) -> None:
        """
        Perform a math operation on the data.
        Supported operations: add, sub, mul, div
        """

        super().__init__()

        self.__operation = operation
        """The math operation to perform: add, sub, mul, div"""

        self.__operand = operand
        """The operand to use in the math operation"""

    def _run(self, np_array: np.ndarray) -> np.ndarray:
        if self.__operation == "add":
            result = np_array + self.__operand
        elif self.__operation == "sub":
            result = np_array - self.__operand
        elif self.__operation == "mul":
            result = np_array * self.__operand
        elif self.__operation == "div":
            result = np_array / self.__operand
        else:
            raise ValueError(f"Unsupported operation: {self.__operation}")

        return result

    def _to_json(self) -> dict[str, Any]:
        return {"type": "TransformMathOp", "operation": self.__operation, "operand": self.__operand}

    @staticmethod
    def _from_json(json_dict: dict[str, Any]) -> TransformLinkBase:
        operation = json_dict["operation"]
        operand = json_dict["operand"]
        return TransformLinkMathOp(operation, operand)


# Register the TransformMathOp class in the TransformLinkDB
TransformRegistry.register_link("TransformMathOp", TransformLinkMathOp)
