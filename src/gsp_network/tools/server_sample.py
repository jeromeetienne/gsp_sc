#!/usr/bin/env python3
"""
Server example using Flask to render a scene from JSON input.

- use Flask to create a simple web server
- render with matplotlib
- it is able to handle delta encoding of the scene using jsonpatch
"""

# stdlib imports
import io

# pip imports
from flask import Flask, request, send_file, Response
import jsonpatch
import argparse
import http_constants.status
import colorama

# local imports
import gsp
import gsp_matplotlib
from gsp.core.types import SceneDict
from gsp.types import DiffableNdarraySerialisationError
from gsp_network import NetworkPayload

flask_app = Flask(__name__)

# Store the last absolute scene for each client (for diff rendering)
absolute_scenes: dict[str, SceneDict] = {}
"""Dictionary mapping client IDs to their last absolute scene data."""

json_parser = gsp.renderer.json.JsonParser()


# =============================================================================
# Colorama alias
# =============================================================================
def text_cyan(text: str) -> str:
    return colorama.Fore.CYAN + text + colorama.Style.RESET_ALL


def text_green(text: str) -> str:
    return colorama.Fore.GREEN + text + colorama.Style.RESET_ALL


def text_red(text: str) -> str:
    return colorama.Fore.RED + text + colorama.Style.RESET_ALL


# =============================================================================
# flask callback
# =============================================================================
@flask_app.route("/render_scene", methods=["POST"])
def render_scene_json() -> Response:
    payload: NetworkPayload = request.get_json()

    # Log the received payload for debugging
    print(f"Received payload: client_id={text_cyan(payload.get('client_id'))}, type={text_cyan(payload.get('type'))}")

    ###############################################################################
    #   Parse the payload
    #
    client_id = payload["client_id"]
    if payload["type"] == "absolute":
        payload_data = payload["data"]
        assert isinstance(payload_data, dict), f"Expected payload data to be a dictionary for 'absolute' type, got {type(payload_data).__name__}"
        # Store the absolute scene for this client
        absolute_scenes[client_id] = payload_data
        scene_dict: SceneDict = payload_data
        # log the operation
        print(f"Rendering scene for client_id={client_id}. {text_green('Absolute')} Scene size: {text_cyan(str(len(str(scene_dict))))} bytes")
    elif payload["type"] == "json_diff":
        old_scene_dict = absolute_scenes.get(client_id)
        # If no previous absolute scene exists, return an error
        if old_scene_dict is None:
            # return 410 Gone
            return Response("json_diff resource not found. Resend as 'absolute'.", status=http_constants.status.HttpStatus.GONE)
        # Reconstruct the absolute scene by applying the diff
        scene_diff = payload["data"]
        scene_dict = jsonpatch.apply_patch(old_scene_dict, scene_diff)
        # Update the stored absolute scene
        absolute_scenes[client_id] = scene_dict
        # log the operation
        print(
            f"Rendering scene for client_id={client_id}. {text_green('Diff')} size: {text_cyan(str(len(str(scene_diff))))} bytes, Full scene size: {text_cyan(str(len(str(scene_dict))))} bytes"
        )
    else:
        assert False, f"Unknown rendering type: {payload['type']}"

    ###############################################################################
    # Load the scene from JSON
    #
    try:
        canvas_parsed, viewports_parsed, cameras_parsed = json_parser.parse(scene_dict)
    except DiffableNdarraySerialisationError as e:
        # return 410 Gone
        return Response("DiffableNdarray not found.", status=http_constants.status.HttpStatus.GONE)

    ###############################################################################
    # Render the loaded scene with matplotlib
    #
    matplotlib_renderer = gsp_matplotlib.MatplotlibRenderer()
    image_png_data = matplotlib_renderer.render(canvas_parsed, viewports_parsed, cameras_parsed, show_image=False)
    matplotlib_renderer.close()  # free memory

    print(f"Rendered image size: {text_cyan(str(len(image_png_data)))} bytes")

    ###############################################################################
    # Return the rendered image as a PNG file
    #
    return send_file(
        io.BytesIO(image_png_data),
        mimetype="image/png",
        as_attachment=True,
        download_name="rendered_scene.png",
    )


# =============================================================================
#
# =============================================================================


class ServerSample:
    """
    Sample class to demonstrate server functionality.
    """

    def __init__(self):
        pass

    def run(self):
        flask_app.run(threaded=False, debug=False)  # Enable debug mode if desired


#######################################################################################

if __name__ == "__main__":
    argParser = argparse.ArgumentParser(description="Run the network server for rendering. see ./examples/network_client.py for usage.")
    args = argParser.parse_args()

    server = ServerSample()
    server.run()
