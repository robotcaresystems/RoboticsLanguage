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


from lxml import etree
from RoboticsLanguage.Base import Utilities

def transform(code, parameters):
  Utilities.logging.info("Transforming Type Checking...")

  return code, parameters