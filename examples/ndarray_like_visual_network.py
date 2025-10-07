"""
Basic example of creating and rendering a simple GSP scene with matplotlib.
"""

# stdlib imports
import os

# pip imports
import numpy as np

# local imports
import gsp_sc.src as gsp_sc
from gsp_sc.src.transform import TransformChain

__dirname__ = os.path.dirname(os.path.abspath(__file__))
# Set random seed for reproducibility
gsp_sc.core.Random.set_random_seed(10)
np.random.seed(10)

# =============================================================================
# Create a GSP scene
# =============================================================================
canvas = gsp_sc.core.Canvas(width=512, height=512, dpi=100)
camera = gsp_sc.core.Camera("perspective")

viewport = gsp_sc.core.Viewport(
    origin_x=0,
    origin_y=0,
    width=canvas.width,
    height=canvas.height,
    background_color=gsp_sc.Constants.White,
)
canvas.add(viewport=viewport)

# =============================================================================
# Add some random points with transformed positions
# =============================================================================

n_points = 300
positions_np = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float64)

# Use TransformChain to scale and translate positions
npy_url = f"file://{__dirname__}/data/sample_positions_3d.npy"
position_chain = TransformChain().load(npy_url).math_op('mul', 1/3).lambdaFunc(lambda x: x + 0.2).complete()

sizes_np = np.array([1])
colors_np = np.array([gsp_sc.Constants.Green])
pixels = gsp_sc.visuals.Pixels(positions=position_chain, sizes=sizes_np, colors=colors_np)
viewport.add(pixels)

# ==============================================================================
# Render locally the scene
# ==============================================================================

matplotlib_renderer = gsp_sc.renderer.matplotlib.MatplotlibRenderer()
image_png_data = matplotlib_renderer.render(canvas, camera)

# Save the image to a file
local_image_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}_local_image.png"
with open(local_image_path, "wb") as file_writer:
    file_writer.write(image_png_data)
print(f"Image saved to {local_image_path}")

# ==============================================================================
# Render the scene using a network renderer
# ==============================================================================
camera = gsp_sc.core.Camera("perspective")
network_renderer = gsp_sc.renderer.network.NetworkRenderer(
    server_url="http://localhost:5000/"
)
image_png_data = network_renderer.render(canvas, camera)

# ==============================================================================
# Save the image to a file
# ==============================================================================

server_image_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}_server_image.png"
with open(server_image_path, "wb") as file_writer:
    file_writer.write(image_png_data)
print(f"Image saved to {server_image_path}")
