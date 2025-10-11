# stdlib imports
import typing

# pip imports
import matplotlib.artist
import matplotlib.collections
import numpy as np
from pyrr import matrix44

# local imports
from objects.points import Points
from renderers.matplotlib.renderer import RendererMatplotlib
from cameras.camera_orthographic import CameraOrthographic
from cameras.camera_base import CameraBase


class MatplotlibRendererPoints:
    @staticmethod
    def render(renderer: "RendererMatplotlib", points: Points, camera: CameraBase) -> list[matplotlib.artist.Artist]:
        # Placeholder for rendering logic for Points objects using matplotlib
        print(f"Rendering Points at positions {points.get_world_position()}")

        if points.uuid not in renderer._artists:
            mpl_path_collection = renderer._axis.scatter([], [])  # type: ignore
            mpl_path_collection.set_visible(False)  # hide until properly positioned and sized
            renderer._axis.add_collection(mpl_path_collection)
            renderer._artists[points.uuid] = mpl_path_collection

        mpl_path_collection = typing.cast(matplotlib.collections.PathCollection, renderer._artists[points.uuid])
        mpl_path_collection.set_visible(True)

        # vertices is [N, 3]
        vertices = points.vertices

        # apply world matrix to vertices
        if False:
            world_matrix = points.get_world_matrix()
            vertices_hom = np.hstack([vertices, np.ones((vertices.shape[0], 1), dtype=vertices.dtype)])  # [N, 4]
            vertices_world_hom = vertices_hom @ world_matrix  # [N, 4]
            vertices_ndc = vertices_world_hom[:, :3] / vertices_world_hom[:, 3:4]  # [N, 3]
            vertices_2d = vertices_ndc[:, :2]  # drop z for 2D rendering
        elif True:
            camera_position = camera.get_world_position()
            camera_target = np.array([0.0, 0.0, 0.0], dtype=np.float32)
            camera_up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
            camera_matrix = matrix44.create_look_at(eye=camera_position, target=camera_target, up=camera_up)

            # View matrix is inverse of camera world matrix
            view_matrix = matrix44.inverse(camera_matrix)
            model_matrix = points.get_world_matrix()
            # view_matrix = camera.get_view_matrix()
            projection_matrix = camera.get_projection_matrix()

            temp = matrix44.multiply(view_matrix, model_matrix)
            full_transform = matrix44.multiply(projection_matrix, temp)

            vertices_hom = np.hstack([vertices, np.ones((vertices.shape[0], 1), dtype=vertices.dtype)])  # [N, 4]
            vertices_world_hom = vertices_hom @ full_transform  # [N, 4]
            vertices_clip = vertices_world_hom[:, :3]  # [N, 4]
            vertices_ndc = vertices_clip / vertices_world_hom[:, 3:4]  # [N, 3]

            vertices_2d = vertices_ndc[:, :2]  # drop z for 2D rendering

            vertices_2d /= 2
        else:
            assert False, "unreachable"

        mpl_path_collection.set_offsets(offsets=vertices_2d)
        mpl_path_collection.set_sizes([400] * len(points.vertices))  # set a default size for each point
        mpl_path_collection.set_color((0, 0, 1, 0.5))
        mpl_path_collection.set_edgecolor((0, 0, 0, 1))
        mpl_path_collection.set_linewidth(2)

        return [mpl_path_collection]
