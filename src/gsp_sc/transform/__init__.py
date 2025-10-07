"""
Transform is a chainable data transformation utility.
It allows you to load data, perform mathematical operations on numpy arrays.
"""

from .transform_link_base import TransformLinkBase
from .transform_serialisation import TransformSerialisation

# from .transform_or_ndarray_TOREMOVE import TransformOrNdarray

from .links import TransformLinkAssertShape
from .links import TransformLinkImmediate
from .links import TransformLinkLambda
from .links import TransformLinkLoad
from .links import TransformLinkMathOp


# TransformChain is only an helper to build a chain of TransformLinkBase. MUST NOT be used in the library
from .transform_chain import TransformChain
