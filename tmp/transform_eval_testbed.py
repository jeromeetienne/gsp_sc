import numpy as np
import inspect

def transform_link(np_array: np.ndarray) -> np.ndarray:
    """A simple transformation function that adds 1 to each element in the input array."""
    return np_array + 1



pass
print('sfdsdf')

func_src = inspect.getsource(transform_link)

func_src = """
def new_transform_link(np_array: np.ndarray) -> np.ndarray:
    return np_array + 1

new_transform_link
"""

# x = 10
func_src = "lambda a: a + 10"
print(func_src)

new_func = eval(func_src)

test_array = np.array([1, 2, 3])
result = new_func(test_array)
print(result)  # Expected output: [2 3 4]