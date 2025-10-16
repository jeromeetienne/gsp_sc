"""
Example of serialising a scene to JSON and loading it back.
It is rendered before and after to verify the scene serialisation works correctly.
"""

import gsp
import gsp_matplotlib
import numpy as np
import matplotlib.image

import os
import json


__dirname__ = os.path.dirname(os.path.abspath(__file__))
# Set random seed for reproducibility
gsp.core.Random.set_random_seed(10)
np.random.seed(10)

canvas = gsp.core.Canvas(512, 512, 100)

###############################################################################
# Create two viewports
#
viewport1 = gsp.core.Viewport(0, 0, 256, 256, gsp.Constants.White)
canvas.add(viewport1)

viewport2 = gsp.core.Viewport(256, 0, 256, 256, gsp.Constants.White)
canvas.add(viewport2)

###############################################################################
# Add some random points to both viewports
#
n_points = 100
positions_np = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float32)
sizes_np = np.random.uniform(5, 10, n_points).astype(np.float32)
colors_np = np.array([[0, 1, 0, 0.5]], dtype=np.float32)
pixels = gsp.visuals.Pixels(positions_np, sizes_np, colors_np)
viewport1.add(pixels)
viewport2.add(pixels)

###############################################################################
# Add an image to viewport1
#

image_path = f"{__dirname__}/images/UV_Grid_Sm.jpg"
image_data_np = matplotlib.image.imread(image_path)
texture = gsp.core.Texture(image_data=image_data_np)
image = gsp.visuals.Image(np.array([0.5, 0.5, 0.5]), (-1, +1, -1, +1), texture)
viewport1.add(image)

###############################################################################
# Save and render the scene to verify it looks correct
#
camera = gsp.core.Camera("perspective")
matplotlib_renderer = gsp_matplotlib.MatplotlibRenderer()
rendered_image_png_data = matplotlib_renderer.render(canvas, [viewport1, viewport2], [camera, camera])

# save the rendered image to a file
rendered_image_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}_original_image.png"
with open(rendered_image_path, "wb") as f:
    f.write(rendered_image_png_data)

print(f"original Rendered image saved to: {rendered_image_path}")

###############################################################################
# Export the scene to JSON
#
json_renderer = gsp.renderer.json.JsonRenderer()
scene_dict = json_renderer.render(canvas, [viewport1, viewport2], [camera, camera])
scene_json = json.dumps(scene_dict, indent=4)

json_output_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}.gsp.json"
with open(json_output_path, "w") as json_file:
    json_file.write(scene_json)
print(f"Scene exported to JSON and saved to {json_output_path}")

###############################################################################
# Load the scene from JSON
#
json_parser = gsp.renderer.json.JsonParser()
canvas_parsed, viewports_parsed, cameras_parsed = json_parser.parse(scene_json)

###############################################################################
# Render the loaded scene with matplotlib to visually verify it was loaded correctly
#
matplotlib_renderer = gsp_matplotlib.MatplotlibRenderer()
rendered_loaded_image_png_data = matplotlib_renderer.render(canvas_parsed, viewports_parsed, cameras_parsed)

# save the rendered loaded image to a file
rendered_loaded_image_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}_parsed_image.png"
with open(rendered_loaded_image_path, "wb") as f:
    f.write(rendered_loaded_image_png_data)

print(f"Network rendered image saved to: {rendered_loaded_image_path}")
