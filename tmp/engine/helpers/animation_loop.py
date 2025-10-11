import typing
import matplotlib.animation
import matplotlib.artist
import matplotlib.pyplot
from core.object_3d import Object3D
from cameras.camera_base import CameraBase
from renderers.matplotlib.renderer import RendererMatplotlib

# do a callback type for the animation loop
AnimationLoopCallbackType = typing.Callable[[], None]


class AnimationLoop:
    def __init__(self, renderer: RendererMatplotlib):
        self._callbacks = []
        self._renderer = renderer

    def start(self, scene: Object3D, camera: CameraBase):
        # define a animation function for matplotlib
        def update_scene(frame) -> list[matplotlib.artist.Artist]:
            for callback in self._callbacks:
                callback()

            changed_artists = self._renderer.render(scene, camera)
            print(f"  Number of changed artists: {len(changed_artists)}")
            return changed_artists

        ani = matplotlib.animation.FuncAnimation(self._renderer._figure, update_scene, frames=100, interval=1000 / 60, blit=True)

        matplotlib.pyplot.show()

    def stop(self):
        raise NotImplementedError()

    def add(self, func: AnimationLoopCallbackType):
        self._callbacks.append(func)

    def remove(self, func: AnimationLoopCallbackType):
        self._callbacks.remove(func)
