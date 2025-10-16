# stdlib imports
import os

# pip imports
import numpy as np

# local imports
from common.scene_examples import SceneExamples
import gsp
import gsp_matplotlib

# Setup __dirname__
__dirname__ = os.path.dirname(os.path.abspath(__file__))
# Set random seed for reproducibility
gsp.core.Random.set_random_seed(10)
np.random.seed(10)

# =============================================================================
# Create a canvas and a viewport
# =============================================================================
canvas = gsp.core.Canvas(512, 512, 100)
viewport = gsp.core.Viewport(0, 0, canvas.width, canvas.height, gsp.Constants.White)
canvas.add(viewport)

# =============================================================================
# Add all visuals to the viewport
# =============================================================================

SceneExamples.add_all_visuals(viewport)

# =============================================================================
# Render the scene with a perspective camera
# =============================================================================
camera = gsp.core.Camera(camera_type="perspective")
renderer = gsp_matplotlib.MatplotlibRenderer()
image_png_buffer = renderer.render(canvas, [viewport], [camera], interactive=True)

# Save the rendered image to a file
image_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}.png"
with open(image_path, "wb") as png_file:
    png_file.write(image_png_buffer)
print(f"Rendered image saved to {image_path}")
