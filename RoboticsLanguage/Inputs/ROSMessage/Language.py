#
#   This is the Robotics Language compiler
#
#   Language.py: Definition of the language for this package
#
#   Created on: 08 February, 2019
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#

from RoboticsLanguage.Base.Types import arguments, optional, returns


language = {
    '{rosm}message': {
        'definition': {
            arguments: arguments('rosm:name rosm:definition'),
            returns: returns('nothing')
        },
        'output': {
            'Cpp': ''
        }
    },
    '{rosm}name': {
        'definition': {
            arguments: arguments('nothing'),
            returns: returns('nothing')
        },
        'output': {
            'Cpp': ''
        }
    },
    '{rosm}definition': {
        'definition': {
            arguments: arguments('nothing'),
            returns: returns('nothing')
        },
        'output': {
            'Cpp': ''
        }
    }
}
