# stdlib imports
import os

# pip imports
import matplotlib.pyplot
import matplotlib.image
import numpy as np
import mpl3d.glm

# local imports
from common.mesh_parser.mesh_parser_meshio import MeshParserMeshio
from common.scene_examples import SceneExamples
import gsp_sc

# Setup __dirname__
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
# Add all visuals to the viewport
# =============================================================================

SceneExamples.add_all_visuals(viewport)

# =============================================================================
# Render the scene with a perspective camera
# =============================================================================
camera = gsp_sc.core.Camera(camera_type="perspective")
renderer = gsp_sc.renderer.matplotlib.MatplotlibRenderer()
image_png_buffer = renderer.render(canvas, camera, interactive=True)

# Save the rendered image to a file
image_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}.png"
with open(image_path, "wb") as png_file:
    png_file.write(image_png_buffer)
print(f"Rendered image saved to {image_path}")
