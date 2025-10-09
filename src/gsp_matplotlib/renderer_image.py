# stdlib imports
import numpy as np

# pip imports
import matplotlib.axes
import mpl3d.glm

# local imports
from gsp.core.camera import Camera
from gsp.visuals.image import Image
from .renderer import MatplotlibRenderer


class MatplotlibRendererImage:
    @staticmethod
    def render(
        renderer: "MatplotlibRenderer",
        axes: matplotlib.axes.Axes,
        image: Image,
        full_uuid: str,
        camera: Camera,
    ) -> None:
        if full_uuid not in renderer._axesImages:
            # print(f"Creating new AxesImage for image visual {full_uuid}")
            renderer._axesImages[full_uuid] = axes.imshow(np.zeros((2, 2, 3)))

        axes_image = renderer._axesImages[full_uuid]
        axes_image.set_data(image.image_data)

        #

        # extent_3d = np.array([
        #     [image.position[0]+image.image_extent[0], image.position[1]+image.image_extent[2], image.position[2]],
        #     [image.position[0]+image.image_extent[1], image.position[1]+image.image_extent[2], image.position[2]],
        #     [image.position[0]+image.image_extent[1], image.position[1]+image.image_extent[3], image.position[2]],
        #     [image.position[0]+image.image_extent[0], image.position[1]+image.image_extent[3], image.position[2]],
        # ])

        # transformed_positions: np.ndarray = mpl3d.glm.transform(
        #     V=extent_3d, mvp=camera.transform
        # )
        # transformed_extent = (
        #     transformed_positions[0, 0],
        #     transformed_positions[0, 1],
        #     transformed_positions[0, 2],
        #     transformed_positions[0, 3],
        # )
        # axes_image.set_extent(transformed_extent)

        positions = np.array([image.position])
        transformed_positions: np.ndarray = mpl3d.glm.transform(positions, camera.transform)
        # FIXME should be divided by W after rotation
        # but there is nothing to compensate for the camera z
        transformed_extent = (
            transformed_positions[0, 0] + image.image_extent[0],
            transformed_positions[0, 0] + image.image_extent[1],
            transformed_positions[0, 1] + image.image_extent[2],
            transformed_positions[0, 1] + image.image_extent[3],
        )
        axes_image.set_extent(transformed_extent)
