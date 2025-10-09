# !/usr/bin/env python3

"""
Basic example of creating and rendering a simple GSP scene with matplotlib.
"""

# stdlib imports
import os

# pip imports
import numpy as np

# local imports
import gsp_sc
import gsp_network
from common.fps_monitor import FpsMonitor
from common.gsp_animator import GspAnimatorNetwork


__dirname__ = os.path.dirname(os.path.abspath(__file__))
# Set random seed for reproducibility
gsp_sc.core.Random.set_random_seed(10)
np.random.seed(10)


###############################################################################
# Create a GSP scene
#
canvas = gsp_sc.core.Canvas(256, 256, 100)
viewport = gsp_sc.core.Viewport(0, 0, canvas.width, canvas.height, gsp_sc.Constants.White)
canvas.add(viewport)


###############################################################################
# Add some random points
#
n_points = 3_000
positions = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float32)
sizes = np.array([50 for _ in range(n_points)], np.float32)
colors = np.array([gsp_sc.Constants.Green for _ in range(n_points)], np.float32)

positions = gsp_sc.types.DiffableNdarray(positions)
sizes = gsp_sc.types.DiffableNdarray(sizes)
colors = gsp_sc.types.DiffableNdarray(colors)

pixels = gsp_sc.visuals.Pixels(positions, sizes, colors)
viewport.add(pixels)


###############################################################################
# Render the scene with matplotlib
#
camera = gsp_sc.core.Camera(camera_type="perspective")
network_renderer = gsp_network.NetworkRenderer(server_url="http://localhost:5000/", jsondiff_allowed=False)

# =============================================================================
# Animate the scene with matplotlib thru the network renderer
# =============================================================================
fps_monitor = FpsMonitor()


def animate() -> list[gsp_sc.core.VisualBase]:
    # copy inplace to avoid reallocations
    sizes[:] = np.random.uniform(10, 100, (n_points,)).astype(np.float32)

    # measure FPS to monitor performance
    fps_monitor.print_fps()

    changed_visuals: list[gsp_sc.core.VisualBase] = [pixels]
    return changed_visuals


gsp_animator = GspAnimatorNetwork(network_renderer)
gsp_animator.animate(canvas, camera, [animate])
