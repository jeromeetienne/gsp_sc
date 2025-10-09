"""
Define the visuals module for GSP_SC

This module contains different types of visual elements that can be added to a scene,

Currently supported visuals are:
- Pixels: to display a grid of colored pixels
- Image: to display an image within specified bounds
"""

from . pixels import Pixels
from . image import Image
from . mesh import Mesh