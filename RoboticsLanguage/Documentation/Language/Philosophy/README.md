# The Robotics Language philosophy

The Robotics Language (RoL) is in its simplest form described by function composition.

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


On top of the base function composition representation other types of operators are introduced to make the RoL more human readable.

- infix operators (`+`, `-`, `*`, `=`, `:`, `∈`, etc)
- bracket operators (`[]`, `{}`, `""`, etc)
- alternative function names (`ℤ`, `ℕ`, `ℝ`, etc)
- special forms (function definition, etc)

RoL programs are written to resemble hand-written mathematics as much as possible, within the limitations of unicode text:

```coffeescript
node(
  name:"example Fibonacci",
  definitions: block(

    # incoming and outgoing signals
    question ∈ Signals(ℕ, rosTopic: '/fibonacci/question', onNew: answer = Fibonacci(question)),
    answer ∈ Signals(ℕ, rosTopic: '/fibonacci/answer'),

    # Definition of a function
    define Fibonacci(n ∈ ℕ) -> ℕ:
      if(n ≡ 0 ∨ n ≡ 1,
          return(n),
          return(Fibonacci(n-1)+Fibonacci(n-2))
        )
  )
)
```
