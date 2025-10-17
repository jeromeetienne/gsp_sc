"""
Basic example of creating and rendering a simple GSP scene with matplotlib.
"""

import matplotlib.image
import numpy as np
import os
import gsp
import gsp_matplotlib

__dirname__ = os.path.dirname(os.path.abspath(__file__))
# Set random seed for reproducibility
gsp.core.Random.set_random_seed(10)
np.random.seed(10)

# =============================================================================
# Create a canvas and a viewport
# =============================================================================
canvas = gsp.core.Canvas(width=512, height=512, dpi=100)
viewport = gsp.core.Viewport(
    origin_x=0,
    origin_y=0,
    width=canvas.width,
    height=canvas.height,
    background_color=gsp.core.Constants.White,
)
canvas.add(viewport=viewport)

# =============================================================================
# Add some random points
# =============================================================================
image_path = f"{__dirname__}/images/UV_Grid_Sm.jpg"
image_data_np = matplotlib.image.imread(image_path)
texture = gsp.core.Texture(image_data=image_data_np)
image_position = np.array([0, 0, 0])
image = gsp.visuals.Image(position=image_position, image_extent=(-1, +1, -1, +1), texture=texture)
viewport.add(image)

# =============================================================================
# Render the canvas with a perspective camera
# =============================================================================
camera = gsp.core.Camera(camera_type="perspective")
renderer = gsp_matplotlib.MatplotlibRenderer()
image_png_buffer = renderer.render(canvas, [viewport], [camera], interactive=True)

# Save the rendered image to a file
image_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}.png"
with open(image_path, "wb") as png_file:
    png_file.write(image_png_buffer)
print(f"Rendered image saved to {image_path}")
