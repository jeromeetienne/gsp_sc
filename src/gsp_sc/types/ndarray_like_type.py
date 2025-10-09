# pip imports
import numpy as np

# local imports
from ..transform.transform_link_base import TransformLinkBase
from .diffable_ndarray.diffable_ndarray import DiffableNdarray

NdarrayLikeType = TransformLinkBase | DiffableNdarray | np.ndarray
