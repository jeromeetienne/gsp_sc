"""
GSP_SC: Graphic Server Protocol - Scientific Computing version

TMP: This one is using a 'scene-graph' API

A Python library for creating and rendering 2D/3D graphics for scientific computing using a client-server architecture.
"""

# Official version number of the package.
__version__ = "0.1.0"

from . import core
from . import renderer
from . import visuals
from . import types
from .core.constants import Constants

from . import transform
