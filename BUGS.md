# The Robotics Language BUGS

## RoL parser

### Strings are not HTML safe

The code wii return an error:

```coffeescript
print('x > 1')
```


###  Issue with parsing real numbers in scientific notation. Conflicting with negation operator:

Parsing: `-1.3e-44` results in:

```xml
<negate p="32">
      <real p="32">1.3e-44</real>
</negate>
```    


Parsing: `- 1.3 e - 44` results in:

```xml
<negate p="29">
  <real p="29">1.3</real>
</negate>
<minus p="36">
  <variable p="31">e</variable>
  <integer p="36">44</integer>
</minus>
```



###  In the command line if two files are repeated a message is displayed

```bash
rol helloworld.rol helloworld.rol
```

```
WARNING: the following files are disregarded:
/Users/glopes/Projects/RoboticsLanguage/Examples/helloworld.rol
```


### if first element of the custom vector is '' it does not work
In the custom language operator definition the first parameter cannot be ''. This works:

```python
'functionDefinition': {
    'input': {
        'RoL': {
            'custom': ['define', ':','->',',','->', '']
        }
    },
 ...
```
An so a function can be defined in RoL by:
```
define f:R -> R,
         x -> x+1
```

This does not work:

```python
'functionDefinition': {
    'input': {
        'RoL': {
            'custom': ['', ':','->',',','->', '']
        }
    },
 ...
```
```
f:R -> R,
  x -> x+1
```


# Performance issues

## caching

The function `cache` can store static elements in a file saved at `~/.ros/cache`. If the cache exists it loads the `data` from a file. Otherwise, it uses the function `functionThatCreatesData` to generate the data online:

```python
data =  cache('name', functionThatCreatesData )
```
## RoL parser

the RoL parser currently works by generating the composition of
strings of text (see functions `xml` and `xmlInfix`) that are eventually parsed into XML.
This makes the implementation simple but my incur some performance issues when mini languages
are used. Mini languages return XML objects that are converted to text to integrate into the language.
When this parser returns the result is converts everything into an XML object, which means that the mini
language code is converted to xml text and then back to XML objects, thus waisting CPU time. If performance
become critical in the future this should be addressed.
