#!/usr/bin/env python3
"""
Server example using Flask to render a scene from JSON input.

- use Flask to create a simple web server
- render with matplotlib
"""

# stdlib imports
import io

# pip imports
from flask import Flask, request, send_file, Response
import jsonpatch
import argparse
import http_constants.status

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


@flask_app.route("/render_scene", methods=["POST"])
def render_scene_json() -> Response:
    payload: NetworkPayload = request.get_json()

    # Log the received payload for debugging
    print(f"Received payload: client_id={payload.get('client_id')}, type={payload.get('type')}")

    ###############################################################################
    #   Parse the payload
    #
    client_id = payload["client_id"]
    if payload["type"] == "absolute":
        # Store the absolute scene for this client
        absolute_scenes[client_id] = payload["data"]
        scene_dict: SceneDict = payload["data"]
        # log the operation
        print(f"Rendering absolute scene for client_id={client_id}. Scene size: {len(str(scene_dict))} bytes")
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
        print(f"Rendering diff scene for client_id={client_id}. Diff size: {len(str(scene_diff))} bytes, Full scene size: {len(str(scene_dict))} bytes")
    else:
        assert False, f"Unknown rendering type: {payload['type']}"

    ###############################################################################
    # Load the scene from JSON
    #
    try:
        canvas_parsed, camera_parsed = json_parser.parse(scene_dict)
    except DiffableNdarraySerialisationError as e:
        # return 410 Gone
        return Response("DiffableNdarray not found.", status=http_constants.status.HttpStatus.GONE)

    ###############################################################################
    # Render the loaded scene with matplotlib
    #
    matplotlib_renderer = gsp_matplotlib.MatplotlibRenderer()
    image_png_data = matplotlib_renderer.render(canvas=canvas_parsed, camera=camera_parsed, show_image=False)
    matplotlib_renderer.close()  # free memory

    print(f"Rendered image size: {len(image_png_data)} bytes")

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
