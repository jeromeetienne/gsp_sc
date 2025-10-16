from typing import NamedTuple, TypedDict


###############################################################################
#   Type for the network payload
#
class SceneDict(TypedDict):
    canvas: dict
    """Canvas data in JSON format."""


class Color(NamedTuple):
    """
    Color representation in RGBA format with components ranging from 0 to 1.

    Parameters
    ----------
    r : float
        Red component of the color (0 to 1).
    g : float
        Green component of the color (0 to 1).
    b : float
        Blue component of the color (0 to 1).
    a : float
        Alpha (opacity) component of the color (0 to 1).
    """

    r: float
    """
    Red component of the color (0 to 1).
    """
    g: float
    """
    Green component of the color (0 to 1).
    """
    b: float
    """
    Blue component of the color (0 to 1).
    """
    a: float
    """
    Alpha (opacity) component of the color (0 to 1).
    """
