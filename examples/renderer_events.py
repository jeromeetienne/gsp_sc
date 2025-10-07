"""
Basic example of creating and rendering a simple GSP scene with matplotlib.
"""

import typing
import matplotlib.image
import numpy as np
import os

import gsp_sc

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
n_points = 1000
positions_np = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float64)
sizes_np = np.ones((n_points,)).astype(np.float32)
colors_np = np.random.uniform(0, 1, (n_points, 4)).astype(np.float32)
colors_np[:, 3] = 1.0
pixels = gsp_sc.visuals.Pixels(positions=positions_np, sizes=sizes_np, colors=colors_np) # type: ignore
viewport.add(pixels)


###############################################################################
# Handle pixels events
# - sort pixels by z value after transform to have correct overlapping
# - change sizes based on z value to have a "perspective" effect
#
def on_post_transform(
    renderer: gsp_sc.renderer.matplotlib.MatplotlibRenderer,
    camera: gsp_sc.core.Camera,
    transformed_positions: np.ndarray,
) -> None:
    # sort inplace transformed positions by z value (3rd column). Largest z first
    indices = np.argsort(-transformed_positions[:, 2])
    transformed_positions[:] = transformed_positions[indices]

    # NOTE: Trick to force the static typing of pixels.positions/sizes/colors to np.ndarray (and never TransformChain)
    pixels.positions = typing.cast(np.ndarray, pixels.positions)
    pixels.sizes = typing.cast(np.ndarray, pixels.sizes)
    pixels.colors = typing.cast(np.ndarray, pixels.colors)

    # apply same sorting to pixels.positions and pixels.colors
    pixels.positions[:] = pixels.positions[indices]
    pixels.colors[:] = pixels.colors[indices]

    # Normalize z values to range 0-1
    z_coordinates = transformed_positions[:, 2] + camera.mpl3d_camera.zoom
    z_min, z_max = camera.mpl3d_camera.zoom_min, camera.mpl3d_camera.zoom_max
    z_coordinates = 1 - (z_coordinates - z_min) / (z_max - z_min)  # normalize to 0-1

    # set sizes between min_size and max_size based on z_coordinate
    min_size, max_size = 10, 125
    pixels.sizes[:] = min_size + z_coordinates * (max_size - min_size)


pixels.post_transform.connect(on_post_transform)


###############################################################################
# Render the scene with matplotlib
#
camera = gsp_sc.core.Camera(camera_type="perspective")
renderer = gsp_sc.renderer.matplotlib.MatplotlibRenderer()
image_png_buffer = renderer.render(canvas, camera, interactive=True)

# Save the rendered image to a file
image_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}.png"
with open(image_path, "wb") as png_file:
    png_file.write(image_png_buffer)
print(f"Rendered image saved to {image_path}")
