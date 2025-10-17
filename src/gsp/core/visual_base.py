# pip imports
import blinker
from typing import Protocol
import numpy as np

# local imports
from .random import Random
from .event import Event


class VisualPreRenderingCallback(Protocol):
    def __call__(self, visual: "VisualBase") -> None: ...


class VisualTransformCallback(Protocol):
    def __call__(self, renderer: object, camera: object, transformed_positions: "np.ndarray") -> None: ...


class VisualPostRenderingCallback(Protocol):
    def __call__(self, visual: "VisualBase") -> None: ...


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
        self.pre_rendering = Event[VisualPreRenderingCallback]
        """Event triggered before rendering the visual."""

        self.post_transform = Event[VisualTransformCallback]
        """
        Event triggered after applying 3d transformations to the visual.
        Happening in the rendering pipeline after model-view-projection transformations.

        Arguments sent to subscribers:
        - transformed_positions: The numpy array of transformed positions (shape: n x 3).
        """

        self.post_rendering = Event[VisualPostRenderingCallback]
        """Event triggered after rendering the visual."""
