from __future__ import annotations

from .visual_base import VisualBase
from .random import Random
from .canvas import Canvas
from .object_3d import Object3D


class Viewport:
    __slots__ = (
        "uuid",
        "origin_x",
        "origin_y",
        "width",
        "height",
        "background_color",
        "_canvas",
        "visuals",
        "scene",
    )

    def __init__(self, origin_x: int, origin_y: int, width: int, height: int, background_color: tuple[float, float, float, float] = (1, 1, 1, 1)) -> None:
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

        # self._canvas: Canvas | None = None
        """Set internally when the viewport is added to a canvas."""

        self.scene: Object3D = Object3D()
        """The root scene object of the viewport."""

        self.visuals: list[VisualBase] = []
        """List of visuals associated with this viewport"""

    def add(self, visual: VisualBase) -> None:
        """
        Add a visual to the viewport.

        Args:
            visual (VisualBase): The visual to add.
        """
        self.visuals.append(visual)
        self.scene.add(visual)

    def remove(self, visual: VisualBase) -> None:
        """
        Remove a visual from the viewport.

        Args:
            visual (VisualBase): The visual to remove.
        """
        self.visuals.remove(visual)
        self.scene.remove(visual)

    # def set_canvas(self, canvas: Canvas | None) -> None:
    #     """
    #     Set the canvas for the viewport.

    #     Args:
    #         canvas (Canvas | None): The canvas to set. Use None to unset.
    #     """
    #     self._canvas = canvas

    # def has_canvas(self) -> bool:
    #     """
    #     Check if the viewport is associated with a canvas.

    #     Returns:
    #         bool: True if the viewport has a canvas, False otherwise.
    #     """
    #     return self._canvas is not None

    # def get_canvas(self) -> Canvas:
    #     """
    #     Get the canvas associated with the viewport.

    #     Returns:
    #         Canvas | None: The canvas associated with the viewport, or None if not set.
    #     """
    #     # sanity check
    #     assert self._canvas is not None, "Viewport is not associated with any canvas. Check with .has_canvas() before calling get_canvas()."

    #     return self._canvas
