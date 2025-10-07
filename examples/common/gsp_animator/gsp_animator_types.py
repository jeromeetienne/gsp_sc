# stdlib imports
from typing import Callable

# local imports
import gsp_sc


GSPAnimatorFunc = Callable[[], list[gsp_sc.core.VisualBase]]
"""Type alias for a GSP animator function."""
