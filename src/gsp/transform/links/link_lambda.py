# stdlib imports
import typing
import inspect

# pip imports
import numpy as np

# local imports
from ..transform_link_base import TransformLinkBase
from ..transform_registry import TransformRegistry


class TransformLinkLambda(TransformLinkBase):

    def __init__(self, lambda_func: typing.Callable[[np.ndarray], np.ndarray] | str) -> None:
        """
        Define a lambda function to apply to the numpy array

        NOTE: some black magic is used to serialize the lambda function passed as arguement to a string.
        don't use it more than once per lines of code, as it will not work.
        If you hit issues, just pass the lambda function as a string.
        e.g. 'lambda x: x + 1'
        """

        super().__init__()

        if isinstance(lambda_func, str):
            self.__lambda_func_source = lambda_func
        else:
            lambda_function_source = TransformLinkLambda.lambda_to_str(lambda_func)
            self.__lambda_func_source = lambda_function_source

    def _run(self, np_array: np.ndarray) -> np.ndarray:
        value = eval(self.__lambda_func_source)(np_array)
        new_array = typing.cast(np.ndarray, value)
        return new_array

    def _to_json(self) -> dict[str, typing.Any]:
        return {"type": "TransformLinkLambda", "lambda_func_source": self.__lambda_func_source}

    @staticmethod
    def _from_json(json_dict: dict[str, typing.Any]) -> TransformLinkBase:
        lambda_func_source = json_dict["lambda_func_source"]
        return TransformLinkLambda(lambda_func_source)

    @staticmethod
    def lambda_to_str(lambda_func: typing.Callable[[np.ndarray], np.ndarray]) -> str:
        lines, lineno = inspect.getsourcelines(lambda_func)
        source_lines = "".join(lines)
        source_lambda = TransformLinkLambda.__extract_lambda_from_sourcelines(source_lines)

        return source_lambda

    @staticmethod
    def __extract_lambda_from_sourcelines(code_string: str) -> str:
        """
        Parses a string containing a Python call to extract a lambda function.
        WARNING: Super black magic.

        This function finds the 'lambda' keyword and then scans the string,
        balancing parentheses to correctly identify the end of the lambda
        expression, even with nested structures.
        """
        # watchdog to ensure only one lambda is present in this line
        # - in this case, we would not be able to determine which one to extract
        if code_string.count("lambda ") != 1:
            raise ValueError("TransformLinkLambda: The code line MUST NOT contains 'lambda' expression. please pass the lambda function as a string.")

        # Find the starting position of the 'lambda' keyword.
        start_index = code_string.index("lambda ")

        # Use a counter to track the balance of parentheses.
        paren_level = 0
        # Iterate from the start of 'lambda' to the end of the string.
        for i in range(start_index, len(code_string)):
            char = code_string[i]
            if char == "(":
                paren_level += 1
            elif char == ")":
                paren_level -= 1
                # If the level drops below zero, we've found the closing
                # parenthesis of the containing function call. The lambda
                # expression ends just before this character.
                if paren_level < 0:
                    return code_string[start_index:i]
            elif char == "," and paren_level == 0:
                # If we find a comma at the top level (not inside any
                # parentheses), it marks the end of the lambda argument.
                return code_string[start_index:i]

        # This part would be reached if the lambda extends to the end of the string.
        return code_string[start_index:]


# Register the TransformLinkLambda class in the TransformLinkDB
TransformRegistry.register_link("TransformLinkLambda", TransformLinkLambda)
