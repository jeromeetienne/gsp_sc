# pip imports
import numpy as np

# local imports
import gsp
from .datoviz_shape_collection import DatovizShapeCollection


class DatovizMesh:
    def __init__(self, shapeCollection: DatovizShapeCollection):
        vertices = np.array((0.0, 0.0, 0.0))
        indices = np.array((0, 0, 0))
        self._gsp_mesh = gsp.visuals.Mesh(vertices_coords=vertices, faces_indices=indices)
