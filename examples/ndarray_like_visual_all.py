"""
Basic example of creating and rendering a simple GSP scene with matplotlib.
"""

# stdlib imports
import os
import json

# pip imports
import numpy as np
import matplotlib.pyplot
import matplotlib.image

# local imports
import gsp_sc.src as gsp_sc
from gsp_sc.src.types.diffable_ndarray.diffable_ndarray import DiffableNdarray
from gsp_sc.src.transform import TransformChain

__dirname__ = os.path.dirname(os.path.abspath(__file__))
# Set random seed for reproducibility
gsp_sc.core.Random.set_random_seed(10)
np.random.seed(10)

###############################################################################
# Create a GSP scene
#
canvas = gsp_sc.core.Canvas(width=512, height=512, dpi=100)
viewport = gsp_sc.core.Viewport(
    origin_x=0,
    origin_y=0,
    width=canvas.width,
    height=canvas.height,
    background_color=gsp_sc.Constants.White,
)
canvas.add(viewport=viewport)

###############################################################################
# Add some random points with transformed positions
#

n_points = 300
positions_np = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float64)
# Use TransformChain to scale and translate positions
# position_ndarray_like = TransformChain(positions_np).math_op("mul", 1 / 3).math_op("add", 0.2).complete()
position_ndarray_like = DiffableNdarray(positions_np)


sizes_np = np.array([10])
colors_np = np.array([gsp_sc.Constants.Green])
pixels = gsp_sc.visuals.Pixels(positions=position_ndarray_like, sizes=sizes_np, colors=colors_np)
viewport.add(pixels)

# =============================================================================
# Add an image to viewport
# =============================================================================

image_path = f"{__dirname__}/images/UV_Grid_Sm.jpg"
image_data_np = matplotlib.image.imread(image_path)
image = gsp_sc.visuals.Image(
    position=np.array([0.5, 0.5, 0.5]),
    image_extent=(-1, +1, -1, +1),
    image_data=image_data_np,
)
viewport.add(image)

# =============================================================================
# Add a mesh to viewport
# =============================================================================
obj_mesh_path = f"{__dirname__}/data/bunny.obj"
mesh = gsp_sc.visuals.Mesh.from_obj_file(
    obj_mesh_path,
    cmap=matplotlib.pyplot.get_cmap("magma"),
    edgecolors=(0, 0, 0, 0.25),  # type: ignore
)
viewport.add(mesh)

# =============================================================================
# Export the scene to JSON
# =============================================================================
camera = gsp_sc.core.Camera("perspective")
json_renderer = gsp_sc.renderer.json.JsonRenderer()
scene_dict = json_renderer.render(canvas, camera)
scene_json = json.dumps(scene_dict, indent=4)

# save to file as json
json_output_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}.gsp.json"
with open(json_output_path, "w") as file_writer:
    file_writer.write(scene_json)

print(f"Scene exported to JSON and saved to {json_output_path}. length={len(scene_json)}")

###############################################################################
# Import the scene from JSON
#

json_parser = gsp_sc.renderer.json.JsonParser()
canvas_parsed, camera_parsed = json_parser.parse(scene_json)

###############################################################################
# Render the scene with matplotlib
#
renderer = gsp_sc.renderer.matplotlib.MatplotlibRenderer()
image_png_buffer = renderer.render(canvas_parsed, camera_parsed, interactive=True)

# Save the rendered image to a file
image_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}.png"
with open(image_path, "wb") as png_file:
    png_file.write(image_png_buffer)
print(f"Rendered image saved to {image_path}")
