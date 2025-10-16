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

### Lack of consistency

- app = dvz.App(): create an app (no adding)
- figure = app.figure() create a figure and add it to the app
- panel = figure.panel() create a panel and add it to the figure
- panzoom = panel.panzoom() create a camera controller and set it to the panel
- image = app.image() create an image (no adding to figure)
