# stdlib imports
import os

# pip imports
import numpy as np


# local imports
from core.object_3d import Object3D
from cameras.camera_orthographic import CameraOrthographic
from renderers.matplotlib.renderer import RendererMatplotlib
from helpers.animation_loop import AnimationLoop
from objects.lines import Lines


def main():
    # =============================================================================
    # Setup the scene
    # =============================================================================
    scene = Object3D()

    camera = CameraOrthographic()
    scene.add_child(camera)
    camera.position[2] = 5.0

    # Create a renderer
    renderer = RendererMatplotlib(512, 512)
    # Create an animation loop
    animation_loop = AnimationLoop(renderer)

    # =============================================================================
    # Load a model
    # =============================================================================

    num_lines = 10
    vertices = np.random.uniform(-1, 1, size=(num_lines * 2, 3)).astype(np.float32)

    lines = Lines(vertices)
    scene.add_child(lines)

    def update(delta_time: float, time_stamp: float) -> None:
        lines.vertices = np.random.uniform(-1, 1, size=(num_lines * 2, 3)).astype(np.float32)
        # lines.rotation_euler[1] += delta_time * 0.5
        # lines.rotation_euler[0] += delta_time * 0.25

    animation_loop.add_callback(update)

    # =============================================================================
    # Start the animation loop
    # =============================================================================
    animation_loop.start(scene, camera)


if __name__ == "__main__":
    main()
