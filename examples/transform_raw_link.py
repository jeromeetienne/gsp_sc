import os
import numpy as np
from gsp_sc.src.transform import TransformLinkLoad, TransformLinkMathOp, TransformLinkImmediate, TransformLinkLambda


__dirname__ = os.path.dirname(os.path.abspath(__file__))
url_npy = f"file://{__dirname__}/data/sample_positions_3d.npy"

###############################################################################

myTransform1 = TransformLinkLoad(data_url=url_npy).chain(TransformLinkMathOp("add", 5)).chain(TransformLinkMathOp("mul", 2))
np_array1 = myTransform1.run()
print(f"Loaded array1: {np_array1}")

###############################################################################

myTransform2 = TransformLinkImmediate(np.array([10, 20, 30])).chain(TransformLinkMathOp("add", 5)).chain(TransformLinkMathOp("mul", 2))
np_array2 = myTransform2.run()
print(f"Loaded array2: {np_array2}")


###############################################################################

myTransform3 = TransformLinkImmediate(np.array([10, 20, 30])).chain(TransformLinkLambda(lambda x: x+3))
np_array3 = myTransform3.run()
print(f"Loaded array3: {np_array3}")
