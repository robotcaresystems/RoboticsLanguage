# -*- coding: utf-8 -*-
#
#   This is the Robotics Language compiler
#
#   Parse.py: The parser for the Robotics Language
#
#   @NOTE the RoL parser currently works by generating the composition of
#   strings of text (see functions `xml` and `miniLanguage`) that are eventually parsed into XML.
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

# @TODO generalise when RoL parameters become dictionaries
def nodeParametersToDictionary(xml):
  return {'node': {key: value.text for (key, value) in Utilities.optionalArguments(xml).iteritems()}}


# creates XML text for entry
def xml(tag, content, position=0):
  text = ''.join(content) if isinstance(content, list) else content
  return '<' + tag + ' p="' + str(position) + '" >' + text + '</' + tag + '>'


def miniLanguage(key, text, position, parameters):

  try:
    code, parameters = Utilities.importModule(
        'Inputs', key, 'Parse').Parse.parse(text, parameters)
    result = etree.tostring(code)
    return result
  except:
    Utilities.logging.error("Failed to parse mini-language " + key)


def prepareGrammarEngine(parameters):

  keywords = {}

  # load language definitions for all modules
  for transform in parameters['manifesto']['Transformers'].keys():
    keywords.update(Utilities.importModule(
        'Transformers', transform, 'Language').Language.language)

  # the base grammar defines atomic elements, special elements, and the flow of precedence
  base_grammar = r"""
digits = <digit+>
word = <letter+>

# comments
wws = (ws longComment)* (ws shortComment)* ws

longComment = ('##'  <(~('##') anything)+>:c  '##' -> xml('comment',str(c), self.input.position))

shortComment = ('#'  <(~('\n') anything)+>:c  '\n' -> xml('comment',str(c), self.input.position))

# types
variable = word:a -> xml('variable', a, self.input.position)

type = ( number | string | boolean )

string = (('"' | '\''):q <(~exactly(q) anything)*>:xs exactly(q)) -> xml('string',xs, self.input.position)

number = ( real | integer )

boolean = ( 'true' | 'false' ):b -> xml('boolean',b, self.input.position)

integer = < '-'? wws digits >:x -> xml('integer',str(x), self.input.position)

real =  < ('-' wws)? (( '.' digits | digits '.' digits? ) ( ('e' | 'E') ('+' | '-')? digits)?
              |  digits ('e' | 'E') ('+' | '-')? digits
              ) >:x -> xml('real',str(x), self.input.position)

# special functions, brackets
language = word:n wws '<{' code:l '}>' -> miniLanguage(n, l, self.input.position)

code = <(~('}>') anything)+>

function = ( word:a1 wws '(' wws mixed:a2 wws ')' -> xml(a1, a2, self.input.position)
           | word:a1 wws '(' wws ')' -> xml(a1, '', self.input.position)
           )

part = word:a1 '[' wws values:a2 wws ']' -> xml('part',xml('variable',a1,self.input.position)+xml('index',a2,self.input.position),self.input.position)

# definition of values, key-values, or mixed arguments
optionDefinition = word:a1 wws ':' wws Pmin:a2 -> xml('optionalArgument',xml('name',a1,self.input.position)+a2,self.input.position)
valuesDefinition = Pmin:a1 (wws ',' wws Pmin )+:a2 -> ''.join([a1]+a2)
mixedDefinition = option:a1 (wws ',' wws option )+:a2 -> ''.join([a1]+a2)
keyValuesDefinition = optionDefinition:a1 (wws ',' wws optionDefinition )+:a2 -> ''.join([a1]+a2)

mixed = ( mixedDefinition | option )
values = ( valuesDefinition | Pmin )
keyValues = ( keyValuesDefinition | Pmin )
option = ( optionDefinition | Pmin )

parenthesis = '(' wws Pmin:a wws ')' -> a
"""

 # the structure of the main element
  main_loop_start = r"""
# main loop
main = wws ( language
         | function
         | part
         | """

  main_loop_end = r"""
         | type
         | variable
         ):a wws -> a
"""

  # extract the definitions from the language (i.e. remove the 'input/RoL' part from the path)
  definitions = Utilities.ExtractLanguageDefinitions(keywords, 'input', 'RoL')

  # create pre/in/post fix part of the grammar
  fix_text, max_precedence = Utilities.CreatePreInPostFixGrammar(definitions)

  # create the bracket operators part of the grammar
  bracket_text, bracket_keys = Utilities.CreateBracketGrammar(definitions)

  # add the brackets to the main list of elements
  bracket_keys_text = '\n         | '.join(bracket_keys)

  # set the element with maximum precedence
  max_precedence_text = '\nP' + \
      str(max_precedence) + ' = ( parenthesis | main )\n'

  # the grammar is the concatenation of many definitions
  grammar = base_grammar + fix_text + bracket_text + max_precedence_text + \
      main_loop_start + bracket_keys_text + main_loop_end

  return grammar


def semanticTransformations(xml):
  # look for all the variables in the definitions block
  variables_defined = xml.xpath('/node/definitions/element/variable[1]/text()')

  # from the previous list, find tags with these variable names
  variables_used = funcy.flatten(
      map(lambda x: xml.xpath('//' + x), variables_defined))

  # rename the variable tag to 'function' and add the name to the attribute 'name'
  for variable in variables_used:
    name = variable.tag
    variable.tag = 'function'
    variable.attrib['name'] = name

  return xml


def parse(text, parameters):

  # @TODO need to reimplement language localisation
  # load cached language and grammar or create from scratch if needed
  grammar = Utilities.cache('RoL-language-grammar',
                            lambda: prepareGrammarEngine(parameters))

  # show the grammar if `--debug-rol-grammar` is set in the command line
  if parameters['Inputs']['RoL']['debug']['grammar']:
    print(grammar)

  # @NOTE could not pickle the language itself to cache. Is there a way to solve this?
  # create the grammar
  language = parsley.makeGrammar(grammar, {'xml': xml,
                                           'miniLanguage': lambda x, y, z: miniLanguage(x, y, z, parameters)})

  try:
    # parse the text against the grammar
    parsed_xml_text = ''.join(language(text).main())

  except parsley.ParseError as error:
    Utilities.logErrors(Utilities.formatParsleyErrorMessage(error), parameters)
    sys.exit(1)

  try:
    # create XML object from xml string
    parsed_xml = etree.fromstring(parsed_xml_text)

  except etree.XMLSyntaxError as error:
    Utilities.logErrors(Utilities.formatLxmlErrorMessage(error), parameters)
    sys.exit(1)

  # If the node has parameters, then add them to the global parameters dictionary
  parameters = Utilities.mergeDictionaries(
      nodeParametersToDictionary(parsed_xml), parameters)

  # apply semantic changes
  parsed_xml = semanticTransformations(parsed_xml)

  return parsed_xml, parameters
