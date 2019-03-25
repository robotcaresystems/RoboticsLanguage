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

default = {
    'definition': {arguments: arguments('anything'), returns: returns('nothing')},
    'output': {'Cpp': '', 'Python': ''}
}

language = {
    '{fts}name': default,
    '{fts}log_topics': default,
    '{fts}fault_handler': default,
    '{fts}failure_handler': default,
    '{fts}fault_detection_topics': default,
    '{fts}fault_detection_processes': default,
    '{fts}fault_detection_heartbeat': default,
}
