# stdlib imports
import time
import sys
import os

# pip imports
import numpy as np
import matplotlib.pyplot
import matplotlib.animation
import matplotlib.artist
from pyrr import vector3


# local imports
from core.object_3d import Object3D
from core.constants import Constants
from helpers.mesh_parser_meshio import MeshParserMeshio
from helpers.mesh_parser_obj_manual import MeshParserObjManual
from objects.points import Points
from objects.textured_mesh import TexturedMesh
from cameras.camera_orthographic import CameraOrthographic
from renderers.matplotlib.renderer import RendererMatplotlib
from cameras.camera_perspective import CameraPerspective
from helpers.transform_utils import TransformUtils

__dirname__ = os.path.dirname(os.path.abspath(__file__))


def main():
    scene = Object3D()
    scene.name = "Scene"

    camera = CameraOrthographic()
    # camera = CameraPerspective()
    camera.name = "Camera"
    scene.add_child(camera)
    camera.position[2] = 5.0

    child = Object3D()
    child.name = "Child"
    scene.add_child(child)

    grand_child = Object3D()
    grand_child.name = "GrandChild"
    child.add_child(grand_child)
    grand_child.position[2] = 10.0

    # =============================================================================
    # Load a model
    # =============================================================================

    model_root = Object3D()
    model_root.name = "ModelRoot"
    model_root.scale[:] = 1
    scene.add_child(model_root)

    # vertices_coords, _, _, _ = MeshParserMeshio.parse_obj_file(os.path.join(__dirname__, "data", "models", "head_meshio.obj"))
    # vertices_coords = TransformUtils.normalize_vertices_to_unit_cube(vertices_coords)
    # points_head = Points(vertices_coords, color=Constants.PURPLE)
    # model_root.add_child(points_head)

    # vertices_coords, _, _, _ = MeshParserMeshio.parse_obj_file(os.path.join(__dirname__, "data", "models", "bunny.obj"))
    # vertices_coords = TransformUtils.normalize_vertices_to_unit_cube(vertices_coords)
    # points_bunny = Points(vertices_coords, color=Constants.CYAN)
    # model_root.add_child(points_bunny)

    # =============================================================================
    # Textured mesh
    # =============================================================================

    # obj_path = os.path.join(__dirname__, "data", "models", "head_meshio.obj")
    obj_path = os.path.join(__dirname__, "data", "models", "cube_meshio.obj")
    texture_path = os.path.join(__dirname__, "data", "images", "uv-grid.png")

    print(f"Loading .obj file from {obj_path}")
    print(f"Loading texture image from {texture_path}")
    vertices_coords, faces_indices, faces_uvs, faces_normals = MeshParserObjManual.parse_obj_file(obj_path)
    # vertices_coords, faces_indices, faces_uvs, faces_normals = MeshParserMeshio.parse_obj_file(obj_path)
    assert faces_uvs is not None, "The .obj file must contain texture coordinates (vt)"
    # vertices_coords = TransformUtils.normalize_vertices_to_unit_cube(vertices_coords)
    faces_vertices = vertices_coords[faces_indices]
    texture = MeshParserMeshio.load_texture(texture_path)
    textured_mesh = TexturedMesh(faces_vertices, faces_uvs, texture)
    textured_mesh.name = "TexturedMesh"
    model_root.add_child(textured_mesh)

    # =============================================================================
    #
    # =============================================================================
    renderer = RendererMatplotlib()

    # define a animation function for matplotlib
    def update_scene(frame) -> list[matplotlib.artist.Artist]:
        print(f"Frame {frame}")
        textured_mesh.position[0] = np.sin(time.time() / 2)

        # points_head.position[0] = np.sin(time.time() * 2)
        # points_head.position[1] = np.cos(time.time() * 2)

        # points_bunny.position[0] = -np.sin(time.time() * 2)
        # points_bunny.position[1] = -np.cos(time.time() * 2)

        changed_artists = renderer.render(scene, camera)
        print(f"  Number of changed artists: {len(changed_artists)}")
        return changed_artists

    ani = matplotlib.animation.FuncAnimation(renderer._figure, update_scene, frames=100, interval=1000 / 60, blit=True)

    matplotlib.pyplot.show()


if __name__ == "__main__":
    main()
