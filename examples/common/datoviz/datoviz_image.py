# pip imports
import numpy as np


# local imports
import gsp


class DatovizImage:
    def __init__(self, image: np.ndarray):
        image = gsp.visuals.Image(
            vertices=np.array([0.5, 0.5, 0.5]),
            image_extent=(-0.1, +0.1, -0.1, +0.1),
            image_data=image_data_np,
        )
