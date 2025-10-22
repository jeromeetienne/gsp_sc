#!/usr/bin/env python

# stdlib imports
from pathlib import Path
import sys

# pip imports
import argparse

# local imports
from gsp.renderer.json.parser import JsonParser
from gsp_matplotlib.renderer.renderer import MatplotlibRenderer

if __name__ == "__main__":
    # parse command line arguments
    argParser = argparse.ArgumentParser(description="Process GSP JSON data and render to PNG.")
    argParser.add_argument("--input-file", "-i", type=str, help="Path to the input file (default: stdin)")
    argParser.add_argument("--output-file", "-o", type=str, help="Path to the output file (default: stdout)")
    args = argParser.parse_args()

    # read input file or stdin
    if args.input_file:
        with open(args.input_file, "r") as file_reader:
            file_content = file_reader.read()
    else:
        file_content = sys.stdin.read()

    # determine image format based on output file extension
    # - default to "png" if no output file is specified
    image_format = "png"
    if args.output_file:
        # Get the file extension with pathlib
        output_extension = Path(args.output_file).suffix
        # Remove the leading dot and convert to lower case
        image_format = output_extension.lower().lstrip(".")

    # parse scene
    json_parser = JsonParser()
    canvas, viewports, cameras = json_parser.parse(file_content)

    # render scene
    matplotlib_renderer = MatplotlibRenderer()
    image_png = matplotlib_renderer.render(canvas, viewports, cameras, image_format=image_format)

    # write output file or stdout
    if args.output_file:
        with open(args.output_file, "wb") as file_writer:
            file_writer.write(image_png)
    else:
        sys.stdout.buffer.write(image_png)
