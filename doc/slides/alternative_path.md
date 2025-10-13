---
marp: true
theme: marpit-theme
---

# Alternative Path


---

- defensive coding
- test the whole stack
- use CI/CD
- use static analysis tools
- use linters

---

# Use engineering good practices for softwar engineering
- good engineering practices - https://www.perplexity.ai/search/good-practice-in-engineering-CLw14nwnTZerrEUSTfSopw
- use version control
- use code reviews
- write documentation
  - documentation in the code is better than external documentation
  - introduced by knuth in 1984 [link](https://en.wikipedia.org/wiki/Literate_programming)
- write unit tests are cool for complex functions (e.g. tracked diffable ndarray)
- prefere to write end2end tests than unit tests
  - for the whole pipeline
  - it is covering way more code for much less efforts
- refactor regularly

---

# Strong typing is not optional

## What does it bring ?
- catch errors early
  - good for libraries users
  - good for team developpers
- it gives trust in the code
  - to the developper and to the users
- make the code more maintainable
  - dev teams is more in controls of the code
  - avoid unexpected behaviors or misunderstandings 
  - "the code talks"
- always assume the code will fails, 
- do many assert in the code. Fail early, fail loudly

- make the code more readable
- make the code more self-documenting
- Help new adopters to understand the codebase

---

# Coding Standards
- no global variables
- no single letter variable names
- no hardcoded values
- use meaningful names
- write comments and __doc__ strings
- add __doc__ string to instance variables too
- lint the code on save
- write tests
- follow coding standards
- "the code talks"

# Losely Coupled Modules
- a renderer is totally separated from the core
  - no inheritance which may cause conflicts
  - aka the core may stop working if the renderer is buggy
- a network module is totally separated from the core
- json is just a renderer format


---

## Network

- Goal: satisfy GDPR laws (General Data Protection Regulation)

- implemented a network server/clients

- delta encoding to minimize data transfer
  - diff at the json level on the whole scene 
    - good if usage pattern is "small scene"
    - it is slow at to do diff if the scene is large
  - diff at the ndarray level on each visual
    - good if usage pattern is "large scene"
    - PRO: much faster to compute the diff at the scene level
    - CON: more complex to implement
    - CON: more complex to maintain
  - even the diff at the ndarray level got some tech choises depending on usage pattern
    - Track per indice modifications (more memory usage, smaller serialised size)
    - Track single bounding box per axis (less memory usage, larger serialised size) <- we do this one
    - Track multiple bounding boxes (more memory usage, smaller serialised size, more complex code/maintenance)


# Tests

- end2end tests: 21
- unit tests: 23
- Grammar to check the command generation: **Checked**