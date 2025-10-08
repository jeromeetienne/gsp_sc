# stdlib imports
import numpy as np

# pip imports
import matplotlib.collections
import matplotlib.colors
import matplotlib.axes
import matplotlib.collections
import mpl3d.glm

# local imports
from ...core.camera import Camera
from ...visuals.mesh import Mesh
from .renderer import MatplotlibRenderer


class MatplotlibRendererMesh:
    @staticmethod
    def render(
        renderer: "MatplotlibRenderer",
        axes: matplotlib.axes.Axes,
        mesh: Mesh,
        full_uuid: str,
        camera: Camera,
    ) -> None:
        transform = camera.transform

        if full_uuid not in renderer._polyCollections:
            # print(f"Creating new PathCollection for mesh visual {full_uuid}")
            renderer._polyCollections[full_uuid] = matplotlib.collections.PolyCollection([], clip_on=False, snap=False)
            axes.add_collection(renderer._polyCollections[full_uuid], autolim=False)

        polyCollection = renderer._polyCollections[full_uuid]

        vertices_transformed = mpl3d.glm.transform(mesh.vertices, transform)
        faces_coords_3d = vertices_transformed[mesh.face_indices]
        faces_depths = -faces_coords_3d[:, :, 2].mean(axis=1)

        if mesh.cmap is not None:
            # Facecolors using depth buffer
            color_normalizer = matplotlib.colors.Normalize(vmin=faces_depths.min(), vmax=faces_depths.max())
            facecolors = mesh.cmap(color_normalizer(faces_depths))
        else:
            facecolors = mesh.facecolors

        edgecolors = mesh.edgecolors
        linewidths = mesh.linewidths

        # Back face culling
        if mesh.mode == "front":
            front, back = mpl3d.glm.frontback(faces_coords_3d)
            faces_coords_3d = faces_coords_3d[front]
            faces_depths = faces_depths[front]
            if len(facecolors) == len(mesh.face_indices):
                facecolors = facecolors[front]
            if len(edgecolors) == len(mesh.face_indices):
                edgecolors = edgecolors[front]

        # Front face culling
        elif mesh.mode == "back":
            front, back = mpl3d.glm.frontback(faces_coords_3d)
            faces_coords_3d = faces_coords_3d[back]
            faces_depths = faces_depths[back]
            if len(facecolors) == len(mesh.face_indices):
                facecolors = facecolors[back]
            if len(edgecolors) == len(mesh.face_indices):
                edgecolors = edgecolors[back]

        # Separate 2d triangles from zbuffer
        faces_coords_2d = faces_coords_3d[:, :, :2]
        antialiased = linewidths > 0

        # Sort triangles according to z buffer
        faces_indices_sorted = np.argsort(faces_depths)
        faces_coords_2d = faces_coords_2d[faces_indices_sorted, :]
        if len(facecolors) == len(faces_indices_sorted):
            facecolors = facecolors[faces_indices_sorted, :]
        if len(edgecolors) == len(faces_indices_sorted):
            edgecolors = edgecolors[faces_indices_sorted, :]

        polyCollection.set_verts(faces_coords_2d)
        polyCollection.set_linewidth(linewidths)
        polyCollection.set_facecolor(facecolors)  # type: ignore
        polyCollection.set_edgecolor(edgecolors)  # type: ignore
        polyCollection.set_antialiased(antialiased)
