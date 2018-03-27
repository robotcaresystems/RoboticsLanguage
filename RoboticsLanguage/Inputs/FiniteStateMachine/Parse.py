#
#   This is the Robotics Language compiler
#
#   Parameters.py: Definition of the parameters for this package
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
from lxml import etree
from RoboticsLanguage.Base import Utilities
import parsley

# creates XML text for entry. This is used inside the grammar
def xml(tag, content, position):
  return '<' + tag + ' p="' + str(position) + '">' + content + '</' + tag + '>'



def miniLanguage(key, text, position, parameters):
  try:
    code, parameters = Utilities.importModule('Inputs', key, 'Parse').Parse.parse(text, parameters)
    result = etree.tostring(code)
    return result
  except:
    Utilities.logging.error("Failed to parse mini-language "+key)



# the main parsing function
def parse(text, parameters):
  Utilities.logging.info("Parsing FiniteStateMachine language...")

  # definition of the grammar according to Parsley
  # http://parsley.readthedocs.io/en/latest/tutorial.html
  grammar = r"""
# the language is collection of transitions separated by white space
main = ( ws transition:fsm ws -> fsm)*

# a transition are two words separared by an arrow ->. Return an XML string
transition = ws word:b ws '->' ws word:e -> xml('transition',xml('begin',b,self.input.position)+xml('end',e,self.input.position),self.input.position)

# a word is a collection of letters
word = ( language | letters )

language = letters:n ws '<<' code:l '>>' ws  -> miniLanguage(n, l, self.input.position)

code = <(~('>>') anything)+>

letters = <letter+>
"""

  # create the language object
  language = parsley.makeGrammar(grammar, {'xml': xml,
                                           'miniLanguage': lambda x,y,z : miniLanguage(x, y, z, parameters) })

  # parse the text using the grammar
  parsed_xml_text = '<FiniteStateMachine>'+''.join(language(text).main())+'</FiniteStateMachine>'

  # Convert xml string to xml object
  parsed_xml = etree.fromstring(parsed_xml_text)

  return parsed_xml, parameters
