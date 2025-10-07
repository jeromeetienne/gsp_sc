"""
Example of serialising a scene to JSON and MessagePack files.
"""

import gsp_sc.src as gsp_sc
import numpy as np
import os
import msgpack
import json
from gsp_sc.src.types import DiffableNdarray


__dirname__ = os.path.dirname(os.path.abspath(__file__))
# Set random seed for reproducibility
# gsp_sc.core.Random.set_random_seed(10)
# np.random.seed(10)

canvas = gsp_sc.core.Canvas(width=512, height=512, dpi=100)

###############################################################################
# Create a viewport
#
viewport = gsp_sc.core.Viewport(0, 0, 256, 256, (1, 1, 1, 1))
canvas.add(viewport=viewport)

###############################################################################
# Add some random points to viewport
#
n_points = 3
positions_np = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float32)
sizes_np = np.ones((n_points,)).astype(np.float32)
sizes_np = DiffableNdarray(sizes_np)
colors_np = np.array([gsp_sc.Constants.Green])
pixels = gsp_sc.visuals.Pixels(positions=positions_np, sizes=sizes_np, colors=colors_np)
viewport.add(pixels)


sizes_np[0] = 5.0

###############################################################################
# Render the scene to JSON and save to file
#
camera = gsp_sc.core.Camera("perspective")
json_renderer = gsp_sc.renderer.json.JsonRenderer()
scene_dict1 = json_renderer.render(canvas, camera)


# Save to file as json before modifying it
file_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}_1.gsp.json"
with open(file_path, "w") as file_writer:
    json.dump(scene_dict1, file_writer, indent=4)
print(f"Scene exported to JSON and saved to {file_path}.")

sizes_np[1] = 10.0

# render again
scene_dict2 = json_renderer.render(canvas, camera)

# Save to file as json after modifying it
file_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}_2.gsp.json"
with open(file_path, "w") as file_writer:
    json.dump(scene_dict2, file_writer, indent=4)
print(f"Scene exported to JSON and saved to {file_path}.")
