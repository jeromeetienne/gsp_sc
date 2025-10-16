import gsp
from gsp.core import canvas
from .datoviz_points import DatovizPoints


class DatovizPanel:
    def __init__(self):
        # self._gsp_viewport = gsp.core.Viewport(width=512, height=512, dpi=100)
        self._gsp_viewport = gsp.core.Viewport(origin_x=0, origin_y=0, width=512, height=512, background_color=gsp.Constants.Black)

    def add(self, visual: DatovizPoints) -> None:
        if isinstance(visual, DatovizPoints):
            self._gsp_viewport.add(visual._gsp_pixels)
        else:
            raise TypeError("Expected a Visual instance.")

    # =============================================================================
    # Creators
    # =============================================================================
    def panzoom(self) -> None:
        pass
