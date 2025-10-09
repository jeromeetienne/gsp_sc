# stdlib imports
import numpy as np

# pip imports
import matplotlib.axes
import mpl3d.glm

# local imports
from gsp_sc.core.camera import Camera
from gsp_sc.visuals.pixels import Pixels
from gsp_sc.types.ndarray_like_utils import NdarrayLikeUtils
from .renderer import MatplotlibRenderer


class MatplotlibRendererPixels:
    @staticmethod
    def render(
        renderer: "MatplotlibRenderer",
        axes: matplotlib.axes.Axes,
        pixels: Pixels,
        full_uuid: str,
        camera: Camera,
    ) -> None:
        # Notify pre-rendering event
        pixels.pre_rendering.send(renderer)

        if full_uuid in renderer._pathCollections:
            pathCollection = renderer._pathCollections[full_uuid]
        else:
            # print(f"Creating new PathCollection for pixels visual {full_uuid}")
            pathCollection = axes.scatter([], [])
            renderer._pathCollections[full_uuid] = pathCollection

        # compute positions
        pixels_positions = NdarrayLikeUtils.to_numpy(pixels.positions)

        # apply camera transform to positions
        transformed_positions: np.ndarray = mpl3d.glm.transform(pixels_positions, camera.transform)

        # Notify post-transform event
        pixels.post_transform.send(
            renderer,
            **{
                "camera": camera,
                "transformed_positions": transformed_positions,
            },
        )

        pathCollection.set_offsets(transformed_positions)
        pathCollection.set_sizes(NdarrayLikeUtils.to_numpy(pixels.sizes))
        pathCollection.set_color(NdarrayLikeUtils.to_numpy(pixels.colors).tolist())
        # pathCollection.set_edgecolor([0,0,0,1])

        # Notify post-rendering event
        pixels.post_rendering.send()
