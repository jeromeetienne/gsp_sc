# stdlib imports
from typing import Callable

# local imports
import gsp


GSPAnimatorFunc = Callable[[], list[gsp.core.VisualBase]]
"""Type alias for a GSP animator function."""
