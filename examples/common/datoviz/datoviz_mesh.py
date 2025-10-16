# pip imports
import numpy as np

# local imports
import gsp
from .datoviz_shape_collection import DatovizShapeCollection


class DatovizMesh:
    def __init__(self, shapeCollection: DatovizShapeCollection):
        assert len(shapeCollection._dvz_shape) == 1, "Only one shape is supported for now"
        shape = shapeCollection._dvz_shape[0]
        vertices = shape.vertices_coords
        indices = shape.faces_indices
        self._gsp_mesh = gsp.visuals.Mesh(vertices_coords=vertices, faces_indices=indices)
