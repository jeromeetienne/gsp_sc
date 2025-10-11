# stdlib imports
import os

# pip imports
import numpy as np
import matplotlib.image

# local imports
from helpers.mesh_parser_obj_manual import MeshParserObjManual
from objects.points import Points
from core.object_3d import Object3D
from core.constants import Constants
from helpers.transform_utils import TransformUtils
from objects.textured_mesh import TexturedMesh
from helpers.mesh_parser_meshio import MeshParserMeshio


__dirname__ = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(__dirname__, "../data")
models_path = os.path.join(data_path, "models")
images_path = os.path.join(data_path, "images")


class SceneExamples:
    @staticmethod
    def getBunnyPoints() -> Points:
        face_indices, vertex_coords, uv_coords, normal_coords = MeshParserObjManual.parse_obj_file(os.path.join(models_path, "bunny.obj"))
        vertex_coords = TransformUtils.normalize_vertices_to_unit_cube(vertex_coords)
        points_bunny = Points(vertex_coords, color=Constants.PURPLE)
        return points_bunny

    @staticmethod
    def getCubePoints() -> Points:
        face_indices, vertex_coords, uv_coords, normal_coords = MeshParserObjManual.parse_obj_file(os.path.join(models_path, "cube_meshio.obj"))
        vertex_coords = TransformUtils.normalize_vertices_to_unit_cube(vertex_coords)
        points_bunny = Points(vertex_coords, color=Constants.CYAN)
        return points_bunny

    @staticmethod
    def getHeadPoints() -> Points:
        faces_indices, vertices_coords, uvs_coords, normals_coords = MeshParserObjManual.parse_obj_file(os.path.join(models_path, "head_meshio.obj"))
        vertices_coords = TransformUtils.normalize_vertices_to_unit_cube(vertices_coords)
        points_bunny = Points(vertices_coords, color=Constants.CYAN)
        return points_bunny

    @staticmethod
    def getHeadTexturedMesh() -> TexturedMesh:
        texture = SceneExamples.getUvGridTexture()

        obj_path = os.path.join(models_path, "head_meshio.obj")
        faces_indices, vertices_coords, uvs_coords, normals_coords = MeshParserObjManual.parse_obj_file(obj_path)
        assert uvs_coords is not None, "The .obj file must contain texture coordinates (vt)"
        textured_mesh = TexturedMesh(faces_indices, vertices_coords, uvs_coords, texture)
        textured_mesh.name = "TexturedMesh"
        return textured_mesh

    @staticmethod
    def getUvGridTexture() -> np.ndarray:
        texture_path = os.path.join(images_path, "uv-grid.png")
        texture = SceneExamples._load_texture(texture_path)
        return texture

    @staticmethod
    def _load_texture(file_path: str) -> np.ndarray:
        """
        Load a texture image from file.

        Arguments:
            file_path (str): Path to the image file.
        Returns:
            np.ndarray: Loaded image as a numpy array.
        """
        texture = matplotlib.image.imread(file_path)
        if texture.dtype != np.uint8:
            # convert to uint8
            texture = (texture * 255).astype(np.uint8)

        return texture
