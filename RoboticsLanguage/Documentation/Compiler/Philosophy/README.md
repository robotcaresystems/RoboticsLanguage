# The Robotics Language compiler philosophy

The `rol` compiler implements a generic engine that works by processing two types of information, **code** and **parameters**, thought three steps: **input**, **transformations**, and **output**. Parameters are represented internally by a python dictionary. Code is represented internally by an XML object.

![](../../Assets/compiler-flow.png)
