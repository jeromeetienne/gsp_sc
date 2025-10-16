# pip imports
import matplotlib.pyplot
import numpy as np

# local imports
from .datoviz_app import DatovizApp
from ..asset_downloader import download_data
from .datoviz_mesh import DatovizMesh


class datoviz:

    @staticmethod
    def App() -> DatovizApp:
        app = DatovizApp()
        return app

    # doc https://github.com/datoviz/datoviz/blob/main/datoviz/utils.py#L26> np.ndarray5
    @staticmethod
    def cmap(name: str, values: np.ndarray) -> np.ndarray:
        cmap = matplotlib.pyplot.get_cmap(name)
        colors = np.array([cmap(value) for value in values])
        return colors

    @staticmethod
    def download_data(rel_path: str, force_download: bool = False):
        """Download data from the gsp_sc repository."""
        return download_data(rel_path, force_download)

    @staticmethod
    def mesh(shape_collection, **kwargs):
        dvz_mesh = DatovizMesh()
        return dvz_mesh
