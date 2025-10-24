import gsp_n as gsp
import numpy as np


def main():
    # Create a canvas
    canvas = gsp.Canvas(800, 600, 96.0)

    # Create a viewport and add it to the canvas
    viewport = gsp.Viewport(400, 300)
    canvas.add(viewport)

    # =============================================================================
    # Add random points
    # - various ways to create Buffers
    # =============================================================================
    point_count = 1024
    # Random positions - Create buffer from numpy array
    positions_buffer = gsp.Buffer.from_numpy(np.random.rand(point_count, 3).astype(np.float32))
    # all pixels red - Create buffer and fill it with a constant
    colors_buffer = gsp.Buffer(point_count, gsp.BufferType.color).fill(gsp.Constants.red)  # Red color
    # one group for all points - create buffer and set value with immediate assignment
    groups_buffer = gsp.Buffer(1, gsp.BufferType.uint32)
    # TODO set the [0] element to 1
    # groups_buffer[0] = gsp.BufferType.uint32(1)  # one group

    pixels = gsp.Pixels(positions_buffer, colors_buffer, groups_buffer)
    viewport.add(pixels)

    # Set the model matrix for the visual
    model_matrix = gsp.Mat4x4.from_numpy(np.eye(4, dtype=np.float32))
    pixels.set_model_matrix(model_matrix)

    # =============================================================================
    # Add an image
    # =============================================================================
    # texture buffer - example of DataSource to Buffer conversion
    texture_buffer = gsp.DataSource("path/to/your/image.png").to_buffer(gsp.BufferType.uint8)
    texture = gsp.Texture2D(texture_buffer)

    positions_buffer = gsp.Buffer.from_numpy(np.array([[100.0, 100.0, 0.0]], dtype=np.float32))
    sizes_buffer = gsp.Buffer.from_numpy(np.array([[200.0, 150.0]], dtype=np.float32))
    axis_buffer = gsp.Buffer.from_numpy(np.array([[0.0, 0.0, 1.0]], dtype=np.float32))
    angles_buffer = gsp.Buffer.from_numpy(np.array([np.pi / 4], dtype=np.float32))
    groups_buffer = gsp.Buffer.from_numpy(np.array([1], dtype=np.uint32))
    images = gsp.Images(positions_buffer, sizes_buffer, axis_buffer, angles_buffer, [texture], groups_buffer)
    viewport.add(images)

    # =============================================================================
    # Render the canvas
    # =============================================================================
    # Create a camera
    view_matrix = gsp.Mat4x4()
    projection_matrix = gsp.Mat4x4([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, -0.1], [0, 0, -1, 0]])
    camera = gsp.Camera(view_matrix, projection_matrix)

    # Create a renderer and render the scene
    matplotlibRenderer = gsp.MatplotlibRenderer(canvas)
    matplotlibRenderer.render([pixels, images], [camera, camera])


if __name__ == "__main__":
    main()
