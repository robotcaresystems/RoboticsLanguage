#
#   This is the Robotics Language compiler
#
#   Parse.py: Parses the Shell language
#
#   Created on: 15 February, 2019
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#
from RoboticsLanguage.Tools import Parsing


def shellLanguageEscape(text):
  return text.replace('\\', '\\\\').replace('"', '\\"').replace("\n", "\\n\\\n")


def parse(text, parameters):

  code = Parsing.xmlNamespace('shell')('script', text=shellLanguageEscape(text))

  return code, parameters
