# The Robotics Language compiler tutorials

## Command line examples


Show the command line help
```shell
rol -h
```

Show information about installed packages
```shell
rol --info
```

Show information about a specific package
```shell
rol --info-packages ROS
```

Removes the copiler cache. Very useful when developping plugins, or when something does not work as expected.
```shell
rol --remove-cache
```


### Parameters

Show all parameters
```shell
rol --show-parameters
# or
rol -p
```

Show a specific parameter with known path
```shell
rol --show-parameters-path 'globals'
# or
rol -P 'globals'
```


Show a specific parameter using [dpath](https://pypi.org/project/dpath/). In this examples it looks for all language elements that have optional parameters.
```shell
rol -P 'language/*/definition/optional'
```

### Code


Show the abstract syntax tree
```shell
rol 1_hello_world.rol --show-code
# or
rol 1_hello_world.rol -x
```

Show a specific part of the abstract syntax tree. In this case, the tag `print`
```shell
rol 1_hello_world.rol --show-code-path 'print'
# or
rol 1_hello_world.rol -X 'print'
```


Show a specific part of the abstrac syntax tree using [xpath](https://www.w3schools.com/xml/xml_xpath.asp). In this example it looks for tags `variable` with attribute name `machine`.
```shell
rol 8_finite_state_machine.rol -X '//variable[@name="machine"]'
```

In this example it looks for tags `variable` with attribute name `machine`, and shows them from one level higher.
```shell
rol 8_finite_state_machine.rol -X '//variable[@name="machine"]/..'
```

### Debugging

Show debug information. You can choose from `debug`, `error`, `fatal`, `info`, `none`, `warn`
```shell
rol 1_hello_world.rol --verbose debug
# or
rol 1_hello_world.rol -v debug
```
Show code at step 5 and stop the compiler
```shell
rol 1_hello_world.rol --show-code --show-step 5 --show-stop
# or
rol 1_hello_world.rol -xs5 --show-stop
```

Skip the transformer `ROS`
```shell
rol 1_hello_world.rol --skip ROS
```

### Code parsing

Shows the Robotics Language grammar definition
```shell
rol --show-rol-grammar
```

### Code generation

Shows the Jinja2 templates that will be used for code generation
```shell
rol 1_hello_world.rol --show-intermediate-templates
```

Show the dependencies between outputs. For example `RosCpp` inherits from `Cpp`
```shell
rol --show-output-dependencies
```



### Inputs and outputs


Outputs to ROS in python and generates an HTML gui
```shell
rol 1_hello_world.rol -o RosPy HTMLGUI
```

Overides file extension detection, and loads file assuming it is in the `RoL` language format
```shell
rol 1_hello_world.txt -i RoL
```

### Execution

Compile the generated code
```shell
rol 1_hello_world.rol --compile
# or
rol 1_hello_world.rol -c
```

Beautify automatically the generated code
```shell
rol 1_hello_world.rol --beautify
# or
rol 1_hello_world.rol -b
```

Launch the node directly
```shell
rol 1_hello_world.rol --launch
# or
rol 1_hello_world.rol -l
```

In this example it beautifies the code, compiles, and launches the node
```shell
rol 1_hello_world.rol -cbl
```
### Template creation

Creates a generic input template. Sets up a simple grammar and connects to the [Parsley parser](https://github.com/pyga/parsley)
```shell
rol --create-input-template "my input template"
```

Creates a [JSON](https://www.json.org) based input parser. Converts from JSON to XML
```shell
rol --create-input-json-template "my input template"
```

Creates an XML based input parser. Directly injects XML into abstract syntax tree
```shell
rol --create-input-xml-template "my input template"
```

Creates a [YAML](https://yaml.org) based input parser. Converts from YAML to XML
```shell
rol --create-input-yaml-template "my input template"
```

Creates a transformer template. Traverses all outputs and look for tag used for code injection
```shell
rol --create-transformer-template "my transformer template"
```

Creates an output template.
```shell
rol --create-output-template "my output template"
```


### miscelaneous

Show progress while compiling
```shell
rol 1_hello_world.rol --progress
```

Shows output without colours
```shell
rol 1_hello_world.rol -x --no-colours
```

Copies a collection of examples into the current path
```shell
rol --copy-examples-here
```
