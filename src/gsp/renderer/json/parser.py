# stdlib imports
import json
from typing import Any

# pip imports
import numpy as np
import matplotlib.pyplot

# local imports
from ...core import Canvas
from ...core import Viewport
from ...core import Camera
from ...core import SceneDict
from ...core import Texture
from ...visuals import Pixels
from ...visuals import Image
from ...visuals import Mesh
from ...types import NdarrayLikeUtils, DiffableNdarrayDb


class JsonParser:
    """
    A parser to convert a JSON representation of a scene into GSP objects.
    """

    def __init__(self) -> None:
        self._diffable_ndarray_db = DiffableNdarrayDb()

    def parse(self, _scene: str | SceneDict) -> tuple[Canvas, Camera]:
        if isinstance(_scene, dict):
            scene_dict: SceneDict = _scene
        else:
            scene_dict: SceneDict = json.loads(_scene)

        camera_info = scene_dict["camera"]
        camera = Camera(camera_info["type"])
        camera.uuid = camera_info["uuid"]  # restore the original uuid

        canvas_info = scene_dict["canvas"]
        canvas = Canvas(canvas_info["width"], canvas_info["height"], canvas_info["dpi"])
        canvas.uuid = canvas_info["uuid"]  # restore the original uuid

        for viewport_info in canvas_info["viewports"]:
            viewport = Viewport(
                origin_x=viewport_info["origin_x"],
                origin_y=viewport_info["origin_y"],
                width=viewport_info["width"],
                height=viewport_info["height"],
                background_color=viewport_info["background_color"],
            )
            # restore the original uuid
            viewport.uuid = viewport_info["uuid"]
            canvas.add(viewport)

            for visual_info in viewport_info["visuals"]:
                if visual_info["type"] == "Pixels":
                    pixels = Pixels(
                        positions=NdarrayLikeUtils.from_json(visual_info["positions"], self._diffable_ndarray_db),
                        sizes=NdarrayLikeUtils.from_json(visual_info["sizes"], self._diffable_ndarray_db),
                        colors=NdarrayLikeUtils.from_json(visual_info["colors"], self._diffable_ndarray_db),
                    )
                    # restore the original uuid
                    pixels.uuid = visual_info["uuid"]
                    visual = pixels
                elif visual_info["type"] == "Image":
                    texture = JsonParser.texture_from_json(visual_info["texture"])
                    image = Image(position=np.array(visual_info["position"]), image_extent=visual_info["bounds"], texture=texture)
                    # restore the original uuid
                    image.uuid = visual_info["uuid"]
                    visual = image
                elif visual_info["type"] == "Mesh":
                    cmap = None if visual_info["cmap"] is None else matplotlib.pyplot.get_cmap(visual_info["cmap"])
                    mesh = Mesh(
                        vertices_coords=np.array(visual_info["vertices"]),
                        faces_indices=np.array(visual_info["faces"]),
                        cmap=cmap,
                        facecolors=visual_info.get("facecolors", "white"),
                        edgecolors=visual_info.get("edgecolors", "black"),
                        linewidths=visual_info.get("linewidths", 0.5),
                        culling_mode=visual_info.get("mode", "front"),
                    )
                    # restore the original uuid
                    mesh.uuid = visual_info["uuid"]
                    visual = mesh
                else:
                    raise NotImplementedError(f"Parsing for visual type {visual_info['type']} is not implemented.")

                viewport.add(visual)

        return canvas, camera

    @staticmethod
    def texture_from_json(texture_dict: dict[str, Any]) -> Texture:
        image_data = np.array(texture_dict["image_data"]).reshape(tuple(texture_dict["image_data_shape"]))
        texture = Texture(image_data)
        return texture
