import numpy as np
import pytest
from gsp_sc.transform import TransformLinkImmediate, TransformLinkAssertShape, TransformLinkMathOp, TransformLinkLambda


def test_transformchain_math_op_add():
    arr = np.array([1, 2, 3])
    result = TransformLinkImmediate(arr).chain(TransformLinkMathOp("add", 2)).run()
    np.testing.assert_array_equal(result, np.array([3, 4, 5]))


def test_transformchain_math_op_mul():
    arr = np.array([1, 2, 3])
    result = TransformLinkImmediate(arr).chain(TransformLinkMathOp("mul", 5)).run()
    np.testing.assert_array_equal(result, np.array([5, 10, 15]))


def test_transformchain_assert_shape_pass():
    arr = np.array([1, 2, 3])
    result = TransformLinkImmediate(arr).chain(TransformLinkAssertShape((3,))).run()
    np.testing.assert_array_equal(result, arr)


def test_transformchain_assert_shape_fail():
    arr = np.array([[1, 2], [3, 4]])
    with pytest.raises(ValueError):
        TransformLinkImmediate(arr).chain(TransformLinkAssertShape((3,))).run()


def test_transformchain_lambdaFunc():
    arr = np.array([1, 2, 3])
    result = TransformLinkImmediate(arr).chain(TransformLinkLambda(lambda x: x * 2)).run()
    np.testing.assert_array_equal(result, np.array([2, 4, 6]))


def test_transformchain_empty_init():
    result = TransformLinkImmediate(np.array([])).run()
    assert isinstance(result, np.ndarray) and result.size == 0
