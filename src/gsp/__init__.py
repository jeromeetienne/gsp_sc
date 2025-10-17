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

from . import transform

from . import math

from . import materials
from . import geometry
from . import objects
from . import lights
from . import cameras
