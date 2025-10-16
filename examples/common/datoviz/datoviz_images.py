# pip imports
import numpy as np


# local imports
import gsp
from .datoviz_texture import DatovizTexture


class DatovizImages:
    def __init__(self, positions: np.ndarray, sizes: np.ndarray):

        # sanity checks
        assert positions.shape[1] == 3, f"Expected positions to be of shape (N, 3), got {positions.shape}"
        assert sizes.shape[1] == 2, f"Expected sizes to be of shape (N, 2), got {sizes.shape}"
        assert (
            positions.shape[0] == sizes.shape[0]
        ), f"Expected positions and sizes to have the same number of rows, got {positions.shape[0]} and {sizes.shape[0]}"
        assert positions.shape[0] == 1, f"Only one image supported for now"

        self._positions = positions
        """The positions of the images as a numpy array of shape (N, 3)"""
        self._sizes = sizes
        """The sizes of the images as a numpy array of shape (N, 2)"""

        # position is (3,)
        # size is (2,)

        sizes_ndc = np.zeros((1, 2), dtype=np.float32)
        viewport_w = 512
        viewport_h = 512
        sizes_ndc[:, 0] = sizes[:, 0] / viewport_w
        sizes_ndc[:, 1] = sizes[:, 1] / viewport_h

        image_extent_ndc = (-sizes_ndc[0][0] / 2, +sizes_ndc[0][0] / 2, -sizes_ndc[0][1] / 2, +sizes_ndc[0][1] / 2)
        self._gsp_image = gsp.visuals.Image(
            position=positions[0],
            image_extent=image_extent_ndc,
        )

    def set_texture(self, texture: DatovizTexture):
        self._gsp_image.texture = texture._gsp_texture
