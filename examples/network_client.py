"""
Example of using a network renderer to render a scene.

NOTE: This example requires the network server to be running. You can start the server by running the
`network_server.py` script in a separate terminal.
"""

from matplotlib import colors
import gsp
import gsp_matplotlib
import gsp_network
import numpy as np
import matplotlib.pyplot
import matplotlib.image

import os

__dirname__ = os.path.dirname(os.path.abspath(__file__))
# Set random seed for reproducibility
gsp.core.Random.set_random_seed(10)
np.random.seed(10)

###############################################################################
# Create a GSP scene
#
canvas = gsp.core.Canvas(width=512, height=512, dpi=100)
viewport = gsp.core.Viewport(
    origin_x=0,
    origin_y=0,
    width=canvas.width,
    height=canvas.height,
    background_color=gsp.Constants.White,
)
canvas.add(viewport=viewport)

# =============================================================================
# Add some random points
# =============================================================================

n_points = 1000
positions_np = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float32)
sizes_np = np.random.uniform(5, 10, n_points).astype(np.float32)
colors_np = np.array([gsp.Constants.Green])
pixels = gsp.visuals.Pixels(positions=positions_np, sizes=sizes_np, colors=colors_np)
viewport.add(pixels)

###############################################################################
# Add an image to viewport
#
image_path = f"{__dirname__}/images/UV_Grid_Sm.jpg"
image_data_np = matplotlib.image.imread(image_path)
image = gsp.visuals.Image(
    vertices=np.array([0.5, 0.5, 0.5]),
    image_extent=(-0.1, +0.1, -0.1, +0.1),
    image_data=image_data_np,
)
viewport.add(image)

###############################################################################
# Render the scene using the matplotlib renderer to verify it looks correct
#
camera = gsp.core.Camera("perspective")
matplotlib_renderer = gsp_matplotlib.MatplotlibRenderer()
image_png_data = matplotlib_renderer.render(canvas, camera)

# Save the image to a file
local_image_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}_local_image.png"
with open(local_image_path, "wb") as file_writer:
    file_writer.write(image_png_data)
print(f"Image saved to {local_image_path}")

# ###############################################################################
# Render the scene using a network renderer
#
camera = gsp.core.Camera("perspective")
network_renderer = gsp_network.NetworkRenderer(server_url="http://localhost:5000/")
image_png_data = network_renderer.render(canvas, camera)

###############################################################################
# Save the image to a file
#
server_image_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}_server_image.png"
with open(server_image_path, "wb") as file_writer:
    file_writer.write(image_png_data)
print(f"Image saved to {server_image_path}")
