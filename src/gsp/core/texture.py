# stdlib imports
import numpy as np


class Texture:
    def __init__(self, image_data: np.ndarray):
        self.image_data: np.ndarray = image_data
        """The image data as a NumPy array"""
