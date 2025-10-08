import numpy as np


class MeshParserObjManual:
    @staticmethod
    def parse_obj_file(
        file_path: str,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray | None, np.ndarray | None]:
        """
        Parse a Wavefront .obj file and extract vertex, texture, and normal coordinates.

        Arguments:
            file_path (str): Path to the .obj file.

        Returns:
            tuple: A tuple containing:
                - vertices_coords (np.ndarray): Array of vertex coordinates. Shape (N, 3).
                - faces_indices (np.ndarray): Array of face indices. Shape (M, 3).
                - uvs_coords (np.ndarray | None): Array of texture coordinates (if available). Shape (N, 2) or None.
                - normals_coords (np.ndarray | None): Array of normal coordinates (if available). Shape (N, 3) or None.
        """

        vertices_coords, uvs_coords, normals_coords, faces_vertex_indices, faces_uv_indices, faces_normal_indices = MeshParserObjManual.parse_raw(file_path)

        # Sanity checks - a valid .obj file should have at least vertices and faces
        assert len(vertices_coords) > 0, "No vertices found in the .obj file."
        assert len(faces_vertex_indices) > 0, "No faces found in the .obj file."

        vertices_coords = vertices_coords
        faces_indices = faces_vertex_indices
        faces_uvs = uvs_coords[faces_uv_indices] if len(uvs_coords) > 0 and len(faces_uv_indices) > 0 else None
        faces_normals = normals_coords[faces_normal_indices] if len(normals_coords) > 0 and len(faces_normal_indices) > 0 else None

        return vertices_coords, faces_indices, faces_uvs, faces_normals

    @staticmethod
    def parse_raw(filename: str) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Read a wavefront filename and returns vertices, texcoords and
        respective indices for faces and texcoords

        Arguments:
            filename (str): Path to the .obj file.

        Returns:
            tuple: A tuple containing:
                - vertices_coords (np.ndarray): Array of vertex coordinates. Shape (N, 3).
                - uvs_coords (np.ndarray): Array of texture coordinates. Shape (N, 2).
                - normals_coords (np.ndarray): Array of normal coordinates. Shape (N, 3).
                - faces_vertex_indices (np.ndarray): Array of face vertex indices. Shape (M, 3).
                - faces_uv_indices (np.ndarray): Array of face texture coordinate indices. Shape (M, 3).
                - faces_normal_indices (np.ndarray): Array of face normal coordinate indices. Shape (M, 3).
        """

        vertices_coords, uvs_coords, normals_coords, faces_vertex_indices, faces_uv_indices, faces_normal_indices = [], [], [], [], [], []
        with open(filename) as f:
            for line in f.readlines():
                if line.startswith("#"):
                    continue
                values = line.split()
                if not values:
                    continue
                if values[0] == "v":
                    vertices_coords.append([float(x) for x in values[1:4]])
                elif values[0] == "vt":
                    uvs_coords.append([float(x) for x in values[1:3]])
                elif values[0] == "vn":
                    normals_coords.append([float(x) for x in values[1:4]])
                elif values[0] == "f":
                    faces_vertex_indices.append([int(indices.split("/")[0]) for indices in values[1:]])
                    faces_uv_indices.append([int(indices.split("/")[1]) for indices in values[1:]])
                    faces_normal_indices.append([int(indices.split("/")[2]) for indices in values[1:]])
        return (
            np.array(vertices_coords),
            np.array(uvs_coords),
            np.array(normals_coords),
            np.array(faces_vertex_indices) - 1,
            np.array(faces_uv_indices) - 1,
            np.array(faces_normal_indices) - 1,
        )
