"""
Example of using a network renderer to render a scene.

NOTE: This example requires the network server to be running. You can start the server by running the
`network_server.py` script in a separate terminal.
"""

# stdlib imports
import os

# pip imports
import numpy as np

# import jsondiff
import json
import jsonpatch


# local imports
import gsp


__dirname__ = os.path.dirname(os.path.abspath(__file__))
# Set random seed for reproducibility
gsp.core.Random.set_random_seed(10)
np.random.seed(10)

###############################################################################
# Create a GSP scene
#
camera = gsp.core.Camera("perspective")
canvas = gsp.core.Canvas(width=512, height=512, dpi=100)
viewport = gsp.core.Viewport(
    origin_x=0,
    origin_y=0,
    width=canvas.width,
    height=canvas.height,
    background_color=gsp.Constants.White,
)
canvas.add(viewport=viewport)

# Add some random points
n_points = 10
positions_np = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float32)
sizes_np = np.random.uniform(5, 10, n_points).astype(np.float32)
colors_np = np.array([gsp.Constants.Green])
pixels = gsp.visuals.Pixels(positions=positions_np, sizes=sizes_np, colors=colors_np)
viewport.add(pixels)


###############################################################################
#   Render the scene in JSON format
#
json_renderer = gsp.renderer.json.JsonRenderer()
scene_dict1 = json_renderer.render(canvas, camera)
# print(f"Initial scene JSON:\n{scene_dict}")

###############################################################################
#   modify the scene - move the points randomly
#
# displacement_np = np.random.uniform(-0.1, 0.1, (1, 3)).astype(np.float32)
sizes_np[0] = 123
pixels.sizes = sizes_np

###############################################################################
#   Render the scene in JSON format again
#
json_renderer = gsp.renderer.json.JsonRenderer()
scene_dict2 = json_renderer.render(canvas, camera)
# print(f"Initial scene JSON:\n{scene_dict}")

###############################################################################
#   Compute the diff between the two scene JSONs and reconstruct the second scene from the first and the diff
#
# scene_diff = jsondiff.diff(scene_dict1, scene_dict2)
scene_diff = jsonpatch.JsonPatch.from_diff(scene_dict1, scene_dict2)
print(f"Scene diff JSON:\n{scene_diff}")


# def convert_keys_symbol_to_str(data):
#     if not isinstance(data, dict):
#         return data
#     data_dict: dict = data
#     result = {}
#     for key, value in data_dict.items():
#         if hasattr(key, "__module__") and key.__module__ == "symbol":
#             key = str(key)
#         result[key] = convert_keys_symbol_to_str(value)
#     return result

# scene_diff = convert_keys_symbol_to_str(scene_diff)
scene_diff_json = str(scene_diff)


###############################################################################
#   Reconstruct the second scene from the first and the diff
#
# scene_diff_reconstructed = json.loads(scene_diff_json)
# scene_dict3 = jsondiff.patch(scene_dict1, scene_diff_reconstructed)
# scene_dict3 = DeepDiff(scene_dict1, scene_diff_reconstructed)
scene_dict3 = jsonpatch.apply_patch(scene_dict1, scene_diff_json)
print(f"Reconstructed scene JSON:=")
print(json.dumps(scene_dict3, indent=4))
