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
- visual.set_texture(texture) <- `image.add_texture(texture)` it should be possible to have multiple textures per image
  - if not supported by backend, raise an error
  - to have a clean API, should the api support multiple texture, even if the backend doesnt support it? thus the 'information is not lost' in case it is faster for other backend
- `Image` -> `Images` (plural)
  - because it can handle multiple images
- `image.set_texture()`
  - RULE: we allow `.get_attr()` and `.set_attr()` for all attributes
  - RULE: all attributes may be passed thru the ctor
  - matplotlib is doing that
- coordinate conversion
  - Q. can we say 'viewport are in ndc' ?
  - if the user express it in pixel, we do the conversion as soon as we receive the coordinates
  - thus the conversion is done in the constructor (or any user facing function), and internally we handle it as ndc
- `ShapeCollection` ? why not an array of meshes
  - [link](https://github.com/datoviz/datoviz/blob/4ca6c6e94e46b336b2834487017c5628f613f063/examples/visuals/mesh.py#L16C10-L21)
  - to renamed `Shapes`

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
