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
from RoboticsLanguage.Base import Utilities

def transform(code, parameters):
  Utilities.logging.info("Transforming FiniteStateMachine...")


  # add parameters
  list_of_states = list(set(code.xpath("//FiniteStateMachine/transitions/transition/begin/text()") +
                            code.xpath("//FiniteStateMachine/transitions/transition/end/text()")))
  transition_labels = code.xpath("//FiniteStateMachine/transitions/transition/label/text()")
  transition_begins = code.xpath("//FiniteStateMachine/transitions/transition/begin/text()")
  transition_ends = code.xpath("//FiniteStateMachine/transitions/transition/end/text()")
  init = code.xpath("//FiniteStateMachine/initial/text()")
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
