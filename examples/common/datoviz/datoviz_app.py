# pip imports
import numpy as np

# Local imports
import gsp
import gsp_matplotlib
from ..gsp_animator import GspAnimatorMatplotlib

from .datoviz_figure import DatovizFigure
from .datoviz_panel import DatovizPanel
from .datoviz_points import DatovizPoints


class DatovizApp:
    def __init__(self):
        self._dvz_figure: DatovizFigure = DatovizFigure()

        self._gsp_camera = gsp.core.Camera(camera_type="perspective")
        self._gsp_renderer = gsp_matplotlib.MatplotlibRenderer()
        self._gsp_animator_matplotlib = GspAnimatorMatplotlib(self._gsp_renderer)

    def add_figure(self, figure: DatovizFigure):
        self._dvz_figure = figure

    def run(self):
        def animator_callback() -> list[gsp.core.VisualBase]:
            # print("Animating...")
            changed_visuals: list[gsp.core.VisualBase] = []
            return changed_visuals

        self._gsp_animator_matplotlib.animate(self._dvz_figure._gsp_canvas, self._gsp_camera, [animator_callback])

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
