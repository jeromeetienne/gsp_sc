# local imports
from .datoviz_app import DatovizApp


class datoviz:

    @staticmethod
    def App() -> DatovizApp:
        app = DatovizApp()
        return app
