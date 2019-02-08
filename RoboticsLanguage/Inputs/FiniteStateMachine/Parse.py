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

from parsley import makeGrammar
from RoboticsLanguage.Tools import Parsing
import copy


def endTag(element):
  # extract the begin state (second element) and make a deep copy
  child = copy.copy(element[0].getchildren()[1])
  # rename it to an "end" tag
  child.tag = '{fsm}end'
  return child


grammar_definition = """
word = <letter letterOrDigit*>

name = 'name' ws ':' ws word:name -> xml('name',text=name)

initial = 'initial' ws ':' ws word:state -> xml('initial', text=state)

state = '(' ws word:state ws ')' -> state

transition = state:begin ws '-' ws word:label ws '->' ws ( transition:t -> [ xml('transition', [xml('label', text=label), xml('begin', text=begin), endTag(t)])] + t
                                                         | state:end -> [ xml('transition', [xml('label', text=label), xml('begin', text=begin), xml('end', text=end)]) ]
                                                         )

machine = ws name:n ws initial:i (ws transition)*:t ws -> xml('machine',[n, i] + [item for sublist in t for item in sublist])
"""


def parse(text, parameters):
  # make the grammar
  grammar = makeGrammar(grammar_definition, {'xml': Parsing.xmlNamespace('fsm'), 'endTag': endTag})

  # parse the text
  code = grammar(text).machine()

  return code, parameters
