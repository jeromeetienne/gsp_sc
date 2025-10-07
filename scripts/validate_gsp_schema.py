#!/usr/bin/env python3
"""
Validate all .gsp.json files in the repository against schema/gsp.json (Draft-07).

Usage: python tools/validate_gsp.py
"""
import json
import sys
from pathlib import Path

import jsonschema
import os

__dirname__ = os.path.dirname(__file__)

json_schema_path = os.path.join(__dirname__, "../data/json-schemas/early_gsp.schema.json")
output_folder_path = os.path.join(__dirname__, "../examples/output")


# Load the JSON schema
def load_schema() -> dict:
    with open(json_schema_path, "r", encoding="utf-8") as file_reader:
        schema: dict = json.load(file_reader)
        return schema


def find_gsp_file_paths():
    # TODO change that in string
    repo_root = Path(__dirname__, "..").resolve()
    return list(repo_root.glob("**/*.gsp.json"))


# =============================================================================
# Validate a single file
# =============================================================================
def validate_file(json_schema: dict, file_path: Path) -> tuple[bool, str | None]:
    """
    Validate a single file against the schema.
    Returns (True, None) if valid, (False, error_message) if invalid.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            file_data = json.load(f)
    except Exception as error:
        return False, f"Failed to load JSON: {error}"

    validator = jsonschema.Draft7Validator(json_schema)
    errors = sorted(validator.iter_errors(file_data), key=lambda error: error.path)
    if not errors:
        return True, None
    msg_lines = []
    for error in errors[:10]:
        msg_lines.append(f"{list(error.path)}: {error.message}")
    if len(errors) > 10:
        msg_lines.append(f"... and {len(errors)-10} more errors")
    return False, "\n".join(msg_lines)


# =============================================================================
# Main function
# =============================================================================
def main():
    json_schema = load_schema()
    file_paths = find_gsp_file_paths()
    if not file_paths:
        print("No .gsp.json files found.")
        return 0

    total = 0
    passed = 0
    for file_path in file_paths:
        total += 1
        ok, err = validate_file(json_schema, file_path)
        if ok:
            print(f"OK: {file_path}")
            passed += 1
        else:
            print(f"FAIL: {file_path}\n{err}\n")

    print(f"Summary: {passed}/{total} passed")
    return 0 if passed == total else 1


# =============================================================================
# Entry point
# =============================================================================
if __name__ == "__main__":
    main()
