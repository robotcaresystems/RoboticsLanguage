![](RoboticsLanguage/Documentation/Assets/rol-logo.png)

# What is the language of Robotics?

This is a very deep question with difficult answers. If robotics is meant to equal or even surpass human capabilities, then the language of robotics should be able to describe human behaviour, all the way from muscle activation to intelligence. Achieving this on a single programming language seems like an impossible task. This project proposes a new framework where multiple domain specific languages are used together to describe the behaviour of a robot. Specifically, the *Robotics Language (RoL)* is a high level robotics programming language that generates ROS c++ nodes.

[Domain Specific Languages](https://en.wikipedia.org/wiki/Domain-specific_language) *are computer languages specialised to a particular application domain*. Such languages use the minimum information required to describe a particular concept for a domain, thus present an **abstraction** of information. This project uses the concept of **mini-languages** to abstract programming by combining multiple domain specific languages in a single file.  



The base RoL language has a structure similar to standard high-level programming languages

```coffeescript
# A simple topic echo node
node(
  name:'example echo',

  definitions: block(
    # the input signal
    echo_in ∈ Signals(Strings, rosTopic:'/echo/in', onNew: echo_out = echo_in ),

    # the echo signal
    echo_out ∈ Signals(Strings, rosTopic:'/echo/out')
  )
)
```

The power of the RoL is in its ability to integrate mini-languages to build code abstractions.

```coffeescript
# A finite state machine
node(
  name:'example state machine',

  definitions: block(

    # a mini-language: code is defined within `<{ }>`
    FiniteStateMachine<{

        name:machine
        initial:idle

        (idle) -start-> (running) -stop-> (idle)
        (running) -error-> (fault) -reset-> (idle)

      }>,

    # the start signal
    start ∈ Signals(Empty, rosTopic:'/start', onNew: machine.fire('start')),

    # the stop signal
    stop ∈ Signals(Empty, rosTopic:'/stop', onNew: machine.fire('stop'))

  )
)
```

The RoL is in practice an **open compiler** where users can develop their own languages by means of plug-ins. The RoL is programmed in python and uses XML as the internal abstract syntax tree.

## Documentation

- The Robotics Language
  - [Philosophy](RoboticsLanguage/Documentation/Language/Philosophy/README.md)
  - [Tutorials](RoboticsLanguage/Documentation/Language/Tutorials/README.md)
  - [Reference](RoboticsLanguage/Documentation/Language/Reference/README.md)

- The Robotics Language compiler
  - [Philosophy](RoboticsLanguage/Documentation/Compiler/Philosophy/README.md)
  - [Tutorials](RoboticsLanguage/Documentation/Compiler/Tutorials/README.md)
  - [Reference](RoboticsLanguage/Documentation/Compiler/Reference/README.md)


## Install

If you are a user run:
```shell
pip install .
```

If you are a developer run:
```shell
pip install -e .
```

## Examples
You can try the RoL compiler by testing the examples in the folder `RoboticsLanguage/Examples`:

```shell
rol RoboticsLanguage/Examples/helloworld.rol
```

This will create a ROS node in the folder `~/deploy`. If you have installed the catkin workspace at `~/catkin_ws` then you can supply the path to the compiler and compile and launch the node directly:

```shell
rol -p ~/catkin_ws/src/deploy/ RoboticsLanguage/Examples/helloworld.rol -c -l
```

## Docker image

You can test the robotics language using a docker environment. First make sure the Robotics Language is installed

```shell
sudo -H pip install -e .
```

Next start the docker image

```shell
rol_docker
```

You can open another shell by repeating the previous command as many times as you want.

Once in the docker, everything is configured. You can compile the example:

```shell
rol RoboticsLanguage/Examples/helloworld.rol -c
```

Make sure to source for the first time:

```shell
source ~/catkin_ws/devel/setup.bash
```

Now you are ready to launch:

```shell
rol RoboticsLanguage/Examples/helloworld.rol -l
```



## Acknowledgements

The Robotics Language is developed by Robot Care Systems B.V. (http://www.robotcaresystems.com)

***
<!--
    ROSIN acknowledgement from the ROSIN press kit
    @ https://github.com/rosin-project/press_kit
-->

<a href="http://rosin-project.eu">
  <img src="http://rosin-project.eu/wp-content/uploads/rosin_ack_logo_wide.png"
       alt="rosin_logo" height="60" >
</a>

Supported by ROSIN - ROS-Industrial Quality-Assured Robot Software Components.  
More information: <a href="http://rosin-project.eu">rosin-project.eu</a>

<img src="http://rosin-project.eu/wp-content/uploads/rosin_eu_flag.jpg"
     alt="eu_flag" height="45" align="left" >  

This project has received funding from the European Union’s Horizon 2020  
research and innovation programme under grant agreement no. 732287.
