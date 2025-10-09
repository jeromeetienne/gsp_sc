"""
Renderer module to handle different output formats.

Currently supported renderers are:
- matplotlib: to render using matplotlib
- json: to export the scene to a JSON description
- network: to render using a remote rendering server
"""

from . import json

from .json import JsonRenderer, JsonParser
