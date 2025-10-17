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
# Design 

There are three main design goals for GSP:
- **Portability**: the protocol should be usable in different contexts and with different rendering backends
- **Support for remote data**: the protocol should support referencing data that is not local to the developer machine. GRPD compliance is a key aspect of this goal.
- **Maintainability**: the protocol should be simple enough to be easily understood and modified

## Portable 

- it should be possible to implement GSP in different programming languages
- it should be possible to implement GSP with different rendering backends
  - e.g. matplotlib, datoviz, three.js, vtk, etc.

### Origin

> "GSP is for graphics what LSP is for languages"

- comes from LSP in vscode
  - https://symflower.com/en/company/blog/2022/lsp-in-vscode-extension/
  - https://code.visualstudio.com/api/language-extensions/language-server-extension-guide
  - https://microsoft.github.io/language-server-protocol/
  - vscode had the same problem with supporting multiple languages that we have with supporting multiple rendering backends.
  - they solved it by creating a protocol to describe language features
  - then they created language servers that implement the protocol for each language
  - the vscode client can then communicate with any language server that implements the protocol
  - their solution is very successful and is now widely adopted
  - their solution is similar in principle to what we want to do with GSP



# Remote data
- Another key aspect of GSP is the support of remote data
  - in europe, there is an important law that states that data should stay in the country of origin
  - the name of this law is GDPR
  - https://gdpr.eu/
  - so to be compliant with this law, we need to be able to visualize data that is not local to the developer machine

## How to modify remote data before visualizing it
- TODO talk about transforms 


## Maintenable
- previous experience with vispy showed that it is hard to maintain a rendering library
- by separating the scene description from the rendering, we can focus on each part independently
- the scene description is simple enough to be easily understood and modified
- the rendering can be improved independently, and multiple renderers can coexist
- tools will be provided to ensure compliance
  - json schema to validate the scene description


### How to pick tech to match the design goals
- follow the unix philosophy : "do one thing and do it well"
- [rfc 1925](https://tools.ietf.org/html/rfc1925)
- keep it simple, stupid (KISS)
  - prefer simplicity over cleverness
  - prefer readability over writability
  - prefer explicitness over implicitness
  - prefer consistency over convenience
- use widely adopted tech and standards
- dont name things which are against user's expectations
  - e.g. if your users call something "image", dont name it "raster" in your code
- be specific in naming things
  - e.g. if you have a function that computes the mean of an array, name it "compute_mean" and not "compute"
- avoid premature optimization
  - "premature optimization is the root of all evil" - donald knuth
- optimize for the common case, not the edge case
  - it is ok to have edge cases, but handle them separately
- avoid reinventing the wheel
- "be conservative in what you send, be liberal in what you accept" - jon postel [link](https://en.wikipedia.org/wiki/Robustness_principle)

### When writing code, how to be maintainable
- write tests
- make it easy to read by non-experts
- be consistent
- document everything
- use type hints, linters, formatters
- be sure that any error is detected as early as possible

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