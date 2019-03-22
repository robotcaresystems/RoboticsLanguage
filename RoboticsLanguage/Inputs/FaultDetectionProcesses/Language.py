#
#   This is the Robotics Language compiler
#
#   Language.py: Definition of the language for this package
#
#   Created on: 08 March, 2019
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#

from RoboticsLanguage.Base.Types import arguments, optional, returns


language = {
  '{fdp}word': {
    'definition': {
      arguments: arguments('anything'),
      returns: returns('nothing')
    },
    'output': {
      'RosCpp': 'ROS_INFO("{{text}}")'
    }
  }
}