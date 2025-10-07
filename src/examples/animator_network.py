# !/usr/bin/env python3

"""
Basic example of creating and rendering a simple GSP scene with matplotlib.
"""

import numpy as np
import os
import time
import gsp_sc
from examples.common.gsp_animator import GspAnimatorNetwork


__dirname__ = os.path.dirname(os.path.abspath(__file__))
# Set random seed for reproducibility
gsp_sc.core.Random.set_random_seed(10)
np.random.seed(10)

###############################################################################
# Create a GSP scene
#
canvas = gsp_sc.core.Canvas(width=256, height=256, dpi=100)
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
n_points = 3_000
positions_np = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float32)
sizes_np = np.array([50 for _ in range(n_points)], np.float32)
colors_np = np.array([gsp_sc.Constants.Green for _ in range(n_points)], np.float32)
pixels = gsp_sc.visuals.Pixels(positions_np, sizes_np, colors_np)
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
    sizes_np[:] = np.random.uniform(10, 100, (n_points,)).astype(np.float32)

    # measure FPS to monitor performance
    monitor_fps()

    changed_visuals: list[gsp_sc.core.VisualBase] = [pixels]
    return changed_visuals


def main() -> None:
    gsp_animator = GspAnimatorNetwork(network_renderer)
    gsp_animator.animate(canvas, camera, [animate])


if __name__ == "__main__":
    main()
