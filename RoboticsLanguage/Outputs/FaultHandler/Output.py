#
#   This is the Robotics Language compiler
#
#   Parameters.py: Definition of the parameters for this package
#
#   Created on: 05 March, 2019
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#


import sys
from RoboticsLanguage.Base import Utilities
from RoboticsLanguage.Tools import Templates

def output(code, parameters):
  Utilities.logging.info("Output Fault Handler...")

  # run template engine to generate code
  if not Templates.templateEngine(code, parameters):
    sys.exit(1)

  return 0