"""
Basic example of creating and rendering a simple GSP scene with matplotlib.
"""

import numpy as np
from gsp.core.canvas import Canvas
from gsp.core.viewport import Viewport
from gsp.core.camera import Camera
from gsp_matplotlib import MatplotlibRenderer
from gsp.renderer.json import JsonRenderer
from gsp_network import NetworkRenderer
from gsp.visuals.pixels import Pixels

# Create a GSP scene
canvas = Canvas(512, 512, 100)
viewport = Viewport(0, 0, canvas.width, canvas.height, (1, 1, 1, 1))
canvas.add(viewport)

# Add some random points
n_points = 100
positions = np.random.uniform(-0.5, 0.5, (n_points, 3))
sizes = np.random.uniform(5, 20, n_points)
pixels = Pixels(positions, sizes, colors=np.array([[1, 0, 0, 1]]))
viewport.add(pixels)

# Render the scene with matplotlib
camera = Camera("perspective")
renderer = MatplotlibRenderer()
png_image = renderer.render(canvas, camera)

# Export the scene to JSON
json_renderer = JsonRenderer()
scene_json = json_renderer.render(canvas, camera)

# Render the scene remotely (if you have a GSP server running)
network_renderer = NetworkRenderer("http://localhost:5000")
png_image2 = network_renderer.render(canvas, camera)
