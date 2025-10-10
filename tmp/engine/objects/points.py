from core.object_3d import Object3D
from pyrr import Vector3
import numpy as np


class Points(Object3D):
    def __init__(self, vertices: list[Vector3] = []):
        super().__init__()

        assert all(isinstance(v, Vector3) for v in vertices), "Vertices must be a list of Vector3 objects"

        self.vertices: list[Vector3] = vertices
