# Robotics Language language reference



## Index of keywords


- Outputs
  
  - RosCpp

    [arguments](#arguments), [block](#block), [boolean](#boolean), [content](#content), [cycle](#cycle), [function](#function), [functionDefinition](#functiondefinition), [integer](#integer), [natural](#natural), [print](#print), [real](#real), [return](#return), [returns](#returns), [string](#string), [Strings](#strings), [variable](#variable)
  

- Transformers
  
  - TemporalLogic

    [always](#always), [eventually](#eventually)
  
  - Base

    [anything](#anything), [defineFunction](#definefunction), [Event](#event), [events](#events), [if](#if), [node](#node), [option](#option), [Signals](#signals), [Time](#time)
  
  - LinearAlgebra

    [and](#and), [assign](#assign), [divide](#divide), [equal](#equal), [larger](#larger), [largerEqual](#largerequal), [minus](#minus), [negative](#negative), [notEqual](#notequal), [or](#or), [plus](#plus), [positive](#positive), [smaller](#smaller), [smallerEqual](#smallerequal), [times](#times)
  

- Inputs
  
  - RoL

    [associativeArray](#associativearray), [Booleans](#booleans), [element](#element), [Integers](#integers), [Naturals](#naturals), [Reals](#reals), [set](#set), [vector](#vector)
  







# Outputs, RosCpp



## arguments














Definition:

`arguments` ( `anything` ) -> `nothing`









Alternative notations

notation | example code
--|--
functional | `arguments()`
xml | `<arguments> </arguments>`






&#x274C; Missing:


 - definition: optional arguments 

 - documentation: title 
 - documentation: description 
 - documentation: usage 
 - documentation: localisation 


## block














Definition:

`block` ( `anything` ) -> `code block`









Alternative notations

notation | example code
--|--
functional | `block()`
xml | `<block> </block>`


Localisation available for:

language | keyword
--|--




&#x274C; Missing:


 - definition: optional arguments 

 - documentation: title 
 - documentation: description 
 - documentation: usage 



## boolean
















Alternative notations

notation | example code
--|--
functional | `boolean()`
xml | `<boolean> </boolean>`


Localisation available for:

language | keyword
--|--




&#x274C; Missing:

 - definition: argument types 
 - definition: optional arguments 
 - definition: return type 
 - documentation: title 
 - documentation: description 
 - documentation: usage 



## content














Definition:

`content` ( `anything` ) -> `nothing`









Alternative notations

notation | example code
--|--
functional | `content()`
xml | `<content> </content>`






&#x274C; Missing:


 - definition: optional arguments 

 - documentation: title 
 - documentation: description 
 - documentation: usage 
 - documentation: localisation 


## cycle
















Alternative notations

notation | example code
--|--
functional | `cycle()`
xml | `<cycle> </cycle>`


Localisation available for:

language | keyword
--|--
pt | repetir




&#x274C; Missing:

 - definition: argument types 
 - definition: optional arguments 
 - definition: return type 
 - documentation: title 
 - documentation: description 
 - documentation: usage 



## function














Definition:

`function` ( `anything` ) -> `nothing`









Alternative notations

notation | example code
--|--
functional | `function()`
xml | `<function> </function>`






&#x274C; Missing:


 - definition: optional arguments 

 - documentation: title 
 - documentation: description 
 - documentation: usage 
 - documentation: localisation 


## functionDefinition














Definition:

`functionDefinition` ( `anything` ) -> `nothing`









Alternative notations

notation | example code
--|--
functional | `functionDefinition()`
xml | `<functionDefinition> </functionDefinition>`






&#x274C; Missing:


 - definition: optional arguments 

 - documentation: title 
 - documentation: description 
 - documentation: usage 
 - documentation: localisation 


## integer
















Alternative notations

notation | example code
--|--
functional | `integer()`
xml | `<integer> </integer>`


Localisation available for:

language | keyword
--|--
pt | inteiro




&#x274C; Missing:

 - definition: argument types 
 - definition: optional arguments 
 - definition: return type 
 - documentation: title 
 - documentation: description 
 - documentation: usage 



## natural
















Alternative notations

notation | example code
--|--
functional | `natural()`
xml | `<natural> </natural>`


Localisation available for:

language | keyword
--|--
pt | natural




&#x274C; Missing:

 - definition: argument types 
 - definition: optional arguments 
 - definition: return type 
 - documentation: title 
 - documentation: description 
 - documentation: usage 



## print














Definition:

`print` ( `string , ... , string` ) -> `nothing`






Optional parameters:

name | type
--|--
`level` | `string`




Alternative notations

notation | example code
--|--
functional | `print()`
xml | `<print> </print>`


Localisation available for:

language | keyword
--|--
el | εκτύπωσε
nl | afdrukken
pt | imprimir




&#x274C; Missing:




 - documentation: title 
 - documentation: description 
 - documentation: usage 



## real
















Alternative notations

notation | example code
--|--
functional | `real()`
xml | `<real> </real>`


Localisation available for:

language | keyword
--|--
pt | real




&#x274C; Missing:

 - definition: argument types 
 - definition: optional arguments 
 - definition: return type 
 - documentation: title 
 - documentation: description 
 - documentation: usage 



## return














Definition:

`return` ( `anything` ) -> `nothing`









Alternative notations

notation | example code
--|--
functional | `return()`
xml | `<return> </return>`


Localisation available for:

language | keyword
--|--




&#x274C; Missing:


 - definition: optional arguments 

 - documentation: title 
 - documentation: description 
 - documentation: usage 



## returns














Definition:

`returns` ( `anything` ) -> `nothing`









Alternative notations

notation | example code
--|--
functional | `returns()`
xml | `<returns> </returns>`






&#x274C; Missing:


 - definition: optional arguments 

 - documentation: title 
 - documentation: description 
 - documentation: usage 
 - documentation: localisation 


## string
















Alternative notations

notation | example code
--|--
functional | `string()`
xml | `<string> </string>`


Localisation available for:

language | keyword
--|--
pt | texto




&#x274C; Missing:

 - definition: argument types 
 - definition: optional arguments 
 - definition: return type 
 - documentation: title 
 - documentation: description 
 - documentation: usage 



## Strings














Definition:

`Strings` ( `anything` ) -> `nothing`









Alternative notations

notation | example code
--|--
functional | `Strings()`
xml | `<Strings> </Strings>`


Localisation available for:

language | keyword
--|--
pt | texto




&#x274C; Missing:


 - definition: optional arguments 

 - documentation: title 
 - documentation: description 
 - documentation: usage 



## variable














Definition:

`variable` ( `anything` ) -> `nothing`









Alternative notations

notation | example code
--|--
functional | `variable()`
xml | `<variable> </variable>`


Localisation available for:

language | keyword
--|--
pt | variável




&#x274C; Missing:


 - definition: optional arguments 

 - documentation: title 
 - documentation: description 
 - documentation: usage 






# Transformers, TemporalLogic



## always
















Alternative notations

notation | example code
--|--
functional | `always()`
xml | `<always> </always>`


Localisation available for:

language | keyword
--|--
pt | sempre




&#x274C; Missing:

 - definition: argument types 
 - definition: optional arguments 
 - definition: return type 
 - documentation: title 
 - documentation: description 
 - documentation: usage 



## eventually
















Alternative notations

notation | example code
--|--
functional | `eventually()`
xml | `<eventually> </eventually>`


Localisation available for:

language | keyword
--|--
pt | eventualmente




&#x274C; Missing:

 - definition: argument types 
 - definition: optional arguments 
 - definition: return type 
 - documentation: title 
 - documentation: description 
 - documentation: usage 




# Transformers, Base



## anything














Definition:

`anything` ( `anything` ) -> `nothing`









Alternative notations

notation | example code
--|--
functional | `anything()`
xml | `<anything> </anything>`


Localisation available for:

language | keyword
--|--




&#x274C; Missing:


 - definition: optional arguments 

 - documentation: title 
 - documentation: description 
 - documentation: usage 



## defineFunction














Definition:

`defineFunction` ( `anything` ) -> `nothing`









Alternative notations

notation | example code
--|--
functional | `defineFunction()`
xml | `<defineFunction> </defineFunction>`


Localisation available for:

language | keyword
--|--




&#x274C; Missing:


 - definition: optional arguments 

 - documentation: title 
 - documentation: description 
 - documentation: usage 



## Event
















Alternative notations

notation | example code
--|--
functional | `Event()`
xml | `<Event> </Event>`


Localisation available for:

language | keyword
--|--
pt | eventos




&#x274C; Missing:

 - definition: argument types 
 - definition: optional arguments 
 - definition: return type 
 - documentation: title 
 - documentation: description 
 - documentation: usage 



## events
















Alternative notations

notation | example code
--|--
functional | `events()`
xml | `<events> </events>`


Localisation available for:

language | keyword
--|--
pt | eventos




&#x274C; Missing:

 - definition: argument types 
 - definition: optional arguments 
 - definition: return type 
 - documentation: title 
 - documentation: description 
 - documentation: usage 



## if
















Alternative notations

notation | example code
--|--
functional | `if()`
xml | `<if> </if>`


Localisation available for:

language | keyword
--|--
pt | se




&#x274C; Missing:

 - definition: argument types 
 - definition: optional arguments 
 - definition: return type 
 - documentation: title 
 - documentation: description 
 - documentation: usage 



## node






**The main software node**



 This is the main RoL node. Definitions, initialisation, events, etc., are defined here.



 Usage:
```coffeescript
node(
  name:"hello world",
  initialise(print("hello world"))
)
```





Definition:

`node` ( `anything` ) -> `nothing`






Optional parameters:

name | type
--|--
`definitions` | `anything`
`rate` | `real`
`initialise` | `anything`
`name` | `string`
`finalise` | `anything`




Alternative notations

notation | example code
--|--
functional | `node()`
xml | `<node> </node>`


Localisation available for:

language | keyword
--|--
el | κόμβος
pt | nó













## option
















Alternative notations

notation | example code
--|--
functional | `option()`
xml | `<option> </option>`


Localisation available for:

language | keyword
--|--
pt | parâmetro




&#x274C; Missing:

 - definition: argument types 
 - definition: optional arguments 
 - definition: return type 
 - documentation: title 
 - documentation: description 
 - documentation: usage 



## Signals






**A time or event based signal**



 Defines a signal type.



 Usage:
```coffeescript
x in Signals(Reals,rostopic:'/test/signal')
```





Definition:

`Signals` ( `anything` ) -> `nothing`






Optional parameters:

name | type
--|--
`onNew` | `block`
`onChange` | `block`
`flow` | `string`
`rosTopic` | `string`




Alternative notations

notation | example code
--|--
functional | `Signals()`
xml | `<Signals> </Signals>`


Localisation available for:

language | keyword
--|--
pt | sinal













## Time
















Alternative notations

notation | example code
--|--
functional | `Time()`
xml | `<Time> </Time>`


Localisation available for:

language | keyword
--|--
pt | eventos




&#x274C; Missing:

 - definition: argument types 
 - definition: optional arguments 
 - definition: return type 
 - documentation: title 
 - documentation: description 
 - documentation: usage 




# Transformers, LinearAlgebra



## and






**Logical `and` operator**



 Is the logical AND function. It evaluates its arguments in order, giving False immediately if any of them are False, and True if they are all True. 



 Usage:
```coffeescript
a = b and c
```





Definition:

`and` ( `boolean` ) -> `boolean`









Alternative notations

notation | example code
--|--
infix | `type` `{'flat': True, 'order': 600, 'key': ['and', '\xe2\x88\xa7']}` `type`
functional | `and()`
xml | `<and> </and>`


Localisation available for:

language | keyword
--|--
pt | e




&#x274C; Missing:


 - definition: optional arguments 







## assign














Definition:

`assign` ( `anything` ) -> `nothing`









Alternative notations

notation | example code
--|--
infix | `type` `{'order': 100, 'key': '='}` `type`
functional | `assign()`
xml | `<assign> </assign>`


Localisation available for:

language | keyword
--|--
pt | atribuir




&#x274C; Missing:


 - definition: optional arguments 

 - documentation: title 
 - documentation: description 
 - documentation: usage 



## divide














Definition:

`divide` ( `number` ) -> `None`









Alternative notations

notation | example code
--|--
infix | `type` `{'flat': True, 'order': 1200, 'key': '/'}` `type`
functional | `divide()`
xml | `<divide> </divide>`


Localisation available for:

language | keyword
--|--
pt | dividir




&#x274C; Missing:


 - definition: optional arguments 

 - documentation: title 
 - documentation: description 
 - documentation: usage 



## equal














Definition:

`equal` ( `number or string or boolean` ) -> `boolean`









Alternative notations

notation | example code
--|--
infix | `type` `{'order': 700, 'key': ['==', '\xe2\x89\xa1']}` `type`
functional | `equal()`
xml | `<equal> </equal>`


Localisation available for:

language | keyword
--|--
pt | igual




&#x274C; Missing:


 - definition: optional arguments 

 - documentation: title 
 - documentation: description 
 - documentation: usage 



## larger














Definition:

`larger` ( `number` ) -> `boolean`









Alternative notations

notation | example code
--|--
infix | `type` `{'order': 800, 'key': '>'}` `type`
functional | `larger()`
xml | `<larger> </larger>`


Localisation available for:

language | keyword
--|--
pt | maior




&#x274C; Missing:


 - definition: optional arguments 

 - documentation: title 
 - documentation: description 
 - documentation: usage 



## largerEqual














Definition:

`largerEqual` ( `number` ) -> `boolean`









Alternative notations

notation | example code
--|--
infix | `type` `{'order': 800, 'key': ['>=', '\xe2\x89\xa5']}` `type`
functional | `largerEqual()`
xml | `<largerEqual> </largerEqual>`


Localisation available for:

language | keyword
--|--
pt | maiorIgual




&#x274C; Missing:


 - definition: optional arguments 

 - documentation: title 
 - documentation: description 
 - documentation: usage 



## minus














Definition:

`minus` ( `number` ) -> `None`









Alternative notations

notation | example code
--|--
infix | `type` `{'flat': True, 'order': 1100, 'key': '-'}` `type`
functional | `minus()`
xml | `<minus> </minus>`


Localisation available for:

language | keyword
--|--
pt | subtrair




&#x274C; Missing:


 - definition: optional arguments 

 - documentation: title 
 - documentation: description 
 - documentation: usage 



## negative






**Number negation**



 Normal number or variable negation. 



 Usage:
```coffeescript
a = -b
```





Definition:

`negative` ( `anything` ) -> `None`









Alternative notations

notation | example code
--|--
prefix | `{'order': 1300, 'key': '-'}` ( `type` )
functional | `negative()`
xml | `<negative> </negative>`


Localisation available for:

language | keyword
--|--
pt | negativo




&#x274C; Missing:


 - definition: optional arguments 







## notEqual














Definition:

`notEqual` ( `number or string or boolean` ) -> `boolean`









Alternative notations

notation | example code
--|--
infix | `type` `{'order': 700, 'key': ['!=', '\xe2\x89\xa0']}` `type`
functional | `notEqual()`
xml | `<notEqual> </notEqual>`


Localisation available for:

language | keyword
--|--
pt | diferente




&#x274C; Missing:


 - definition: optional arguments 

 - documentation: title 
 - documentation: description 
 - documentation: usage 



## or














Definition:

`or` ( `boolean` ) -> `boolean`









Alternative notations

notation | example code
--|--
functional | `or()`
xml | `<or> </or>`


Localisation available for:

language | keyword
--|--
pt | {'prefix': 'ou', 'infix': ['ou', '\xe2\x88\xa7']}




&#x274C; Missing:


 - definition: optional arguments 

 - documentation: title 
 - documentation: description 
 - documentation: usage 



## plus














Definition:

`plus` ( `number or string` ) -> `None`









Alternative notations

notation | example code
--|--
infix | `type` `{'flat': True, 'order': 1100, 'key': '+'}` `type`
functional | `plus()`
xml | `<plus> </plus>`


Localisation available for:

language | keyword
--|--
pt | adicionar




&#x274C; Missing:


 - definition: optional arguments 

 - documentation: title 
 - documentation: description 
 - documentation: usage 



## positive






**Positive sign**



 Has no effect on sign.



 Usage:
```coffeescript
a = +b
```





Definition:

`positive` ( `anything` ) -> `None`









Alternative notations

notation | example code
--|--
prefix | `{'order': 1300, 'key': '+'}` ( `type` )
functional | `positive()`
xml | `<positive> </positive>`


Localisation available for:

language | keyword
--|--
pt | positivo




&#x274C; Missing:


 - definition: optional arguments 







## smaller














Definition:

`smaller` ( `number` ) -> `boolean`









Alternative notations

notation | example code
--|--
infix | `type` `{'order': 800, 'key': '<'}` `type`
functional | `smaller()`
xml | `<smaller> </smaller>`


Localisation available for:

language | keyword
--|--
pt | menor




&#x274C; Missing:


 - definition: optional arguments 

 - documentation: title 
 - documentation: description 
 - documentation: usage 



## smallerEqual














Definition:

`smallerEqual` ( `number` ) -> `boolean`









Alternative notations

notation | example code
--|--
infix | `type` `{'order': 800, 'key': ['<=', '\xe2\x89\xa4']}` `type`
functional | `smallerEqual()`
xml | `<smallerEqual> </smallerEqual>`


Localisation available for:

language | keyword
--|--
pt | menorIgual




&#x274C; Missing:


 - definition: optional arguments 

 - documentation: title 
 - documentation: description 
 - documentation: usage 



## times






**Number multiplication**



 Normal number, vector, or matrix multiplication. 



 Usage:
```coffeescript
a = 2*3
```





Definition:

`times` ( `number` ) -> `None`









Alternative notations

notation | example code
--|--
infix | `type` `{'flat': True, 'order': 1200, 'key': '*'}` `type`
functional | `times()`
xml | `<times> </times>`


Localisation available for:

language | keyword
--|--
pt | multiplicar




&#x274C; Missing:


 - definition: optional arguments 










# Inputs, RoL



## associativeArray






**Set**



 A set of values



 Usage:
```coffeescript
a = { b, c ,d }
```







Alternative notations

notation | example code
--|--
functional | `associativeArray()`
xml | `<associativeArray> </associativeArray>`


Localisation available for:

language | keyword
--|--




&#x274C; Missing:

 - definition: argument types 
 - definition: optional arguments 
 - definition: return type 






## Booleans














Definition:

`Booleans` ( `anything` ) -> `nothing`









Alternative notations

notation | example code
--|--
functional | `Booleans()`
xml | `<Booleans> </Booleans>`


Localisation available for:

language | keyword
--|--
pt | boleano




&#x274C; Missing:


 - definition: optional arguments 

 - documentation: title 
 - documentation: description 
 - documentation: usage 



## element






**Element of a set of type**



 Defines a variable to be an element of a set or a type. If a set is provided, then the variable takes the type of the elements of the set



 Usage:
```coffeescript
x in Reals
```





Definition:

`element` ( `anything` ) -> `nothing`









Alternative notations

notation | example code
--|--
infix | `type` `{'order': 150, 'key': ['in', '\xe2\x88\x88']}` `type`
functional | `element()`
xml | `<element> </element>`


Localisation available for:

language | keyword
--|--
pt | elemento




&#x274C; Missing:


 - definition: optional arguments 







## Integers






**Integer numbers type**



 A type representing integer numbers. Assumptions on the number of bits used by the compiler to represent an integer number is given as information in the editor.



 Usage:
```coffeescript
x in Integers
```





Definition:

`Integers` ( `anything` ) -> `nothing`






Optional parameters:

name | type
--|--
`bits` | `integer`




Alternative notations

notation | example code
--|--
functional | `Integers()`
xml | `<Integers> </Integers>`


Localisation available for:

language | keyword
--|--
pt | inteiro













## Naturals






**Natural numbers type**



 A type representing natural numbers. Assumptions on the number of bits used by the compiler to represent an natural number is given as information in the editor.



 Usage:
```coffeescript
x in Naturals
```





Definition:

`Naturals` ( `anything` ) -> `nothing`






Optional parameters:

name | type
--|--
`bits` | `natural`




Alternative notations

notation | example code
--|--
functional | `Naturals()`
xml | `<Naturals> </Naturals>`


Localisation available for:

language | keyword
--|--
pt | natural













## Reals






**Real numbers type**



 A type representing real numbers. Assumptions on the number of bits used by the compiler to represent a real number is given as information in the editor.



 Usage:
```coffeescript
x in Reals
```





Definition:

`Reals` ( `anything` ) -> `nothing`






Optional parameters:

name | type
--|--
`bits` | `integer`




Alternative notations

notation | example code
--|--
functional | `Reals()`
xml | `<Reals> </Reals>`


Localisation available for:

language | keyword
--|--
pt | real













## set
















Alternative notations

notation | example code
--|--
functional | `set()`
xml | `<set> </set>`


Localisation available for:

language | keyword
--|--
pt | conjunto




&#x274C; Missing:

 - definition: argument types 
 - definition: optional arguments 
 - definition: return type 
 - documentation: title 
 - documentation: description 
 - documentation: usage 



## vector
















Alternative notations

notation | example code
--|--
functional | `vector()`
xml | `<vector> </vector>`


Localisation available for:

language | keyword
--|--
pt | vector




&#x274C; Missing:

 - definition: argument types 
 - definition: optional arguments 
 - definition: return type 
 - documentation: title 
 - documentation: description 
 - documentation: usage 









# Outputs matrix


keyword | RoL | RosCpp | HTMLDocumentation | RoLXML | HTMLGUI | Developer 
--|--|--|--|--|--|--
always | &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;
and | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x2714;| &#x26A0;
anything | &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;
arguments | &#x26A0;| &#x2714;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;
assign | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x2714;| &#x26A0;
associativeArray | &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;
block | &#x26A0;| &#x2714;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;
boolean | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x2714;| &#x26A0;
Booleans | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x2714;| &#x26A0;
content | &#x26A0;| &#x2714;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;
cycle | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x2714;| &#x26A0;
defineFunction | &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;
divide | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x26A0;| &#x26A0;
element | &#x26A0;| &#x2714;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;
equal | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x2714;| &#x26A0;
Event | &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;
events | &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;
eventually | &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;
function | &#x26A0;| &#x2714;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;
functionDefinition | &#x26A0;| &#x2714;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;
if | &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;
integer | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x2714;| &#x26A0;
Integers | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x2714;| &#x26A0;
larger | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x2714;| &#x26A0;
largerEqual | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x2714;| &#x26A0;
minus | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x2714;| &#x26A0;
natural | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x2714;| &#x26A0;
Naturals | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x2714;| &#x26A0;
negative | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x26A0;| &#x26A0;
node | &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;
notEqual | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x2714;| &#x26A0;
option | &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;
or | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x2714;| &#x26A0;
plus | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x2714;| &#x26A0;
positive | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x26A0;| &#x26A0;
print | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x2714;| &#x26A0;
real | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x2714;| &#x26A0;
Reals | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x2714;| &#x26A0;
return | &#x26A0;| &#x2714;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;
returns | &#x26A0;| &#x2714;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;
set | &#x26A0;| &#x2714;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;
Signals | &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;
smaller | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x2714;| &#x26A0;
smallerEqual | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x2714;| &#x26A0;
string | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x2714;| &#x26A0;
Strings | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x2714;| &#x26A0;
Time | &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;
times | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x26A0;| &#x26A0;
variable | &#x2714;| &#x2714;| &#x2714;| &#x26A0;| &#x2714;| &#x26A0;
vector | &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;| &#x26A0;