import typing
import matplotlib.pyplot
import matplotlib.patches
import matplotlib.artist
from core.object_3d import Object3D
from objects.points import Points
from objects.textured_mesh import TexturedMesh
from cameras.orthographic_camera import OrthographicCamera


class RendererMatplotlib:
    def __init__(self):
        # init a matplotlib figure and axis
        self._figure = matplotlib.pyplot.figure()
        self._axis = self._figure.add_axes((0, 0, 1, 1), frameon=False)
        self._axis.set_xlim(-1, 1)
        self._axis.set_ylim(-1, 1)
        self._artists: dict[str, matplotlib.artist.Artist] = {}

    def render(self, scene: Object3D, camera: OrthographicCamera) -> list[matplotlib.artist.Artist]:
        # Placeholder for rendering logic using matplotlib
        # print("Rendering scene with matplotlib renderer")

        # FIXME should not happen with render loop
        # self._axis.cla()  # Clear the axis for fresh rendering

        # update world matrices
        scene.update_matrix_world(force=True)

        # render from back to front
        # (not implemented here, just a placeholder comment)

        # render objects
        object3ds: list[Object3D] = []
        scene.traverse(lambda obj: object3ds.append(obj))

        changed_artists: list[matplotlib.artist.Artist] = []
        for object3d in object3ds:
            _changed_artists = self._render_object(object3d, camera)
            changed_artists.extend(_changed_artists)

        matplotlib.pyplot.draw()

        return changed_artists

    def _render_object(self, object3d: Object3D, camera: OrthographicCamera) -> list[matplotlib.artist.Artist]:
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
