"""
Example of using a network renderer to render a scene.

NOTE: This example requires the network server to be running. You can start the server by running the
`network_server.py` script in a separate terminal.
"""

import gsp
import gsp_matplotlib
import gsp_network
import numpy as np
import os

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
# Render the scene using the matplotlib renderer to verify it looks correct
#
matplotlib_renderer = gsp_matplotlib.MatplotlibRenderer()
image_png_data = matplotlib_renderer.render(canvas, camera)

# Save the image to a file
local_image_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}_local_image_pre_diff.png"
with open(local_image_path, "wb") as file_writer:
    file_writer.write(image_png_data)
print(f"Image saved to {local_image_path}")

###############################################################################
# Render the scene using a network renderer
#
network_renderer = gsp_network.NetworkRenderer(
    server_url="http://localhost:5000/",
    jsondiff_allowed=True,
)
image_png_data = network_renderer.render(canvas, camera)

###############################################################################
# Save the image to a file
#
server_image_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}_server_image_pre_diff.png"
with open(server_image_path, "wb") as file_writer:
    file_writer.write(image_png_data)
print(f"Image saved to {server_image_path}")

###############################################################################
# Modify the scene - change the size of the first point

sizes_np[0] = 123.0
pixels.sizes = sizes_np

###############################################################################
# Render the scene using the matplotlib renderer to verify it looks correct
#
image_png_data = matplotlib_renderer.render(canvas, camera)

# Save the image to a file
local_image_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}_local_image_post_diff.png"
with open(local_image_path, "wb") as file_writer:
    file_writer.write(image_png_data)
print(f"Image saved to {local_image_path}")

###############################################################################
# Render the scene using a network renderer
#
image_png_data = network_renderer.render(canvas, camera)

###############################################################################
# Save the image to a file
#
server_image_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}_server_image_post_diff.png"
with open(server_image_path, "wb") as file_writer:
    file_writer.write(image_png_data)
print(f"Image saved to {server_image_path}")
