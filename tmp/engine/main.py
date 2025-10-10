# stdlib imports
import time
import sys
import os

# pip imports
import numpy as np
from pyrr import Matrix44, Vector3
import pyrr
import matplotlib.pyplot
import matplotlib.animation
import matplotlib.patches
import matplotlib.artist


# local imports
from objects.points import Points
from objects.textured_mesh import TexturedMesh
from core.object_3d import Object3D
from cameras.orthographic_camera import OrthographicCamera
from renderers.matplotlib.renderer import RendererMatplotlib

__dirname__ = os.path.dirname(os.path.abspath(__file__))


def main():
    renderer = RendererMatplotlib()
    scene = Object3D()

    camera = OrthographicCamera()
    camera.position = pyrr.Vector3([0, 0, 10])
    scene.add_child(camera)

    vertices = [Vector3([0.0, 0.0, 0.0]), Vector3([0.5, 0.5, 0.0]), Vector3([-0.5, 0.5, 0.0]), Vector3([-0.5, -0.5, 0.0]), Vector3([0.5, -0.5, 0.0])]
    points = Points(vertices)
    scene.add_child(points)

    # model_path = os.path.join(__dirname__, "../textured_head/head.obj")
    # model_path = os.path.join(__dirname__, "cube.obj")
    # texture_path = os.path.join(__dirname__, "../textured_head/uv-grid.png")
    # texture_mesh = TexturedMesh.from_obj(model_path=model_path, texture_path=texture_path)
    # texture_mesh.position.z += 1
    # circle.add_child(texture_mesh)

    child = Object3D()
    scene.add_child(child)
    child.position = pyrr.Vector3([1, 0, 0.2])

    grand_child = Object3D()
    child.add_child(grand_child)
    grand_child.position.x += 2

    def mpl_update(frame) -> list[matplotlib.artist.Artist]:
        points.position.x = 0.3 * np.cos(frame * 0.1)
        changed_artists = renderer.render(scene, camera)
        return changed_artists

    animation = matplotlib.animation.FuncAnimation(renderer._figure, mpl_update, frames=120, interval=1000 / 60)

    matplotlib.pyplot.show(block=True)


if __name__ == "__main__":
    main()
