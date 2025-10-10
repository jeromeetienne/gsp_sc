from core.object_3d import Object3D
from pyrr import Matrix44, Vector3
import numpy as np


class OrthographicCamera(Object3D):
    def __init__(self):
        super().__init__()
        self.left = -1.0
        self.right = 1.0
        self.bottom = -1.0
        self.top = 1.0
        self.near = 0.1
        self.far = 100.0

    def get_projection_matrix(self):
        l = self.left
        r = self.right
        b = self.bottom
        t = self.top
        n = self.near
        f = self.far

        proj_matrix = Matrix44(
            [[2 / (r - l), 0, 0, -(r + l) / (r - l)], [0, 2 / (t - b), 0, -(t + b) / (t - b)], [0, 0, -2 / (f - n), -(f + n) / (f - n)], [0, 0, 0, 1]],
            dtype=np.float32,
        )

        return proj_matrix
