from typing import TypeAlias
import numpy as np

from ..core.visual_base import VisualBase
from ..types.ndarray_like_type import NdarrayLikeType


class Pixels(VisualBase):
    __slots__ = ("positions", "sizes", "colors")

    def __init__(
        self,
        positions: NdarrayLikeType,
        sizes: NdarrayLikeType,
        colors: NdarrayLikeType,
    ) -> None:
        """
        Initialize a Pixels visual.

        Args:
            positions (NdarrayLikeType): Array of shape (N, 3) representing the 3D positions of the pixels.
            sizes (NdarrayLikeType): Array of shape (N,) representing the sizes of the pixels.
            colors (NdarrayLikeType): Array of shape (4,) representing the RGBA color of the pixels.

        Raises:
            AssertionError: If input arrays do not have the expected shapes.
        """
        super().__init__()

        # sanity check - np.ndarray type checking at runtime
        if type(positions) is np.ndarray:
            assert positions.shape[1:] == (3,), "Positions must have shape (N, 3) where N is the number of positions."
        if type(sizes) is np.ndarray:
            assert sizes.shape.__len__() == 1, "Sizes must have shape (N, 1) where N is the number of sizes."
        if type(colors) is np.ndarray:
            assert colors.shape[1:] == (4,), "Colors must be a numpy array of shape (4,)"

        self.positions = positions
        self.sizes = sizes
        self.colors = colors
