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
        renderer: 'MatplotlibRenderer',
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

        T = mpl3d.glm.transform(mesh.vertices, transform)[mesh.faces]
        Z = -T[:, :, 2].mean(axis=1)

        if mesh.cmap is not None:
            # Facecolors using depth buffer
            norm = matplotlib.colors.Normalize(vmin=Z.min(), vmax=Z.max())
            facecolors = mesh.cmap(norm(Z))
        else:
            facecolors = mesh.facecolors

        edgecolors = mesh.edgecolors
        linewidths = mesh.linewidths

        # Back face culling
        if mesh.mode == "front":
            front, back = mpl3d.glm.frontback(T)
            T, Z = T[front], Z[front]
            if len(facecolors) == len(mesh.faces):
                facecolors = facecolors[front]
            if len(edgecolors) == len(mesh.faces):
                edgecolors = edgecolors[front]

        # Front face culling
        elif mesh.mode == "back":
            front, back = mpl3d.glm.frontback(T)
            T, Z = T[back], Z[back]
            if len(facecolors) == len(mesh.faces):
                facecolors = facecolors[back]
            if len(edgecolors) == len(mesh.faces):
                edgecolors = edgecolors[back]

        # Separate 2d triangles from zbuffer
        triangles = T[:, :, :2]
        antialiased = linewidths > 0

        # Sort triangles according to z buffer
        I = np.argsort(Z)
        triangles = triangles[I, :]
        if len(facecolors) == len(I):
            facecolors = facecolors[I, :]
        if len(edgecolors) == len(I):
            edgecolors = edgecolors[I, :]

        polyCollection.set_verts(triangles)
        polyCollection.set_linewidth(linewidths)
        polyCollection.set_facecolor(facecolors)  # type: ignore
        polyCollection.set_edgecolor(edgecolors)  # type: ignore
        polyCollection.set_antialiased(antialiased)
