# Finite State Machines tutorial - 2. Searching the abstract syntax tree and generating code elements

The abstract syntax tree of a segment of code should provide the necessary information to generate executable text code. Some of the information can be used for **semantic checking**, while other elements can be used to **bootstrap/infer** new information, i.e. *refine* abstract concepts. For example, in ROS it is not necessary to state if a topic is a publisher or a subscriber. By analysing the usage of the topic in the code it is possible to infer its signal type. In practice one needs to **search** and **annotate** the abstract syntax tree. This is mostly accomplished using the `xpath` syntax ([definition](https://www.w3.org/TR/xpath/all/), [examples](https://www.w3schools.com/xml/xml_xpath.asp), [xpath in python](https://lxml.de/xpathxslt.html)).

In the first part of this tutorial we perform semantic checking by looking for repeated transitions for a state. The assumption being that this package implements deterministic finite state machines.
In the second part we inject c++ code that implements the finite state machine.

## Creating a new transformer

Start by creating a new transformer:

```bash
rol --create-transformer-template "My Finite State Machine"
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
rol ~/.rol/plugins/Transformers/MyFiniteStateMachine/Examples/MyFiniteStateMachine.rol -v info
```

Note: sometimes when editing plugins it is useful to use the flag `--remove-cache`. This cleans `rol`s cache, to make sure the most updated code is running:

```bash
rol --remove-cache
```


To make sure your new package is installed type:

```bash
rol --info
```

```
The Robotics Language version: 0.3
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
<node p="174">
  <option p="37" name="name">
    <string p="37">my finite state machine</string>
  </option>
  <option p="173" name="definitions">
    <mfsm:machine xmlns:mfsm="mfsm">
      <mfsm:name>test</mfsm:name>
      <mfsm:initial>idle</mfsm:initial>
      <mfsm:transition name="start">
        <mfsm:state>idle</mfsm:state>
        <mfsm:state>walk</mfsm:state>
      </mfsm:transition>
      <mfsm:transition name="start">
        <mfsm:state>idle</mfsm:state>
        <mfsm:state>run</mfsm:state>
      </mfsm:transition>
    </mfsm:machine>
  </option>
</node>
```


Note that this XML representation is using a namespace `mfsm` to isolate the tags from other packages. This renders the `xpath` queries slightly more complex, but still manageable.

First look globally for each machine using xpath:

```xpath
//mfsm:machine
```

Next, for each machine look for each **local** transition (notice the `.//` at the begining of the xpath expression):

```xpath
.//mfsm:transition
```

Now we want to get the names of the start state and the name of the transition elements for each transition. This can be done using the following python expression:

```python
pair = [transition.getchildren()[0].text, transition.attrib['name']]
```


We can write the `transform` function in `Transform.py`:

```python
def transform(code, parameters):

  # define the namespace used by the finite state machine package
  namespace = {'namespaces': {'mfsm': 'mfsm'}}

  # look for all machines
  for machine in code.xpath('//mfsm:machine', **namespace):

    # a buffer to store pairs of state/transition names
    pairs = []

    # look for all transitions in a machine
    for transition in machine.xpath('.//mfsm:transition', **namespace):

      # extract state/transition pair
      pair = [transition.getchildren()[0].text, transition.attrib['name']]

      # check if pairs already exist
      if pair in pairs:
        print('Error: repeated transitions in FSM "{}": ({}) -{}-> ... '.format(
            machine.xpath('.//mfsm:name/text()', **namespace)[0], *pair))
      else:
        pairs.append(pair)

  return code, parameters
```

In the previous example a simple error message is printed. This behaviour can be improved by creating an [error handling function]().

## Generating code using Templates

When creating a new transformer package `rol` traverses all the output template files looking for special tags. For example the file [`RoboticsLanguage/Outputs/RosCpp/Templates/_nodename_/src/_nodename_.cpp`](https://github.com/robotcaresystems/RoboticsLanguage/blob/development/RoboticsLanguage/Outputs/RosCpp/Templates/_nodename_/src/_nodename_.cpp.template) contains special tags as `<<<'initialise'|group>>>` or `<<<'functions'|group>>>`. These tags represent locations where transformers can inject code. After creating the transformer plugin the file `~/.rol/plugins/Transformers/MyFiniteStateMachine/Templates/Outputs/RosCpp/_nodename_/src/_nodename_.cpp.template` is created with the contents:

```jinja

...

{% set initialise %}

{% endset %}

...

{% set functions %}

{% endset %}

...
```

By modifying these files on can inject code into the source files generated by the outputs. For more information please read the [Template Engine]() documentation. The templates use the [jinja2](http://jinja.pocoo.org) library, please make sure to read the [documentation](http://jinja.pocoo.org/docs/).

We start by editing the template file header file for the node: `~/.rol/plugins/Transformers/MyFiniteStateMachine/Templates/Outputs/RosCpp/_nodename_/include/_nodename_/_nodename_.h.template`

We assume we have a C++ finite state library that implements the machinery required for finite state machines. See e.g. [FiniteStateMachine.hpp](https://github.com/robotcaresystems/RoboticsLanguage/blob/development/RoboticsLanguage/Transformers/FiniteStateMachine/Templates/Outputs/RosCpp/_nodename_/include/_nodename_/FiniteStateMachine.hpp)

In this file we:
 - Include the header file for `FiniteStateMachine.hpp`
 - Instantiate the `FiniteStateMachine` class for each machine found on the code.

```jinja
{% set includes %}

{% if code|xpaths('//mfsm:machine', {'mfsm':'mfsm'})|length > 0 %}
//Finite state machine library
#include "FiniteStateMachine.hpp"
{% endif %}

{% endset %}



{% set definitions %}

{% for machine in code|xpaths('//mfsm:machine', {'mfsm':'mfsm'}) %}
  {% set machine_name = machine|xpath('mfsm:name/text()', {'mfsm':'mfsm'}) %}

  FiniteStateMachine {{machine_name}} = FiniteStateMachine("{{machine_name}}");

{% endfor %}

{% endset %}
```

Inside the `{% set includes %}` group we search the abstract syntax tree for definitions of finite state machines using the `xpath` query `//mfsm:machine`. If found then include the header file `FiniteStateMachine.h`

Inside the `{% set definitions %}` group we search for all machines, and for each one get the name using `mfsm:name/text()`. Then instantiate the class using the name. Using the examples above:

```xml
<mfsm:machine xmlns:mfsm="mfsm">
   <mfsm:name>machine</mfsm:name>
...
</mfsm:machine>
```

generates the elements of c++ code in the header file:

```cpp
//Finite state machine library
#include "FiniteStateMachine.hpp"

...

  FiniteStateMachine machine = FiniteStateMachine("machine");

...
```

Now that the header file definitions are established we initialise the class in the file `~/.rol/plugins/Transformers/MyFiniteStateMachine/Templates/Outputs/RosCpp/_nodename_/src/_nodename_.cpp.template`.





```jinja
{% set initialise %}

{% for machine in code|xpaths('//mfsm:machine', {'mfsm':'mfsm'}) -%}
  {% set machine_name = machine|xpath('mfsm:name/text()', {'mfsm':'mfsm'})-%}

    //////////////////////////////////////////////////////////
    // Definitions for Finite State Machine "{{machine_name}}"

    // Transitions
  {% for transition in machine|xpaths('.//mfsm:transition', {'mfsm':'mfsm'}) -%}
    {{machine_name}}.addTransition("{{transition|attribute('name')}}",
                                   "{{transition.getchildren()[0]|text}}",
                                   "{{transition.getchildren()[1]|text}}");
  {% endfor -%}

    // Initial state
    {{machine_name}}.setInitialState("{{machine|xpath('mfsm:initial/text()', {'mfsm':'mfsm'})}}");

{% endfor -%}

{% endset %}
```

In the template above, for each machine `//mfsm:machine` iterate over the transitions `mfsm:transitions/mfsm:transition`.


The example

```xml
<node p="174">
  <option p="37" name="name">
    <string p="37">my finite state machine</string>
  </option>
  <option p="173" name="definitions">
    <mfsm:machine xmlns:mfsm="mfsm">
      <mfsm:name>machine</mfsm:name>
      <mfsm:initial>idle</mfsm:initial>
      <mfsm:transition name="start">
        <mfsm:state>idle</mfsm:state>
        <mfsm:state>running</mfsm:state>
      </mfsm:transition>
      <mfsm:transition name="stop">
        <mfsm:state>running</mfsm:state>
        <mfsm:state>idle</mfsm:state>
      </mfsm:transition>
    </mfsm:machine>
  </option>
</node>
```

results in the c++ code element:

```cpp
//////////////////////////////////////////////////////////
// Definitions for Finite State Machine "machine"

// Transitions
machine.addTransition("start","idle","running");
machine.addTransition("stop","running","idle");

// Initial state
machine.setInitialState("idle");
```

## Language definition for abstract syntax tree

The final step in creating the transformer is defining the language keywords for this package so that type checker can analyse the code on the abstract syntax tree. For this we can add the following text to the file `~/.rol/plugins/Transformers/MyFiniteStateMachine/Language.py`

```python
language = {
    '{mfsm}machine': {},
    '{mfsm}name': {},
    '{mfsm}initial': {},
    '{mfsm}transitions': {},
    '{mfsm}transition': {},
    '{mfsm}label': {},
    '{mfsm}begin': {},
    '{mfsm}end': {}
}
```

With the previous text the type checker with not validate and will always pass. See [Type Checking]() for more information on creating languages with rules.
