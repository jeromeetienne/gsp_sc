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

# Use engineering good practices
- use version control
- use code reviews
- write documentation
- refactor regularly

---

# Strong typing is no option

## What does it bring ?
- catch errors early
  - good for libraries users
  - good for team developpers
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
- write unit tests
- follow coding standards

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
