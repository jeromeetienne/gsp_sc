"""
Basic example of creating and rendering a simple GSP scene with matplotlib.
"""

# pip imports
import numpy as np
import os
import gsp
import gsp_matplotlib
import mpl3d.glm
import matplotlib.pyplot

# local imports
from common.gsp_animator import GspAnimatorMatplotlib
from common.fps_monitor import FpsMonitor
from common.mesh_parser import MeshParserMeshio

__dirname__ = os.path.dirname(os.path.abspath(__file__))
# Set random seed for reproducibility
gsp.core.Random.set_random_seed(10)
np.random.seed(10)

###############################################################################
# Create a GSP scene
#
canvas = gsp.core.Canvas(512, 512, 100)
viewport = gsp.core.Viewport(0, 0, canvas.width, canvas.height, gsp.Constants.White)
canvas.add(viewport)

###############################################################################
# Add some random points
#
n_points = 20
positions_np = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float32)
sizes_np = np.array([50 for _ in range(n_points)], np.float32)
colors_np = np.array([gsp.Constants.Green for _ in range(n_points)], np.float32)
pixels = gsp.visuals.Pixels(positions_np, sizes_np, colors_np)
viewport.add(pixels)

# =============================================================================
# Add a mesh
# =============================================================================

obj_mesh_path = f"{__dirname__}/data/bunny.obj"
vertices_coords, faces_indices, uvs_coords, normals_coords = MeshParserMeshio.parse_obj_file(obj_mesh_path)
vertices_coords = mpl3d.glm.fit_unit_cube(vertices_coords)
mesh = gsp.visuals.Mesh(vertices_coords, faces_indices, cmap=matplotlib.pyplot.get_cmap("magma"), edgecolors=(0, 0, 0, 0.25))  # type: ignore
viewport.add(mesh)

###############################################################################
# Render the scene with matplotlib
#
camera = gsp.core.Camera(camera_type="perspective")
renderer = gsp_matplotlib.MatplotlibRenderer()
renderer.render(canvas, camera)

# =============================================================================
# Animate the scene with matplotlib
# =============================================================================
fps_monitor = FpsMonitor()


def animator_callback() -> list[gsp.core.VisualBase]:
    new_sizes = np.random.uniform(10, 100, (n_points,)).astype(np.float32)
    # copy inplace to avoid reallocations
    sizes_np[:] = new_sizes

    # measure FPS to monitor performance
    fps_monitor.print_fps()

    changed_visuals: list[gsp.core.VisualBase] = [pixels]
    return changed_visuals


animator_matplotlib = GspAnimatorMatplotlib(renderer)
animator_matplotlib.animate(canvas, camera, [animator_callback])
