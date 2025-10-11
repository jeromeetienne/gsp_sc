# stdlib imports
import os

# pip imports
import numpy as np


# local imports
from core.object_3d import Object3D

from cameras.camera_orthographic import CameraOrthographic
from renderers.matplotlib.renderer import RendererMatplotlib
from helpers.animation_loop import AnimationLoop
from helpers.scene_examples import SceneExamples

__dirname__ = os.path.dirname(os.path.abspath(__file__))


def main():
    # =============================================================================
    # Setup the scene
    # =============================================================================
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

    # Create a renderer
    renderer = RendererMatplotlib()
    # Create an animation loop
    animation_loop = AnimationLoop(renderer)

    # =============================================================================
    # Load a model
    # =============================================================================

    model_root = Object3D()
    model_root.name = "ModelRoot"
    model_root.scale[:] = 1
    scene.add_child(model_root)

    model_root.add_child(SceneExamples.getCubePoints())

    bunny_root = Object3D()
    bunny_root.name = "BunnyRoot"
    bunny_root.position[1] = -2.5
    bunny_root.scale[:] = 0.2
    model_root.add_child(bunny_root)

    bunny_points = SceneExamples.getBunnyPoints()
    bunny_root.add_child(bunny_points)

    def update_model_root(delta_time: int, timestamp: int) -> None:
        range = np.sin(timestamp) * 1 + 2
        bunny_points.position[1] = np.abs(np.cos(timestamp * 5) * range)

    animation_loop.add(update_model_root)

    # =============================================================================
    # Start the animation loop
    # =============================================================================
    animation_loop.start(scene, camera)


if __name__ == "__main__":
    main()
