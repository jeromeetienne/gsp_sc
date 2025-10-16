# stdlib imports
import os

# pip imports
import numpy as np
import matplotlib.pyplot
import mpl3d.glm

# local imports
from common.mesh_parser.mesh_parser_meshio import MeshParserMeshio
import gsp
import gsp_matplotlib


__dirname__ = os.path.dirname(os.path.abspath(__file__))
# Set random seed for reproducibility
gsp.core.Random.set_random_seed(10)
np.random.seed(10)

canvas = gsp.core.Canvas(width=512, height=512, dpi=100)

###############################################################################
# Create 4 viewports
#
canvas_half = canvas.width // 2
viewport1 = gsp.core.Viewport(0, canvas_half, canvas_half, canvas_half, (1, 1, 1, 1))
canvas.add(viewport1)

viewport2 = gsp.core.Viewport(canvas_half, canvas_half, canvas_half, canvas_half, (1, 1, 1, 1))
canvas.add(viewport2)

viewport3 = gsp.core.Viewport(0, 0, canvas_half, canvas_half, (1, 1, 1, 1))
canvas.add(viewport3)

viewport4 = gsp.core.Viewport(canvas_half, 0, canvas_half, canvas_half, (1, 1, 1, 1))
canvas.add(viewport4)

###############################################################################
# Add a mesh and add it to all viewports
#
obj_mesh_path = f"{__dirname__}/data/bunny.obj"
vertices_coords, faces_indices, uvs_coords, normals_coords = MeshParserMeshio.parse_obj_file(obj_mesh_path)
vertices_coords = mpl3d.glm.fit_unit_cube(vertices_coords)
mesh = gsp.visuals.Mesh(vertices_coords, faces_indices, cmap=matplotlib.pyplot.get_cmap("magma"), edgecolors=(0, 0, 0, 0.25))  # type: ignore

viewport1.add(mesh)
viewport2.add(mesh)
viewport3.add(mesh)
viewport4.add(mesh)

###############################################################################
# setup one camera per viewport
#
camera1 = gsp.core.Camera(camera_type="perspective")
camera1.mpl3d_camera.trackball._model = mpl3d.glm.yrotate(-30) @ mpl3d.glm.xrotate(-10)
camera1.mpl3d_camera.transform = camera1.mpl3d_camera.proj @ camera1.mpl3d_camera.view @ camera1.mpl3d_camera.trackball.model.T

camera2 = gsp.core.Camera(camera_type="ortho")
camera2.mpl3d_camera.trackball._model = mpl3d.glm.xrotate(-90)
camera2.mpl3d_camera.transform = camera2.mpl3d_camera.proj @ camera2.mpl3d_camera.view @ camera2.mpl3d_camera.trackball.model.T

camera3 = gsp.core.Camera(camera_type="ortho")
camera3.mpl3d_camera.trackball._model = mpl3d.glm.yrotate(-90)
camera3.mpl3d_camera.transform = camera3.mpl3d_camera.proj @ camera3.mpl3d_camera.view @ camera3.mpl3d_camera.trackball.model.T

camera4 = gsp.core.Camera(camera_type="perspective")
camera4.mpl3d_camera.trackball._model = np.eye(4)
camera4.mpl3d_camera.transform = camera4.mpl3d_camera.proj @ camera4.mpl3d_camera.view @ camera4.mpl3d_camera.trackball.model.T

###############################################################################
# Render the scene
#
matplotlib_renderer = gsp_matplotlib.MatplotlibRenderer()
viewports = [viewport1, viewport2, viewport3, viewport4]
cameras = [camera1, camera2, camera3, camera4]
image_png_buffer = matplotlib_renderer.render(canvas, viewports, cameras, interactive=True)

# Save the rendered image to a file
image_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}.png"
with open(image_path, "wb") as png_file:
    png_file.write(image_png_buffer)
print(f"Rendered image saved to {image_path}")
