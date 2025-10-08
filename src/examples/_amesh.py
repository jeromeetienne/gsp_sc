import matplotlib.pyplot
import matplotlib.image
import numpy as np
import os

import gsp_sc

# Setup __dirname__
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
