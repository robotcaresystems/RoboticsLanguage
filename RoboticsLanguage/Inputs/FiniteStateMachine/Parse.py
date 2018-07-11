#
#   This is the Robotics Language compiler
#
#   Parameters.py: Definition of the parameters for this package
#
#   Created on: 11 July, 2018
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#
from lxml import etree
from parsley import makeGrammar
from RoboticsLanguage.Base import Utilities

grammar_definition = """

var = <letter letterOrDigit*>
word = <letter+>

initialisation = 'init' ws ':' ws word:state -> xml('initial',state)

transitions = ( ws transition:fsm -> fsm[0])*

transition = word:begin ws '-' ws '(' ws var:label ws ')' ws '->' ws  ( ws transition:t -> xml('transition', xml('label',label)[0]+ xml('begin',begin)[0]+  xml('end',str(t[1][0]))[0] , rest = begin , text = t[0])
                                | ws word:end -> xml('transition', xml('label',label)[0] + xml('begin',begin)[0] +  xml('end',end)[0] , rest=begin )
                                )

result = ws initialisation:a ws transitions:t ws -> a + xml('transitions', ''.join(t))

"""


def xml(tag, content, rest='', text=''):
  return '<' + tag + '>' + content + '</' + tag + '>' + text, rest


def parse(text, parameters):
  Utilities.logging.info("Parsing FiniteStateMachine language...")

  # make the grammar
  grammar = makeGrammar(grammar_definition, {'xml': xml})

  # parse the text
  result = grammar(text).result()

  # convert to XML object
  code = etree.fromstring('<FiniteStateMachine>' + ''.join(result) + '</FiniteStateMachine>')

  # add parameters
  list_of_states = list(set(code.xpath("/FiniteStateMachine/transitions/transition/begin/text()") +
                            code.xpath("/FiniteStateMachine/transitions/transition/end/text()")))
  transition_labels = code.xpath("/FiniteStateMachine/transitions/transition/label/text()")
  transition_begins = code.xpath("/FiniteStateMachine/transitions/transition/begin/text()")
  transition_ends = code.xpath("/FiniteStateMachine/transitions/transition/end/text()")
  init = code.xpath("/FiniteStateMachine/initial/text()")
  num_of_transitions = int(code.xpath("count(//FiniteStateMachine/transitions/transition)"))
  num_of_states = int(len(list_of_states))

  parameters['Inputs']['FiniteStateMachine']['parameters'] = {
      'list_of_states': list_of_states,
      'transition_labels': transition_labels,
      'transition_begins': transition_begins,
      'transition_ends': transition_ends,
      'init': init,
      'num_of_transitions': num_of_transitions,
      'num_of_states': num_of_states,
  }

  return code, parameters
