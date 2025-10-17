"""
Basic example of creating and rendering a simple GSP scene with matplotlib.
"""

# pip imports
import numpy as np
import os
import matplotlib.pyplot

# local imports
import gsp
from gsp_object3d_matplotlib.renderer import Renderer
from gsp.geometry import Geometry
from gsp.materials import PointsMaterial
from gsp.objects.points import Points
from common.scene_examples import SceneExamples

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

# # Add points
# point_count = 1000
# geometry = Geometry(np.random.uniform(-1, 1, (point_count, 3)))
# colors = np.array([[1, 0, 0, 1] for i in range(point_count)])
# material = PointsMaterial(colors=colors)
# points = Points(geometry, material)
# points.scale[:] = 0.5
# viewport.scene.add(points)


# bunny_points = SceneExamples.getBunnyPoints()
# viewport.scene.add(bunny_points)

light1 = SceneExamples.getThreePointsLighting()
viewport.scene.add(light1)

textured_mesh = SceneExamples.getHeadTexturedMesh()
viewport.scene.add(textured_mesh)

# =============================================================================
# Render the canvas with a perspective camera
# =============================================================================


camera = gsp.cameras.CameraOrthographic()
viewport.scene.add(camera)
camera.position = np.array([0.0, 0.0, 5.0])


renderer = Renderer()
renderer.render(viewport.scene, camera)

# show the result
matplotlib.pyplot.show(block=True)
