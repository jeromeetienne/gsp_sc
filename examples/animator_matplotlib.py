"""
Basic example of creating and rendering a simple GSP scene with matplotlib.
"""

import numpy as np
import os
import gsp_sc
import gsp_matplotlib

from common.gsp_animator import GspAnimatorMatplotlib
from common.fps_monitor import FpsMonitor

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
n_points = 2000
positions_np = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float32)
sizes_np = np.array([50 for _ in range(n_points)], np.float32)
colors_np = np.array([gsp_sc.Constants.Green for _ in range(n_points)], np.float32)
pixels = gsp_sc.visuals.Pixels(positions_np, sizes_np, colors_np)
viewport.add(pixels)


###############################################################################
# Render the scene with matplotlib
#
camera = gsp_sc.core.Camera(camera_type="perspective")
renderer = gsp_matplotlib.MatplotlibRenderer()
renderer.render(canvas, camera)

# =============================================================================
# Animate the scene with matplotlib
# =============================================================================
fps_monitor = FpsMonitor()


def animator_callback() -> list[gsp_sc.core.VisualBase]:
    new_sizes = np.random.uniform(10, 100, (n_points,)).astype(np.float32)
    # copy inplace to avoid reallocations
    sizes_np[:] = new_sizes

    # measure FPS to monitor performance
    fps_monitor.print_fps()

    changed_visuals: list[gsp_sc.core.VisualBase] = [pixels]
    return changed_visuals


animator_matplotlib = GspAnimatorMatplotlib(renderer)
animator_matplotlib.animate(canvas, camera, [animator_callback])
