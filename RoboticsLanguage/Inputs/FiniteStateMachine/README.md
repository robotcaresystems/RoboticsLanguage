# Module FiniteStateMachine


This module works as an starting point to make your own mini-language

To test this Module you can look at the XML code generated bu the parser by running the parser directly on a `fsm` file:

```shell
rol RoboticsLanguage/Examples/FiniteStateMachine/example.fsm --debug-xml-before-transformations
```

... or using as a mini-language inside the Robotics Language:

```shell
rol RoboticsLanguage/Examples/FiniteStateMachine/FiniteStateMachine.rol --debug-xml-before-transformations
```

## Creating your own Module

To create your own module you can use


```shell
cd RoboticsLanguage/Inputs
rol ../Examples/helloworld.rol -ci "My Module" -p . -o Developer -v debug
```
_(forget about the `../Examples/helloworld.rol` part. Will not be necessary in the future)_

Then edit the file `RoboticsLanguage/Inputs/MyModule/Parameters.py` to fit your needs.

The parsing file is available at `RoboticsLanguage/Inputs/MyModule/Parse.py`


Before you use the new module make sure to clean the cache:

```shell
rol --remove-cache
```
