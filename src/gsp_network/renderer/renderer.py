# stdlib imports
from typing import TypedDict, Literal, Any
import json

# pip imports
import requests
import uuid
import jsonpatch
import http_constants.status


# local imports
from gsp.core.canvas import Canvas
from gsp.core.viewport import Viewport
from gsp.core.camera import Camera
from gsp.core.types import SceneDict
from gsp.renderer.json.renderer import JsonRenderer


###############################################################################
#   Type for the network payload
#
class NetworkPayload(TypedDict):
    client_id: str
    """Unique client ID for the server to identify the client."""
    type: Literal["absolute", "json_diff"]  # or other literal string values if any
    """Type of rendering to perform. "absolute" to always render the full scene, "json_diff" to only render changes since last call."""
    data: SceneDict | str
    """The scene data in JSON format. `SceneDict` for 'absolute', `str` (JSON Patch) for 'json_diff'"""


###############################################################################
#   Network Renderer
#
class NetworkRenderer:
    __slots__ = ("__server_url", "__client_id", "__jsondiff_allowed", "__absolute_scene", "__renderer_json")

    def __init__(self, server_url: str, jsondiff_allowed: bool = False) -> None:
        """
        Renderer that sends the scene to a network server for rendering.

        Arguments:
            server_url (str): URL of the server, e.g. "http://localhost:5000/".
            diff_enabled (bool): True to enable diff rendering, False to always render the full scene
        """

        self.__server_url = server_url
        """URL of the server, e.g. "http://localhost:5000/"."""

        self.__client_id = str(uuid.uuid4())
        """Unique client ID for the server to identify the client."""

        self.__jsondiff_allowed = jsondiff_allowed
        """True to allow diff rendering, False to always render the full scene."""

        self.__absolute_scene: SceneDict | None = None
        """The last absolute scene data sent to the server, or None if none has been sent."""

        self.__renderer_json = JsonRenderer()
        """JSON renderer to convert the scene to JSON format."""

    # =============================================================================
    # .close()
    # =============================================================================
    def close(self) -> None:
        """Close the renderer and free resources."""
        self.__renderer_json.close()
        self.__absolute_scene = None

    # =============================================================================
    # .render()
    # =============================================================================
    def render(self, canvas: Canvas, viewports: list[Viewport], cameras: list[Camera]) -> bytes:

        # sanity checks
        assert len(viewports) == len(cameras), "Number of viewports must match number of cameras"

        # Convert the canvas to JSON
        scene_dict = self.__renderer_json.render(canvas, viewports, cameras)

        # Build the payload
        if self.__jsondiff_allowed and self.__absolute_scene is not None:
            # Diff rendering - compute the diff between the current scene and the last absolute scene
            json_patch = jsonpatch.JsonPatch.from_diff(self.__absolute_scene, scene_dict)
            scene_diff = str(json_patch)
            payload: NetworkPayload = {
                "client_id": self.__client_id,
                "type": "json_diff",
                "data": scene_diff,
            }
        else:
            # Absolute rendering
            payload: NetworkPayload = {
                "client_id": self.__client_id,
                "type": "absolute",
                "data": scene_dict,
            }

        # Send the POST request with JSON data
        call_url = f"{self.__server_url}/render_scene"
        headers = {"Content-Type": "application/json"}
        response = requests.post(call_url, data=json.dumps(payload), headers=headers)

        # If the server responds with 410, clear json renderer cache and resend as "absolute"
        # - this may happen if the server has lost the previous state
        if response.status_code == http_constants.status.HttpStatus.GONE:
            # Clear the JSON renderer cache to avoid sending diffs based on old data - typically when using DiffableNdarray
            self.__renderer_json.clear_cache()
            # Rebuild the scene dict from scratch
            scene_dict = self.__renderer_json.render(canvas, viewports, cameras)
            # rebuild the payload as absolute rendering
            payload: NetworkPayload = {
                "client_id": self.__client_id,
                "type": "absolute",
                "data": scene_dict,
            }
            # The server does not have the previous state, resend as absolute
            response = requests.post(call_url, data=json.dumps(payload), headers=headers)

        # Check the response status
        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}")

        # Mark that an absolute rendering has been sent
        # - MUST be done after the response is successful
        if self.__jsondiff_allowed and payload["type"] == "absolute":
            self.__absolute_scene = scene_dict

        # return png data as bytes
        image_png_data = response.content
        return image_png_data
