# pip imports
from typing import Callable

from pyrr import Matrix44, Vector3
from math import atan2, asin
import numpy as np
from core.my_random import Random

# define a type for the traverse callback
TraverseCallback = Callable[["Object3D"], None]


class Object3D:
    def __init__(self) -> None:
        self.uuid = Random.random_uuid()
        self.position: Vector3 = Vector3([0.0, 0.0, 0.0], dtype=np.float32)
        self.rotation: Vector3 = Vector3([0.0, 0.0, 0.0], dtype=np.float32)  # Euler XYZ, radians
        self.scale: Vector3 = Vector3([1.0, 1.0, 1.0], dtype=np.float32)

        self.parent: Object3D | None = None
        self._children: list[Object3D] = []

        self._local_matrix = Matrix44.identity(dtype=np.float32)
        self._world_matrix = Matrix44.identity(dtype=np.float32)
        self._dirty = True  # marks transform cache as invalid

    def _mark_dirty(self) -> None:
        self._dirty = True
        for c in self._children:
            c._mark_dirty()

    def add_child(self, child: "Object3D") -> None:
        child.parent = self
        self._children.append(child)
        child._mark_dirty()

    def remove_child(self, child: "Object3D") -> None:
        assert child in self._children, "Child not found"
        self._children.remove(child)
        child.parent = None

    def traverse(self, func: TraverseCallback) -> None:
        func(self)
        for child in self._children:
            child.traverse(func)

    def get_local_matrix(self, force=False) -> np.ndarray:
        if self._dirty or self._local_matrix is None or force:
            t = Matrix44.from_translation(self.position)
            rx = Matrix44.from_x_rotation(self.rotation.x)
            ry = Matrix44.from_y_rotation(self.rotation.y)
            rz = Matrix44.from_z_rotation(self.rotation.z)
            r = rz @ ry @ rx
            s = Matrix44.from_scale(self.scale)

            self._local_matrix = t @ r @ s
        return self._local_matrix

    def get_world_matrix(self, force=False) -> np.ndarray:
        if self._dirty or self._world_matrix is None or force:
            if self.parent:
                self._world_matrix = self.parent.get_world_matrix(force=force) @ self.get_local_matrix(force=force)
            else:
                self._world_matrix = self.get_local_matrix(force=force)
            self._dirty = False
        return self._world_matrix

    def update_matrix_world(self, force=False) -> None:
        self.get_world_matrix(force=force)
        for child in self._children:
            child.update_matrix_world(force=force)

    # =============================================================================
    #
    # =============================================================================
    def get_world_position(self) -> Vector3:
        world_matrix = self.get_world_matrix()
        return Vector3(world_matrix[3, :3].tolist())

    def get_world_rotation(self) -> Vector3:
        if self.parent:
            parent_rotation = self.parent.get_world_rotation()
            return Vector3(
                (
                    parent_rotation.x + self.rotation.x,
                    parent_rotation.y + self.rotation.y,
                    parent_rotation.z + self.rotation.z,
                )
            )
        else:
            return self.rotation

    def get_world_scale(self) -> Vector3:
        if self.parent:
            parent_scale = self.parent.get_world_scale()
            return Vector3(parent_scale.x * self.scale.x, parent_scale.y * self.scale.y, parent_scale.z * self.scale.z)
        else:
            return self.scale
