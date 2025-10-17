# stdlib imports
from enum import Enum

# pip imports
from pyrr import vector4


class Constants:
    """
    A class to hold constant values used throughout the application.
    """

    # Colors
    Black = (0, 0, 0, 1)
    White = (1, 1, 1, 1)
    Red = (1, 0, 0, 1)
    Green = (0, 1, 0, 1)
    Blue = (0, 0, 1, 1)

    class FaceCulling(Enum):
        FrontSide = 0
        BackSide = 1
        BothSides = 2

    class Color:
        WHITE = vector4.create(1.0, 1.0, 1.0, 1.0)
        BLACK = vector4.create(0.0, 0.0, 0.0, 1.0)
        RED = vector4.create(1.0, 0.0, 0.0, 1.0)
        LIGHT_RED = vector4.create(1.0, 0.5, 0.5, 1.0)
        DARK_RED = vector4.create(0.55, 0.0, 0.0, 1.0)
        GREEN = vector4.create(0.0, 1.0, 0.0, 1.0)
        LIGHT_GREEN = vector4.create(0.5, 1.0, 0.5, 1.0)
        DARK_GREEN = vector4.create(0.0, 0.55, 0.0, 1.0)
        BLUE = vector4.create(0.0, 0.0, 1.0, 1.0)
        LIGHT_BLUE = vector4.create(0.678, 0.847, 0.902, 1.0)
        DARK_BLUE = vector4.create(0.0, 0.0, 0.55, 1.0)
        YELLOW = vector4.create(1.0, 1.0, 0.0, 1.0)
        CYAN = vector4.create(0.0, 1.0, 1.0, 1.0)
        MAGENTA = vector4.create(1.0, 0.0, 1.0, 1.0)
        GRAY = vector4.create(0.5, 0.5, 0.5, 1.0)
        LIGHT_GRAY = vector4.create(0.75, 0.75, 0.75, 1.0)
        DARK_GRAY = vector4.create(0.25, 0.25, 0.25, 1.0)
        ORANGE = vector4.create(1.0, 0.65, 0.0, 1.0)
        PURPLE = vector4.create(0.5, 0.0, 0.5, 1.0)
