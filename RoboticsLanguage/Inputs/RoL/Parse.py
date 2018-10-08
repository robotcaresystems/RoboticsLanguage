# -*- coding: utf-8 -*-
#
#   This is the Robotics Language compiler
#
#   Parse.py: The parser for the Robotics Language
#
#   @NOTE the RoL parser currently works by generating the composition of
#   strings of text (see functions `Utilities.xml` and `Utilities.xmlMiniLanguage`) that are eventually
#   parsed into XML.
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
  '''Extracts the optional parameters given in the `node` function and adds them to the parameters dictionary'''
  return {'node': {key: value.text for (key, value) in Utilities.optionalArguments(xml).iteritems()}}


@Utilities.cache_in_disk
def prepareGrammarEngine(parameters):
  '''Build the grammer for the robotics language. Can be cached'''
  # keywords = {}
  #
  # # load language definitions for all modules
  # for transform in parameters['manifesto']['Transformers'].keys():
  #   keywords.update(Utilities.importModule(
  #       'Transformers', transform, 'Language').Language.language)

  # the base grammar defines atomic elements, special elements, and the flow of precedence
  base_grammar = r"""
digits = <digit+>
objectName = <letter ( letter | '_' | digit )*>

# comments
wws = (ws longComment)* (ws shortComment)* ws

longComment = ('##'  <(~('##') anything)+>:c  '##' -> xml('comment',str(c), self.input.position))

shortComment = ('#'  <(~('\n') anything)+>:c  '\n' -> xml('comment',str(c), self.input.position))

# types
variable = functionName:a -> xmlVariable(a,self.input.position)

type = ( real | integer | natural | string | boolean )

string = (('"' | '\''):q <(~exactly(q) anything)*>:xs exactly(q)) -> xml('string',xs, self.input.position)

boolean = ( 'true' | 'false' ):b -> xml('boolean',b, self.input.position)

natural = digits:x -> xml('natural',str(x), self.input.position)

integer = < '-' wws digits >:x -> xml('integer',str(x), self.input.position)

real =  < ('-' wws)? (( '.' digits | digits '.' digits? ) ( ('e' | 'E') ('+' | '-')? digits)?
              |  digits ('e' | 'E') ('+' | '-')? digits
              ) >:x -> xml('real',str(x), self.input.position)

# special functions, brackets
language = objectName:n wws '<{' code:l '}>' -> xmlMiniLanguage(n, l, self.input.position)

code = <(~('}>') anything)+>

function = ( functionName:a1 wws '(' wws mixed:a2 wws ')' -> xmlFunction(a1, a2, self.input.position)
           | functionName:a1 wws '(' wws ')' -> xmlFunction(a1, '', self.input.position)
           )

part = objectName:a1 '[' wws values:a2 wws ']' -> xml('part',xmlVariable(a1,self.input.position)+xml('index',a2,self.input.position),self.input.position)

functionDefinition  = 'define' wws functionName:a1 wws '(' ( values | wws ):a2 ')' ( wws '->' wws '(' values:a3 ')' wws | wws '->' wws Pmin:a3 wws | wws:a3 ) ':' wws function:a4 -> xmlFunctionDefinition(a1,a2,a3,a4,self.input.position)

# definition of values, key-values, or mixed arguments
optionDefinition = objectName:a1 wws ':' wws Pmin:a2 -> xmlAttributes('option',a2,self.input.position, attributes={'name':a1})
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
main = wws ( functionDefinition
         | language
         | function
         | part"""

  main_loop_end = r"""
         | type
         | variable
         ):a wws -> a
"""

  # extract the definitions from the language (i.e. remove the 'input/RoL' part from the path)
  definitions = Utilities.ExtractLanguageDefinitions(
      parameters['language'], 'input', 'RoL')

  # create pre/in/post fix part of the grammar
  fix_text, max_precedence = Utilities.CreatePreInPostFixGrammar(definitions)

  # create the bracket operators part of the grammar
  bracket_text, bracket_keys = Utilities.CreateBracketGrammar(definitions)

  # create generic operators
  generic_text, generic_keys = Utilities.CreateGenericGrammar(definitions)

  # add the brackets to the main list of elements
  if len(bracket_keys) > 0:
    bracket_keys_text = '         | ' + '\n         | '.join(bracket_keys)
  else:
    bracket_keys_text = ''

  # add the generic key to the main list of elements
  if len(generic_keys) > 0:
    generic_keys_text = '         | ' + '\n         | '.join(generic_keys)
  else:
    generic_keys_text = ''

  # set the element with maximum precedence
  max_precedence_text = '\nP' + \
      str(max_precedence) + ' = ( parenthesis | main )\n'

  # the grammar is the concatenation of many definitions
  grammar = base_grammar + fix_text + bracket_text + generic_text + max_precedence_text + \
      main_loop_start + generic_keys_text + bracket_keys_text + main_loop_end

  return grammar


def parse(text, parameters):
  '''Main parser for the robotics language'''

  # @TODO need to reimplement language localisation
  # load cached language and grammar or create from scratch if needed
  grammar = prepareGrammarEngine(parameters)

  # show the grammar if `--show-rol-grammar` is set in the command line
  if parameters['Inputs']['RoL']['developer']['grammar']:
    print(grammar)

  # @NOTE could not pickle the language itself to cache. Is there a way to solve this?
  # create the grammar
  language = parsley.makeGrammar(grammar, {'xml': Utilities.xml,
                                           'xmlAttributes': Utilities.xmlAttributes,
                                           'xmlFunctionDefinition': lambda x, y, z, w, k: Utilities.xmlFunctionDefinition(parameters, x, y, z, w, k),
                                           'xmlVariable': lambda x, y: Utilities.xmlVariable(parameters, x, y),
                                           'xmlFunction': lambda x, y, z: Utilities.xmlFunction(parameters, x, y, z),
                                           'xmlMiniLanguage': lambda x, y, z: Utilities.xmlMiniLanguage(parameters, x, y, z)})

  try:
    # parse the text against the grammar
    parsed_xml_text = ''.join(language(text).main())

  except parsley.ParseError as error:
    # with Error.exception(parameters, stop=True)
    Utilities.logErrors(Utilities.formatParsleyErrorMessage(error), parameters)
    sys.exit(1)

  try:
    # create XML object from xml string
    parsed_xml = etree.fromstring(parsed_xml_text)

  except etree.XMLSyntaxError as error:
    # with Error.exception(parameters, stop=True)
    Utilities.logErrors(Utilities.formatLxmlErrorMessage(error), parameters)
    sys.exit(1)

  # If the node has parameters, then add them to the global parameters dictionary
  parameters = Utilities.mergeDictionaries(
      nodeParametersToDictionary(parsed_xml), parameters)

  return parsed_xml, parameters
