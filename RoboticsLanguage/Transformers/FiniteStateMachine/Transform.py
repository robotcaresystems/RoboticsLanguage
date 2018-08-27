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

  n = {'fsm': 'fsm'}

  # add a list of states
  parameters['Inputs']['FiniteStateMachine']['states'] ={}

  # look for all state machines
  for machine in code.xpath('//fsm:machine', namespaces=n):

    states = set()
    # get name of machine
    name = machine.xpath('fsm:name/text()', namespaces=n)[0]

    # add initial states
    states.add(machine.xpath('fsm:initial/text()', namespaces=n)[0])

    # add states found in every transition
    transitions = machine.xpath('fsm:transitions', namespaces=n)[0]
    for transition in transitions.xpath('fsm:transition', namespaces=n):
      states.add(transition.xpath('fsm:begin/text()', namespaces=n)[0])
      states.add(transition.xpath('fsm:end/text()', namespaces=n)[0])

    # save the set of states for each machine
    parameters['Inputs']['FiniteStateMachine']['states'][name] = states

  return code, parameters
