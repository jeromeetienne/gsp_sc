"""
Renderer module to handle different output formats.

Currently supported renderers are:
- matplotlib: to render using matplotlib
- json: to export the scene to a JSON description
- network: to render using a remote rendering server
"""

from . import json
from . import matplotlib
from . import network

from .json import JsonRenderer, JsonParser
from .matplotlib import MatplotlibRenderer
from .network import NetworkRenderer
