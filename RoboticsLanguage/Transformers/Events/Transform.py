# -*- coding: utf-8 -*-
#
#   This is the Robotics Language compiler
#
#   Parameters.py: Definition of the parameters for this package
#
#   Created on: 05 September, 2018
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#


from RoboticsLanguage.Base import Utilities


def transform(code, parameters):

  Utilities.printCode(code.xpath('//when'))

  return code, parameters
