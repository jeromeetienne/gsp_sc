import mpl3d.glm
import numpy as np
import nptyping

import meshio

from ..core.visual_base import VisualBase
import matplotlib.colors


class Mesh(VisualBase):
    __slots__ = (
        "vertices",
        "faces",
        "cmap",
        "facecolors",
        "edgecolors",
        "linewidths",
        "mode",
    )

    def __init__(
        self,
        vertices: nptyping.NDArray[nptyping.Shape["*, 3"], nptyping.Float],
        faces: nptyping.NDArray[nptyping.Shape["*, 3"], nptyping.Int],
        cmap=None,
        facecolors="white",
        edgecolors="black",
        linewidths=0.5,
        mode="front",
    ) -> None:
        """
        Initialize a Mesh visual.

        Arguments:
           vertices: np.ndarray of shape (N, 3) representing the 3D vertices of the mesh
           faces: np.ndarray of shape (M, 3) representing the triangular faces of the
        """
        super().__init__()

        # sanity check - np.ndarray type checking at runtime
        assert vertices.shape[1:] == (
            3,
        ), "Vertices must have shape (N, 3) where N is the number of vertices."
        assert faces.shape[1:] == (
            3,
        ), "Faces must have shape (M, 3) where M is the number of faces."

        self.vertices = vertices
        self.faces = faces
        self.cmap = cmap
        self.facecolors = matplotlib.colors.to_rgba_array(facecolors)
        self.edgecolors = matplotlib.colors.to_rgba_array(edgecolors)
        self.linewidths = linewidths
        self.mode = mode

    @staticmethod
    def from_obj_file(
        file_path: str,
        cmap=None,
        facecolors="white",
        edgecolors="black",
        linewidths=0.5,
        mode="front",
    ) -> "Mesh":
        """
        Create a Mesh visual from an .obj file.

        Arguments:
            file_path (str): Path to the .obj file.
            cmap: Colormap for face colors based on depth (default: None).
            facecolors: Default face color (default: "white").
            edgecolors: Edge color (default: "black").
            linewidths: Width of the edges (default: 0.5).
            mode: Culling mode, either "front", "back", or "none" (default: "front").
        """

        meshio_mesh = meshio.read(file_path)
        vertices = meshio_mesh.points
        vertices = mpl3d.glm.fit_unit_cube(vertices)
        faces = meshio_mesh.cells[0].data
        return Mesh(
            vertices=vertices,
            faces=faces,
            cmap=cmap,
            facecolors=facecolors,
            edgecolors=edgecolors,
            linewidths=linewidths,
            mode=mode,
        )
