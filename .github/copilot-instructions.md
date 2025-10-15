# Copilot Instructions for gsp_sc

## Project Overview
- **gsp_sc** is a Python library for creating and rendering 2D/3D graphics for scientific computing, using a scene-graph API and a client-server architecture.
- Major components are in `src/gsp/`:
  - `core/`: Scene graph primitives (Canvas, Viewport, VisualBase, Camera, etc.)
  - `types/`: Array types and serialization (supports numpy, delta, and transform ndarrays unified as `NdarrayLike`)
  - `renderer/`, `visuals/`, `transform/`: Rendering, visual objects, and transformation logic
- Examples and test scripts are in `examples/` and `tests/`.

## Key Patterns & Conventions
- **Scene Graph**: Compose scenes using `Canvas`, `Viewport`, and `VisualBase` objects. Add visuals to viewports, and viewports to canvases.
- **NdarrayLike**: All array-like data (numpy, delta, transform) should be handled via `NdarrayLikeUtils` for serialization/deserialization and conversion.
- **Events**: Use `blinker.Signal` for pre/post rendering and transformation hooks in visuals.
- **Output Validation**: Output files from examples are compared against expected files in `examples/expected/` using deep JSON/image comparison.
- **Testing**: Run all tests and examples via `make test` or `python tools/run_all_examples.py`.
- **Linting/Type Checking**: Use `make lint` (runs pyright on `src/` and `examples/`).
- **JSON Schema Validation**: Validate `.gsp.json` files with `python tools/validate_gsp_schema.py`.
- **Network Server**: Start with `make network_server` or `make network_server_dev` (auto-reloads on changes).

## Developer Workflows
- **Build/Test**: `make test` runs lint, pytest, all examples, and output checks.
- **Run Examples**: `python tools/run_all_examples.py` (kills/restarts network server as needed).
- **Check Output**: `python tools/check_expected_output.py` compares generated outputs to expected results.
- **Lint**: `make lint` or `pyright src/gsp/` and `pyright examples/`.
- **Network Server**: `make network_server` (prod) or `make network_server_dev` (dev, with auto-restart).

## Integration & Extensibility
- **Add new ndarray types** by extending `NdarrayLikeType` and updating `NdarrayLikeUtils`.
- **Visuals**: Add new visual types by subclassing `VisualBase` and registering with the scene graph.
- **Schema**: JSON schemas for output validation are in `data/json-schemas/`.
- **External dependencies**: See `pyproject.toml` for required packages (numpy, blinker, meshio, etc.).

## References
- Main entry: `src/gsp/__init__.py`
- Scene graph: `src/gsp/core/`
- Array types: `src/gsp/types/`, especially `ndarray_like_utils.py`
- Example scripts: `examples/`
- Test suite: `tests/`
- Output validation: `tools/check_expected_output.py`
- JSON schema validation: `tools/validate_gsp_schema.py`
- Network server: `tools/network_server.py`

---

If any conventions or workflows are unclear, please ask for clarification or check the referenced files for concrete examples.
