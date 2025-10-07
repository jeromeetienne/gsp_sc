"""
Example of using a network renderer to render a scene.

NOTE: This example requires the network server to be running. You can start the server by running the
`network_server.py` script in a separate terminal.
"""

from matplotlib import colors
import gsp_sc.src as gsp_sc
import numpy as np
import matplotlib.pyplot
import matplotlib.image

import os

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

# Add some random points
n_points = 1000
positions_np = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float32)
sizes_np = np.random.uniform(5, 10, n_points).astype(np.float32)
colors_np = np.array([gsp_sc.Constants.Green])
pixels = gsp_sc.visuals.Pixels(positions=positions_np, sizes=sizes_np, colors=colors_np)
viewport.add(pixels)

###############################################################################
# Add an image to viewport
#
image_path = f"{__dirname__}/images/UV_Grid_Sm.jpg"
image_data_np = matplotlib.image.imread(image_path)
image = gsp_sc.visuals.Image(
    position=np.array([0.5, 0.5, 0.5]),
    image_extent=(-0.1, +0.1, -0.1, +0.1),
    image_data=image_data_np,
)
viewport.add(image)

###############################################################################
# Add a mesh
#
obj_mesh_path = f"{__dirname__}/data/bunny.obj"
mesh = gsp_sc.visuals.Mesh.from_obj_file(
    obj_mesh_path,
    cmap=matplotlib.pyplot.get_cmap("magma"),
    edgecolors=(0, 0, 0, 0.25),  # type: ignore
)
viewport.add(mesh)

###############################################################################
# Render the scene using the matplotlib renderer to verify it looks correct
#
camera = gsp_sc.core.Camera("perspective")
matplotlib_renderer = gsp_sc.renderer.matplotlib.MatplotlibRenderer()
image_png_data = matplotlib_renderer.render(canvas, camera)

# Save the image to a file
local_image_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}_local_image.png"
with open(local_image_path, "wb") as file_writer:
    file_writer.write(image_png_data)
print(f"Image saved to {local_image_path}")

# ###############################################################################
# Render the scene using a network renderer
#
camera = gsp_sc.core.Camera("perspective")
network_renderer = gsp_sc.renderer.network.NetworkRenderer(
    server_url="http://localhost:5000/"
)
image_png_data = network_renderer.render(canvas, camera)

###############################################################################
# Save the image to a file
#
server_image_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}_server_image.png"
with open(server_image_path, "wb") as file_writer:
    file_writer.write(image_png_data)
print(f"Image saved to {server_image_path}")
