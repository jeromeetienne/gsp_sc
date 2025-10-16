import gsp
from .datoviz_panel import DatovizPanel


class DatovizFigure:
    def __init__(self):
        self._gsp_canvas = gsp.core.Canvas(width=512, height=512, dpi=100)

    def add_panel(self, panel: DatovizPanel):
        self._gsp_canvas.add(panel._gsp_viewport)

    # =============================================================================
    # Creators
    # =============================================================================

    def panel(self, **kwargs):
        panel = DatovizPanel()
        self.add_panel(panel)
        return panel
