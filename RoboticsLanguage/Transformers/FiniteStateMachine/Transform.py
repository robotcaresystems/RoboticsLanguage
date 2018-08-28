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

import os
from lxml import etree
from RoboticsLanguage.Base import Utilities

def transform(code, parameters):

  # this is the absolute path to the extra header file needed for finite state machines
  header_file = Utilities.myPluginPath(parameters) + '/Templates/Outputs/RosCpp/_nodename_/include/_nodename_/FiniteStateMachine.h'

  # skip header file if no state machines are defined
  if len(code.xpath('//fsm:machine', namespaces={'fsm': 'fsm'})) == 0:
    parameters['globals']['skipCopyFiles'].append(header_file)

  return code, parameters
