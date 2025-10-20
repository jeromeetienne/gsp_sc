from typing import Literal
import numpy as np

import mpl3d.camera
import mpl3d.glm

from .random import Random


class Camera:
    __slots__ = ["uuid", "camera_type", "__position", "__mpl3d_camera"]

    def __init__(self, camera_type: Literal["ortho", "perspective"]):
        self.uuid = Random.random_uuid()
        """The unique identifier of the camera."""

        self.camera_type = camera_type
        """The type of camera: "ortho" or "perspective" """

        self.__position = np.array([0, 0, 1], dtype=np.float32)
        """The position of the camera in world coordinates."""

        self.__mpl3d_camera = mpl3d.camera.Camera(mode=camera_type)
        """The internal mpl3d camera """

    # A getter for the internal mpl3d camera.transform
    @property
    def transform(self) -> np.ndarray:
        """MVP transformation matrix of the camera."""
        return self.__mpl3d_camera.transform

    @property
    def mpl3d_camera(self) -> mpl3d.camera.Camera:
        return self.__mpl3d_camera

    def get_position(self) -> np.ndarray:
        return self.__position.copy()

    def set_position(self, position: np.ndarray) -> None:
        if position.shape != (3,):
            raise ValueError("Position must be a 3D vector.")
        self.__position = position.copy()
        self.__update_mpl3d_matrix()

    def __update_mpl3d_matrix(self) -> None:
        position_x, position_y, position_z = self.__position
        self.__mpl3d_camera.view = mpl3d.glm.translate(position_x, position_y, position_z) @ mpl3d.glm.scale(self.__mpl3d_camera.scale)
        self.__mpl3d_camera.transform = self.__mpl3d_camera.proj @ self.__mpl3d_camera.view @ self.__mpl3d_camera.trackball.model.T
