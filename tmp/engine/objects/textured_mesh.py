# pip imports
from typing_extensions import deprecated
import numpy as np
import matplotlib.pyplot

# local imports
from core.object_3d import Object3D


class TexturedMesh(Object3D):

    def __init__(self, faces_vertices: np.ndarray, faces_uvs: np.ndarray, texture: np.ndarray):
        super().__init__()
        self.faces_vertices = faces_vertices
        self.faces_uvs = faces_uvs
        self.texture = texture

        # remove the alpha channel if any
        texture = texture[::-1, ::1, :3]

        assert faces_vertices.ndim == 3 and faces_vertices.shape[1:] == (3, 3)
        assert faces_uvs.ndim == 3 and faces_uvs.shape[1:] == (3, 2)
        assert texture.ndim == 3 and texture.shape[2] == 3

        assert len(faces_vertices) == len(faces_uvs)

    @staticmethod
    @deprecated("Use MeshParserObjManual or MeshParserMeshio instead and load texture")
    def from_obj(model_path: str, texture_path: str) -> "TexturedMesh":
        vertices_coords, uvs_coords, normals_coords, faces_vertice_indices, face_uv_indices, face_normal_indices = TexturedMesh.parse_model_obj(model_path)
        faces_vertices = vertices_coords[faces_vertice_indices]
        faces_uvs = uvs_coords[face_uv_indices]

        texture = matplotlib.pyplot.imread(texture_path) * 255
        # remove the alpha channel if any
        texture = texture[::-1, ::1, :3]

        return TexturedMesh(faces_vertices=faces_vertices, faces_uvs=faces_uvs, texture=texture)

    # =============================================================================
    # OBJ file reader
    # =============================================================================
    @staticmethod
    @deprecated("Use MeshParserObjManual or MeshParserMeshio instead")
    def parse_model_obj(filename):
        """
        Read a wavefront filename and returns vertices, texcoords and
        respective indices for faces and texcoords
        """

        vertices_coords, uvs_coords, normals_coords, faces_vertice_indices, face_uv_indices, face_normal_indices = [], [], [], [], [], []
        with open(filename) as f:
            for line in f.readlines():
                if line.startswith("#"):
                    continue
                values = line.split()
                if not values:
                    continue
                if values[0] == "v":
                    vertices_coords.append([float(x) for x in values[1:4]])
                elif values[0] == "vt":
                    uvs_coords.append([float(x) for x in values[1:3]])
                elif values[0] == "vn":
                    normals_coords.append([float(x) for x in values[1:4]])
                elif values[0] == "f":
                    faces_vertice_indices.append([int(indices.split("/")[0]) for indices in values[1:]])
                    face_uv_indices.append([int(indices.split("/")[1]) for indices in values[1:]])
                    face_normal_indices.append([int(indices.split("/")[2]) for indices in values[1:]])
        return (
            np.array(vertices_coords),
            np.array(uvs_coords),
            np.array(normals_coords),
            np.array(faces_vertice_indices) - 1,
            np.array(face_uv_indices) - 1,
            np.array(face_normal_indices) - 1,
        )
