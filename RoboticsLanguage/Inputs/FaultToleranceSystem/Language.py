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

from RoboticsLanguage.Base.Types import arguments, returns


language = {
    '{fts}fault_handler': {
        'definition': {arguments: arguments('anything'), returns: returns('nothing')},
        'output': {'Cpp': '', 'Python': ''}
    },
    '{fts}fault_detection_topics': {
        'definition': {arguments: arguments('anything'), returns: returns('nothing')},
        'output': {'Cpp': '', 'Python': ''}
    },
    '{fts}failure_handler': {
        'definition': {arguments: arguments('anything'), returns: returns('nothing')},
        'output': {'Cpp': '', 'Python': ''}
    },
    '{fts}name': {
        'definition': {arguments: arguments('anything'), returns: returns('nothing')},
        'output': {'Cpp': '', 'Python': ''}
    },
    '{fts}fault_detection_processes': {
        'definition': {arguments: arguments('anything'), returns: returns('nothing')},
        'output': {'Cpp': '', 'Python': ''}
    },
    '{fts}fault_detection_heartbeat': {
        'definition': {arguments: arguments('anything'), returns: returns('nothing')},
        'output': {'Cpp': '', 'Python': ''}
    },
}
