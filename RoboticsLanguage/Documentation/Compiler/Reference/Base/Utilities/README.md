<h1 id="Base.Utilities">Base.Utilities</h1>


<h2 id="Base.Utilities.xml">xml</h2>

```python
xml(tag, content, position=0)
```
creates XML text for entry
<h2 id="Base.Utilities.xmlVariable">xmlVariable</h2>

```python
xmlVariable(parameters, name, position=0)
```
creates XML for variables
<h2 id="Base.Utilities.fillDefaultsInOptionalArguments">fillDefaultsInOptionalArguments</h2>

```python
fillDefaultsInOptionalArguments(code, parameters)
```
Fill in defaults in optional arguments in case they are not explicitely defined.
<h2 id="Base.Utilities.xmlFunction">xmlFunction</h2>

```python
xmlFunction(parameters, tag, content, position=0)
```
creates XML for functions
<h2 id="Base.Utilities.xmlMiniLanguage">xmlMiniLanguage</h2>

```python
xmlMiniLanguage(parameters, key, text, position)
```
Calls a different parser to process inline mini languages
<h2 id="Base.Utilities.xmlAttributes">xmlAttributes</h2>

```python
xmlAttributes(tag, content, position=0, attributes={})
```
creates XML text for entry with attributes
