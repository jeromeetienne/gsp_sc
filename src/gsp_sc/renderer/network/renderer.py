# stdlib imports
from typing import TypedDict, Literal, Any
import json

# pip imports
import requests
import uuid
import jsonpatch

# local imports
from ...core.canvas import Canvas
from ...core.camera import Camera
from ...core.types import SceneDict
from ..json.renderer import JsonRenderer


###############################################################################
#   Type for the network payload
#
class NetworkPayload(TypedDict):
    client_id: str
    """Unique client ID for the server to identify the client."""
    type: Literal["absolute", "json_diff"]  # or other literal string values if any
    """Type of rendering to perform. "absolute" to always render the full scene, "json_diff" to only render changes since last call."""
    data: SceneDict | Any  # or a more specific type if you know the structure of scene_json
    """The scene data in JSON format."""


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

    def render(self, canvas: Canvas, camera: Camera) -> bytes:
        # Convert the canvas to JSON
        scene_dict = self.__renderer_json.render(canvas, camera)

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
        gone_status_code = 410  # HTTP status code for "Gone" - https://developer.mozilla.org/fr/docs/Web/HTTP/Reference/Status/410
        if response.status_code == gone_status_code:
            # Clear the JSON renderer cache to avoid sending diffs based on old data - typically when using DiffableNdarray
            self.__renderer_json.clear_cache()
            # Rebuild the scene dict from scratch
            scene_dict = self.__renderer_json.render(canvas, camera)
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
        # TODO do this IIF jsondiff was allowed?
        if payload["type"] == "absolute":
            self.__absolute_scene = scene_dict

        # return png data as bytes
        image_png_data = response.content
        return image_png_data
