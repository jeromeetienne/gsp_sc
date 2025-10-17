"""
Basic example of creating and rendering a simple GSP scene with matplotlib.
"""

# pip imports
import matplotlib.pyplot
import numpy as np
import os
from typing import Sequence
import mpl3d.glm
import sys

# local imports
from common.gsp_animator import GspAnimatorMatplotlib
import gsp
import gsp_matplotlib
from common.mesh_parser import MeshParserMeshio

__dirname__ = os.path.dirname(os.path.abspath(__file__))
# Set random seed for reproducibility
gsp.core.Random.set_random_seed(10)
np.random.seed(10)

# =============================================================================
# Figure 1
# =============================================================================


def create_scene_1() -> gsp_matplotlib.MatplotlibRenderer:
    # =============================================================================
    # Create a canvas and a viewport
    # =============================================================================

    canvas = gsp.core.Canvas(width=512, height=512, dpi=100)
    viewport = gsp.core.Viewport(0, 0, canvas.width, canvas.height, gsp.core.Constants.White)
    canvas.add(viewport=viewport)

    # =============================================================================
    # Add some random points
    # =============================================================================

    n_points = 300
    positions_np = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float64)
    sizes_np = np.random.uniform(5, 10, n_points).astype(np.float32)
    colors_np = np.array([gsp.core.Constants.Green])
    pixels = gsp.visuals.Pixels(positions=positions_np, sizes=sizes_np, colors=colors_np)
    viewport.add(pixels)

    # =============================================================================
    # Render the canvas with a perspective camera
    # =============================================================================
    camera = gsp.core.Camera(camera_type="perspective")
    renderer = gsp_matplotlib.MatplotlibRenderer()
    image_png_buffer = renderer.render(canvas, [viewport], [camera])

    # init the animator with the renderer
    animator = GspAnimatorMatplotlib(renderer)

    @animator.event_listener
    def update(delta_time: float) -> Sequence[gsp.core.VisualBase]:
        print("update 1")
        new_sizes = np.random.uniform(10, 100, (n_points,)).astype(np.float32)
        # copy inplace to avoid reallocations
        sizes_np[:] = new_sizes
        return [pixels]

    animator.start(canvas, [viewport], [camera], block=False)

    return renderer


# =============================================================================
# Figure 2
# =============================================================================


def create_scene_2() -> gsp_matplotlib.MatplotlibRenderer:
    # =============================================================================
    # Create a canvas and a viewport
    # =============================================================================

    canvas = gsp.core.Canvas(width=512, height=512, dpi=100)
    viewport = gsp.core.Viewport(0, 0, canvas.width, canvas.height, gsp.core.Constants.White)
    canvas.add(viewport=viewport)

    # =============================================================================
    # Add content to the viewport
    # =============================================================================

    obj_mesh_path = f"{__dirname__}/data/bunny.obj"
    vertices_coords, faces_indices, uvs_coords, normals_coords = MeshParserMeshio.parse_obj_file(obj_mesh_path)
    vertices_coords = mpl3d.glm.fit_unit_cube(vertices_coords)
    mesh = gsp.visuals.Mesh(vertices_coords, faces_indices, cmap=matplotlib.pyplot.get_cmap("magma"), edgecolors=(0, 0, 0, 0.25))  # type: ignore
    viewport.add(mesh)

    # =============================================================================
    # Render the canvas with a perspective camera
    # =============================================================================
    camera = gsp.core.Camera(camera_type="perspective")
    renderer = gsp_matplotlib.MatplotlibRenderer()
    image_png_buffer = renderer.render(canvas, [viewport], [camera])

    # init the animator with the renderer
    animator = GspAnimatorMatplotlib(renderer)

    @animator.event_listener
    def update(delta_time: float) -> Sequence[gsp.core.VisualBase]:
        print("update 2")
        # mesh.vertices_coords[:, 1] += 0.01
        return [mesh]

    animator.start(canvas, [viewport], [camera], block=False)

    return renderer


# =============================================================================
# Main entry point
# =============================================================================

if __name__ == "__main__":
    renderer1 = create_scene_1()
    renderer2 = create_scene_2()

    # detect if we are in not interactive mode - used during testing
    gsp_sc_interactive = "GSP_SC_INTERACTIVE" not in os.environ or os.environ["GSP_SC_INTERACTIVE"] != "False"
    if gsp_sc_interactive == False:
        basename = os.path.splitext(os.path.basename(__file__))[0]
        figure1 = list(renderer1._figures.values())[0]
        figure1.savefig(f"{__dirname__}/output/{basename}_1.png")
        figure2 = list(renderer2._figures.values())[0]
        figure2.savefig(f"{__dirname__}/output/{basename}_2.png")
        sys.exit(0)

    # show all figures
    matplotlib.pyplot.show()
