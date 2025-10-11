import typing
import matplotlib.pyplot
import matplotlib.patches
import matplotlib.artist
from core.object_3d import Object3D
from objects.points import Points
from objects.textured_mesh import TexturedMesh
from cameras.camera_orthographic import CameraOrthographic
from cameras.camera_base import CameraBase


class RendererMatplotlib:
    def __init__(self):
        # init a matplotlib figure and axis
        self._figure = matplotlib.pyplot.figure(figsize=(2, 2), dpi=100)
        self._axis = self._figure.add_axes((0, 0, 1, 1), frameon=False)
        self._axis.set_xlim(-1, 1)
        self._axis.set_ylim(-1, 1)
        self._artists: dict[str, matplotlib.artist.Artist] = {}

    def render(self, scene: Object3D, camera: CameraBase) -> list[matplotlib.artist.Artist]:
        # update world matrices
        scene.update_world_matrix()

        # render from back to front
        # (not implemented here, just a placeholder comment)

        # render objects
        changed_artists: list[matplotlib.artist.Artist] = []
        for object3d in scene.traverse():
            _changed_artists = self._render_object(object3d, camera)
            changed_artists.extend(_changed_artists)

        matplotlib.pyplot.draw()

        return changed_artists

    def _render_object(self, object3d: Object3D, camera: CameraBase) -> list[matplotlib.artist.Artist]:
        if isinstance(object3d, Points):
            from renderers.matplotlib.renderer_points import MatplotlibRendererPoints

            return MatplotlibRendererPoints.render(self, object3d, camera)
        elif isinstance(object3d, TexturedMesh):
            from renderers.matplotlib.renderer_textured_mesh import MatplotlibRendererTexturedMesh

            return MatplotlibRendererTexturedMesh.render(self, object3d, camera)
        elif isinstance(object3d, Object3D):
            # base class, do nothing
            return []
        else:
            raise NotImplementedError(f"Rendering for {type(object3d)} not implemented yet")
        return []
