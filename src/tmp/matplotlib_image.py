#!/usr/bin/env python3
"""Minimal example: load a PNG and display it with matplotlib.

Edit IMAGE_PATH below to point to the PNG you want to display.
"""

import os
import io
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

# Path to the image to display. Edit this as needed.
# By default this points to the repository example image.
IMAGE_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "../examples/images/UV_Grid_Sm.jpg"))


def _load_and_show(path: str) -> None:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Image not found: {path}")

    # load the file contents
    with open(path, "rb") as file_reader:
        image_png_data = file_reader.read()

    img = mpimg.imread(io.BytesIO(image_png_data))
    plt.figure(figsize=(6, 6))
    if img.ndim == 2:
        plt.imshow(img, cmap="gray")
    else:
        plt.imshow(img)
    plt.axis("off")
    plt.show()


_load_and_show(IMAGE_PATH)
