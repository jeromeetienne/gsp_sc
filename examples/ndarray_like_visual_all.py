"""
Basic example of creating and rendering a simple GSP scene with matplotlib.
"""

# stdlib imports
import os
import json

# pip imports
import numpy as np

# local imports
import gsp_sc
import gsp_matplotlib
from gsp_sc.types import DiffableNdarray
from common.transform import TransformChain

__dirname__ = os.path.dirname(os.path.abspath(__file__))
# Set random seed for reproducibility
gsp_sc.core.Random.set_random_seed(10)
np.random.seed(10)

# =============================================================================
# Create a canvas and a viewport
# =============================================================================
canvas = gsp_sc.core.Canvas(512, 512, 100)
viewport = gsp_sc.core.Viewport(0, 0, canvas.width, canvas.height, gsp_sc.Constants.White)
canvas.add(viewport)

# =============================================================================
# Add some random points with ndarray-like positions
# =============================================================================

n_points = 300
positions_np = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float64)
# Use TransformChain to scale and translate positions
# position_ndarray_like = TransformChain(positions_np).math_op("mul", 1 / 3).math_op("add", 0.2).complete()
position_ndarray_like = DiffableNdarray(positions_np)

sizes_ndarray_like = TransformChain(np.ones((n_points,))).lambdaFunc(lambda x: x * 100).complete()
colors_np = np.array([gsp_sc.Constants.Green])
pixels = gsp_sc.visuals.Pixels(position_ndarray_like, sizes_ndarray_like, colors_np)
viewport.add(pixels)

# =============================================================================
# Export the scene to JSON
# =============================================================================
camera = gsp_sc.core.Camera("perspective")
json_renderer = gsp_sc.renderer.JsonRenderer()
scene_dict = json_renderer.render(canvas, camera)
scene_json = json.dumps(scene_dict, indent=4)

# save to file as json
json_output_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}.gsp.json"
with open(json_output_path, "w") as file_writer:
    file_writer.write(scene_json)

print(f"Scene exported to JSON and saved to {json_output_path}. length={len(scene_json)}")

# =============================================================================
# Import the scene from JSON
# =============================================================================
json_parser = gsp_sc.renderer.JsonParser()
canvas_parsed, camera_parsed = json_parser.parse(scene_json)

# =============================================================================
# Render the scene with matplotlib
# =============================================================================
renderer = gsp_matplotlib.MatplotlibRenderer()
image_png_buffer = renderer.render(canvas_parsed, camera_parsed, interactive=True)

# Save the rendered image to a file
image_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}.png"
with open(image_path, "wb") as png_file:
    png_file.write(image_png_buffer)
print(f"Rendered image saved to {image_path}")
