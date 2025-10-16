# stdlib imports
from typing import Callable, Sequence

# local imports
import gsp


# do a callback type for the animation loop
GSPAnimatorFunc = Callable[[], Sequence[gsp.core.VisualBase]]
"""A simple animation loop manager for matplotlib rendering.

Arguments:
    delta_time (float): Time elapsed since the last frame in milliseconds.
"""
