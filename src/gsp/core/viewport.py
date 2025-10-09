from .visual_base import VisualBase
from .random import Random


class Viewport:
    __slots__ = (
        "uuid",
        "origin_x",
        "origin_y",
        "width",
        "height",
        "background_color",
        "visuals",
    )

    def __init__(
        self,
        origin_x: int,
        origin_y: int,
        width: int,
        height: int,
        background_color: tuple[float, float, float, float] = (1, 1, 1, 1),
    ) -> None:
        """
        Initialize a viewport.

        Args:
            origin_x (int): The x position of the viewport in the Canvas.
            origin_y (int): The y position of the viewport in the Canvas.
            width (int): The width of the viewport in the Canvas.
            height (int): The height of the viewport in the Canvas.
            background_color (tuple[float, float, float, float]): The background color of the viewport.
        """
        self.uuid = Random.random_uuid()
        """The unique identifier of the viewport"""
        self.origin_x = origin_x
        """The x position of the viewport in the Canvas"""
        self.origin_y = origin_y
        """The y position of the viewport in the Canvas"""
        self.width = width
        """The width of the viewport in the Canvas"""
        self.height = height
        """The height of the viewport in the Canvas"""
        self.background_color = background_color
        """The background color of the viewport"""

        self.visuals: list[VisualBase] = []
        """List of visuals associated with this viewport"""

    def add(self, visual: VisualBase) -> None:
        """
        Add a visual to the viewport.

        Args:
            visual (VisualBase): The visual to add.
        """
        self.visuals.append(visual)

    def remove(self, visual: VisualBase) -> None:
        """
        Remove a visual from the viewport.

        Args:
            visual (VisualBase): The visual to remove.
        """
        self.visuals.remove(visual)
