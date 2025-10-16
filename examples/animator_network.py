# !/usr/bin/env python3

"""
Basic example of creating and rendering a simple GSP scene with matplotlib.
"""

# stdlib imports
import os

# pip imports
import numpy as np

# local imports
import gsp
import gsp_network
from common.fps_monitor import FpsMonitor
from common.gsp_animator import GspAnimatorNetwork


__dirname__ = os.path.dirname(os.path.abspath(__file__))
# Set random seed for reproducibility
gsp.core.Random.set_random_seed(10)
np.random.seed(10)


###############################################################################
# Create a GSP scene
#
canvas = gsp.core.Canvas(256, 256, 100)
viewport = gsp.core.Viewport(0, 0, canvas.width, canvas.height, gsp.Constants.White)
canvas.add(viewport)


###############################################################################
# Add some random points
#
n_points = 3_000
positions = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float32)
sizes = np.array([50 for _ in range(n_points)], np.float32)
colors = np.array([gsp.Constants.Green for _ in range(n_points)], np.float32)

positions = gsp.types.DiffableNdarray(positions)
sizes = gsp.types.DiffableNdarray(sizes)
colors = gsp.types.DiffableNdarray(colors)

pixels = gsp.visuals.Pixels(positions, sizes, colors)
viewport.add(pixels)

###############################################################################
# Render the scene with matplotlib
#
camera = gsp.core.Camera(camera_type="perspective")
network_renderer = gsp_network.NetworkRenderer(server_url="http://localhost:5000/", jsondiff_allowed=False)
gsp_animator = GspAnimatorNetwork(network_renderer)

# =============================================================================
# Animate the scene with matplotlib thru the network renderer
# =============================================================================
fps_monitor = FpsMonitor()


@gsp_animator.event_listener
def animate(delta_time: float) -> list[gsp.core.VisualBase]:
    # copy inplace to avoid reallocationsd
    sizes[:] = np.random.uniform(10, 100, (n_points,)).astype(np.float32)

    # measure FPS to monitor performance
    fps_monitor.print_fps()

    changed_visuals: list[gsp.core.VisualBase] = [pixels]
    return changed_visuals


gsp_animator.start(canvas, [viewport], [camera])
