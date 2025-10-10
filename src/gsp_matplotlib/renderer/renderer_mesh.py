# stdlib imports
import numpy as np

# pip imports
import matplotlib.collections
import matplotlib.colors
import matplotlib.axes
import matplotlib.collections
import mpl3d.glm

# local imports
from gsp.core.camera import Camera
from gsp.visuals.mesh import Mesh
from .renderer import MatplotlibRenderer


class MatplotlibRendererMesh:
    @staticmethod
    def render(renderer: MatplotlibRenderer, axes: matplotlib.axes.Axes, mesh: Mesh, full_uuid: str, camera: Camera) -> None:
        transform = camera.transform

        # =============================================================================
        # Transform and render the mesh
        # =============================================================================

        vertices_transformed = mpl3d.glm.transform(mesh.vertices_coords, transform)
        faces_coords = vertices_transformed[mesh.face_indices]

        edgecolors = mesh.edgecolors
        linewidths = mesh.linewidths

        # =============================================================================
        # Face culling
        # =============================================================================
        if mesh.culling_mode == "front":
            faces_to_keep, _ = mpl3d.glm.frontback(faces_coords)
        elif mesh.culling_mode == "back":
            _, faces_to_keep = mpl3d.glm.frontback(faces_coords)
        elif mesh.culling_mode == "all":
            faces_to_keep = np.arange(len(faces_coords))
        else:
            raise ValueError(f"Invalid mesh.mode: {mesh.culling_mode}, should be 'front', 'back' or 'all'")

        # Cull faces
        faces_coords = faces_coords[faces_to_keep]

        faces_depths = -faces_coords[:, :, 2].mean(axis=1)

        # compute facecolors
        if mesh.cmap is not None:
            # Facecolors using depth buffer
            color_normalizer = matplotlib.colors.Normalize(vmin=faces_depths.min(), vmax=faces_depths.max())
            facecolors = mesh.cmap(color_normalizer(faces_depths))
        else:
            facecolors = mesh.facecolors

        # Separate 2d triangles from zbuffer
        faces_coords_2d = faces_coords[:, :, :2]
        antialiased = linewidths > 0

        # =============================================================================
        # Sort triangles by depth (painter's algorithm)
        # =============================================================================
        faces_indices_sorted = np.argsort(faces_depths)
        faces_coords_2d = faces_coords_2d[faces_indices_sorted, :]
        facecolors = facecolors[faces_indices_sorted, :] if len(facecolors) == len(faces_indices_sorted) else facecolors
        edgecolors = edgecolors[faces_indices_sorted, :] if len(edgecolors) == len(faces_indices_sorted) else edgecolors

        # =============================================================================
        # Create the matplotlib artist if needed
        # =============================================================================
        # Create a PolyCollection for this mesh if it doesn't exist yet
        if full_uuid not in renderer._polyCollections:
            # print(f"Creating new PathCollection for mesh visual {full_uuid}")
            renderer._polyCollections[full_uuid] = matplotlib.collections.PolyCollection([], clip_on=False, snap=False)
            axes.add_collection(renderer._polyCollections[full_uuid], autolim=False)

        # Retrieve the PolyCollection for this mesh
        polyCollection = renderer._polyCollections[full_uuid]

        # =============================================================================
        # Update the matplotlib artist
        # =============================================================================

        polyCollection.set_verts(faces_coords_2d)
        polyCollection.set_linewidth(linewidths)
        polyCollection.set_facecolor(facecolors)  # type: ignore
        polyCollection.set_edgecolor(edgecolors)  # type: ignore
        polyCollection.set_antialiased(antialiased)
