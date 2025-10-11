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
from objects.points import Points
from cameras.camera_orthographic import CameraOrthographic
from renderers.matplotlib.renderer import RendererMatplotlib
from cameras.camera_perspective import CameraPerspective

__dirname__ = os.path.dirname(os.path.abspath(__file__))


def main():
    scene = Object3D()
    scene.name = "Scene"

    # camera = OrthographicCamera()
    camera = CameraPerspective()
    camera.name = "Camera"
    scene.add_child(camera)
    camera.position[2] = 5.0

    child = Object3D()
    child.name = "Child"
    scene.add_child(child)

    grand_child = Object3D()
    grand_child.name = "GrandChild"
    child.add_child(grand_child)

    vertices = np.array([[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]], dtype=np.float32)
    points = Points(vertices)
    grand_child.add_child(points)

    scene.update_world_matrix()

    renderer = RendererMatplotlib()

    while True:
        # grand_child.rotation_euler[:] += 0.1
        # points.rotation_euler[2] = time.time() * 0.2
        # points.position[0] = 0.5 * np.sin(time.time())
        # points.position[1] = 0.5 * np.cos(time.time())
        # grand_child.scale[:] = 1 + 0.5 * np.sin(2 * time.time())
        # points.position[1] = 0.5 * np.sin(time.time())

        renderer.render(scene, camera)
        matplotlib.pyplot.pause(0.1)

    # print("Scene graph:")

    # while True:
    #     for object in scene.traverse():
    #         print(f" - {object.name}: pos={object.get_world_position()} scl={object.get_world_scale()} rot={object.get_world_rotation_euler()}")

    #     child.position[0] += 0.1
    #     # grand_child.position[2] += 0.1
    #     # child.rotation_euler[1] += 0.1
    #     child.scale[:] += 0.1

    #     scene.update_world_matrix()

    #     # clear the figure
    #     matplotlib.pyplot.clf()

    #     # display the scene graph
    #     ax = matplotlib.pyplot.gca()
    #     ax.set_title("Scene Graph")
    #     ax.set_xlabel("X")
    #     ax.set_ylabel("Y")
    #     ax.set_xlim(-5, 5)
    #     ax.set_ylim(-5, 5)
    #     ax.grid(True, linestyle="--", alpha=0.4)
    #     ax.set_aspect("equal")

    #     for obj in scene.traverse():
    #         pos = obj.get_world_position()
    #         ax.scatter(pos[0], pos[1], s=100, label=obj.name)
    #         ax.text(pos[0], pos[1], obj.name, fontsize=8, ha="center", va="bottom")

    #     matplotlib.pyplot.pause(1.0)


if __name__ == "__main__":
    main()
