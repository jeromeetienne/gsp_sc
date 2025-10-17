# GSP

# What is GSP

- GSP stands for Graphical Server Protocol
  - the goal is to have a protocol to describe graphical scenes
  - thus it is abstract enough to be used in different contexts
  - people can easily implement various renderers for it
  - we provide a reference implementation in python using matplotlib
    - python is widely used in the data science community
    - matplotlib is a widely used plotting library in python
    - numpy is used for numerical computations in python
  - datoviz presents another implementation in C++/python using Vulkan

---

# Protocol

- there is a payload .gsp.json file
- it contains a scene description

# What is a scene

- a canvas may contain multiple viewports
- most of the time there is only one viewport
- a viewport contains multiple visuals
- there is a camera associated with the viewport, a camera can be orthographic or perspective

# List of visuals

Based on previous experience with vispy, we identified that the following visuals are the most common ones and should be supported by GSP.

## Image

TODO

## Markers

TODO

## Paths

TODO

## Pixels

TODO

## Points

TODO

## Polygons

TODO

## Segments

TODO

## Volumes

TODO
