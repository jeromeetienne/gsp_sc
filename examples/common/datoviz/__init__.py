# pip imports
import matplotlib.pyplot
import numpy as np

# local imports
from .datoviz import datoviz
from .datoviz_app import DatovizApp
from .datoviz_points import DatovizPoints


# =============================================================================
#
# =============================================================================
def App() -> DatovizApp:
    app = datoviz.App()
    return app


# doc https://github.com/datoviz/datoviz/blob/main/datoviz/utils.py#L26> np.ndarray5
def cmap(name: str, values: np.ndarray) -> np.ndarray:
    cmap = matplotlib.pyplot.get_cmap(name)
    colors = np.array([cmap(value) for value in values])
    return colors
