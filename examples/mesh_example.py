"""
Basic example of creating and rendering a simple GSP scene with matplotlib.
"""

# pip imports
import numpy as np
import os
import mpl3d.glm
import matplotlib.pyplot

# local imports
from common.mesh_parser import MeshParserMeshio
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
    background_color=gsp.Constants.White,
)
canvas.add(viewport=viewport)

# =============================================================================
# Add content to the viewport
# =============================================================================

obj_mesh_path = f"{__dirname__}/data/bunny.obj"
vertices_coords, faces_indices, uvs_coords, normals_coords = MeshParserMeshio.parse_obj_file(obj_mesh_path)
vertices_coords = mpl3d.glm.fit_unit_cube(vertices_coords)
mesh = gsp.visuals.Mesh(vertices_coords, faces_indices, cmap=matplotlib.pyplot.get_cmap("magma"), edgecolors=(0, 0, 0, 0.25))  # type: ignore
viewport.add(mesh)

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
