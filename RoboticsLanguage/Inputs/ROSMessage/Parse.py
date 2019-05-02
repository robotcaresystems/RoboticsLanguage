#
#   This is the Robotics Language compiler
#
#   Parse.py: Parses the ROS Message language
#
#   Created on: 08 February, 2019
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#
from parsley import makeGrammar
from RoboticsLanguage.Tools import Parsing
from RoboticsLanguage.Base import Utilities

grammar_definition = """
word = <letterOrDigit+>

name =  'name' ws ':' ws word:n ws -> xml('name', text=n)

definition = <anything*>:d end -> xml('definition', text='\\n'.join(map(lambda x: x.lstrip(), d.splitlines())))

main = ws name:n ws definition:d -> xml('message', [n,d])
"""


def parse(text, parameters):
  Utilities.logging.info("Parsing ROS Message language...")

  # make the grammar
  grammar = makeGrammar(grammar_definition, {'xml': Parsing.xmlNamespace('rosm')})

  # parse the text
  code = grammar(text).main()

  return code, parameters
