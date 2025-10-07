import numpy as np
import pytest
from gsp_sc.transform import TransformChain

def test_transformchain_math_op_add():
    arr = np.array([1, 2, 3])
    result = TransformChain(arr).math_op("add", 2).run()
    np.testing.assert_array_equal(result, np.array([3, 4, 5]))

def test_transformchain_math_op_mul():
    arr = np.array([1, 2, 3])
    result = TransformChain(arr).math_op("mul", 5).run()
    np.testing.assert_array_equal(result, np.array([5, 10, 15]))

def test_transformchain_assert_shape_pass():
    arr = np.array([1, 2, 3])
    result = TransformChain(arr).assert_shape((3,)).run()
    np.testing.assert_array_equal(result, arr)

def test_transformchain_assert_shape_fail():
    arr = np.array([[1, 2], [3, 4]])
    with pytest.raises(ValueError):
        TransformChain(arr).assert_shape((3,)).run()

def test_transformchain_lambdaFunc():
    arr = np.array([1, 2, 3])
    result = TransformChain(arr).lambdaFunc(lambda x: x * 2).run()
    np.testing.assert_array_equal(result, np.array([2, 4, 6]))

def test_transformchain_empty_init():
    result = TransformChain().run()
    assert isinstance(result, np.ndarray) and result.size == 0