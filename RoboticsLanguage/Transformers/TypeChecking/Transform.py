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

  # check if should ignore semantic checking
  if parameters['Transformers']['TypeChecking']['ignoreSemanticErrors']:
    return code, parameters

  # do all semantic checking
  code, parameters = Semantic.Checker(code, parameters)

  return code, parameters
