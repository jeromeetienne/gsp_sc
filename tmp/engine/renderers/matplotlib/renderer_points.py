# stdlib imports
import typing

# pip imports
import matplotlib.artist
import matplotlib.collections
import numpy as np

# local imports
from objects.points import Points
from renderers.matplotlib.renderer import RendererMatplotlib
from cameras.orthographic_camera import OrthographicCamera


class MatplotlibRendererPoints:
    @staticmethod
    def render(renderer: "RendererMatplotlib", points: Points, camera: OrthographicCamera) -> list[matplotlib.artist.Artist]:
        # Placeholder for rendering logic for Points objects using matplotlib
        print(f"Rendering Points at positions {points.get_world_position()}")

        if points.uuid not in renderer._artists:
            mpl_path_collection = renderer._axis.scatter([], [])  # type: ignore
            mpl_path_collection.set_visible(False)  # hide until properly positioned and sized
            renderer._axis.add_collection(mpl_path_collection)
            renderer._artists[points.uuid] = mpl_path_collection

        mpl_path_collection = typing.cast(matplotlib.collections.PathCollection, renderer._artists[points.uuid])
        mpl_path_collection.set_visible(True)

        # Update positions and sizes
        arr = np.asarray([p.xy for p in points.get_world_position()])

        offsets = [p.xy for p in points.vertices]
        mpl_path_collection.set_offsets(offsets=offsets)
        mpl_path_collection.set_sizes([200] * len(points.vertices))  # set a default size for each point

        return [mpl_path_collection]
