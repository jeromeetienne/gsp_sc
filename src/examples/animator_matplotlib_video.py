"""
Basic example of creating and rendering a simple GSP scene with matplotlib.
"""

# stdlib imports
import os

# pip imports
import numpy as np

# local imports
import gsp_sc
from examples.common.gsp_animator import GspAnimatorMatplotlib

__dirname__ = os.path.dirname(os.path.abspath(__file__))
# Set random seed for reproducibility
# gsp_sc.core.Random.set_random_seed(10)
# np.random.seed(10)

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
n_points = 10
positions = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float32)
sizes = np.array([100 for _ in range(n_points)], np.float32)
colors = np.array([gsp_sc.Constants.Green for _ in range(n_points)], np.float32)
pixels = gsp_sc.visuals.Pixels(positions, sizes, colors)
viewport.add(pixels)

# =============================================================================
# Define random velocities for each point
# =============================================================================
velocities = np.zeros((n_points, 3), dtype=np.float32)
for i in range(n_points):
    angle = np.random.uniform(0, 2 * np.pi)
    speed = 1
    velocities[i, 0] = speed * np.cos(angle)
    velocities[i, 1] = speed * np.sin(angle)

###############################################################################
# Render the scene with matplotlib
#
camera = gsp_sc.core.Camera(camera_type="ortho")
renderer = gsp_sc.renderer.matplotlib.MatplotlibRenderer()
renderer.render(canvas, camera)

# =============================================================================
# Animate the scene with matplotlib
# =============================================================================
current_time = 0.0
target_fps = 60


def animator_callback() -> list[gsp_sc.core.VisualBase]:
    # Update the time tracking
    global current_time
    delta_time = 1.0 / target_fps
    current_time += delta_time

    # update positions with velocities
    positions[:] += velocities * delta_time

    # bounce on the walls
    wall_limit = 1
    out_of_bounds_x = np.abs(positions[:, 0]) > wall_limit
    out_of_bounds_y = np.abs(positions[:, 1]) > wall_limit
    out_of_bounds_z = np.abs(positions[:, 2]) > wall_limit
    velocities[out_of_bounds_x, 0] *= -1
    velocities[out_of_bounds_y, 1] *= -1
    velocities[out_of_bounds_z, 2] *= -1

    # Render the scene to update the positions
    # - this is needed because those positions are rotated in 3d space based on the camera position
    # - this is not needed when the data is going directly to matplotlib (e.g. sizes, colors)
    # - this is not needed when the scene is rendered via network renderer
    renderer.render(canvas, camera)

    changed_visuals: list[gsp_sc.core.VisualBase] = [pixels]
    return changed_visuals


video_path = os.path.join(__dirname__, f"output/{os.path.basename(__file__).replace('.py', '')}.mp4")
print(f"Saving video to {video_path}")
animator = GspAnimatorMatplotlib(renderer, target_fps=target_fps, video_path=video_path)
animator.animate(canvas, camera, [animator_callback])
