#!/usr/bin/env python3
"""
Run an example module while ensuring the project src/ directory is on sys.path.

Usage:
  python scripts/run_example.py animator_network [args...]

This will run the example module `examples.animator_network` as if you had run
`python -m examples.animator_network`, but you can run the script directly.

It finds the workspace root by walking up from this file until it finds a `pyproject.toml`
(or stops at filesystem root). It then inserts the project's `src` directory at
sys.path[0] so package imports like `import gsp_sc` work correctly.

This is a small convenience wrapper. Prefer `python -m examples.animator_network`
for normal usage, or install the package in editable mode (`pip install -e .`).
"""
import os
import sys
import runpy


def find_project_root(start_path: str) -> str | None:
    cur = os.path.abspath(start_path)
    while True:
        if os.path.exists(os.path.join(cur, 'pyproject.toml')):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return None
        cur = parent


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: run_example.py <example_module_name> [args...]")
        print("Example: python scripts/run_example.py animator_network")
        return 2

    example_name = argv[1]
    example_args = argv[2:]

    repo_root = find_project_root(__file__)
    if repo_root is None:
        print("Could not find project root (pyproject.toml). Using current working directory.")
        repo_root = os.getcwd()

    src_dir = os.path.join(repo_root, 'src')
    if os.path.isdir(src_dir):
        # Put src at the front of sys.path so packages in src/ are importable
        sys.path.insert(0, src_dir)
    else:
        # If there's no src/ (unlikely in this repo), insert repo root
        sys.path.insert(0, repo_root)

    # Forward remaining args to the example via sys.argv
    sys.argv = [f"examples.{example_name}"] + example_args

    module_name = f"examples.{example_name}"
    # Use runpy to execute the module as a script (sets __name__ == '__main__')
    try:
        runpy.run_module(module_name, run_name='__main__', alter_sys=True)
        return 0
    except Exception as e:
        print(f"Error running example '{example_name}': {e!r}")
        raise


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
