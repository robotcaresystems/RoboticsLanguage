# Robotics Language reference



## and

<table border="1">


<tr><td>Infix notation: </td>
<td><p>

<pre><span style="color:gray">type</span> and <span style="color:gray">type</span></pre><br>

<pre><span style="color:gray">type</span> ∧ <span style="color:gray">type</span></pre><br>

</p></td></tr>










<tr><td>
Function notation:
</td><td>
<pre>and()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;and&gt; &lt;/and&gt;</pre>
</td></tr>
</table>

 **Boolean and operator**

  Boolean and operator ...

  ```
  a = b and c
  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> {'prefix': 'e', 'infix': ['e', '\xe2\x88\xa7']} </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## function

<table border="1">











<tr><td>
Function notation:
</td><td>
<pre>function()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;function&gt; &lt;/function&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```




  <span style="color:red">Missing:</span>



   - localisation




## smaller

<table border="1">


<tr><td>Infix notation: </td>
<td><p>

<pre><span style="color:gray">type</span> < <span style="color:gray">type</span></pre><br>

</p></td></tr>










<tr><td>
Function notation:
</td><td>
<pre>smaller()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;smaller&gt; &lt;/smaller&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> menor </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## divide

<table border="1">


<tr><td>Infix notation: </td>
<td><p>

<pre><span style="color:gray">type</span> / <span style="color:gray">type</span></pre><br>

</p></td></tr>










<tr><td>
Function notation:
</td><td>
<pre>divide()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;divide&gt; &lt;/divide&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> dividir </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## eventually

<table border="1">











<tr><td>
Function notation:
</td><td>
<pre>eventually()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;eventually&gt; &lt;/eventually&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> eventualmente </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## Signals

<table border="1">











<tr><td>
Function notation:
</td><td>
<pre>Signals()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;Signals&gt; &lt;/Signals&gt;</pre>
</td></tr>
</table>

 **A time or event based signal**

  Defines a signal type.

  ```
  x in Signals(Reals,rostopic:'/test/signal')
  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> sinal </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## set

<table border="1">







<tr><td>Notation: </td></tr>





<tr><td>
Function notation:
</td><td>
<pre>set()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;set&gt; &lt;/set&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> conjunto </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## negate

<table border="1">





<tr><td>Prefix notation: </td>
<td><p>

 <pre>- ( <span style="color:gray">type</span> ) </pre><br>

</p></td></tr>







<tr><td>
Function notation:
</td><td>
<pre>negate()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;negate&gt; &lt;/negate&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> negação </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## events

<table border="1">











<tr><td>
Function notation:
</td><td>
<pre>events()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;events&gt; &lt;/events&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> eventos </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## Reals

<table border="1">





<tr><td>Prefix notation: </td>
<td><p>

 <pre>Reals ( <span style="color:gray">type</span> ) </pre><br>

 <pre>ℝ ( <span style="color:gray">type</span> ) </pre><br>

</p></td></tr>







<tr><td>
Function notation:
</td><td>
<pre>Reals()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;Reals&gt; &lt;/Reals&gt;</pre>
</td></tr>
</table>

 **Real numbers type**

  A type representing real numbers. Assumptions on the number of bits used by the compiler to represent a real number is given as information in the editor.

  ```
  x in Reals
  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> real </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## times

<table border="1">


<tr><td>Infix notation: </td>
<td><p>

<pre><span style="color:gray">type</span> * <span style="color:gray">type</span></pre><br>

</p></td></tr>










<tr><td>
Function notation:
</td><td>
<pre>times()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;times&gt; &lt;/times&gt;</pre>
</td></tr>
</table>

 **Number multiplication**

  Normal number, vector, or matrix multiplication.

  ```
  a = 2*3
  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> multiplicar </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## if

<table border="1">











<tr><td>
Function notation:
</td><td>
<pre>if()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;if&gt; &lt;/if&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> se </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## smallerEqual

<table border="1">


<tr><td>Infix notation: </td>
<td><p>

<pre><span style="color:gray">type</span> <= <span style="color:gray">type</span></pre><br>

<pre><span style="color:gray">type</span> ≤ <span style="color:gray">type</span></pre><br>

</p></td></tr>










<tr><td>
Function notation:
</td><td>
<pre>smallerEqual()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;smallerEqual&gt; &lt;/smallerEqual&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> menorIgual </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## functionDefinition

<table border="1">










<tr><td>Custom notation:</td></tr>


<tr><td>
Function notation:
</td><td>
<pre>functionDefinition()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;functionDefinition&gt; &lt;/functionDefinition&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> definirFunção </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## or

<table border="1">











<tr><td>
Function notation:
</td><td>
<pre>or()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;or&gt; &lt;/or&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> {'prefix': 'ou', 'infix': ['ou', '\xe2\x88\xa7']} </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## Booleans

<table border="1">





<tr><td>Prefix notation: </td>
<td><p>

 <pre>Booleans ( <span style="color:gray">type</span> ) </pre><br>

 <pre>𝔹 ( <span style="color:gray">type</span> ) </pre><br>

</p></td></tr>







<tr><td>
Function notation:
</td><td>
<pre>Booleans()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;Booleans&gt; &lt;/Booleans&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> boleano </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## initialise

<table border="1">











<tr><td>
Function notation:
</td><td>
<pre>initialise()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;initialise&gt; &lt;/initialise&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>el </td><td> αρχικοποίηση </td></tr>

<tr><td>nl </td><td> initialiseren </td></tr>

<tr><td>pt </td><td> inicializar </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## print

<table border="1">











<tr><td>
Function notation:
</td><td>
<pre>print()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;print&gt; &lt;/print&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>el </td><td> εκτύπωσε </td></tr>

<tr><td>nl </td><td> afdrukken </td></tr>

<tr><td>pt </td><td> imprimir </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## shortComment

<table border="1">











<tr><td>
Function notation:
</td><td>
<pre>shortComment()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;shortComment&gt; &lt;/shortComment&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

  </table>



  <span style="color:red">Missing:</span>








## parameter

<table border="1">











<tr><td>
Function notation:
</td><td>
<pre>parameter()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;parameter&gt; &lt;/parameter&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> parâmetro </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## finalise

<table border="1">











<tr><td>
Function notation:
</td><td>
<pre>finalise()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;finalise&gt; &lt;/finalise&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> finalizar </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## real

<table border="1">











<tr><td>
Function notation:
</td><td>
<pre>real()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;real&gt; &lt;/real&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> real </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## Integers

<table border="1">





<tr><td>Prefix notation: </td>
<td><p>

 <pre>Integers ( <span style="color:gray">type</span> ) </pre><br>

 <pre>ℤ ( <span style="color:gray">type</span> ) </pre><br>

</p></td></tr>







<tr><td>
Function notation:
</td><td>
<pre>Integers()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;Integers&gt; &lt;/Integers&gt;</pre>
</td></tr>
</table>

 **Integer numbers type**

  A type representing integer numbers. Assumptions on the number of bits used by the compiler to represent an integer number is given as information in the editor.

  ```
  x in real
  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> inteiro </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## repeat

<table border="1">











<tr><td>
Function notation:
</td><td>
<pre>repeat()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;repeat&gt; &lt;/repeat&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> repetir </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## node

<table border="1">











<tr><td>
Function notation:
</td><td>
<pre>node()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;node&gt; &lt;/node&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>el </td><td> κόμβος </td></tr>

<tr><td>pt </td><td> nó </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## string

<table border="1">











<tr><td>
Function notation:
</td><td>
<pre>string()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;string&gt; &lt;/string&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> texto </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## minus

<table border="1">


<tr><td>Infix notation: </td>
<td><p>

<pre><span style="color:gray">type</span> - <span style="color:gray">type</span></pre><br>

</p></td></tr>










<tr><td>
Function notation:
</td><td>
<pre>minus()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;minus&gt; &lt;/minus&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> subtrair </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## largerEqual

<table border="1">


<tr><td>Infix notation: </td>
<td><p>

<pre><span style="color:gray">type</span> >= <span style="color:gray">type</span></pre><br>

<pre><span style="color:gray">type</span> ≥ <span style="color:gray">type</span></pre><br>

</p></td></tr>










<tr><td>
Function notation:
</td><td>
<pre>largerEqual()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;largerEqual&gt; &lt;/largerEqual&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> maiorIgual </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## Time

<table border="1">











<tr><td>
Function notation:
</td><td>
<pre>Time()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;Time&gt; &lt;/Time&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> eventos </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## variable

<table border="1">











<tr><td>
Function notation:
</td><td>
<pre>variable()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;variable&gt; &lt;/variable&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> variável </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## integer

<table border="1">











<tr><td>
Function notation:
</td><td>
<pre>integer()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;integer&gt; &lt;/integer&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> inteiro </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## Strings

<table border="1">











<tr><td>
Function notation:
</td><td>
<pre>Strings()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;Strings&gt; &lt;/Strings&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> texto </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## notEqual

<table border="1">


<tr><td>Infix notation: </td>
<td><p>

<pre><span style="color:gray">type</span> != <span style="color:gray">type</span></pre><br>

<pre><span style="color:gray">type</span> ≠ <span style="color:gray">type</span></pre><br>

</p></td></tr>










<tr><td>
Function notation:
</td><td>
<pre>notEqual()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;notEqual&gt; &lt;/notEqual&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> diferente </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## always

<table border="1">











<tr><td>
Function notation:
</td><td>
<pre>always()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;always&gt; &lt;/always&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> sempre </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## longComment

<table border="1">











<tr><td>
Function notation:
</td><td>
<pre>longComment()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;longComment&gt; &lt;/longComment&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

  </table>



  <span style="color:red">Missing:</span>








## larger

<table border="1">


<tr><td>Infix notation: </td>
<td><p>

<pre><span style="color:gray">type</span> > <span style="color:gray">type</span></pre><br>

</p></td></tr>










<tr><td>
Function notation:
</td><td>
<pre>larger()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;larger&gt; &lt;/larger&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> maior </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## equal

<table border="1">


<tr><td>Infix notation: </td>
<td><p>

<pre><span style="color:gray">type</span> == <span style="color:gray">type</span></pre><br>

<pre><span style="color:gray">type</span> ≡ <span style="color:gray">type</span></pre><br>

</p></td></tr>










<tr><td>
Function notation:
</td><td>
<pre>equal()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;equal&gt; &lt;/equal&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> igual </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## element

<table border="1">


<tr><td>Infix notation: </td>
<td><p>

<pre><span style="color:gray">type</span> in <span style="color:gray">type</span></pre><br>

<pre><span style="color:gray">type</span> ∈ <span style="color:gray">type</span></pre><br>

</p></td></tr>










<tr><td>
Function notation:
</td><td>
<pre>element()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;element&gt; &lt;/element&gt;</pre>
</td></tr>
</table>

 **Element of a set of type**

  Defines a variable to be an element of a set or a type. If a set is provided, then the variable takes the type of the elements of the set

  ```
  x in Reals
  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> elemento </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## vector

<table border="1">







<tr><td>Notation: </td></tr>





<tr><td>
Function notation:
</td><td>
<pre>vector()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;vector&gt; &lt;/vector&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> vector </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## plus

<table border="1">


<tr><td>Infix notation: </td>
<td><p>

<pre><span style="color:gray">type</span> + <span style="color:gray">type</span></pre><br>

</p></td></tr>










<tr><td>
Function notation:
</td><td>
<pre>plus()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;plus&gt; &lt;/plus&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> adicionar </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## definitions

<table border="1">











<tr><td>
Function notation:
</td><td>
<pre>definitions()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;definitions&gt; &lt;/definitions&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> definicoes </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## assign

<table border="1">


<tr><td>Infix notation: </td>
<td><p>

<pre><span style="color:gray">type</span> = <span style="color:gray">type</span></pre><br>

</p></td></tr>










<tr><td>
Function notation:
</td><td>
<pre>assign()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;assign&gt; &lt;/assign&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> atribuir </td></tr>

  </table>



  <span style="color:red">Missing:</span>








## Event

<table border="1">











<tr><td>
Function notation:
</td><td>
<pre>Event()</pre>
</td></tr>

<tr><td>
Internal XML notation:
</td><td>
<pre> &lt;Event&gt; &lt;/Event&gt;</pre>
</td></tr>
</table>

 ****



  ```

  ```

  Localisation available for:
<table border="1">

<tr><td>pt </td><td> eventos </td></tr>

  </table>



  <span style="color:red">Missing:</span>
