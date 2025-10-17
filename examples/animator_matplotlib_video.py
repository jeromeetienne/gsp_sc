"""
Basic example of creating and rendering a simple GSP scene with matplotlib.
"""

# stdlib imports
import os

# pip imports
import numpy as np

# local imports
import gsp
import gsp_matplotlib
from common.gsp_animator import GspAnimatorMatplotlib

__dirname__ = os.path.dirname(os.path.abspath(__file__))
# Set random seed for reproducibility
gsp.core.Random.set_random_seed(10)
np.random.seed(10)

# =============================================================================
# Create a GSP canvas
# =============================================================================
canvas = gsp.core.Canvas(512, 512, 100)
viewport = gsp.core.Viewport(0, 0, canvas.width, canvas.height, gsp.core.Constants.White)
canvas.add(viewport)


# Initializee the camera
camera = gsp.core.Camera(camera_type="ortho")

# matplotlib renderer
renderer = gsp_matplotlib.MatplotlibRenderer()

# Save the animation to a video file
video_path = os.path.join(__dirname__, f"output/{os.path.basename(__file__).replace('.py', '')}.mp4")
print(f"Saving video to {video_path}")

# Init a animator
animator = GspAnimatorMatplotlib(renderer, fps=60, video_duration=10.0, video_path=video_path)


@animator.on_video_saved.event_listener
def on_save():
    # log the video path
    print(f"Video saved to: {video_path}")

    # stop the animator
    animator.stop()

    # close the renderer
    renderer.close()


# =============================================================================
# Add some random points
# =============================================================================
n_points = 10
positions = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float32)
sizes = np.array([100 for _ in range(n_points)], np.float32)
colors = np.array([gsp.core.Constants.Green for _ in range(n_points)], np.float32)
pixels = gsp.visuals.Pixels(positions, sizes, colors)
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


# =============================================================================
# Animate the scene with matplotlib
# =============================================================================


@animator.event_listener
def animator_callback(delta_time: float) -> list[gsp.core.VisualBase]:
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
    renderer.render(canvas, [viewport], [camera])

    changed_visuals: list[gsp.core.VisualBase] = [pixels]
    return changed_visuals


# Create the animator and start the animation
animator.start(canvas, [viewport], [camera])
