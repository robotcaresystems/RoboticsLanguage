# -*- coding: utf-8 -*-
#
#   This is the Robotics Language compiler
#
#   Parse.py: The parser for the Robotics Language
#
#   @NOTE the RoL parser currently works by generating the composition of
#   strings of text (see functions `xml` and `xmlInfix`) that are eventually parsed into XML.
#   This makes the implementation simple but my incur some performance issues when mini languages
#   are used. Mini languages return XML objects that are converted to text to integrate into the language.
#   When this parser returns the result is converts everything into an XML object, which means that the mini
#   language code is converted to xml text and then back to XML objects, thus waisting CPU time. If performance
#   become critical in the future this should be addressed.
#
#   Created on: June 22, 2017
#       Author: Gabriel A. D. Lopes
#      Licence: Apache 2.0
#    Copyright: 2014-2017 Robot Care Systems BV, The Hague, The Netherlands. All rights reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import parsley
from lxml import etree
from RoboticsLanguage.Base import Utilities
import sys
import funcy

# creates XML text for entry
def xml(name, content, position, keyword_dictionary={}, attributes = {}):
  attrib = ' '.join([a+'="'+str(b)+'"' for a,b in attributes.iteritems()])

  # @BUG might generate an error. Add try/except
  # if len(keyword_dictionary) > 0:
  #   tag = keyword_dictionary[name]
  # else:
  tag = name

  if isinstance(content, list):
    content = [x for x in content if x != ',']
    return '<' + tag + ' p="' + str(position) + '" '+attrib+'>' + ''.join(content) + '</' + tag + '>'
  else:
    return '<' + tag + ' p="' + str(position) + '" '+attrib+'>' + content + '</' + tag + '>'

def xmlInfix(start, pairs, position):
  result = start
  for op, value in pairs:
    result = '<'+op+' p="' + str(position) + '">'+result+str(value)+'</'+op+'>'
  return result


def createPreInPostfixGrammar(parameters,input):
  # initialise variables
  keywords = {}

  # load language definitions for all modules
  for transform in parameters['manifesto']['Transformers'].keys():
    keywords.update(Utilities.importModule('Transformers', transform, 'Language').Language.language)

  grammar = ''
  operators = []

  for key, value in keywords.iteritems():
    if 'input' in value.keys():
      if input in value['input'].keys():
        if 'pre-in-postfix' in value['input'][input].keys():
          grammar += key+' = \''+value['input'][input]['pre-in-postfix'][0] + '\' ws ( ws expression | ws \''+value['input'][input]['pre-in-postfix'][1] + '\' )*:e ws \''+value['input'][input]['pre-in-postfix'][2] + '\' -> xml(\''+key+'\', e, self.input.position, dictionary)\n'
          operators.append(key)

  grammar += 'preinpostfixElements = '+' | '.join(operators)+'\n'

  return grammar


def createCustomGrammar(parameters,input):
  # @BUG if first element of the custom vector is '' it does not work
  # initialise variables
  keywords = {}

  # load language definitions for all modules
  for transform in parameters['manifesto']['Transformers'].keys():
    keywords.update(Utilities.importModule('Transformers', transform, 'Language').Language.language)

  grammar = ''
  operators = []

  for key, value in keywords.iteritems():
    if 'input' in value.keys():
      if input in value['input'].keys():
        if 'custom' in value['input'][input].keys():
          custom = value['input'][input]['custom']
          expressions = ['expression:e'+str(i) for i in range(len(custom)-1)]
          infixes = [' ws \''+custom[i]+'\' ws ' for i in range(1,len(custom)-1)]

          fullexpression = [x for t in zip(expressions, infixes) for x in t]
          fullexpression.append(expressions[-1])

          if custom[0] is not '':
            fullexpression.insert(0, '\''+custom[0]+'\' ws ')

          if custom[-1] is not '':
            fullexpression.append(' ws \''+custom[0]+'\'')

          grammar += key + ' = ' + ''.join(fullexpression) + ' -> xml(\''+key+'\', '+ '+'.join(['e'+str(i) for i in range(len(custom)-1)]) +', self.input.position, dictionary)\n'
          operators.append(key)


  grammar += 'customElements = '+' | '.join(operators)+'\n'

  return grammar

# @TODO generalise when RoL parameters become dictionaries
def nodeParametersToDictionary(xml):
  return {'node': { key:value.text for (key, value) in Utilities.optionalArguments(xml).iteritems() } }


def miniLanguage(key, text, position, parameters):
  try:
    code, parameters = Utilities.importModule('Inputs', key, 'Parse').Parse.parse(text, parameters)
    result = etree.tostring(code)
    return result
  except:
    Utilities.logging.error("Failed to parse mini-language "+key)


def createPrefixGrammar(parameters,input):
  # initialise variables
  keywords = {}

  # load language definitions for all modules
  for transform in parameters['manifesto']['Transformers'].keys():
    keywords.update(Utilities.importModule('Transformers', transform, 'Language').Language.language)

  grammar = ''
  operators = []

  for key, value in keywords.iteritems():
    if 'input' in value.keys():
      if input in value['input'].keys():
        if 'prefix' in value['input'][input].keys():
          if isinstance(value['input'][input]['prefix'],list):
            pass
          else:
            grammar += key+' = \''+value['input'][input]['prefix'] + '\' ws ( language | preinpostfixElements | function | customElements | type | variable ):e -> xml(\''+key+'\', e, self.input.position, dictionary)\n'
            operators.append(key)

  grammar += 'prefixElements = '+' | '.join(operators)+'\n'

  return grammar


def createLocalisationDictionary(parameters,language):
  # initialise variables
  keywords = {}

  # load language definitions for all modules
  for transform in parameters['manifesto']['Transformers'].keys():
    keywords.update(Utilities.importModule('Transformers', transform, 'Language').Language.language)

  dictionary = {}

  for key, value in keywords.iteritems():
    if 'localisation' in keywords[key].keys():
      if language in keywords[key]['localisation'].keys():
        if isinstance(keywords[key]['localisation'][language],dict):
          dictionary[keywords[key]['localisation'][language]['prefix']] = key
        else:
          dictionary[keywords[key]['localisation'][language]] = key
      else:
        dictionary[key] = key
    else:
      dictionary[key] = key

  return dictionary


def createInfixGrammar(parameters,input):
  # initialise variables
  keywords = {}

  # load language definitions for all modules
  for transform in parameters['manifesto']['Transformers'].keys():
    keywords.update(Utilities.importModule('Transformers', transform, 'Language').Language.language)

  infix_grammar = ''
  infix_operators = []
  orders = {}

  for key, value in keywords.iteritems():
    if 'input' in value.keys():
      if input in value['input'].keys():
        if 'infix' in value['input'][input].keys():
          infix_operators.append({'key': key, 'infix': value['input'][input]['infix'], 'order': value['input'][input]['infixOrder']})

          if value['input'][input]['infixOrder'] not in orders.keys():
            orders[value['input'][input]['infixOrder']] = []

          orders[value['input'][input]['infixOrder']].append(key)

  sorted_orders = sorted(orders)

  # definition of parenthesis
  infix_grammar += 'parenthesis = \'(\' ws infixElements:e ws \')\' -> e\n'

  # create language infix clauses
  for infix in infix_operators:
    if isinstance(infix['infix'],list):
      symbol = '( \'' + '\' | \''.join(infix['infix']) + '\' )'
    else:
      symbol = '\''+infix['infix']+'\''

    infix_grammar += infix['key'] + ' = ' + symbol + ' ws level' + str(infix['order']) + ':n -> (\'' + infix['key'] + '\', n )\n'

  infix_grammar += 'level'+str(sorted_orders[-1])+' = language | prefixElements | customElements | preinpostfixElements | function | type | variable | parenthesis\n'

  # create language level groups
  for key, value in orders.iteritems():
    if len(value)>1:
      symbol = '( ' + ' | '.join(value) + ' )'
    else:
      symbol = ''+value[0]+''
    infix_grammar += 'level'+str(key)+'keys = ws '+symbol + '\n'

  infix_grammar += 'infixElements = level'+str(sorted_orders[0])+':left level'+str(sorted_orders[0])+'keys*:right -> xmlInfix(left,right, self.input.position)\n'

  for i in range(1,len(sorted_orders)):
    infix_grammar += 'level'+str(sorted_orders[i-1])+' = level'+str(sorted_orders[i])+':left level'+str(sorted_orders[i])+'keys*:right -> xmlInfix(left,right, self.input.position)\n'

  return infix_grammar


def prepareGrammarEngine(parameters):
  # This is the base function composition grammar
  # Includes base types (string, numbers, booleans),
  # comments and optional parameters using the ':' element.

  function_composition_grammar = r"""
main  = ( ws function:f ws -> f
        | ws comment:c ws -> c
        )*

language = word:n ws '<{' code:l '}>' ws  -> miniLanguage(n, l, self.input.position)

code = <(~('}>') anything)+>

expression = language | prefixElements | preinpostfixElements | infixElements | function | customElements | type | variable

# Function composition
function = (word:f ws '('  ( ws optionalArgument | ws expression | ws ',' )*:p ws ')' -> xml(f, p, self.input.position,dictionary))

optionalArgument = (word:p ws ':' ws expression:w -> xml('optionalArgument',xml('name',str(p),self.input.position)+str(w), self.input.position) )

variable = (word:w -> xml('variable',str(w), self.input.position) )

# comments
comment = ( longComment | shortComment )

longComment = ('##'  <(~('##') anything)+>:c  '##' -> xml('longComment',str(c), self.input.position))

shortComment = ('#'  <(~('\n') anything)+>:c  '\n' -> xml('shortComment',str(c), self.input.position))

# base data types
type = ( number | string | boolean )

string = (('"' | '\''):q <(~exactly(q) anything)*>:xs exactly(q)) -> xml('string',xs, self.input.position)

number = ( real | integer )

boolean = ( 'true' | 'false' ):b -> xml('boolean',b, self.input.position)

integer = < '-'? ws digits >:x -> xml('integer',x, self.input.position)

real = ( <'-'? ws digits '.' digits? ( ('e' | 'E') ('+' | '-')? digits)? >
       | <'-'? ws '.' digits ( ('e' | 'E') ('+' | '-')? digits)? >
       | <'-'? ws digits ( ('e' | 'E') ('+' | '-')? digits) >
       ):x -> xml('real',x, self.input.position)

# base definitions
word = <(letter|latinCharacter|greekCharacter)+>
digits = <digit+>
latinCharacter = :x ?(x in 'áàâãéèêíìîóòõôúùûÁÀÂÃÉÈÊÍÌÎÓÒÕÔÚÙÛ') -> x
greekCharacter = :x ?(x in 'ΆΈΉΊ΋Ό΍ΎΏΐΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡ΢ΣΤΥΦΧΨΩΪΫάέήίΰαβγδεζηθικλμνξοπρςστυφχψωϊϋόύώϏϐϑϒϓϔϕϖϗϘϙϚϛϜϝϞϟϠϡϢϣϤϥϦϧϨϩϪϫϬϭϮϯϰϱϲϳϴϵ϶ϷϸϹϺϻϼϽϾϿ') -> x
"""

  # load other types of grammar elements
  extra_grammars  = createInfixGrammar(parameters,'RoL')
  extra_grammars += createPreInPostfixGrammar(parameters,'RoL')
  extra_grammars += createPrefixGrammar(parameters,'RoL')
  extra_grammars += createCustomGrammar(parameters,'RoL')

  grammar = function_composition_grammar + extra_grammars

  if parameters['globals']['language'] is not 'en':
    dictionary = createLocalisationDictionary(parameters,parameters['globals']['language'])
  else:
    dictionary = {}

  return grammar, dictionary


def semanticTransformations(xml):
  # look for all the variables in the definitions block
  variables_defined = xml.xpath('/node/definitions/element/variable[1]/text()')

  # from the previous list, find tags with these variable names
  variables_used = funcy.flatten(map(lambda x:xml.xpath('//'+x), variables_defined))

  # rename the variable tag to 'function' and add the name to the attribute 'name'
  for variable in variables_used:
    name = variable.tag
    variable.tag = 'function'
    variable.attrib['name'] = name

  return xml


def parse(text, parameters):

  # @BUG If the command line flag --language is used may need to recompute dictionary
  # load cached language and grammar or create from scratch if needed
  grammar, dictionary = Utilities.cache('RoL-language-grammar', lambda : prepareGrammarEngine(parameters))


  if parameters['Inputs']['RoL']['debug']['grammar']:
    print(grammar)

  # @NOTE could not pickle the language itself. Is there a way to solve this?
  # create the grammar
  language = parsley.makeGrammar(grammar, {'xml': xml,
                                           'xmlInfix': xmlInfix,
                                           'dictionary': dictionary,
                                           'miniLanguage': lambda x,y,z : miniLanguage(x, y, z, parameters) })

  try:
    # parse the text against the grammar
    parsed_xml_text = ''.join(language(text).main())
  except parsley.ParseError as error:
    Utilities.logErrors(Utilities.formatParsleyErrorMessage(error),parameters)
    sys.exit(1)

  try:
    # create XML object from xml string
    parsed_xml = etree.fromstring(parsed_xml_text)
  except etree.XMLSyntaxError as error:
    Utilities.logErrors(Utilities.formatLxmlErrorMessage(error),parameters)
    sys.exit(1)

  # If the node has parameters, then add them to the global parameters dictionary
  parameters = Utilities.mergeDictionaries(nodeParametersToDictionary(parsed_xml),parameters)

  # apply semantic changes
  parsed_xml = semanticTransformations(parsed_xml)

  return parsed_xml, parameters
