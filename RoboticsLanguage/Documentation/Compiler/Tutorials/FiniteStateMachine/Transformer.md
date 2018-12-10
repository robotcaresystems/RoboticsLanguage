# Finite State Machines tutorial - 2. Searching the abstract syntax tree and generating code

The abstract syntax tree of a piece of code should provide the necessary information to generate text code. Some of the information can be used for **semantic checking**, while other elements can be used to **bootstrap/infer** new information, i.e. *refine* abstract concepts. For example, in ROS it is not necessary to state if a topic is a publisher or a subscriber. By analysing the usage of the topic in the code it is possible to infer its signal type. In practice one needs to **search** and **annotate** the abstract syntax tree. This is mostly accomplished using the `xpath` syntax ([definition](https://www.w3.org/TR/xpath/all/), [examples](https://www.w3schools.com/xml/xml_xpath.asp), [xpath in python](https://lxml.de/xpathxslt.html)).

In the first part of this tutorial we perform semantic checking by looking for repeated transitions for a state. The assumption being that this package implements deterministic finite state machines.
In the second part we inject c++ code that implements the finite state machine.

## Creating a new transformer

Start by creating a new transformer:

```bash
rol --create-transformer-template "My Finite State Machine" -o Developer
```


`rol` should return the message `Created Transformers plugin "MyFiniteStateMachine" in folder ~/.rol/plugins/Transformers/MyFiniteStateMachine`.

You can now open the folder `~/.rol/plugins/Transformers/MyFiniteStateMachine` with your favourite editor to see its structure:

```
.
├── Documentation
│   ├── README.md
│   ├── Reference.md
│   └── Tutorials.md
├── ErrorHandling.py
├── Examples
│   └── MyFiniteStateMachine.rol
├── Language.py
├── Manifesto.py
├── Messages.py
├── Parameters.py
├── README.md
├── Transform.py
├── Tests
│   └── test_MyFiniteStateMachine.py
├── __init__.py
└── Templates
    └── ...
```

Open the file `Transform.py` and you will notice an empty function:

```python
from RoboticsLanguage.Base import Utilities

def transform(code, parameters):
  Utilities.logging.info("Transforming My Finite State Machine...")

  return code, parameters
```
We will implement this function to search and annotate the abstract syntax tree.

You can check if the new transformer is working correctly by running:

```bash
rol ~/.rol/plugins/Transformers/MyFiniteStateMachine/Examples/MyFiniteStateMachine.rol --remove-cache -v info
```

The flag `--remove-cache` is important to make `rol` find the new package. You can also type

```bash
rol --info --remove-cache
```

To make sure your package is installed:

```
The Robotics Language version: 0.2
Transformers:
  MyFiniteStateMachine (0.0.0) *
  ...
```



## Searching the Abstract Syntax Tree

Next we write a transformer that searches for each finite state machine defined in the abstract syntax tree. For each machine we look for all transition definitions. If repeated transitions with the same name and initial state are found then an error is published.

Consider the following finite state machine definition:

```
(idle)-start->(walk)
(idle)-start->(run)
```
This does not represent a deterministic finite state machine since the transition `start` can lead to two different states for the same initial state. The XML representation output by the [parser](Parser.md) is:

```xml
<fsm:machine xmlns:fsm="fsm">
   <fsm:name>machine</fsm:name>
   <fsm:initial>idle</fsm:initial>
   <fsm:transitions>
     <fsm:transition>
       <fsm:label>start</fsm:label>
       <fsm:begin>idle</fsm:begin>
       <fsm:end>walk</fsm:end>
     </fsm:transition>
     <fsm:transition>
       <fsm:label>start</fsm:label>
       <fsm:begin>idle</fsm:begin>
       <fsm:end>run</fsm:end>
     </fsm:transition>
   </fsm:transitions>
 </fsm:machine>
```


Note that this XML representation is using a namespace `fsm` to isolate the tags from other packages. This renders the `xpath` queries slightly more complex, but still manageable.

First look globally for each machine using xpath:

```xpath
//fsm:machine
```

Next, for each machine look for each **local** transition (notice the `.//` at the begining of the xpath expression):

```xpath
.//fsm:transition
```

Now we want to get the names of the `begin` and `label` elements for each transition. This can be done using the following xpath expression:

```xpath
.//*[self::fsm:begin or self::fsm:label]/text()
```

This will look for each element of the `<fsm:transition>` tag and will return the elements that match either `begin` or `label`. For the found  elements return their content using `text()`.

Now we can write the `transform` function in `Transform.py`:

```python
def transform(code, parameters):

  # define the namespace used by the finite state machine package
  namespace = {'namespaces': {'fsm': 'fsm'}}

  # look for all machines
  for machine in code.xpath('//fsm:machine', **namespace):

    # a buffer to store pairs of state/transition names
    pairs = []

    # look for all transitions in a machine
    for transition in machine.xpath('.//fsm:transition', **namespace):

      # extract state/transition pair
      pair = transition.xpath('.//*[self::fsm:begin or self::fsm:label]/text()', **namespace)

      # check if pairs already exist
      if pair in pairs:
        print('Error: repeated transitions in FSM "{}": ({}) -{}-> ... '.format(
            machine.xpath('.//fsm:name/text()', **namespace)[0], *pair))
      else:
        pairs.append(pair)

  return code, parameters

```

In the previous example a simple error message is printed. This behaviour can be improved by creating an [error handling function]().

## Generating code using Templates
