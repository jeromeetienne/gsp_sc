import gsp_sc.src as gsp_sc
import numpy as np
import os
from gsp_sc.src.transform import TransformChain

__dirname__ = os.path.dirname(os.path.abspath(__file__))
url_npy = f"file://{__dirname__}/data/sample_positions_3d.npy"

np_array1 = TransformChain().load(url_npy).math_op("add", 3).run()
print(f'np_array1:{np_array1}')

np_array2 = TransformChain([1, 2, 3]).assert_shape((3,)).math_op("mul", 10).run()
print(f'np_array2:{np_array2}')

np_array3 = TransformChain().run()
print(f'np_array3:{np_array3}')

np_array4 = TransformChain([1,2,3]).lambdaFunc(lambda x: x+1).run()
print(f'np_array4:{np_array4}')
