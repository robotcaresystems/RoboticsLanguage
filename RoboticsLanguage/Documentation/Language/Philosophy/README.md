# The Robotics Language philosophy


## Overview
The Robotics Language (RoL) is an extensible **domain-specific** (or model-based) language for robotics. RoL is an abstraction on top of ROS to efficiently and quickly develop ROS applications using a mathematics-centred language. Our goal is to make writing very complex ROS ‘n’ RoL applications possible in just a few lines of highly abstracted code.

The proposed Robotics Language is based on the following set of principles and elements:

 -	The design approach for RoL is **parsimonious** and **as simple as possible**.

 - The RoL generates **c++ ROS human-readable code** for high performance in execution. All graphics are based on web technologies (the only standardised device independent document model).

 -	Emphasis on **mathematical notation**. Mathematics notation has evolved for centuries to provide very concise representations of information. The base language is designed to mimic as much as possible natural mathematics writing. Special mathematical symbols are allowed to facilitate reading. For example, an integer variable can be defined by the expression: `x ∈ ℤ`, where the special symbol `∈` can be interchanged with the word `in` or the function `element` and `ℤ` can be interchanged with the set `Integers`. Unicode is used as the default encoding. Any language construct is converted, or can be written, into a function composition form, e.g.:
`x ∈ ℤ`  is equivalent to: `element(x, Integers)`.

 -  **Time and signals**. The language provides mechanisms for naturally expressing signals. An explicit distinction between variables and signals allows to, e.g. construct signal processing pipelines, use of temporal operators, etc.

    ```coffeescript
    x ∈ signal(ℤ, rosTopic:'/some/signal') # a ROS topic
    w ∈ signal(ℤ, device:'/dev/ttyUSB0') # a serial stream
    y ∈ signal(ℤ) # a signal is an element of a function space
    z ∈ ℤ  # z is an element of the integers
    ```


 - 	**Mini-languages** enable the use of many types of mathematical notations, text-based, graphical, or other future mediums. For example, a finite state machine can be included in the description of the node using the following mini-language:

    ```coffeescript
    FiniteStateMachine
    <{
       name: machine
       start: init

       init –(initialise)-> calibrate –(rest)-> idle
       idle -(start)-> run -(stop)-> idle
       run -(fail)-> error -(reset)-> calibrate    
    }>
    ```

 -	**Event driven**. Expressions are automatically updated on a need basis. The compiler identifies the relevant signals/objects for an expression and generates the necessary code on the call-back functions. Consider the example:

    ```coffeescript
    robot_active ∈ Signals(Booleans, rosTopic:'/robot/active')
    robot_sleep  ∈ Signals(Booleans, rosTopic:'/robot/sleep')

    if(☐[0,30](¬robot_active ∧ ¬state('emergency'), robot_sleep=true)
    ```

    This compact expression translates literally to: _if it is always the case in the last 30 second interval that there is no activity and that the robot is not in emergency then it should go to sleep_. In this example the compiler identifies the signal `/robot/active` and the state `emergency` as conditions of the temporal logic "always" operator `☐` and adds the necessary code to the call-back functions of the signal and the finite state machine to check the logical condition and execute the result of the expression if needed.

 -  An **explicit separation between abstract mathematical objects and their computer representation**. When abstract objects are used the compiler has to inform the user about its internal representation. The intention is to completely eliminate ambiguity in the language. For example, an integer variable can be defined in many forms:

    ```coffeescript
    X ∈ ℤ # Abstract mathematical object. Compiler needs to decide how to represent the object
    y ∈ ℤ(bits:16) # explicit declaration of the representation of the object
    ```

    The compiler then pre-processes the Robotics Language and explicitly informs the user of the choices made by directly annotating the code (e.g. using Atom’s linter).

  - **Language localisation**. Mathematics is a universal language, but spoken language is not. The RoL provides support for language localisation so that users can program in their native language. Internally, words in different languages are converted to English tags.

    ```coffeescript
    if(x > 0, y = 1) # English
    se(x > 0, y = 1) # Portuguese
    αν(x > 0, y = 1) # Greek

    if(larger(x,0),assign(y,1)) # all previous expressions converted internally to function composition representation
    ```

 -  **Plug-ins** based language with facilities for users to easily define new plug ins and new mini-languages. Each package by definition must provide examples, documentation, testing, etc.

 -  **Multiple outputs** for the language: ROS nodes, unit testing, debugging, profiling, model checking, documentation generation, user defined outputs.

 -  A **web portal** with documentation, tutorials, examples, use cases and facilities to develop new packages and mini languages.

## Notation

The Robotics Language is in its simplest form described by function composition.

```coffeescript
node(
  print("hello world!")
)
```

Each element of the language has a function form. For example `a + b` is the same as `plus(a,b)`. In fact in RoL **everything is a function**. For example the computation `r = a + b * x + c * x^2` is written as:

```coffeescript
assign(r, plus(a, times(b, x), times(b, power(x,2))))
```

The function composition representation is in essence one to one with the internal abstract syntax tree representation.

```xml
<assign>
  <variable name="r"/>
  <plus>
    <variable name="a"/>
    <times>
      <variable name="b"/>
      <variable name="x"/>
    </times>
    <times>
      <variable name="b"/>
      <power>
        <variable name="x"/>
        <integer>2</integer>
      </power>
    </times>
  </plus>
</assign>
```

Optional argumens can be added to functions using the `:` operator:

```coffeescript
node(
  print("hello world!", level:"debug")
)
```



On top of the base function composition representation other types of operators are introduced to make the RoL more human readable.

- infix operators (`+`, `-`, `*`, `=`, `∈`, etc)
- bracket operators (`[]`, `{}`, `""`, etc)
- alternative function names (`ℤ`, `ℕ`, `ℝ`, etc)
- special forms (function definition, etc)

## Step by step example

RoL programs are meant to be as simple as possible and use as much mathematics notation as possible, within the context of unicode text. Consider a simple node that listens for an integer in topic `/fibonacci/question` and return the Fibonacci number on the topic `/fibonacci/answer`:

```coffeescript
1.   node(
2.     name:"example Fibonacci",
3.     definitions: block(
4.    
5.       # incoming and outgoing signals
6.       question ∈ Signals(ℕ, rosTopic: '/fibonacci/question', onNew: answer = Fibonacci(question)),
7.       answer ∈ Signals(ℕ, rosTopic: '/fibonacci/answer'),
8.    
9.       # Definition of a function
10.      define Fibonacci(n ∈ ℕ) -> ℕ:
11.        if(n ≡ 0 ∨ n ≡ 1,
12.            return(n),
13.            return(Fibonacci(n-1)+Fibonacci(n-2))
14.          )
15.    )
16.  )
```


RoL programs normally start with a `node`, which is a ROS node when using the `RosCpp` output. The `node` function has a few optional arguments: `name`,`definitions`, `initialise`, `finalise`.

- `name` is used to name the ROS node and package. Names can have spaces. In this example the resulting ROS node is called `example_fibonacci`.
- `definitions` is used to define variables and functions on the global scope of the node.
- `initialise` is a block of code that runs before the ros spin cycle starts
- `finalise` is a block of code that runs after the ros spin cycle ends


```coffeescript
1.   node(
2.     name:"example Fibonacci",
3.     definitions: block(
```

Variables can be defined using the `∈` operator. Alternatively, the word `in` can be used. In this example a variable is defined to be a signal of the type os natural numbers (`ℕ`). An optional `rosTopic` argument connects this signal to a ROS topic. The option `onNew` will execute code when new data arrives in the topic. Here the signal `answer` is given the result of the Fibonacci number calculation.


```coffeescript
6.       question ∈ Signals(ℕ, rosTopic: '/fibonacci/question', onNew: answer = Fibonacci(question)),
```

This defines a variable of the type natural numbers, and connects it to a ROS topic. Note that the assignment `answer = Fibonacci(question)` will automatically publish the `answer` variable.

```coffeescript
7.       answer ∈ Signals(ℕ, rosTopic: '/fibonacci/answer'),
```

Here the function `Fibonacci` is defined. Note that input and output types are required.

```coffeescript
10.      define Fibonacci(n ∈ ℕ) -> ℕ:
11.        if(n ≡ 0 ∨ n ≡ 1,
12.            return(n),
13.            return(Fibonacci(n-1)+Fibonacci(n-2))
14.          )
```

## More information

- [Tutorials](../Tutorials/README.md)
- [Language reference](../Reference/README.md)
- [Mini-languages](../Minilanguages/README.md)
