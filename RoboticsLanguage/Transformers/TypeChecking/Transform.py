#
#   This is the Robotics Language compiler
#
#   Parameters.py: Definition of the parameters for this package
#
#   Created on: 31 July, 2018
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#

from RoboticsLanguage.Tools import Semantic


def transform(code, parameters):

  # do all semantic checking
  code, parameters = Semantic.Checker(code, parameters)

  return code, parameters
