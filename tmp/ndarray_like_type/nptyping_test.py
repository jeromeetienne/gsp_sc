import numpy as np
import nptyping
from nptyping import NDArray, Shape, DType, Float, Int, Float


if __name__ == "__main__":
    var_np_array: NDArray[Shape["2, 3"], Int] = np.array([[1, 2], [3, 4]])
    var_float_array: NDArray[Shape["*"], Float] = np.array([1.0, 2.0, 3.0])
    var_other: NDArray = np.array([[1, 2], [3, 4]])
    # var_other: NDArray = "Hello"  # --- IGNORE ---

    arr = np.array([[1, 2], [3, 4]])
    assert isinstance(arr, NDArray), "np.ndarray should be a valid NDArray type"

    def myFunction(x: NDArray[Shape["2, 2"], Int], y: str) -> NDArray[Shape["*"], Int]:
        print("In myFunction:", x, y)
        return x
