"""
Basic example of creating and rendering a simple GSP scene with matplotlib.
"""

import numpy as np
import os
import gsp_sc

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
# Add some random points
#
n_points = 300
positions_np = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float64)
sizes_np = np.random.uniform(5, 10, n_points).astype(np.float32)
colors_np = np.array([gsp_sc.Constants.Green])
pixels = gsp_sc.visuals.Pixels(positions=positions_np, sizes=sizes_np, colors=colors_np)
viewport.add(pixels)


###############################################################################
# Render the scene with matplotlib
#
camera = gsp_sc.core.Camera(camera_type="perspective")
renderer = gsp_sc.renderer.matplotlib.MatplotlibRenderer()
image_png_buffer = renderer.render(canvas, camera, interactive=True)

# Save the rendered image to a file
image_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}.png"
with open(image_path, "wb") as png_file:
    png_file.write(image_png_buffer)
print(f"Rendered image saved to {image_path}")
