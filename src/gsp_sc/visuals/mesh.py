from typing_extensions import Literal
import mpl3d.glm
import numpy as np
import nptyping

import meshio

from ..core.visual_base import VisualBase
import matplotlib.colors


class Mesh(VisualBase):
    __slots__ = (
        "vertices_coords",
        "face_indices",
        "uvs_coords",
        "normals_coords",
        "cmap",
        "facecolors",
        "edgecolors",
        "linewidths",
        "culling_mode",
    )

    def __init__(
        self,
        vertices_coords: nptyping.NDArray[nptyping.Shape["*, 3"], nptyping.Float],
        faces_indices: nptyping.NDArray[nptyping.Shape["*, 3"], nptyping.Int],
        cmap=None,
        facecolors="white",
        edgecolors="black",
        linewidths=0.5,
        culling_mode: Literal["front", "back", "all"] = "front",
    ) -> None:
        """
        Initialize a Mesh visual.

        Arguments:
            vertices_coords (np.ndarray): np.ndarray of shape (N, 3) representing the 3D vertices of the mesh
            faces_indices (np.ndarray): np.ndarray of shape (M, 3) representing the triangular faces of the mesh,
                contains the vertex indices of the 3 points of the triangle
            cmap: Colormap for face colors based on depth (default: None).
            facecolors: Default face color (default: "white").
            edgecolors: Edge color (default: "black").
            linewidths: Width of the edges (default: 0.5).
            culling_mode: Culling mode, either "front", "back", or "all" (default: "front").
        """
        super().__init__()

        # sanity check - np.ndarray type checking at runtime
        assert vertices_coords.shape[1:] == (3,), "Vertices must have shape (N, 3) where N is the number of vertices."
        assert faces_indices.shape[1:] == (3,), "Faces must have shape (M, 3) where M is the number of faces."

        self.vertices_coords = vertices_coords
        """3D vertices of the mesh, shape (N, 3)"""
        self.face_indices = faces_indices
        """Triangular faces of the mesh, contains the vertex indices of the 3 points of the triangle, shape (M, 3)"""
        self.cmap = cmap
        self.facecolors = matplotlib.colors.to_rgba_array(facecolors)
        self.edgecolors = matplotlib.colors.to_rgba_array(edgecolors)
        self.linewidths = linewidths
        self.culling_mode = culling_mode

    # @staticmethod
    # def from_obj_file(
    #     file_path: str,
    #     cmap=None,
    #     facecolors="white",
    #     edgecolors="black",
    #     linewidths=0.5,
    #     culling_mode: Literal["front", "back", "all"] = "front",
    # ) -> "Mesh":
    #     """
    #     Create a Mesh visual from an .obj file.

    #     Arguments:
    #         file_path (str): Path to the .obj file.
    #         cmap: Colormap for face colors based on depth (default: None).
    #         facecolors: Default face color (default: "white").
    #         edgecolors: Edge color (default: "black").
    #         linewidths: Width of the edges (default: 0.5).
    #         mode: Culling mode, either "front", "back", or "none" (default: "front").
    #     """

    #     meshio_mesh = meshio.read(file_path)
    #     vertices_coords = meshio_mesh.points

    #     # only 3d triangular meshes are supported for now
    #     faces_indices = meshio_mesh.cells[0].data

    #     # # Optional texture coordinates
    #     # uvs_coords = meshio_mesh.point_data["obj:vt"] if "obj:vt" in meshio_mesh.point_data else None
    #     # # Optional (per-vertex) normals coordinates
    #     # normals_coords = meshio_mesh.point_data["obj:vn"] if "obj:vn" in meshio_mesh.point_data else None

    #     # Normalize vertices to fit within a unit cube
    #     vertices_coords = mpl3d.glm.fit_unit_cube(vertices_coords)

    #     mesh = Mesh(
    #         vertices_coords=vertices_coords,
    #         faces_indices=faces_indices,
    #         cmap=cmap,
    #         facecolors=facecolors,
    #         edgecolors=edgecolors,
    #         linewidths=linewidths,
    #         culling_mode=culling_mode,
    #     )
    #     return mesh
