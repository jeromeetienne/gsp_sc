# !/usr/bin/env python3

"""
Basic example of creating and rendering a simple GSP scene with matplotlib.
"""

# stdlib imports
import os
import time

# pip imports
import numpy as np

# local imports
import gsp_sc
from examples.common.gsp_animator import GspAnimatorNetwork
from gsp_sc.types import DiffableNdarray


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

positions = DiffableNdarray(positions)
sizes = DiffableNdarray(sizes)
colors = DiffableNdarray(colors)

pixels = gsp_sc.visuals.Pixels(positions, sizes, colors)
viewport.add(pixels)


###############################################################################
# Render the scene with matplotlib
#
camera = gsp_sc.core.Camera(camera_type="perspective")
network_renderer = gsp_sc.renderer.network.NetworkRenderer(server_url="http://localhost:5000/", jsondiff_allowed=True)

# =============================================================================
# Code to measure FPS
# =============================================================================
time_previous_render = None


def monitor_fps() -> None:
    global time_previous_render
    time_now = time.perf_counter()
    if time_previous_render is not None:
        fps = 1.0 / (time_now - time_previous_render)
        print(f"Frame per second: {fps:.2f}")
    time_previous_render = time_now


# =============================================================================
# Animate the scene with matplotlib thru the network renderer
# =============================================================================
def animate() -> list[gsp_sc.core.VisualBase]:
    # copy inplace to avoid reallocations
    sizes[:] = np.random.uniform(10, 100, (n_points,)).astype(np.float32)

    # measure FPS to monitor performance
    monitor_fps()

    changed_visuals: list[gsp_sc.core.VisualBase] = [pixels]
    return changed_visuals


gsp_animator = GspAnimatorNetwork(network_renderer)
gsp_animator.animate(canvas, camera, [animate])
