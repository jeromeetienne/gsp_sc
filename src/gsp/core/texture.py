# stdlib imports
import numpy as np


class Texture:
    def __init__(self, image_data: np.ndarray | None = None):
        self.image_data = image_data if image_data is not None else np.zeros((1, 1, 3), dtype=np.uint8)
        """The image data as a numpy array"""
