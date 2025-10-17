# pip imports
import blinker

# local imports
from .random import Random
from .event import Event


class VisualBase:
    __slots__ = ("uuid", "pre_rendering", "post_transform", "post_rendering")

    def __init__(self) -> None:
        self.uuid = Random.random_uuid()
        """
        The unique identifier of the visual.

        - Used in renderers to track visuals context across multiple render calls.
        """

        # NOTE comparison to gsp
        # - more flexible, more in controls of the users
        # - much simpler that the class overloading which mess up with static typing
        # - faster at runtime
        #   - e.g. gsp do a sort of all position at all rendering, even when there is no transform.
        #   Just because the Transform class "likes" it, eg to implement fog based on z
        # - much less code to maintain
        self.pre_rendering = blinker.Signal()
        """Event triggered before rendering the visual."""

        self.post_transform = blinker.Signal()
        """
        Event triggered after applying 3d transformations to the visual.

        Arguments sent to subscribers:
        - renderer: The renderer instance performing the rendering.
        - camera: The camera used for rendering.
        - transformed_positions: The numpy array of transformed positions (shape: n x 3).
        """

        self.post_rendering = blinker.Signal()
        """Event triggered after rendering the visual."""
