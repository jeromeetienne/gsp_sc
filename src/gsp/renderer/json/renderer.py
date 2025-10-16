# stdlib imports
import typing
from typing import Any
import json

# pip imports
import numpy as np


# local imports
from ...core.canvas import Canvas
from ...core.viewport import Viewport
from ...core.camera import Camera
from ...core.texture import Texture
from ...core.types import SceneDict
from ...visuals.pixels import Pixels
from ...visuals.image import Image
from ...visuals.mesh import Mesh
from ...types import NdarrayLikeUtils, DiffableNdarrayDb, DiffableNdarraySerialisation


class JsonRenderer:
    def __init__(self) -> None:
        self._diffable_ndarray_db = DiffableNdarrayDb()

    def render(self, canvas: Canvas, viewports: list[Viewport], cameras: list[Camera]) -> SceneDict:

        # =============================================================================
        # sanity checks
        # =============================================================================

        assert len(viewports) == len(cameras), f"Number of viewports must match number of cameras, got {len(viewports)} viewports and {len(cameras)} cameras."

        # =============================================================================
        # .to_json scene
        # =============================================================================
        scene_dict: SceneDict = {
            "canvas": {
                "uuid": canvas.uuid,
                "width": canvas.width,
                "height": canvas.height,
                "dpi": canvas.dpi,
                "cameras": [],
                "viewports": [],
            },
        }

        for viewport, camera in zip(viewports, cameras):
            # =============================================================================
            # .to_json camera
            # =============================================================================

            camera_dict = {
                "uuid": camera.uuid,
                "type": camera.camera_type,
            }
            # add camera to this canvas
            scene_dict["canvas"]["cameras"].append(camera_dict)

            # =============================================================================
            # .to_json viewport
            # =============================================================================
            viewport_dict = {
                "uuid": viewport.uuid,
                "origin_x": viewport.origin_x,
                "origin_y": viewport.origin_y,
                "width": viewport.width,
                "height": viewport.height,
                "background_color": viewport.background_color,
                "visuals": [],
            }

            for visual in viewport.visuals:
                if isinstance(visual, Pixels):
                    pixels: Pixels = visual
                    visual_dict = {
                        "type": "Pixels",
                        "uuid": pixels.uuid,
                        "positions": NdarrayLikeUtils.to_json(pixels.positions, self._diffable_ndarray_db),
                        "sizes": NdarrayLikeUtils.to_json(pixels.sizes, self._diffable_ndarray_db),
                        "colors": NdarrayLikeUtils.to_json(pixels.colors, self._diffable_ndarray_db),
                    }
                elif isinstance(visual, Image):
                    image: Image = visual
                    visual_dict = {
                        "type": "Image",
                        "uuid": image.uuid,
                        "position": image.position.tolist(),
                        "bounds": image.image_extent,
                        "texture": JsonRenderer.texture_to_json(image.texture),
                    }
                elif isinstance(visual, Mesh):
                    mesh = visual
                    visual_dict = {
                        "type": "Mesh",
                        "uuid": mesh.uuid,
                        "vertices": mesh.vertices_coords.tolist(),
                        "cmap": None if mesh.cmap is None else mesh.cmap.name,
                        "faces": mesh.face_indices.tolist(),
                        "facecolors": mesh.facecolors.tolist(),
                        "edgecolors": mesh.edgecolors.tolist(),
                        "linewidths": mesh.linewidths,
                        "mode": mesh.culling_mode,
                    }
                else:
                    raise NotImplementedError(f"Rendering for visual type {type(visual)} is not implemented.")

                viewport_dict["visuals"].append(visual_dict)

            # Add viewport to this canvas
            scene_dict["canvas"]["viewports"].append(viewport_dict)

        return scene_dict

    def clear_cache(self) -> None:
        DiffableNdarraySerialisation.reset_db(self._diffable_ndarray_db)

    @staticmethod
    def texture_to_json(texture: Texture) -> dict[str, Any]:
        texture_dict: dict[str, Any] = {
            "image_data": texture.image_data.tolist(),
            "image_data_shape": texture.image_data.shape,
        }
        return texture_dict
