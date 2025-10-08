import matplotlib.pyplot
from examples.common.mesh_parser.mesh_parser_meshio import MeshParserMeshio
import gsp_sc
import numpy as np
import matplotlib.image

import mpl3d.glm
import os

__dirname__ = os.path.dirname(os.path.abspath(__file__))
# Set random seed for reproducibility
gsp_sc.core.Random.set_random_seed(10)
np.random.seed(10)

canvas = gsp_sc.core.Canvas(width=512, height=512, dpi=100)

###############################################################################
# Create two viewports
viewport1 = gsp_sc.core.Viewport(0, 0, 256, 256, (1, 1, 1, 1))
canvas.add(viewport1)

viewport2 = gsp_sc.core.Viewport(256, 0, 256, 256, (1, 1, 1, 1))
canvas.add(viewport2)

viewport3 = gsp_sc.core.Viewport(0, 256, 256, 256, (1, 1, 1, 1))
canvas.add(viewport3)

###############################################################################
# Add some random points to viewport1 and viewport2
#
n_points = 100
positions_np = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float32)
sizes_np = np.random.uniform(5, 10, n_points).astype(np.float32)
colors_np = np.array([[0, 1, 0, 0.5]], dtype=np.float32)
pixels = gsp_sc.visuals.Pixels(positions=positions_np, sizes=sizes_np, colors=colors_np)
viewport1.add(pixels)
viewport2.add(pixels)

###############################################################################
# Add an image to viewport1
#
image_path = f"{__dirname__}/images/UV_Grid_Sm.jpg"
image_data_np = matplotlib.image.imread(image_path)
image_position = np.array([0, 0, 0])
image = gsp_sc.visuals.Image(position=image_position, image_extent=(-1, +1, -1, +1), image_data=image_data_np)
viewport2.add(image)

# =============================================================================
# Add a mesh from an OBJ file
# =============================================================================
obj_mesh_path = f"{__dirname__}/data/bunny.obj"
vertices_coords, faces_indices, uvs_coords, normals_coords = MeshParserMeshio.parse_obj_file(obj_mesh_path)
vertices_coords = mpl3d.glm.fit_unit_cube(vertices_coords)
mesh = gsp_sc.visuals.Mesh(vertices_coords, faces_indices, cmap=matplotlib.pyplot.get_cmap("magma"), edgecolors=(0, 0, 0, 0.25))  # type: ignore

viewport2.add(mesh)
viewport3.add(mesh)

###############################################################################
# Render the scene
#
camera = gsp_sc.core.Camera(camera_type="perspective")

matplotlib_renderer = gsp_sc.renderer.matplotlib.MatplotlibRenderer()
image_png_buffer = matplotlib_renderer.render_viewports(
    canvas,
    viewports=[viewport1, viewport2, viewport3],
    cameras=[camera, camera, camera],
    show_image=True,
)

# Save the rendered image to a file
image_path = f"{__dirname__}/output/viewport_multiple.png"
with open(image_path, "wb") as png_file:
    png_file.write(image_png_buffer)
print(f"Rendered image saved to {image_path}")
