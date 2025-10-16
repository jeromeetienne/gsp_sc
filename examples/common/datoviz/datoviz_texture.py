# pip imports
import numpy as np


# local imports
import gsp


class DatovizTexture:
    def __init__(self, image: np.ndarray):
        self._gsp_texture = gsp.core.Texture(image_data=image)
