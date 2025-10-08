# stdlib imports
import typing
import json

# pip imports
import numpy as np


# local imports
from ...core.canvas import Canvas
from ...core.camera import Camera
from ...core.types import SceneDict
from ...visuals.pixels import Pixels
from ...visuals.image import Image
from ...visuals.mesh import Mesh
from ...types import NdarrayLikeUtils, DiffableNdarrayDb, DiffableNdarraySerialisation


class JsonRenderer:
    def __init__(self) -> None:
        self._diffable_ndarray_db = DiffableNdarrayDb()

    def render(self, canvas: Canvas, camera: Camera) -> SceneDict:

        scene_dict: SceneDict = {
            "camera": {
                "uuid": camera.uuid,
                "type": camera.camera_type,
            },
            "canvas": {
                "uuid": canvas.uuid,
                "width": canvas.width,
                "height": canvas.height,
                "dpi": canvas.dpi,
                "viewports": [],
            },
        }

        for viewport in canvas.viewports:
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
                        "image_data_shape": image.image_data.shape,
                        "image_data": image.image_data.tolist(),
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

            scene_dict["canvas"]["viewports"].append(viewport_dict)

        return scene_dict

    def clear_cache(self) -> None:
        DiffableNdarraySerialisation.reset_db(self._diffable_ndarray_db)
