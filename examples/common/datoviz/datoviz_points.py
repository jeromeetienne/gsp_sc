# pip imports
import numpy as np

# local imports
import gsp


class DatovizPoints:
    def __init__(self, positions: np.ndarray, sizes: np.ndarray, colors: np.ndarray):
        self._gsp_pixels = gsp.visuals.Pixels(positions=positions, sizes=sizes, colors=colors)
