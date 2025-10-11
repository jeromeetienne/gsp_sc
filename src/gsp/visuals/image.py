import numpy as np

from ..core.visual_base import VisualBase


class Image(VisualBase):
    """
    A 2D image in 3D space.
    Always faces the camera.
    """

    __slots__ = ("vertices", "image_extent", "image_data")

    def __init__(self, vertices: np.ndarray, image_extent: tuple[float, float, float, float], image_data: np.ndarray) -> None:
        super().__init__()

        self.vertices = vertices
        """The position of the image in 3D space"""
        self.image_data = image_data
        """The image data as a NumPy array"""
        self.image_extent = image_extent
        """The extent of the image in 3D space"""
