- currently there are 3 types of ndarrays
  - transform ndarray
  - delta ndarray
  - regular ndarray (numpy)
- need to unify them in the code under a common type NdarrayLike
- need to be able to serialize/deserialize them
- need to be able to convert from one to another


- delta ndarray is tech choise which may not be the best one in all cases
  - we need to let the user choose the best one for their use case
  - aka the user should be able to add they own ndarray type