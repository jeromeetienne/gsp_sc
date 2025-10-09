# stdlib imports
import os

# pip imports
import numpy as np
import matplotlib.pyplot
import matplotlib.image
import mpl3d.glm

# local imports
import gsp_sc
from .mesh_parser import MeshParserMeshio

__dirname__ = os.path.dirname(os.path.abspath(__file__))


class SceneExamples:
    @staticmethod
    def add_all_visuals(viewport: gsp_sc.core.Viewport):
        # =============================================================================
        # Add some random points as a Pixels visual
        # =============================================================================
        n_points = 1000
        positions_np = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float32)
        sizes_np = np.random.uniform(5, 10, n_points).astype(np.float32)
        colors_np = np.array([gsp_sc.Constants.Green])
        pixels = gsp_sc.visuals.Pixels(positions=positions_np, sizes=sizes_np, colors=colors_np)
        viewport.add(pixels)

        # =============================================================================
        # Add an image
        # =============================================================================
        image_path = f"{__dirname__}/../images/UV_Grid_Sm.jpg"
        image_data_np = matplotlib.image.imread(image_path)
        image = gsp_sc.visuals.Image(
            position=np.array([0.5, 0.5, 0.5]),
            image_extent=(-0.1, +0.1, -0.1, +0.1),
            image_data=image_data_np,
        )
        viewport.add(image)

        # =============================================================================
        # Add a mesh from an OBJ file
        # =============================================================================
        obj_mesh_path = f"{__dirname__}/../data/bunny.obj"
        vertices_coords, faces_indices, uvs_coords, normals_coords = MeshParserMeshio.parse_obj_file(obj_mesh_path)
        vertices_coords = mpl3d.glm.fit_unit_cube(vertices_coords)
        mesh = gsp_sc.visuals.Mesh(vertices_coords, faces_indices, cmap=matplotlib.pyplot.get_cmap("magma"), edgecolors=(0, 0, 0, 0.25))  # type: ignore
        viewport.add(mesh)
