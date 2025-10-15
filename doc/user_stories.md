# User Stories for GSP

---

## User Roles

List of the various roles of persons that may use GSP.

### Implementer of a new backend for GSP

#### Who is it ?

- quite technical
- knows about rendering libraries
- it will have the time to learn how to do it

#### What does it want ?

- a clear definition of the API
- a test suite to validate the implementation

### Implementer of a scientific visualization library

#### Who is it ?

#### What does it want ?

### Developer using scientific visualization library

#### Who is it ?

- it is a scientist or a software developer close to science
- it has some data to visualize
- it may not be an expert in visualization
- it may not have the time to learn a complex library

#### What does it want ?

- its goals is to have a good visualization of its data
- it wants to be able to use the library in a simple way
- it wants to be able to customize the visualization
- it wants to be able to use the library in a performant way
- it wants to be able to use the library in a reliable way

---

## User Stories

### 1. As a data scientist, I want to visualize large datasets stored on a remote server without downloading them to my local machine, so that I can comply with data privacy regulations

- it needs to be easy to use and efficient
- it needs to support large datasets
- it needs to be able to create dummy data locally for testing

### 2. As a software developer, I want to integrate GSP into my existing data analysis pipeline, so that I can easily visualize the results of my computations

- it needs to have a simple and well-documented API
- it needs to support common data formats
  - produce images in svg or pdf format to include in my papers

### 3. As a researcher, I want to create interactive visualizations of my data that can be shared with collaborators, so that we can explore the data together
