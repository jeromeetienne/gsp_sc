import numpy as np

from gsp.core.texture import Texture
from ..core.visual_base import VisualBase


class Image(VisualBase):
    """
    A 2D image in 3D space.
    Always faces the camera.
    """

    __slots__ = ("position", "image_extent", "texture")

    def __init__(self, position: np.ndarray, image_extent: tuple[float, float, float, float], texture: Texture) -> None:
        super().__init__()

        # TODO add support for

        self.position = position
        """The position of the image in 3D space"""
        self.image_extent = image_extent
        """The extent of the image in 3D space"""
        self.texture = texture
        """The texture of the image"""
