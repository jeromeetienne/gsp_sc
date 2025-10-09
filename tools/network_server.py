#!/usr/bin/env python3
"""
Server example using Flask to render a scene from JSON input.

- use Flask to create a simple web server
- render with matplotlib
"""

# pip imports
import argparse

# local imports
from gsp_network import ServerSample

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run the network server for rendering. see ./examples/network_client.py for usage.")
    args = parser.parse_args()

    server = ServerSample()
    server.run()
