#
#   This is the Robotics Language compiler
#
#   Parameters.py: Definition of the parameters for this package
#
#   Created on: 11 July, 2018
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
from parsley import makeGrammar
from RoboticsLanguage.Base import Utilities

grammar_definition = """
word = <letter letterOrDigit*>

name = 'name' ws ':' ws word:n -> xml('name',n)

initialisation = 'initial' ws ':' ws word:state -> xml('initial',state)

transitions = ( ws transition:fsm -> fsm[0])*

transition = '(' ws word:begin ws ')' ws '-' ws word:label ws '->' ws ( transition:t -> xml('transition', xml('label', label)[0] + xml('begin',begin)[0] + xml('end',str(t[1]))[0] , rest = begin, text = t[0])
                                | '(' ws word:end ws ')' -> xml('transition', xml('label',label)[0] + xml('begin',begin)[0] + xml('end',end)[0], rest = begin)
                                )

result = ws name:a ws initialisation:b ws transitions:t ws -> a + b + xml('transitions', ''.join(t))
"""


def xml(tag, content, rest='', text=''):
  return '<fsm:' + tag + '>' + content + '</fsm:' + tag + '>' + text, rest


def parse(text, parameters):
  Utilities.logging.info("Parsing FiniteStateMachine language...")

  # make the grammar
  grammar = makeGrammar(grammar_definition, {'xml': xml})

  # parse the text
  result = grammar(text).result()

  # convert to XML object
  code = etree.fromstring('<fsm:machine xmlns:fsm="fsm">' + ''.join(result) + '</fsm:machine>')

  return code, parameters
