from .viewport import Viewport
from .random import Random


class Canvas:
    __slots__ = ("uuid", "width", "height", "dpi", "viewports")

    def __init__(self, width: int, height: int, dpi: float = 100.0) -> None:
        """
        Initialize a Canvas object.

        Arguments:
            width (int): The width of the canvas in pixels.
            height (int): The height of the canvas in pixels.
            dpi (float, optional): The DPI (dots per inch) of the canvas. Defaults to 100.0.
        """

        self.uuid = Random.random_uuid()
        """unique identifier of the canvas"""

        self.width = width
        """The width of the canvas in pixels"""

        self.height = height
        """The height of the canvas in pixels"""

        self.dpi = dpi
        """The DPI (dots per inch) of the canvas"""

        self.viewports: list[Viewport] = []
        """List of viewports associated with this canvas"""

    def add(self, viewport: Viewport) -> None:
        """
        Add a viewport to the canvas.

        Args:
            viewport (Viewport): The viewport to add.
        """
        self.viewports.append(viewport)

    def remove(self, viewport: Viewport) -> None:
        """
        Remove a viewport from the canvas.

        Args:
            viewport (Viewport): The viewport to remove.
        """
        self.viewports.remove(viewport)
