# pip imports
import numpy as np

# Local imports
import gsp
import gsp_matplotlib
from ..gsp_animator import GspAnimatorMatplotlib
from ..fps_monitor import FpsMonitor
from .datoviz_texture import DatovizTexture
from .datoviz_figure import DatovizFigure
from .datoviz_points import DatovizPoints
from .datoviz_images import DatovizImages
from .datoviz_shape_collection import DatovizShapeCollection
from .datoviz_mesh import DatovizMesh


class DatovizApp:
    def __init__(self):
        self._dvz_figure: DatovizFigure = DatovizFigure()

        self._gsp_camera = gsp.core.Camera(camera_type="perspective")
        self._gsp_renderer = gsp_matplotlib.MatplotlibRenderer()
        self._gsp_animator_matplotlib = GspAnimatorMatplotlib(self._gsp_renderer)

    def add_figure(self, figure: DatovizFigure):
        self._dvz_figure = figure

    def run(self):
        fps_monitor = FpsMonitor()

        def animator_callback() -> list[gsp.core.VisualBase]:

            # measure FPS to monitor performance
            fps_monitor.print_fps()

            # go through all visuals in the canvas and mark them as changed
            canvas = self._dvz_figure._gsp_canvas

            changed_visuals: list[gsp.core.VisualBase] = []
            for viewport in canvas.viewports:
                for visual in viewport.visuals:
                    changed_visuals.append(visual)

            return changed_visuals

        self._gsp_animator_matplotlib.animate(self._dvz_figure._gsp_canvas, self._dvz_figure._gsp_canvas.viewports, [self._gsp_camera], [animator_callback])

    def destroy(self):
        pass

    # =============================================================================
    # Creators
    # =============================================================================
    def figure(self):
        self._dvz_figure = DatovizFigure()
        return self._dvz_figure

    def point(self, position: np.ndarray, color: np.ndarray, size: np.ndarray):
        dvz_point = DatovizPoints(positions=position, sizes=size, colors=color)
        return dvz_point

    def image(self, positions: np.ndarray, sizes: np.ndarray, **kwargs) -> DatovizImages:
        dvz_image = DatovizImages(positions=positions, sizes=sizes)
        return dvz_image

    def texture_2D(self, image: np.ndarray, **kwargs):
        dvz_texture = DatovizTexture(image=image)
        return dvz_texture

    def mesh(self, shapeCollection: DatovizShapeCollection, **kwargs) -> DatovizMesh:
        dvz_mesh = DatovizMesh(shapeCollection=shapeCollection)
        return dvz_mesh
