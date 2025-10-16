# Datoviz Emulator

## Comments on Datoviz python API

- no explicit camera controller
- `.point` -> `.points` typo
- `.run` `.destroy` -> GOOD!
- figure -> canvas
- panel -> viewport
- too much code in the `__init__.py` of the model
  - it should be declaration only
- [point example](https://datoviz.org/gallery/visuals/point/) you lost the "s"'s in `generate_data`
  - add the "s"'s in the function

## Method Changes

Principle "Add explicitly"

- `points = panel.points(...)` -> `panel.add(Points(...))`
  - GOOD! lets generalize it
- `app.figure()` -> `app.add(Figure())`
- `panel = figure.panel()` -> `figure.add(Panel())`
- `panzoom = panel.panzoom()` -> `panel.set_controller(PanZoom())`
