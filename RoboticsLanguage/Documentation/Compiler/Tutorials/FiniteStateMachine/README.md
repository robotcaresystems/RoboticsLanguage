# Finite State Machines tutorial


[Finite state machines](https://en.wikipedia.org/wiki/Finite-state_machine) are a mathematical model for a system that can only have one state at each time. Finite state machines are very useful in modelling high level behaviour in robotics by grouping abstracted behaviours, e.g the robot is "idle", or "sleeping", "running", etc. This advanced tutorial describes all the steps required to: create a language to describe the finite state machine, all the way to the generation of C++ code that implements such a machine.

 1. [Defining a language and creating a parser](Parser.md)
 2. [Generating code from the abstract syntax tree](Transformer.md)
 3. [Creating an HTML graphical user interface to visualise the finite state machine](HTMLGUI.md)
 4. [Creating an Atom plugin to edit the mini-language graphically](AtomPlugin.md)
