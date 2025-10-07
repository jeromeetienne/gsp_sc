import matplotlib.pyplot
import mpl3d.glm
import os

import gsp_sc.src as gsp_sc
import numpy as np


__dirname__ = os.path.dirname(os.path.abspath(__file__))
# Set random seed for reproducibility
gsp_sc.core.Random.set_random_seed(10)
np.random.seed(10)

canvas = gsp_sc.core.Canvas(width=512, height=512, dpi=100)

###############################################################################
# Create 4 viewports
#
canvas_half = canvas.width // 2
viewport1 = gsp_sc.core.Viewport(0, canvas_half, canvas_half, canvas_half, (1, 1, 1, 1))
canvas.add(viewport1)

viewport2 = gsp_sc.core.Viewport(canvas_half, canvas_half, canvas_half, canvas_half, (1, 1, 1, 1))
canvas.add(viewport2)

viewport3 = gsp_sc.core.Viewport(0, 0, canvas_half, canvas_half, (1, 1, 1, 1))
canvas.add(viewport3)

viewport4 = gsp_sc.core.Viewport(canvas_half, 0, canvas_half, canvas_half, (1, 1, 1, 1))
canvas.add(viewport4)

###############################################################################
# Add a mesh and add it to all viewports
#
obj_mesh_path = f"{__dirname__}/data/bunny.obj"
mesh = gsp_sc.visuals.Mesh.from_obj_file(
    obj_mesh_path,
    cmap=matplotlib.pyplot.get_cmap("magma"),
    edgecolors=(0, 0, 0, 0.25), # type: ignore
)
viewport1.add(mesh)
viewport2.add(mesh)
viewport3.add(mesh)
viewport4.add(mesh)

###############################################################################
# setup one camera per viewport
#
camera1 = gsp_sc.core.Camera(camera_type="perspective")
camera1.mpl3d_camera.trackball._model =  mpl3d.glm.yrotate(-30) @ mpl3d.glm.xrotate(-10)
camera1.mpl3d_camera.transform = camera1.mpl3d_camera.proj @ camera1.mpl3d_camera.view @ camera1.mpl3d_camera.trackball.model.T

camera2 = gsp_sc.core.Camera(camera_type="ortho")
camera2.mpl3d_camera.trackball._model =  mpl3d.glm.xrotate(-90)
camera2.mpl3d_camera.transform = camera2.mpl3d_camera.proj @ camera2.mpl3d_camera.view @ camera2.mpl3d_camera.trackball.model.T

camera3 = gsp_sc.core.Camera(camera_type="ortho")
camera3.mpl3d_camera.trackball._model =  mpl3d.glm.yrotate(-90)
camera3.mpl3d_camera.transform = camera3.mpl3d_camera.proj @ camera3.mpl3d_camera.view @ camera3.mpl3d_camera.trackball.model.T

camera4 = gsp_sc.core.Camera(camera_type="perspective")
camera4.mpl3d_camera.trackball._model =  np.eye(4)
camera4.mpl3d_camera.transform = camera4.mpl3d_camera.proj @ camera4.mpl3d_camera.view @ camera4.mpl3d_camera.trackball.model.T

###############################################################################
# Render the scene
#
matplotlib_renderer = gsp_sc.renderer.matplotlib.MatplotlibRenderer()
viewports = [viewport1, viewport2, viewport3, viewport4]
cameras = [camera1, camera2, camera3, camera4]
image_png_buffer = matplotlib_renderer.render_viewports(canvas, viewports=viewports, cameras=cameras, show_image=True)

# Save the rendered image to a file
image_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}.png"
with open(image_path, "wb") as png_file:
    png_file.write(image_png_buffer)
print(f"Rendered image saved to {image_path}")
