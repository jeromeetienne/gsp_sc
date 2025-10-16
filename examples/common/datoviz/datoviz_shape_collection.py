# pip imports
from pathlib import Path
import matplotlib.pyplot
import numpy as np
from dataclasses import dataclass

# local imports
import mpl3d.glm
from ..mesh_parser import MeshParserMeshio


@dataclass
class DatovizShape:
    vertices_coords: np.ndarray
    faces_indices: np.ndarray


class DatovizShapeCollection:
    def __init__(self):
        self._dvz_shape: list[DatovizShape] = []

    def add_obj(self, file_path: Path, **kwargs):
        obj_mesh_path = file_path.as_posix()
        vertices_coords, faces_indices, uvs_coords, normals_coords = MeshParserMeshio.parse_obj_file(obj_mesh_path)
        vertices_coords = mpl3d.glm.fit_unit_cube(vertices_coords)
        dvz_shape = DatovizShape(vertices_coords=vertices_coords, faces_indices=faces_indices)
        self._dvz_shape.append(dvz_shape)

    def destroy(self):
        self._dvz_shape.clear()
