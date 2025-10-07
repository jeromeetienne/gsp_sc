#!/usr/bin/env python3
import os
import sys
import runpy
import argparse


def find_project_root(start_path: str) -> str | None:
    current_path = os.path.abspath(start_path)
    while True:
        if os.path.exists(os.path.join(current_path, "pyproject.toml")):
            return current_path
        parent = os.path.dirname(current_path)
        if parent == current_path:
            return None
        current_path = parent


def main(argv: list[str]) -> None:
    parser = argparse.ArgumentParser(description="Run an example module with the project's src/ directory on sys.path.")
    parser.add_argument("example_path", help="Name of the example module to run (e.g., animator_network)")
    parser.add_argument("example_args", nargs=argparse.REMAINDER, help="Arguments to pass to the example module")

    args = parser.parse_args(argv[1:])

    example_path = args.example_path
    example_args = args.example_args

    repo_root = find_project_root(__file__)
    if repo_root is None:
        print("Could not find project root (pyproject.toml). Using current working directory.")
        sys.exit(1)

    old_cwd = os.getcwd()

    # change current working directory to the repo root
    os.chdir(repo_root)

    # set PYTHONPATH to current working directory
    os.environ["PYTHONPATH"] = repo_root

    # run the following command line
    cmdline = f"python {example_path} " + " ".join(example_args)
    os.system(cmdline)


if __name__ == "__main__":
    main(sys.argv)
    sys.exit(0)
